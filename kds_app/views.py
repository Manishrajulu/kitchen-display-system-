from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .data_storage import OrderDataStorage
from .counter_config import (
    get_counter_name, get_all_counters, validate_counter_credentials,
    create_counter, update_counter, delete_counter, reset_to_defaults
)
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class OrderViewSet(viewsets.ViewSet):
    """ViewSet for managing orders"""
    
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get all orders"""
        orders = OrderDataStorage.get_all_orders()
        return Response(orders)
    
    def retrieve(self, request, pk=None):
        """Get specific order"""
        order = OrderDataStorage.get_order(pk)
        if order:
            return Response(order)
        return Response(
            {'error': 'Order not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    def create(self, request):
        """Create new order"""
        order_data = request.data
        order_id = OrderDataStorage.create_order(order_data)
        
        # Get the created order
        order = OrderDataStorage.get_order(order_id)
        
        # Notify WebSocket clients
        self._notify_new_order(order)
        
        return Response(order, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Update order"""
        updates = request.data
        success = OrderDataStorage.update_order(pk, updates)
        
        if success:
            order = OrderDataStorage.get_order(pk)
            self._notify_order_update(order)
            return Response(order)
        
        return Response(
            {'error': 'Order not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    def destroy(self, request, pk=None):
        """Delete order"""
        success = OrderDataStorage.delete_order(pk)
        
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(
            {'error': 'Order not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status"""
        status_value = request.data.get('status')
        
        if not status_value:
            return Response(
                {'error': 'Status is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success = OrderDataStorage.update_order_status(pk, status_value)
        
        if success:
            order = OrderDataStorage.get_order(pk)
            self._notify_order_update(order)
            return Response(order)
        
        return Response(
            {'error': 'Order not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get orders by status"""
        status_value = request.query_params.get('status')
        
        if not status_value:
            return Response(
                {'error': 'Status parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orders = OrderDataStorage.get_orders_by_status(status_value)
        return Response(orders)
    
    @action(detail=False, methods=['delete'])
    def clear_all(self, request):
        """Clear all orders"""
        OrderDataStorage.clear_all_orders()
        return Response({'message': 'All orders cleared'})
    
    @action(detail=False, methods=['get'], url_path='counter/(?P<counter_id>[^/.]+)', permission_classes=[AllowAny])
    def orders_by_counter(self, request, counter_id=None):
        """Get orders for a specific counter - only items assigned to this counter"""
        try:
            counter_id = int(counter_id)
            all_orders = OrderDataStorage.get_all_orders()
            
            # Filter orders to show only those with items assigned to this counter
            filtered_orders = []
            for order in all_orders:
                # Filter items to show only those assigned to this counter
                relevant_items = [
                    item for item in order.get('items', []) 
                    if item.get('assigned_counter') == counter_id
                ]
                
                # Only include order if it has items for this counter
                if relevant_items:
                    # Create a copy of the order with only relevant items
                    filtered_order = order.copy()
                    filtered_order['items'] = relevant_items
                    filtered_orders.append(filtered_order)
            
            return Response(filtered_orders)
        except ValueError:
            return Response(
                {'error': 'Invalid counter ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], url_path='create', permission_classes=[AllowAny])
    def create_order(self, request):
        """Create a new order"""
        order_data = request.data
        order_id = OrderDataStorage.create_order(order_data)
        
        # Get the created order
        order = OrderDataStorage.get_order(order_id)
        
        # Notify WebSocket clients
        try:
            self._notify_new_order(order)
        except Exception as e:
            print(f"Error notifying WebSocket clients: {e}")
        
        return Response(order, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='update-item-status', permission_classes=[AllowAny])
    def update_item_status(self, request):
        """Update status of a specific item in an order"""
        order_id = request.data.get('order_id')
        item_index = request.data.get('item_index')
        status = request.data.get('status')
        
        if not all([order_id, item_index is not None, status]):
            return Response(
                {'error': 'order_id, item_index, and status are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success = OrderDataStorage.update_item_status(str(order_id), int(item_index), status)
        
        if success:
            # Get updated order
            order = OrderDataStorage.get_order(str(order_id))
            
            # Notify WebSocket clients about the update
            try:
                self._notify_order_update(order)
            except Exception as e:
                print(f"Error notifying WebSocket clients: {e}")
            
            return Response({
                'success': True, 
                'message': f'Item {item_index} status updated to {status}',
                'order': order
            })
        else:
            return Response(
                {'error': 'Failed to update item status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'], url_path='ready-to-serve', permission_classes=[AllowAny])
    def ready_to_serve_orders(self, request):
        """Get orders that are ready to serve"""
        orders = OrderDataStorage.get_ready_to_serve_orders()
        return Response(orders)
    
    def _notify_new_order(self, order):
        """Notify WebSocket clients about new order"""
        channel_layer = get_channel_layer()
        
        # Get all unique counter IDs from the order items
        counter_ids = set()
        for item in order.get('items', []):
            if item.get('assigned_counter'):
                counter_ids.add(item['assigned_counter'])
        
        # Send to each counter-specific group
        for counter_id in counter_ids:
            async_to_sync(channel_layer.group_send)(
                f'kitchen_display_counter_{counter_id}',
                {
                    'type': 'new_order',
                    'order': order
                }
            )
    
    def _notify_order_update(self, order):
        """Notify WebSocket clients about order update"""
        channel_layer = get_channel_layer()
        
        # Get all unique counter IDs from the order items
        counter_ids = set()
        for item in order.get('items', []):
            if item.get('assigned_counter'):
                counter_ids.add(item['assigned_counter'])
        
        # Send to each counter-specific group
        for counter_id in counter_ids:
            async_to_sync(channel_layer.group_send)(
                f'kitchen_display_counter_{counter_id}',
                {
                    'type': 'order_update',
                    'order': order
                }
            )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Simple login endpoint for kitchen staff"""
    counter_id = request.data.get('counter_id')
    pin = request.data.get('pin')
    
    if validate_counter_credentials(counter_id, pin):
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': {
                'counter_id': counter_id,
                'counter_name': get_counter_name(counter_id),
                'role': 'kitchen_staff'
            }
        })
    else:
        return Response({
            'success': False,
            'message': 'Invalid counter ID or PIN'
        }, status=status.HTTP_401_UNAUTHORIZED)


# Counter management endpoints
@api_view(['GET'])
@permission_classes([AllowAny])
def get_counters(request):
    """Get all available counters"""
    return Response(get_all_counters())

@api_view(['POST'])
@permission_classes([AllowAny])
def create_counter_endpoint(request):
    """Create a new counter"""
    try:
        name = request.data.get('name')
        pin = request.data.get('pin')
        description = request.data.get('description', '')
        
        if not name or not pin:
            return Response(
                {'error': 'Name and PIN are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        counter_id, message = create_counter(name, pin, description)
        
        if counter_id:
            return Response({
                'success': True,
                'message': message,
                'counter_id': counter_id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'error': message
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_counter_endpoint(request, counter_id):
    """Update an existing counter"""
    try:
        name = request.data.get('name')
        pin = request.data.get('pin')
        description = request.data.get('description')
        
        success, message = update_counter(counter_id, name, pin, description)
        
        if success:
            return Response({
                'success': True,
                'message': message
            })
        else:
            return Response({
                'success': False,
                'error': message
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_counter_endpoint(request, counter_id):
    """Delete a counter"""
    try:
        success, message = delete_counter(counter_id)
        
        if success:
            return Response({
                'success': True,
                'message': message
            })
        else:
            return Response({
                'success': False,
                'error': message
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_counters_endpoint(request):
    """Reset counters to default configuration"""
    try:
        success, message = reset_to_defaults()
        
        if success:
            return Response({
                'success': True,
                'message': message
            })
        else:
            return Response({
                'success': False,
                'error': message
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

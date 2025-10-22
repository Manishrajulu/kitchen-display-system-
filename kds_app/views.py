from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .data_storage import OrderDataStorage
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
        """Get orders for a specific counter"""
        try:
            counter_id = int(counter_id)
            # For now, return all orders since we don't have counter-specific filtering
            # In a real system, you'd filter orders by counter_id
            orders = OrderDataStorage.get_all_orders()
            return Response(orders)
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
    
    def _notify_new_order(self, order):
        """Notify WebSocket clients about new order"""
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'kitchen_display',
            {
                'type': 'new_order',
                'order': order
            }
        )
    
    def _notify_order_update(self, order):
        """Notify WebSocket clients about order update"""
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'kitchen_display',
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
    
    # Simple hardcoded credentials for demo purposes
    # Counter IDs and their corresponding PINs
    valid_credentials = {
        1: "1234",  # Main Kitchen
        2: "5678",  # Salad Counter  
        3: "9012"   # Grill Counter
    }
    
    if counter_id in valid_credentials and str(pin) == valid_credentials[counter_id]:
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


def get_counter_name(counter_id):
    """Get counter name by ID"""
    counter_names = {
        1: "Main Kitchen",
        2: "Salad Counter", 
        3: "Grill Counter"
    }
    return counter_names.get(counter_id, "Unknown Counter")

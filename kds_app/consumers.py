import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async  # Not needed for file-based storage
from .data_storage import OrderDataStorage


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get counter ID from query parameters
        self.counter_id = self.scope['query_string'].decode('utf-8')
        if 'counter_id=' in self.counter_id:
            self.counter_id = int(self.counter_id.split('counter_id=')[1].split('&')[0])
        else:
            self.counter_id = None
        
        # Create counter-specific room group
        if self.counter_id:
            self.room_group_name = f'kitchen_display_counter_{self.counter_id}'
        else:
            self.room_group_name = 'kitchen_display_all'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send current orders filtered by counter to the newly connected client
        current_orders = self.get_current_orders_for_counter()
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'orders': current_orders
        }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'update_order_status':
                order_id = data.get('order_id')
                status = data.get('status')
                
                # Update order status
                success = self.update_order_status(order_id, status)
                
                if success:
                    # Broadcast the update to all connected clients
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'order_status_update',
                            'order_id': order_id,
                            'status': status
                        }
                    )
            else:
                # Handle unknown message types gracefully
                print(f"Unknown message type: {message_type}")
            
        except json.JSONDecodeError:
            print(f"Invalid JSON received: {text_data}")
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
        except Exception as e:
            print(f"Error in WebSocket receive: {e}")
            # Don't close the connection, just log the error
    
    async def order_status_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'order_status_update',
            'order_id': event['order_id'],
            'status': event['status']
        }))
    
    async def new_order(self, event):
        # Only send new order if it has items for this counter
        order = event['order']
        if self.counter_id and self.has_items_for_counter(order, self.counter_id):
            await self.send(text_data=json.dumps({
                'type': 'new_order',
                'order': order
            }))
        elif not self.counter_id:
            # Send to all if no specific counter
            await self.send(text_data=json.dumps({
                'type': 'new_order',
                'order': order
            }))
    
    async def order_update(self, event):
        # Only send order update if it has items for this counter
        order = event['order']
        if self.counter_id and self.has_items_for_counter(order, self.counter_id):
            await self.send(text_data=json.dumps({
                'type': 'order_update',
                'order': order
            }))
        elif not self.counter_id:
            # Send to all if no specific counter
            await self.send(text_data=json.dumps({
                'type': 'order_update',
                'order': order
            }))
    
    def get_current_orders_for_counter(self):
        """Get current orders filtered by counter"""
        if not self.counter_id:
            return OrderDataStorage.get_all_orders()
        
        all_orders = OrderDataStorage.get_all_orders()
        filtered_orders = []
        
        for order in all_orders:
            # Filter items to show only those assigned to this counter
            relevant_items = [
                item for item in order.get('items', []) 
                if item.get('assigned_counter') == self.counter_id
            ]
            
            # Only include order if it has items for this counter
            if relevant_items:
                # Create a copy of the order with only relevant items
                filtered_order = order.copy()
                filtered_order['items'] = relevant_items
                filtered_orders.append(filtered_order)
        
        return filtered_orders
    
    def has_items_for_counter(self, order, counter_id):
        """Check if order has items assigned to this counter"""
        return any(
            item.get('assigned_counter') == counter_id 
            for item in order.get('items', [])
        )
    
    def update_order_status(self, order_id, status):
        """Update order status in storage"""
        try:
            return OrderDataStorage.update_order_status(order_id, status)
        except Exception as e:
            print(f"Error updating order status: {e}")
            return False

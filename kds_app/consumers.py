import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async  # Not needed for file-based storage
from .data_storage import OrderDataStorage


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'kitchen_display'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send current orders to the newly connected client
        current_orders = self.get_current_orders()
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
        # Send new order to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_order',
            'order': event['order']
        }))
    
    async def order_update(self, event):
        # Send order update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'order_update',
            'order': event['order']
        }))
    
    def get_current_orders(self):
        """Get current orders from storage"""
        return OrderDataStorage.get_all_orders()
    
    def update_order_status(self, order_id, status):
        """Update order status in storage"""
        try:
            return OrderDataStorage.update_order_status(order_id, status)
        except Exception as e:
            print(f"Error updating order status: {e}")
            return False

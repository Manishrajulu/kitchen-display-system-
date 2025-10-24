import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class OrderDataStorage:
    """Simple file-based storage for orders"""
    
    DATA_FILE = 'orders_data.json'
    
    @classmethod
    def _load_data(cls) -> Dict:
        """Load data from file"""
        if os.path.exists(cls.DATA_FILE):
            try:
                with open(cls.DATA_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {'orders': {}, 'next_id': 1}
        return {'orders': {}, 'next_id': 1}
    
    @classmethod
    def _save_data(cls, data: Dict):
        """Save data to file"""
        try:
            with open(cls.DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving data: {e}")
    
    @classmethod
    def create_order(cls, order_data: Dict) -> str:
        """Create a new order and return its ID"""
        data = cls._load_data()
        order_id = str(data['next_id'])
        
        # Calculate total amount from items and add IDs to items
        items = order_data.get('items', [])
        total_amount = 0
        
        for i, item in enumerate(items):
            # Add ID to each item if not present
            if 'id' not in item:
                item['id'] = f"{order_id}_{i}"
            # Add status if not present
            if 'status' not in item:
                item['status'] = 'pending'
            # Calculate total amount
            price = item.get('price', 0) or 0
            quantity = item.get('quantity', 1) or 1
            total_amount += price * quantity
        
        order = {
            'id': order_id,
            'order_number': f"ORD-{order_id.zfill(4)}",
            'items': items,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'customer_name': order_data.get('customer_name', ''),
            'table_number': order_data.get('table_number', ''),
            'notes': order_data.get('notes', ''),
            'total_amount': total_amount,
            'estimated_time': order_data.get('estimated_time', 15)
        }
        
        data['orders'][order_id] = order
        data['next_id'] += 1
        cls._save_data(data)
        
        return order_id
    
    @classmethod
    def get_order(cls, order_id: str) -> Optional[Dict]:
        """Get order by ID"""
        data = cls._load_data()
        return data['orders'].get(order_id)
    
    @classmethod
    def get_all_orders(cls) -> List[Dict]:
        """Get all orders"""
        data = cls._load_data()
        return list(data['orders'].values())
    
    @classmethod
    def get_orders_by_status(cls, status: str) -> List[Dict]:
        """Get orders by status"""
        data = cls._load_data()
        return [order for order in data['orders'].values() if order['status'] == status]
    
    @classmethod
    def update_order_status(cls, order_id: str, status: str) -> bool:
        """Update order status"""
        data = cls._load_data()
        
        if order_id in data['orders']:
            data['orders'][order_id]['status'] = status
            data['orders'][order_id]['updated_at'] = datetime.now().isoformat()
            cls._save_data(data)
            return True
        
        return False
    
    @classmethod
    def update_order(cls, order_id: str, updates: Dict) -> bool:
        """Update order with new data"""
        data = cls._load_data()
        
        if order_id in data['orders']:
            data['orders'][order_id].update(updates)
            data['orders'][order_id]['updated_at'] = datetime.now().isoformat()
            cls._save_data(data)
            return True
        
        return False
    
    @classmethod
    def delete_order(cls, order_id: str) -> bool:
        """Delete order"""
        data = cls._load_data()
        
        if order_id in data['orders']:
            del data['orders'][order_id]
            cls._save_data(data)
            return True
        
        return False
    
    @classmethod
    def clear_all_orders(cls):
        """Clear all orders"""
        data = {'orders': {}, 'next_id': 1}
        cls._save_data(data)
    
    @classmethod
    def update_item_status(cls, order_id: str, item_index: int, status: str) -> bool:
        """Update status of a specific item in an order"""
        data = cls._load_data()
        
        if order_id in data['orders']:
            order = data['orders'][order_id]
            if item_index < len(order['items']):
                order['items'][item_index]['status'] = status
                order['updated_at'] = datetime.now().isoformat()
                
                # Check if all items are ready
                all_items_ready = all(
                    item.get('status') == 'ready' 
                    for item in order['items']
                )
                
                if all_items_ready:
                    order['status'] = 'ready_to_serve'
                elif any(item.get('status') == 'in_progress' for item in order['items']):
                    order['status'] = 'in_progress'
                else:
                    order['status'] = 'pending'
                
                cls._save_data(data)
                return True
        
        return False
    
    @classmethod
    def get_ready_to_serve_orders(cls) -> List[Dict]:
        """Get orders that are ready to serve (all items ready)"""
        data = cls._load_data()
        return [order for order in data['orders'].values() if order['status'] == 'ready_to_serve']


# Kitchen Display System (KDS) API Documentation

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
The API uses PIN-based authentication for kitchen counters. No JWT tokens required for basic operations.

**Note:** This is a complete Django-based Kitchen Display System with real-time WebSocket updates and persistent login state.

## 1. Authentication Endpoints

### 1.1 Counter Login
**POST** `/kds/login/`

Authenticate a kitchen counter using PIN.

**Request Body:**
```json
{
    "counter_id": 1,
    "pin": "1234"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "user": {
        "counter_id": 1,
        "counter_name": "Main Kitchen",
        "role": "kitchen_staff"
    }
}
```

**Error Response:**
```json
{
    "success": false,
    "message": "Invalid counter ID or PIN"
}
```

## 2. Counter Management

### 2.1 Get All Counters
**GET** `/kds/counters/`

Get all available counters with their PINs.

**Response (Empty System):**
```json
[]
```

**Response (With Counters):**
```json
[
    {
        "id": 1,
        "name": "Coffee Station",
        "pin": "1111",
        "description": "Coffee and hot beverages"
    },
    {
        "id": 2,
        "name": "Grill Station",
        "pin": "2222",
        "description": "Grilled meats and vegetables"
    }
]
```

**Note:** The system starts with no counters. All counters must be created by users through the frontend or API.

### 2.2 Create Counter
**POST** `/kds/counters/create/`

Create a new counter with custom name and PIN.

**Request Body:**
```json
{
    "name": "Coffee Station",
    "pin": "1111",
    "description": "Coffee and hot beverages"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Counter created successfully",
    "counter_id": 1
}
```

**Error Response:**
```json
{
    "success": false,
    "error": "PIN already exists"
}
```

### 2.3 Update Counter
**PUT** `/kds/counters/{counter_id}/update/`

Update an existing counter.

**Request Body:**
```json
{
    "name": "Updated Coffee Station",
    "pin": "9999",
    "description": "Updated description"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Counter updated successfully"
}
```

### 2.4 Delete Counter
**DELETE** `/kds/counters/{counter_id}/delete/`

Delete a counter.

**Response:**
```json
{
    "success": true,
    "message": "Counter deleted successfully"
}
```

### 2.5 Reset All Counters
**POST** `/kds/counters/reset/`

Delete all counters and reset to empty state.

**Response:**
```json
{
    "success": true,
    "message": "All counters deleted"
}
```

## 3. Order Management

### 3.1 List All Orders
**GET** `/kds/orders/`

Get all orders with their items.

**Response:**
```json
[
    {
        "id": 1,
        "order_number": "ORD-0001",
        "table_number": "T-10",
        "customer_name": "Alice Johnson",
        "status": "new",
        "total_amount": 35.50,
        "notes": "Extra spicy",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z",
        "items": [
            {
                "id": 1,
                "order_id": 1,
                "name": "Chicken Burger",
                "category": "Main Course",
                "quantity": 1,
                "price": 18.00,
                "modifiers": {
                    "spice_level": "extra_spicy",
                    "no_onions": true
                },
                "assigned_counter": 1,
                "status": "new",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            },
            {
                "id": 2,
                "order_id": 1,
                "name": "Orange Juice",
                "category": "Beverage",
                "quantity": 2,
                "price": 8.00,
                "modifiers": {},
                "assigned_counter": 2,
                "status": "new",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            }
        ]
    }
]
```

### 3.2 Create New Order
**POST** `/kds/orders/create/`

Create a new order with items.

**Request Body:**
```json
{
    "order_number": "ORD-0001",
    "table_number": "T-10",
    "customer_name": "Alice Johnson",
    "total_amount": 35.50,
    "notes": "Extra spicy",
    "items": [
        {
            "name": "Chicken Burger",
            "category": "Main Course",
            "quantity": 1,
            "price": 18.00,
            "modifiers": {
                "spice_level": "extra_spicy",
                "no_onions": true
            },
            "assigned_counter": 1
        },
        {
            "name": "Orange Juice",
            "category": "Beverage",
            "quantity": 2,
            "price": 8.00,
            "modifiers": {},
            "assigned_counter": 2
        }
    ]
}
```

**Response:**
```json
{
    "id": 1,
    "order_number": "ORD-0001",
    "table_number": "T-10",
    "customer_name": "Alice Johnson",
    "status": "new",
    "total_amount": 35.50,
    "notes": "Extra spicy",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "items": [
        {
            "id": 1,
            "order_id": 1,
            "name": "Chicken Burger",
            "category": "Main Course",
            "quantity": 1,
            "price": 18.00,
            "modifiers": {
                "spice_level": "extra_spicy",
                "no_onions": true
            },
            "assigned_counter": 1,
            "status": "new",
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z"
            },
        {
            "id": 2,
            "order_id": 1,
            "name": "Orange Juice",
            "category": "Beverage",
            "quantity": 2,
            "price": 8.00,
            "modifiers": {},
            "assigned_counter": 2,
            "status": "new",
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z"
        }
    ]
}
```

### 3.3 Get Order Details
**GET** `/kds/orders/{id}/`

Get specific order details.

**Response:**
```json
{
    "id": 1,
    "order_number": "ORD-0001",
    "table_number": "T-10",
    "customer_name": "Alice Johnson",
    "status": "new",
    "total_amount": 35.50,
    "notes": "Extra spicy",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "items": [
        {
            "id": 1,
            "order_id": 1,
            "name": "Chicken Burger",
            "category": "Main Course",
            "quantity": 1,
            "price": 18.00,
            "modifiers": {
                "spice_level": "extra_spicy",
                "no_onions": true
            },
            "assigned_counter": 1,
            "status": "new",
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z"
        }
    ]
}
```

### 3.4 Get Orders for Counter
**GET** `/kds/orders/counter/{counter_id}/`

Get orders assigned to a specific counter.

**Response:**
```json
[
    {
        "id": 1,
        "order_number": "ORD-0001",
        "table_number": "T-10",
        "customer_name": "Alice Johnson",
        "status": "new",
        "total_amount": 35.50,
        "notes": "Extra spicy",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z",
        "items": [
            {
                "id": 1,
                "order_id": 1,
                "name": "Chicken Burger",
                "category": "Main Course",
                "quantity": 1,
                "price": 18.00,
                "modifiers": {
                    "spice_level": "extra_spicy",
                    "no_onions": true
                },
                "assigned_counter": 1,
                "status": "new",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            }
        ]
    }
]
```

### 3.5 Delete Order
**DELETE** `/kds/orders/{id}/delete/`

Delete an order and all its items.

**Response:**
```json
{
    "success": true,
    "message": "Order 1 deleted"
}
```

## 4. Order Item Management

### 4.1 Get Item Details
**GET** `/kds/items/{item_id}/`

Get specific item details.

**Response:**
```json
{
    "id": 1,
    "order_id": 1,
    "name": "Chicken Burger",
    "category": "Main Course",
    "quantity": 1,
    "price": 18.00,
    "modifiers": {
        "spice_level": "extra_spicy",
        "no_onions": true
    },
    "assigned_counter": 1,
    "status": "new",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
}
```

### 4.2 Update Item Status
**POST** `/kds/orders/update-item-status/`

Update the status of an order item.

**Request Body:**
```json
{
    "order_id": 1,
    "item_index": 0,
    "status": "in_progress"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Item 0 status updated to in_progress",
    "order": {
        "id": 1,
        "order_number": "ORD-0001",
        "table_number": "T-10",
        "customer_name": "Alice Johnson",
        "status": "new",
        "total_amount": 35.50,
        "items": [
            {
                "name": "Chicken Burger",
                "category": "Main Course",
                "quantity": 1,
                "price": 18.00,
                "assigned_counter": 1,
                "status": "in_progress"
            }
        ]
    }
}
```

**Valid Status Values:**
- `new` - Item just created
- `in_progress` - Item being prepared
- `ready` - Item completed and ready for pickup
- `cancelled` - Item cancelled

## 5. Statistics and Reporting

### 5.1 Get System Statistics
**GET** `/kds/statistics/`

Get overall system statistics.

**Response:**
```json
{
    "total_orders": 25,
    "total_items": 67,
    "status_counts": {
        "new": 5,
        "in_progress": 8,
        "ready": 10,
        "cancelled": 2
    },
    "active_counters": 4
}
```

## 6. WebSocket Endpoints (Real-time Features)

### 6.1 Kitchen WebSocket
**WebSocket URL:** `ws://127.0.0.1:8000/ws/kitchen/?counter_id=<counter_id>`

Connect to real-time updates for a specific kitchen counter. Each counter only receives updates for orders assigned to them.

**Message Types:**

#### Initial Data
```json
{
    "type": "initial_data",
    "orders": [
        {
            "id": 1,
            "order_number": "ORD-0001",
            "table_number": "T-10",
            "customer_name": "Alice Johnson",
            "status": "new",
            "total_amount": 35.50,
            "items": [...]
        }
    ]
}
```

#### New Order Notification
```json
{
    "type": "new_order",
    "order": {
        "id": 2,
        "order_number": "ORD-0002",
        "table_number": "T-11",
        "customer_name": "Bob Smith",
        "status": "new",
        "total_amount": 28.00,
        "items": [...]
    }
}
```

#### Item Status Update
```json
{
    "type": "item_status_update",
    "item_id": 1,
    "status": "ready",
    "order_id": 1
}
```

#### Order Update
```json
{
    "type": "order_update",
    "order": {
        "id": 1,
        "order_number": "ORD-0001",
        "status": "ready",
        "items": [...]
    }
}
```

#### Order Deleted
```json
{
    "type": "order_deleted",
    "order_id": 1
}
```

### 6.2 WebSocket Client Messages

#### Update Order Status
```json
{
    "type": "update_order_status",
    "order_id": 1,
    "status": "ready"
}
```

## 7. Error Responses

### 400 Bad Request
```json
{
    "error": "item_id and status are required"
}
```

### 401 Unauthorized
```json
{
    "error": "Invalid PIN"
}
```

### 404 Not Found
```json
{
    "error": "Order not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error"
}
```

## 8. Data Models

### Order Model
```json
{
    "id": "integer",
    "order_number": "string",
    "table_number": "string",
    "customer_name": "string",
    "status": "string (new, in_progress, ready, cancelled)",
    "total_amount": "decimal",
    "notes": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "items": "array of Item objects"
}
```

### Item Model
```json
{
    "id": "integer",
    "order_id": "integer",
    "name": "string",
    "category": "string",
    "quantity": "integer",
    "price": "decimal",
    "modifiers": "object",
    "assigned_counter": "integer",
    "status": "string (new, in_progress, ready, cancelled)",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Counter Model
```json
{
    "id": "integer",
    "name": "string",
    "description": "string",
    "pin": "string",
    "is_active": "boolean"
}
```

## 9. Development Notes

### Environment Variables
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Running the Server

**For full functionality with WebSocket support:**
```bash
uvicorn kds_project.asgi:application --reload --port 8000
```

**Note:** Use `python manage.py runserver` only for basic API testing (no WebSocket support).

### Project Structure
```
kds_project/
├── kds_project/          # Main project settings
│   ├── settings.py      # Django settings
│   ├── urls.py          # Main URL configuration
│   └── asgi.py          # ASGI configuration for WebSockets
├── kds_app/             # Core KDS functionality
│   ├── data_storage.py  # In-memory data storage
│   ├── views.py         # API endpoints
│   ├── consumers.py     # WebSocket consumers
│   ├── routing.py       # WebSocket routing
│   └── urls.py          # API URL patterns
├── templates/           # Frontend templates
│   ├── kitchen_login.html   # Kitchen staff interface
│   └── order_management.html # Order creation interface
├── kds/                 # Virtual environment
├── manage.py            # Django management script
├── requirements.txt     # Dependencies
└── README.md           # Project documentation
```

### Features
- **Multi-Counter Support**: Manage multiple kitchen counters (Main Kitchen, Juice Counter, Dessert Counter)
- **Counter-Specific Filtering**: Each counter only sees items assigned to them
- **Real-time Order Management**: Create, view, and update orders with live WebSocket updates
- **PIN-based Authentication**: Simple and secure PIN-based login for kitchen staff
- **Persistent Login State**: Login state persists across page refreshes using localStorage
- **Order Creation Interface**: Dedicated interface for creating new orders
- **Ready-to-Serve Notifications**: Orders marked as ready when all items are completed
- **Real-time Updates**: WebSocket-based live order status updates across all counters
- **In-Memory Storage**: Fast data storage that persists during server session
- **No Database Required**: Lightweight, API-only structure for quick deployment

### Counter System
- **Empty Start**: System starts with no counters
- **User-Created**: All counters must be created by users
- **Unlimited**: Create as many counters as needed
- **Custom Names**: Name counters however you want
- **Unique PINs**: Each counter gets a 4-digit PIN

### Usage Examples

#### 1. Create Counter
```bash
curl -X POST http://127.0.0.1:8000/api/kds/counters/create/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Coffee Station", "pin": "1111", "description": "Coffee and hot beverages"}'
```

#### 2. Counter Login
```bash
curl -X POST http://127.0.0.1:8000/api/kds/login/ \
  -H "Content-Type: application/json" \
  -d '{"counter_id": 1, "pin": "1111"}'
```

#### 3. Get Orders for Counter
```bash
curl http://127.0.0.1:8000/api/kds/orders/counter/1/
```

#### 4. Create New Order
```bash
curl -X POST http://127.0.0.1:8000/api/kds/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": "T-10",
    "customer_name": "Alice Johnson",
    "items": [
      {
        "name": "Coffee",
        "category": "Beverage",
        "quantity": 2,
        "price": 8.00,
        "assigned_counter": 1
      }
    ]
  }'
```

### WebSocket Usage Example
```javascript
// Connect to specific counter
const ws = new WebSocket('ws://127.0.0.1:8000/ws/kitchen/?counter_id=1');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

// Update item status
ws.send(JSON.stringify({
    type: 'update_item_status',
    order_id: 1,
    item_index: 0,
    status: 'ready'
}));
```

### Production Deployment
For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up Redis for production WebSocket support
4. Configure static files serving
5. Set up proper logging
6. Use environment variables for secrets

### License
This project is licensed under the MIT License.

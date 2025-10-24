# Kitchen Display System (KDS) API Documentation

## Base URL
```
http://127.0.0.1:8000/api/
```

## 🤖 Fully Automated System

This is a **fully automated** Kitchen Display System where:
- **Just enter food name and quantity** - no manual counter selection needed
- **Smart category detection** - automatically detects categories from food names
- **Automatic counter assignment** - items are automatically routed to correct counters
- **Real-time WebSocket updates** - instant order status changes across all counters

## 1. Authentication Endpoints

### 1.1 Counter Login
**POST** `/kds/login/`

Authenticate a kitchen counter using PIN.

**Request Body:**
```json
{
    "counter_id": 1,
    "pin": "1702"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "user": {
        "counter_id": 1,
        "counter_name": "Biryani Station",
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

Get all available counters with their categories.

**Response:**
```json
[
    {
        "id": 1,
        "name": "Biryani Station",
        "pin": "1702",
        "description": "Biryani and rice dishes",
        "categories": ["Biryani", "CHICKEN BRIYANI", "MUTTON BRIYANI", "PRAWN BRIYANI", "BEEF BRIYANI"]
    },
    {
        "id": 3,
        "name": "Main Kitchen",
        "pin": "2341",
        "description": "Main kitchen counter",
        "categories": ["Beverage", "Main Course", "Dessert", "lemon juice", "orange juice", "apple juice"]
    }
]
```

### 2.2 Create Counter
**POST** `/kds/counters/create/`

Create a new counter with custom name and PIN.

**Request Body:**
```json
{
    "name": "Biryani Station",
    "pin": "1702",
    "description": "Biryani and rice dishes"
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

### 2.3 Assign Categories to Counter
**POST** `/kds/counters/{counter_id}/categories/`

Assign categories to a counter for automatic item assignment.

**Request Body:**
```json
{
    "categories": ["Biryani", "CHICKEN BRIYANI", "MUTTON BRIYANI", "PRAWN BRIYANI", "BEEF BRIYANI"]
}
```

**Response:**
```json
{
    "success": true,
    "message": "Categories assigned successfully"
}
```

### 2.4 Update Counter
**PUT** `/kds/counters/{counter_id}/update/`

Update an existing counter.

**Request Body:**
```json
{
    "name": "Updated Biryani Station",
    "pin": "9999",
    "description": "Updated description"
}
```

### 2.5 Delete Counter
**DELETE** `/kds/counters/{counter_id}/delete/`

Delete a counter.

**Response:**
```json
{
    "success": true,
    "message": "Counter deleted successfully"
}
```

### 2.6 Reset All Counters
**POST** `/kds/counters/reset/`

Delete all counters and reset to empty state.

**Response:**
```json
{
    "success": true,
    "message": "All counters deleted"
}
```

## 3. Order Management (Fully Automated)

### 3.1 Create New Order (Auto-Assignment)
**POST** `/kds/orders/create/`

Create a new order with **automatic counter assignment**. Just provide food names and quantities - the system handles everything else!

**Request Body:**
```json
{
    "table_number": "T-01",
    "customer_name": "John Doe",
    "notes": "Extra spicy",
    "items": [
        {
            "name": "Chicken Biryani",
            "category": "Biryani",
            "quantity": 1,
            "price": 15.00
        },
        {
            "name": "Orange Juice",
            "category": "Beverage",
            "quantity": 2,
            "price": 8.00
        }
    ]
}
```

**🤖 Auto-Assignment Logic:**
- System automatically detects categories from food names
- Items are automatically assigned to counters based on their categories
- No need to specify `assigned_counter` manually
- If no counter is found for a category, `assigned_counter` is set to `null`

**Response:**
```json
{
    "id": 12,
    "order_number": "ORD-0012",
    "table_number": "T-01",
    "customer_name": "John Doe",
    "status": "pending",
    "total_amount": 31.00,
    "notes": "Extra spicy",
    "created_at": "2025-10-23T20:01:51.783695",
    "updated_at": "2025-10-23T20:01:51.783695",
    "items": [
        {
            "id": "12_0",
            "name": "Chicken Biryani",
            "category": "Biryani",
            "quantity": 1,
            "price": 15.00,
            "assigned_counter": 1,
            "status": "pending"
        },
        {
            "id": "12_1",
            "name": "Orange Juice",
            "category": "Beverage",
            "quantity": 2,
            "price": 8.00,
            "assigned_counter": 3,
            "status": "pending"
        }
    ]
}
```

### 3.2 Get Orders for Counter
**GET** `/kds/orders/counter/{counter_id}/`

Get orders assigned to a specific counter. Only shows orders with items assigned to that counter.

**Response:**
```json
[
    {
        "id": 12,
        "order_number": "ORD-0012",
        "table_number": "T-01",
        "customer_name": "John Doe",
        "status": "pending",
        "total_amount": 15.00,
        "items": [
            {
                "id": "12_0",
                "name": "Chicken Biryani",
                "category": "Biryani",
                "quantity": 1,
                "price": 15.00,
                "assigned_counter": 1,
                "status": "pending"
            }
        ]
    }
]
```

### 3.3 Get All Orders
**GET** `/kds/orders/`

Get all orders in the system.

**Response:**
```json
[
    {
        "id": 12,
        "order_number": "ORD-0012",
        "table_number": "T-01",
        "customer_name": "John Doe",
        "status": "pending",
        "total_amount": 31.00,
        "items": [
            {
                "id": "12_0",
                "name": "Chicken Biryani",
                "category": "Biryani",
                "quantity": 1,
                "price": 15.00,
                "assigned_counter": 1,
                "status": "pending"
            },
            {
                "id": "12_1",
                "name": "Orange Juice",
                "category": "Beverage",
                "quantity": 2,
                "price": 8.00,
                "assigned_counter": 3,
                "status": "pending"
            }
        ]
    }
]
```

### 3.4 Update Item Status
**POST** `/kds/orders/update-item-status/`

Update the status of an order item.

**Request Body:**
```json
{
    "order_id": 12,
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
        "id": 12,
        "order_number": "ORD-0012",
        "status": "in_progress",
        "items": [
            {
                "name": "Chicken Biryani",
                "status": "in_progress"
            }
        ]
    }
}
```

**Valid Status Values:**
- `pending` - Item just created
- `in_progress` - Item being prepared
- `ready` - Item completed and ready for pickup
- `cancelled` - Item cancelled

## 4. Smart Category Detection

The system automatically detects categories from food names:

### Detection Rules
- **Biryani Items**: Contains "biryani", "briyani", "chicken", "mutton", "prawn", "beef" → Category: "Biryani"
- **Beverages**: Contains "juice", "coffee", "tea", "soda", "water", "drink" → Category: "Beverage"
- **Desserts**: Contains "dessert", "sweet", "cake", "ice cream", "kesari", "kulfi" → Category: "Dessert"
- **Main Course**: Contains "burger", "pizza", "pasta", "rice", "curry", "gravy" → Category: "Main Course"

### Examples
| Food Name | Detected Category | Assigned Counter |
|-----------|------------------|------------------|
| "Chicken Biryani" | Biryani | Counter 1 (Biryani Station) |
| "Orange Juice" | Beverage | Counter 3 (Main Kitchen) |
| "Burger" | Main Course | Counter 3 (Main Kitchen) |
| "Kesari" | Dessert | Counter 3 (Main Kitchen) |
| "Coffee" | Beverage | Counter 3 (Main Kitchen) |

## 5. WebSocket Endpoints (Real-time Features)

### 5.1 Kitchen WebSocket
**WebSocket URL:** `ws://127.0.0.1:8000/ws/kitchen/?counter_id=<counter_id>`

Connect to real-time updates for a specific kitchen counter. Each counter only receives updates for orders assigned to them.

**Message Types:**

#### Initial Data
```json
{
    "type": "initial_data",
    "orders": [
        {
            "id": 12,
            "order_number": "ORD-0012",
            "table_number": "T-01",
            "customer_name": "John Doe",
            "status": "pending",
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
        "id": 13,
        "order_number": "ORD-0013",
        "table_number": "T-02",
        "customer_name": "Alice Smith",
        "status": "pending",
        "items": [...]
    }
}
```

#### Item Status Update
```json
{
    "type": "item_status_update",
    "item_id": "12_0",
    "status": "ready",
    "order_id": 12
}
```

#### Order Update
```json
{
    "type": "order_update",
    "order": {
        "id": 12,
        "order_number": "ORD-0012",
        "status": "ready",
        "items": [...]
    }
}
```

## 6. Error Responses

### 400 Bad Request
```json
{
    "error": "order_id, item_index, and status are required"
}
```

### 401 Unauthorized
```json
{
    "success": false,
    "message": "Invalid counter ID or PIN"
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

## 7. Data Models

### Order Model
```json
{
    "id": "integer",
    "order_number": "string",
    "table_number": "string",
    "customer_name": "string",
    "status": "string (pending, in_progress, ready, cancelled)",
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
    "id": "string",
    "name": "string",
    "category": "string",
    "quantity": "integer",
    "price": "decimal",
    "assigned_counter": "integer",
    "status": "string (pending, in_progress, ready, cancelled)"
}
```

### Counter Model
```json
{
    "id": "integer",
    "name": "string",
    "pin": "string",
    "description": "string",
    "categories": "array of strings"
}
```

## 8. Usage Examples

### 8.1 Complete Workflow Example

#### 1. Create Counters
```bash
# Create Biryani Station
curl -X POST http://127.0.0.1:8000/api/kds/counters/create/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Biryani Station", "pin": "1702", "description": "Biryani and rice dishes"}'

# Assign categories
curl -X POST http://127.0.0.1:8000/api/kds/counters/1/categories/ \
  -H "Content-Type: application/json" \
  -d '{"categories": ["Biryani", "CHICKEN BRIYANI", "MUTTON BRIYANI"]}'

# Create Main Kitchen
curl -X POST http://127.0.0.1:8000/api/kds/counters/create/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Main Kitchen", "pin": "2341", "description": "Main kitchen counter"}'

# Assign categories
curl -X POST http://127.0.0.1:8000/api/kds/counters/3/categories/ \
  -H "Content-Type: application/json" \
  -d '{"categories": ["Beverage", "Main Course", "Dessert"]}'
```

#### 2. Create Order (Fully Automated)
```bash
curl -X POST http://127.0.0.1:8000/api/kds/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": "T-01",
    "customer_name": "John Doe",
    "items": [
      {
        "name": "Chicken Biryani",
        "category": "Biryani",
        "quantity": 1,
        "price": 15.00
      },
      {
        "name": "Orange Juice",
        "category": "Beverage",
        "quantity": 2,
        "price": 8.00
      }
    ]
  }'
```

#### 3. Check Orders for Each Counter
```bash
# Check Biryani Station orders
curl http://127.0.0.1:8000/api/kds/orders/counter/1/

# Check Main Kitchen orders
curl http://127.0.0.1:8000/api/kds/orders/counter/3/
```

### 8.2 WebSocket Usage Example
```javascript
// Connect to Biryani Station
const ws = new WebSocket('ws://127.0.0.1:8000/ws/kitchen/?counter_id=1');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
    
    // Handle different message types
    switch(data.type) {
        case 'new_order':
            console.log('New order received:', data.order);
            break;
        case 'item_status_update':
            console.log('Item status updated:', data.item_id, data.status);
            break;
    }
};
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
│   ├── counter_config.py # Dynamic counter management
│   ├── data_storage.py  # In-memory data storage
│   ├── views.py         # API endpoints
│   ├── consumers.py     # WebSocket consumers
│   ├── routing.py       # WebSocket routing
│   └── urls.py          # API URL patterns
├── templates/           # Frontend templates
│   ├── kitchen_login.html   # Kitchen staff interface
│   └── order_management.html # Order creation & counter management
├── kds/                 # Virtual environment
├── manage.py            # Django management script
├── requirements.txt     # Dependencies
└── README.md           # Project documentation
```

### Key Features
- **🤖 Fully Automated**: Just enter food names and quantities
- **🧠 Smart Detection**: Automatically detects categories from food names
- **🎯 Auto-Assignment**: Items automatically routed to correct counters
- **⚡ Real-time Updates**: WebSocket-based live order status updates
- **🔐 PIN Authentication**: Simple and secure PIN-based login
- **💾 Persistent State**: Login state persists across page refreshes
- **🚀 No Database**: Lightweight, in-memory system for quick deployment

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

---

**🎉 Your KDS system is now fully automated! Just enter food names and quantities - the system handles everything else!**
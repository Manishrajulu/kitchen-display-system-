# Kitchen Display System (KDS)

A complete Django-based Kitchen Display System with real-time WebSocket updates, order management, and multi-counter support for restaurants.

## Features

- **Multi-Counter Support**: Manage multiple kitchen counters (Main Kitchen, Salad Counter, Grill Counter)
- **Real-time Order Management**: Create, view, and update orders with live WebSocket updates
- **PIN-based Authentication**: Simple and secure PIN-based login for kitchen staff
- **Persistent Login State**: Login state persists across page refreshes using localStorage
- **Order Creation Interface**: Dedicated interface for creating new orders
- **Real-time Updates**: WebSocket-based live order status updates across all counters
- **In-Memory Storage**: Fast data storage that persists during server session
- **No Database Required**: Lightweight, API-only structure for quick deployment

## Tech Stack

- **Backend**: Python 3.11+, Django 5+, Django REST Framework
- **Real-time**: Django Channels (WebSockets), Uvicorn ASGI server
- **Frontend**: HTML5, JavaScript, CSS3 with localStorage persistence
- **Authentication**: PIN-based authentication system
- **CORS**: Cross-origin resource sharing for frontend integration

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

**For full functionality with WebSocket support:**
```bash
uvicorn kds_project.asgi:application --reload --port 8000
```

**Note:** Use `python manage.py runserver` only for basic API testing (no WebSocket support).

### 3. Access the Application

- **Kitchen Staff Login**: http://127.0.0.1:8000/kitchen_login.html
- **Order Management**: http://127.0.0.1:8000/order_management.html
- **API Documentation**: See API_DOCUMENTATION.md

That's it! Your KDS system is ready with real-time order management and WebSocket updates.

## 🔐 Kitchen Staff Login

### Available Counter PINs:
- **Main Kitchen (Counter 1)**: PIN 1234
- **Salad Counter (Counter 2)**: PIN 5678  
- **Grill Counter (Counter 3)**: PIN 9012

### Login Process:
1. Open http://127.0.0.1:8000/kitchen_login.html
2. Select your counter from the dropdown
3. Enter your 4-digit PIN
4. Click "Login to Counter"
5. Your login state will be automatically saved and restored on page refresh

### Login Flow:
1. Staff selects their counter
2. Enters 4-digit PIN
3. System authenticates and shows assigned orders
4. Staff can update item statuses in real-time

## 📋 Order Management

### Creating Orders:
1. Open http://127.0.0.1:8000/order_management.html
2. Fill in customer details (table number, customer name, notes)
3. Add order items with quantities, prices, and assigned counters
4. Click "Create Order"
5. Orders will appear in real-time on the kitchen display

### Order Status Updates:
- Kitchen staff can update item statuses in real-time
- Status changes are immediately visible across all connected displays
- Login state persists even when orders are created from other pages

## API Endpoints

### Authentication
- `POST /api/kds/login/` - KDS counter PIN login

### Orders
- `GET /api/kds/orders/` - Get all orders
- `POST /api/kds/orders/create/` - Create new order
- `GET /api/kds/orders/counter/<counter_id>/` - Get orders for specific counter

## WebSocket Endpoints

- `ws://127.0.0.1:8000/ws/kitchen/` - Real-time updates for all counters

## Sample Data

The system comes with pre-configured counters:

- **3 KDS Counters**: Main Kitchen, Salad Counter, Grill Counter
- **PIN Codes**: 1234, 5678, 9012
- **Real-time WebSocket**: Instant order updates across all counters
- **Persistent Login**: Login state automatically restored on page refresh

## Usage Examples

### 1. Counter Login
```bash
curl -X POST http://localhost:8000/api/kds/login/ \
  -H "Content-Type: application/json" \
  -d '{"counter_id": 1, "pin": "1234"}'
```

### 2. Get Orders for Counter
```bash
curl http://localhost:8000/api/kds/orders/counter/1/
```

### 3. Update Item Status
```bash
curl -X POST http://localhost:8000/api/kds/update_status/ \
  -H "Content-Type: application/json" \
  -d '{"item_id": 1, "status": "in_progress"}'
```

### 4. Create New Order
```bash
curl -X POST http://localhost:8000/api/kds/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": "T-10",
    "customer_name": "Alice Johnson",
    "total_amount": 35.50,
    "items": [
      {
        "name": "Chicken Burger",
        "category": "Main Course",
        "quantity": 1,
        "price": 18.00,
        "assigned_counter": 1
      },
      {
        "name": "Orange Juice",
        "category": "Beverage",
        "quantity": 2,
        "price": 8.00,
        "assigned_counter": 2
      }
    ]
  }'
```

## WebSocket Usage

Connect to WebSocket for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/kds/1/');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

// Update item status
ws.send(JSON.stringify({
    type: 'update_item_status',
    item_id: 1,
    status: 'ready'
}));
```

## Development

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
└── README.md           # This file
```

### Adding New Features

1. **New API Endpoints**: Add to `kds_app/views.py`
2. **WebSocket Events**: Extend `kds_app/consumers.py`
3. **Data Storage**: Update `kds_app/data_storage.py`
4. **Frontend**: Update HTML templates in `templates/` directory

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up Redis for production WebSocket support
4. Configure static files serving
5. Set up proper logging
6. Use environment variables for secrets

## License

This project is licensed under the MIT License.

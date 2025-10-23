# Kitchen Display System (KDS)

A complete Django-based Kitchen Display System with real-time WebSocket updates, order management, and fully customizable counter system for restaurants.

## Features

- **User-Created Counter System**: Create unlimited kitchen counters with custom names and PINs
- **Real-time Order Management**: Create, view, and update orders with live WebSocket updates
- **Counter Isolation**: Orders only appear on assigned counters - no cross-contamination
- **PIN-based Authentication**: Simple and secure PIN-based login for kitchen staff
- **Persistent Login State**: Login state persists across page refreshes using localStorage
- **Order Creation Interface**: Dedicated interface for creating new orders with counter assignment
- **Real-time Updates**: WebSocket-based live order status updates per counter
- **No Database Required**: Lightweight, in-memory system for quick deployment
- **Complete Flexibility**: Start with empty system, create exactly the counters you need

## Tech Stack

- **Backend**: Python 3.11+, Django 5+, Django REST Framework
- **Real-time**: Django Channels (WebSockets), Uvicorn ASGI server
- **Frontend**: HTML5, JavaScript, CSS3 with localStorage persistence
- **Authentication**: PIN-based authentication system
- **CORS**: Cross-origin resource sharing for frontend integration

## Quick Start

### 1. Setup Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv kds

# Activate virtual environment (Windows)
kds\Scripts\activate

# Activate virtual environment (Linux/Mac)
source kds/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Server

**For full functionality with WebSocket support:**
```bash
uvicorn kds_project.asgi:application --reload --port 8000
```

**Note:** Use `python manage.py runserver` only for basic API testing (no WebSocket support).

### 4. Access the Application

- **Order Management**: http://127.0.0.1:8000/templates/order_management.html
- **Kitchen Staff Login**: http://127.0.0.1:8000/templates/kitchen_login.html
- **API Documentation**: See API_DOCUMENTATION.md

That's it! Your KDS system is ready with real-time order management and WebSocket updates.

## 🔐 Kitchen Staff Login

### First Time Setup:
1. **Create Counters First**: Go to Order Management page to create your counters
2. **Add Counter Details**: Name, 4-digit PIN, and description
3. **Create as Many as Needed**: Add counters for each kitchen station

### Login Process:
1. Open http://127.0.0.1:8000/templates/kitchen_login.html
2. Select your counter from the dropdown (if no counters exist, create them first)
3. Enter your 4-digit PIN
4. Click "Login to Counter"
5. Your login state will be automatically saved and restored on page refresh

### Login Flow:
1. Staff selects their counter
2. Enters 4-digit PIN
3. System authenticates and shows assigned orders
4. Staff can update item statuses in real-time

## 📋 Order Management

### First Time Setup:
1. **Create Your Counters**: Use the Counter Management section to create counters
2. **Add Counter Details**: Name, PIN, and description for each kitchen station
3. **Create as Many as Needed**: Add counters for Coffee Station, Grill, Pizza, etc.

### Creating Orders:
1. Open http://127.0.0.1:8000/templates/order_management.html
2. Create counters if none exist (see Counter Management section)
3. Fill in customer details (table number, customer name, notes)
4. Add order items with quantities, prices, and assigned counters
5. Click "Create Order"
6. Orders will appear in real-time on the assigned kitchen counters only

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
- `POST /api/kds/orders/update-item-status/` - Update item status

### Counters
- `GET /api/kds/counters/` - Get all available counters

## WebSocket Endpoints

- `ws://127.0.0.1:8000/ws/kitchen/?counter_id=<id>` - Real-time updates for specific counter

## 🔧 Counter Management

### Creating Counters:
1. **Go to Order Management page**
2. **Use Counter Management section** to create counters
3. **Fill in details**: Name, 4-digit PIN, Description
4. **Click "Create Counter"**
5. **Repeat for each kitchen station**

### Managing Counters:
- **Edit**: Click "Edit" button on any counter
- **Delete**: Click "Delete" button on any counter
- **Reset**: Click "Delete All Counters" to start fresh

### Counter Features:
- **Unlimited Counters**: Create as many as you need
- **Custom Names**: Name them however you want (Coffee Station, Grill, Pizza, etc.)
- **Unique PINs**: Each counter gets a 4-digit PIN
- **Real-time Updates**: Changes appear immediately
- **Complete Control**: Edit or delete any counter anytime

## Usage Examples

### 1. Create Counter
```bash
curl -X POST http://localhost:8000/api/kds/counters/create/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Coffee Station", "pin": "1111", "description": "Coffee and hot beverages"}'
```

### 2. Counter Login
```bash
curl -X POST http://localhost:8000/api/kds/login/ \
  -H "Content-Type: application/json" \
  -d '{"counter_id": 1, "pin": "1111"}'
```

### 3. Get Orders for Counter
```bash
curl http://localhost:8000/api/kds/orders/counter/1/
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
        "name": "Coffee",
        "category": "Beverage",
        "quantity": 2,
        "price": 8.00,
        "assigned_counter": 1
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

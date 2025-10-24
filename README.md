# Kitchen Display System (KDS)

A fully automated Django-based Kitchen Display System with real-time WebSocket updates, intelligent order routing, and smart counter management for restaurants.

## 🤖 Key Features

- **Fully Automated Order Routing**: Just enter food name and quantity - the system automatically assigns items to the correct counter
- **Smart Category Detection**: Automatically detects food categories from item names (Biryani, Beverage, Main Course, Dessert)
- **Real-time Order Management**: Live WebSocket updates for instant order status changes
- **Counter Isolation**: Orders only appear on assigned counters - no cross-contamination
- **PIN-based Authentication**: Simple and secure PIN-based login for kitchen staff
- **Persistent Login State**: Login state persists across page refreshes using localStorage
- **No Database Required**: Lightweight, in-memory system for quick deployment
- **Complete Flexibility**: Start with empty system, create exactly the counters you need

## 🚀 Quick Start

### 1. Setup Virtual Environment

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

## 🎯 How It Works

### 1. Setup Counters (One-time)
1. Go to **Order Management** page
2. Create counters for your kitchen stations:
   - **Counter 1**: "Biryani Station" (PIN: 1702) - Categories: Biryani, CHICKEN BRIYANI, MUTTON BRIYANI
   - **Counter 2**: "Main Kitchen" (PIN: 2341) - Categories: Beverage, Main Course, Dessert

### 2. Create Orders (Fully Automated)
1. Just enter **food name** and **quantity** - that's it!
2. System automatically:
   - Detects category from food name
   - Assigns to correct counter
   - Routes order to appropriate kitchen station

### 3. Kitchen Staff Login
1. Staff login to their counter with PIN
2. See only orders assigned to their station
3. Update item statuses in real-time

## 🍽️ Smart Category Detection

The system automatically detects categories from food names:

| Food Name | Detected Category | Assigned Counter |
|-----------|------------------|------------------|
| "Chicken Biryani" | Biryani | Counter 1 |
| "Orange Juice" | Beverage | Counter 2 |
| "Burger" | Main Course | Counter 2 |
| "Kesari" | Dessert | Counter 2 |
| "Coffee" | Beverage | Counter 2 |

## 📋 Order Creation Examples

### Example 1: Biryani Order
```
Customer: John Doe
Table: T-01
Items:
- "Chicken Biryani" (Qty: 1) → Auto-assigned to Counter 1
- "Mutton Biryani" (Qty: 2) → Auto-assigned to Counter 1
```

### Example 2: Mixed Order
```
Customer: Alice Smith
Table: T-02
Items:
- "Orange Juice" (Qty: 2) → Auto-assigned to Counter 2
- "Burger" (Qty: 1) → Auto-assigned to Counter 2
- "Kesari" (Qty: 1) → Auto-assigned to Counter 2
```

## 🔐 Kitchen Staff Workflow

### Login Process
1. Open Kitchen Login page
2. Select your counter from dropdown
3. Enter your 4-digit PIN
4. Click "Login to Counter"
5. See orders assigned to your station

### Order Management
- **New**: Item just received
- **Start**: Kitchen staff starts preparing
- **Ready**: Item is ready for pickup
- **Cancel**: Item cancelled

## 🛠️ API Endpoints

### Authentication
- `POST /api/kds/login/` - Counter PIN login

### Orders
- `GET /api/kds/orders/` - Get all orders
- `POST /api/kds/orders/create/` - Create new order (auto-assignment)
- `GET /api/kds/orders/counter/<counter_id>/` - Get orders for specific counter
- `POST /api/kds/orders/update-item-status/` - Update item status

### Counters
- `GET /api/kds/counters/` - Get all available counters
- `POST /api/kds/counters/create/` - Create new counter
- `POST /api/kds/counters/<id>/categories/` - Assign categories to counter

## 🌐 WebSocket Endpoints

- `ws://127.0.0.1:8000/ws/kitchen/?counter_id=<id>` - Real-time updates for specific counter

## 📁 Project Structure

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

## 🧪 Testing the System

### 1. Create Test Counters
```bash
# Create Biryani Counter
curl -X POST http://127.0.0.1:8000/api/kds/counters/create/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Biryani Station", "pin": "1702", "description": "Biryani and rice dishes"}'

# Assign categories
curl -X POST http://127.0.0.1:8000/api/kds/counters/1/categories/ \
  -H "Content-Type: application/json" \
  -d '{"categories": ["Biryani", "CHICKEN BRIYANI", "MUTTON BRIYANI"]}'
```

### 2. Create Test Order
```bash
curl -X POST http://127.0.0.1:8000/api/kds/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": "T-01",
    "customer_name": "Test Customer",
    "items": [
      {
        "name": "Chicken Biryani",
        "category": "Biryani",
        "quantity": 1,
        "price": 15.00
      }
    ]
  }'
```

### 3. Check Counter Orders
```bash
# Check Biryani Station orders
curl http://127.0.0.1:8000/api/kds/orders/counter/1/
```

## 🔧 Configuration

### Counter Categories
- **Biryani Station**: Biryani, CHICKEN BRIYANI, MUTTON BRIYANI, PRAWN BRIYANI, BEEF BRIYANI
- **Main Kitchen**: Main Course, Beverage, Dessert, lemon juice, orange juice, apple juice

### Smart Detection Rules
- **Biryani Items**: Contains "biryani", "briyani", "chicken", "mutton", "prawn", "beef"
- **Beverages**: Contains "juice", "coffee", "tea", "soda", "water", "drink"
- **Desserts**: Contains "dessert", "sweet", "cake", "ice cream", "kesari", "kulfi"
- **Main Course**: Contains "burger", "pizza", "pasta", "rice", "curry", "gravy"

## 🚀 Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up Redis for production WebSocket support
4. Configure static files serving
5. Set up proper logging
6. Use environment variables for secrets

## 📄 License

This project is licensed under the MIT License.

---

**🎉 Your KDS system is now fully automated! Just enter food names and quantities - the system handles everything else!**
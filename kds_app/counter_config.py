# Dynamic counter configuration with in-memory storage
# Users create all counters through the frontend - no predefined counters

# Dynamic counters storage (user-created counters only)
COUNTERS = {}
NEXT_COUNTER_ID = 1

def get_counter_name(counter_id):
    """Get counter name by ID"""
    return COUNTERS.get(counter_id, {}).get("name", "Unknown Counter")

def get_counter_pin(counter_id):
    """Get counter PIN by ID"""
    return COUNTERS.get(counter_id, {}).get("pin", "")

def get_all_counters():
    """Get all available counters"""
    return [
        {
            "id": counter_id,
            "name": data["name"],
            "pin": data["pin"],
            "description": data["description"]
        }
        for counter_id, data in COUNTERS.items()
    ]

def validate_counter_credentials(counter_id, pin):
    """Validate counter credentials"""
    return counter_id in COUNTERS and str(pin) == COUNTERS[counter_id]["pin"]

def create_counter(name, pin, description=""):
    """Create a new counter"""
    global NEXT_COUNTER_ID
    
    # Check if PIN already exists
    for existing_counter in COUNTERS.values():
        if existing_counter["pin"] == str(pin):
            return None, "PIN already exists"
    
    # Create new counter
    counter_id = NEXT_COUNTER_ID
    COUNTERS[counter_id] = {
        "name": name,
        "pin": str(pin),
        "description": description
    }
    NEXT_COUNTER_ID += 1
    
    return counter_id, "Counter created successfully"

def update_counter(counter_id, name=None, pin=None, description=None):
    """Update an existing counter"""
    if counter_id not in COUNTERS:
        return False, "Counter not found"
    
    # Check if new PIN conflicts with existing counters
    if pin:
        for cid, counter in COUNTERS.items():
            if cid != counter_id and counter["pin"] == str(pin):
                return False, "PIN already exists"
    
    # Update fields
    if name is not None:
        COUNTERS[counter_id]["name"] = name
    if pin is not None:
        COUNTERS[counter_id]["pin"] = str(pin)
    if description is not None:
        COUNTERS[counter_id]["description"] = description
    
    return True, "Counter updated successfully"

def delete_counter(counter_id):
    """Delete a counter"""
    if counter_id not in COUNTERS:
        return False, "Counter not found"
    
    del COUNTERS[counter_id]
    return True, "Counter deleted successfully"

def reset_to_defaults():
    """Reset counters to empty state"""
    global COUNTERS, NEXT_COUNTER_ID
    COUNTERS = {}
    NEXT_COUNTER_ID = 1
    return True, "All counters deleted"

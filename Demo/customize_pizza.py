from flask import Blueprint, render_template, request, session, flash
import json
import os

customize_pizza_bp = Blueprint('customize_pizza', __name__)

MENU_ITEMS = {
    "Cheese Pizza": {"price": 10.00},
    "Pepperoni Pizza": {"price": 12.00},
    "Supreme Pizza": {"price": 14.00},
    "Veggie Pizza": {"price": 13.00},
}

ORDERS_FILE = "orders.json"

# Helper Functions to Manage JSON Storage
def load_orders():
    """Load orders from JSON file, creating it if necessary."""
    if not os.path.exists(ORDERS_FILE):
        save_orders([])  # Initialize an empty orders.json if missing
    try:
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
            if not isinstance(orders, list):  # Ensure the data is a list
                print("⚠️ orders.json is not a list. Resetting to an empty list.")
                return []
            return orders
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️ Error loading orders.json! Initializing empty list.")
        return []

def save_orders(orders):
    """Save orders to JSON file safely."""
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)

@customize_pizza_bp.route('/', methods=['GET', 'POST'])
def customize_pizza():
    """Handle pizza customization and display the current order."""
    if "current_order" not in session:
        session["current_order"] = []  # Initialize the order in the session

    orders = session["current_order"]  # Retrieve the current order
    username = session.get("username", "Guest")
    user_id = session.get("user_id", os.urandom(8).hex())  # Generate a user_id if not already set
    session["user_id"] = user_id  # Ensure user_id is stored in the session

    if request.method == 'POST':
        # Process the submitted quantities
        for pizza, details in MENU_ITEMS.items():
            quantity = request.form.get(f"quantity_{pizza}", "0")  # Default to "0" if not provided
            try:
                quantity = int(quantity)  # Convert to integer
                if quantity > 0:
                    # Check if the pizza is already in the order
                    existing_item = next((item for item in orders if item['Item'] == pizza), None)
                    if existing_item:
                        # Update the quantity and price
                        existing_item['Quantity'] += quantity
                        existing_item['Price'] += details['price'] * quantity
                    else:
                        # Add a new item to the order
                        orders.append({
                            'Item': pizza,
                            'Quantity': quantity,
                            'Price': details['price'] * quantity,
                        })
            except ValueError:
                flash(f"Invalid quantity for {pizza}. Skipping.", "error")

        # Save the updated order in the session
        session["current_order"] = orders

        # Save the order to orders.json
        all_orders = load_orders()
        print("Type of all_orders:", type(all_orders))  # Debugging: Ensure it's a list
        new_order = {
            "order_id": len(all_orders) + 1,
            "user_id": user_id,
            "username": username,
            "order_items": orders.copy(),  # Use a copy to avoid modifying the session data
            "status": "Pending"
        }
        all_orders.append(new_order)
        save_orders(all_orders)

        flash("✅ Your order has been updated and saved!", "success")

    # Render the page with the current order
    return render_template('customize_pizza.html', menu=MENU_ITEMS, username=username, order=orders)
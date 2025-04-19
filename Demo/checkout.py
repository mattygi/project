from flask import Blueprint, request, jsonify, session, flash, redirect, url_for, render_template
import json
import os
import logging

checkout_bp = Blueprint('checkout', __name__)

ORDERS_FILE = "orders.json"

# Helper Functions to Manage JSON Storage
def load_orders():
    """Load orders from JSON file, creating it if necessary."""
    if not os.path.exists(ORDERS_FILE):
        save_orders([])  # Initialize an empty orders.json if missing
    try:
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️ Error loading orders.json! Initializing empty list.")
        return []

def save_orders(orders):
    """Save orders to JSON file safely."""
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)

@checkout_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Process checkout for pending orders."""
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to proceed to checkout.", "error")
        return redirect(url_for('login'))

    if request.method == 'GET':
        # Render the checkout page
        orders = load_orders()

        # Find user's pending orders
        user_orders = [order for order in orders if order.get("user_id") == user_id and order.get("status") == "Pending"]

        if not user_orders:
            flash("⚠️ No pending orders to checkout!", "error")
            return redirect(url_for('cart.cart'))  # Redirect back to cart

        return render_template('checkout.html', cart=user_orders)

    elif request.method == 'POST':
        # Redirect to payment page
        return redirect(url_for('payment'))

@checkout_bp.route('/process_checkout', methods=['POST'])
def process_checkout():
    """Handle the checkout process."""
    try:
        # Extract form data
        data = request.json  # Expecting JSON data
        pizza = data.get('pizza')
        quantity = data.get('quantity')
        size = data.get('size')
        price = data.get('price')
        delivery_method = data.get('delivery_method')  # 'in_store_pickup' or 'delivery'
        payment_method = data.get('payment_method')  # 'online' or 'in_store'
        email = data.get('email')

        # Validate required fields
        if not all([pizza, quantity, size, price, delivery_method, payment_method]):
            return jsonify({"error": "Missing order details."}), 400

        # Load existing orders
        orders = load_orders()

        # ✅ Store order details
        user_id = session.get("user_id", os.urandom(8).hex())  # Ensure user_id is set
        order_data = {
            "order_id": len(orders) + 1,
            "user_id": user_id,
            "Pizza": pizza,
            "Quantity": int(quantity),
            "Size": size,
            "Price": float(price),
            "Delivery Method": delivery_method,
            "Payment Method": payment_method,
            "Status": "Complete"
        }
        orders.append(order_data)
        save_orders(orders)  # Save the updated orders to orders.json

        # ✅ Track order completion in session
        session['order_status'] = "Complete"

        logging.info(f"Order processed: {order_data}")
        return jsonify({"message": "Order processed successfully!", "order": order_data}), 200

    except Exception as e:
        logging.error(f"Error processing checkout: {str(e)}")
        return jsonify({"error": str(e)}), 500
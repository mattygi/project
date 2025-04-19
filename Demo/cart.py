import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

cart_bp = Blueprint('cart', __name__)

ORDERS_FILE = "orders.json"

# ✅ Helper Functions to Manage JSON Storage
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

@cart_bp.route('/', methods=['GET'])
def cart():
    """Display pending orders in the user's cart."""
    orders = load_orders()  # Load orders from orders.json
    user_id = session.get("user_id")  # Get the logged-in user's user_id

    if not user_id:
        flash("You must be logged in to view your cart.", "error")
        return redirect(url_for('login'))

    # Filter orders for the logged-in user with status "Pending"
    user_orders = [order for order in orders if order.get("user_id") == user_id and order.get("status") == "Pending"]

    if not user_orders:
        flash("ℹ️ Your cart is empty!", "info")

    return render_template('cart.html', cart=user_orders or [])

@cart_bp.route('/checkout', methods=['GET', 'POST'])
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

        # Debugging: Print user_orders to verify structure
        print("User Orders:", user_orders)

        if not user_orders:
            flash("⚠️ No pending orders to checkout!", "error")
            return redirect(url_for('cart.cart'))  # Redirect back to cart

        return render_template('checkout.html', cart=user_orders)

    elif request.method == 'POST':
        # Handle the checkout process
        orders = load_orders()

        # Find user's pending orders
        user_orders = [order for order in orders if order.get("user_id") == user_id and order.get("status") == "Pending"]

        # Debugging: Print user_orders to verify structure
        print("User Orders:", user_orders)

        if not user_orders:
            flash("⚠️ No pending orders to checkout!", "error")
            return redirect(url_for('cart.cart'))  # Redirect back to cart

        # Update the status of the user's orders to "Completed"
        for order in user_orders:
            order["status"] = "Completed"

        save_orders(orders)  # Save the updated orders

        flash("🎉 Your order has been placed successfully!", "success")
        return redirect(url_for('cart.order_placed'))  # Redirect to a confirmation page

@cart_bp.route('/order_placed', methods=['GET'])
def order_placed():
    """Render the order placed confirmation page."""
    return render_template('order_placed.html')
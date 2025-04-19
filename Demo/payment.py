import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

ORDERS_FILE = "orders.json"  # ✅ JSON file for storing orders

# ✅ Helper Functions for JSON Storage
def load_orders():
    """Load orders from JSON file."""
    try:
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Initialize empty list if file not found

def save_orders(orders):
    """Save orders to JSON file."""
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    """Handle payment selection."""
    if request.method == 'POST':
        payment_method = request.form.get('method', 'Not Provided')  # Get the selected payment method
        flash(f"Payment method selected: {payment_method}. Proceeding to order confirmation.", "success")
        return redirect(url_for('order_placed'))  # Redirect to the order confirmation page

    return render_template('payment.html')

@app.route('/order_placed', methods=['GET'])
def order_placed():
    """Direct to the order confirmation page."""
    return render_template('orderPlaced.html')

if __name__ == '__main__':
    app.run(debug=True)
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

# Import blueprints
from customize_pizza import customize_pizza_bp
from cart import cart_bp

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Keep this secure in production

# Register blueprints
app.register_blueprint(customize_pizza_bp, url_prefix='/customize')
app.register_blueprint(cart_bp, url_prefix='/cart')

# ✅ Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ✅ Hardcoded Menu Items (No Database Needed)
MENU_ITEMS = {
    "Cheese Pizza": "$10.00",
    "Pepperoni Pizza": "$12.00",
    "Supreme Pizza": "$14.00",
    "Veggie Pizza": "$13.00"
}

# ✅ JSON Files for Persistent User & Order Storage
USERS_FILE = "users.json"
ORDERS_FILE = "orders.json"

# ✅ Helper Functions for JSON Storage
def load_json(file):
    """Load data from JSON file."""
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Initialize empty list if file not found
    except json.JSONDecodeError:
        return []  # Handle empty or corrupted JSON file

def save_json(file, data):
    """Save data to JSON file."""
    try:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving to {file}: {e}")
        flash("Failed to save data. Please try again.", "error")  # Inform the user

@app.route('/')
def index():
    """Serve the homepage."""
    return render_template('index.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """Handle admin login."""
    if request.method == 'POST':
        admin_username = request.form.get('username')
        admin_password = request.form.get('password')

        # Check hardcoded admin credentials
        if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['username'] = admin_username
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_menu'))  # Redirect to admin menu
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect(url_for('admin_login'))

    return render_template('adminLogin.html')



@app.route('/proceed', methods=['POST'])
def proceed():
    """Handle the submission of checkout details."""
    delivery_method = request.form.get('method')  # Get the delivery method (e.g., 'delivery' or 'pickup')

    if not delivery_method:
        flash("Please choose a delivery method.", "error")
        return redirect(url_for('checkout'))

    # Redirect to the payment page after processing
    flash(f"Proceeding with {delivery_method} option.", "success")
    return redirect(url_for('payment'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ✅ Admin Login
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["role"] = "store_owner"
            session["username"] = username
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_menu'))

        # ✅ Customer Login
        users = load_json(USERS_FILE)
        user = next((u for u in users if u["username"] == username and u["password"] == password), None)

        if user:
            session["role"] = "customer"
            session["username"] = username
            session["user_id"] = user.get("user_id", os.urandom(8).hex())  # Set user_id
            flash("Login successful!", "success")
            return redirect(url_for('index'))  # Redirect to the homepage

        # Invalid Credentials
        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        users = load_json(USERS_FILE)

        if any(u["username"] == username for u in users):
            flash("Username already exists!", "error")
            return redirect(url_for('register'))

        user_id = os.urandom(8).hex()  # Generate user_id
        users.append({"username": username, "password": password, "role": "customer", "user_id": user_id})
        save_json(USERS_FILE, users)
        session["user_id"] = user_id  # Set user_id
        session["username"] = username  # Set username
        flash("Registration successful!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    """Handle payment process."""
    if request.method == 'POST':
        
        return redirect(url_for('payment'))  # Redirect to order confirmation page
    return render_template('payment.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Handle checkout process for pending orders."""
    orders = load_json(ORDERS_FILE)
    username = session.get("username")

    pending_orders = [order for order in orders if order["username"] == username and order["status"] == "Pending"]

    if request.method == 'POST':
        delivery_method = request.form.get('method')

        if not delivery_method:
            flash("Please choose a delivery method.", "error")
            return render_template('checkout.html', cart=pending_orders)

        for order in orders:
            if order["username"] == username and order["status"] == "Pending":
                order["status"] = "Complete"

        save_json(ORDERS_FILE, orders)
        flash(f"Order placed successfully with {delivery_method} option! Redirecting to payment.", "success")
        return redirect(url_for('payment'))

    return render_template('checkout.html', cart=pending_orders)

@app.route('/store_orders', methods=['GET'])
def store_orders():
    """Show completed orders for the logged-in user."""
    orders = load_json(ORDERS_FILE)
    username = session.get("username")
    completed_orders = [order for order in orders if order["username"] == username and order["status"] == "Complete"]
    return render_template('storeOrders.html', orders=completed_orders)

@app.route('/order_placed', methods=['GET'])
def order_placed():
    """Direct to the order confirmation page."""
    return render_template('orderPlaced.html')

@app.route('/admin_menu')
def admin_menu():
    """Render the admin menu."""
    return render_template('adminMenu.html')

@app.route('/logout')
def logout():
    """Log out the user."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
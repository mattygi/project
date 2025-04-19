from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Replace with a secure key in production

# ✅ Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ✅ Hardcoded Menu Items
MENU_ITEMS = {
    "1": {"name": "Cheese Pizza", "price": "$10.00"},
    "2": {"name": "Pepperoni Pizza", "price": "$12.00"},
    "3": {"name": "Supreme Pizza", "price": "$14.00"},
    "4": {"name": "Veggie Pizza", "price": "$13.00"},
}

# ✅ Hardcoded Orders (Dynamically updated)
ORDERS = []

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form.get('username')
        admin_password = request.form.get('password')

        if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_menu'))  # Redirects to Admin Menu
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect(url_for('admin_login'))

    return render_template('adminLogin.html')

@app.route('/admin_menu')
def admin_menu():
    """Render the admin menu."""
    return render_template('adminMenu.html', message="Welcome Admin! Manage store orders and menu items.")

@app.route('/store_orders')
def store_orders():
    """Render the store orders page."""
    return render_template('storeOrders.html', orders=ORDERS)  # ✅ Now pulling dynamic orders







if __name__ == '__main__':
    app.run(debug=True)
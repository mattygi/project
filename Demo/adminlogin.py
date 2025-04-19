from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Temporary key for development

# ✅ Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """Handle admin login."""
    if request.method == 'POST':
        admin_username = request.form.get('username')
        admin_password = request.form.get('password')

        # For demonstration purposes, always log in successfully
        session['admin_logged_in'] = True  # Set admin login flag
        session['username'] = admin_username  # Store admin username
        flash("Admin login successful!", "success")
        return redirect(url_for('admin_menu'))  # Redirect to admin menu

    return render_template('adminLogin.html')

@app.route('/admin_menu')
def admin_menu():
    """Render the admin menu."""
    # For demonstration purposes, allow access without checking session
    return render_template('adminMenu.html', message="Welcome Admin! Manage your menu here.")

@app.route('/logout')
def logout():
    """Log out the user."""
    session.clear()  # Clear the session
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
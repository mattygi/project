
import os
import json
import re
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

USERS_FILE = "users.json"  # ✅ JSON file for storing user data

# ✅ Helper Functions for JSON Storage
def load_users():
    """Load user data from JSON file."""
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"admin": {"email": "admin@example.com", "password": generate_password_hash("admin123")}}  # Default admin account

def save_users(users):
    """Save user data to JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration with JSON storage."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # ✅ Basic validation
        if not username or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('register'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.", "error")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return redirect(url_for('register'))

        # ✅ Load existing users
        users = load_users()

        # ✅ Check if user already exists
        if username in users or any(user["email"] == email for user in users.values()):
            flash("Username or email already exists.", "error")
            return redirect(url_for('register'))

        # ✅ Hash password before storing
        users[username] = {"email": email, "password": generate_password_hash(password)}
        save_users(users)  # ✅ Store updated user list

        flash("Account created successfully!", "success")
        return redirect(url_for('login'))  # Redirect to login after registration

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login using JSON storage."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ✅ Validate input fields
        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for('login'))

        # ✅ Load users from JSON
        users = load_users()

        # ✅ Authenticate user
        user = users.get(username)
        if user and check_password_hash(user["password"], password):
            session['username'] = username
            flash(f"Login successful! Welcome, {username}.", "success")
            return redirect(url_for('index'))

        flash("Invalid username or password.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Log out user and clear session."""
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

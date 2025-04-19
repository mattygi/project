from flask import Flask, render_template
import json
import os

app = Flask(__name__)

# Path to the orders.json file
ORDERS_FILE = "orders.json"

def load_json(file):
    """Load data from a JSON file."""
    try:
        print(f"Loading JSON from: {file}")  # Debug
        print(f"File exists: {os.path.exists(file)}")  # Debug
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("File not found!")  # Debug
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")  # Debug
        return []  # Handle corrupted or empty JSON files

@app.route('/store_orders', methods=['GET'])
def store_orders():
    """Render the store orders page."""
    orders = load_json(ORDERS_FILE)  # Load orders from the JSON file
    print(f"Orders loaded: {orders}")  # Debugging: Print the loaded orders to the console
    return render_template('storeOrders.html', raw_orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
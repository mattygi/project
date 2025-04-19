from flask import Flask, render_template
import json

app = Flask(__name__)

# Path to the orders.json file
ORDERS_FILE = "orders.json"

def load_json(file):
    """Load data from a JSON file."""
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        return []  # Handle corrupted or empty JSON files

@app.route('/store_orders', methods=['GET'])
def store_orders():
    """Render the store orders page."""
    orders = load_json(ORDERS_FILE)  # Load orders from the JSON file
    print(orders)  # Debugging: Print the loaded orders to the console
    return render_template('storeOrders.html', raw_orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
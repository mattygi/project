from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

@app.route('/order_placed', methods=['GET'])
def order_placed():
    """Direct to the order confirmation page."""
    return render_template('orderPlaced.html')

if __name__ == '__main__':
    app.run(debug=True)
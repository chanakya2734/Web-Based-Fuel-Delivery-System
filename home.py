from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Database file path (in same directory as home.py)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuel.db')


def setup_sqlite_db():
    """Create SQLite schema and insert seed data if not present."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manager (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS delivery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fuelAmount TEXT,
        fuelType TEXT,
        userLocationLat REAL,
        userLocationLng REAL,
        petrolBunkLocationLat REAL,
        petrolBunkLocationLng REAL,
        timestamp_booked TEXT,
        timestamp_delivered TEXT,
        status TEXT DEFAULT 'Pending',
        delivered TEXT DEFAULT 'Not Delivered'
    )
    """)
    cursor.execute("INSERT OR IGNORE INTO manager (username, password) VALUES ('admin', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO customer (username, password) VALUES ('customer1', 'cust123')")
    cursor.execute("INSERT OR IGNORE INTO delivery (username, password) VALUES ('delivery1', 'del123')")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"SQLite database ready at: {DB_PATH}")


# Initialize the database on startup
setup_sqlite_db()


def get_db_connection():
    """Get a SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def database_login(tb_name, username, password):
    """Verify login credentials using parameterized queries."""
    allowed_tables = {'manager', 'customer', 'delivery'}
    if tb_name not in allowed_tables:
        return False

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM {tb_name} WHERE username = ? AND password = ?",
            (username, password)
        )
        result = cursor.fetchall()
        return len(result) > 0
    finally:
        conn.close()


@app.route('/')
def hello():
    return render_template("home.html")


@app.route('/manager', methods=['POST'])
def manager():
    username = request.form.get('Username')
    password = request.form.get('Password')
    f = database_login('manager', username, password)
    if f:
        bookings = get_booking_details()
        stats = {
            'total': len(bookings),
            'pending': sum(1 for b in bookings if b['status'] == 'Pending'),
            'accepted': sum(1 for b in bookings if b['status'] == 'Accepted'),
            'delivered': sum(1 for b in bookings if b['delivered'] == 'Delivered')
        }
        return render_template('manager.html', bookings=bookings, stats=stats)
    else:
        return render_template("home.html", error="Invalid manager credentials. Please try again.")


@app.route('/delivery', methods=['POST'])
def delivery():
    username = request.form.get('Username')
    password = request.form.get('Password')
    f = database_login('delivery', username, password)
    if f:
        bookings = get_booking_details()
        return render_template("delivery.html", bookings=bookings)
    return render_template("home.html", error="Invalid delivery credentials. Please try again.")


@app.route('/customer', methods=['POST'])
def customer():
    username = request.form.get('Username')
    password = request.form.get('Password')
    f = database_login('customer', username, password)
    if f:
        return render_template("customer.html")
    else:
        return render_template("home.html", error="Invalid customer credentials. Please try again.")


def update_booking_status(id, status):
    """Update a booking's status."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, id))
        conn.commit()
    finally:
        conn.close()


def insert_booking_info_into_database(data):
    """Insert a new booking into the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        sql = """INSERT INTO bookings 
                 (fuelAmount, fuelType, userLocationLat, userLocationLng, 
                  petrolBunkLocationLat, petrolBunkLocationLng, 
                  timestamp_booked, timestamp_delivered, status, delivered) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        timestamp_booked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        val = (
            data['fuelAmount'], data['fuelType'],
            data['userLocation']['lat'], data['userLocation']['lng'],
            data['petrolBunkLocation']['lat'], data['petrolBunkLocation']['lng'],
            timestamp_booked, None, 'Pending', 'Not Delivered'
        )

        cursor.execute(sql, val)
        conn.commit()
    finally:
        conn.close()


@app.route('/save_booking_info', methods=['POST'])
def save_booking_info():
    data = request.get_json()
    insert_booking_info_into_database(data)
    return jsonify({'message': 'Booking saved successfully!'}), 200


def get_booking_details():
    """Fetch all booking details from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        rows = cursor.fetchall()
        # Convert sqlite3.Row objects to dicts
        bookings = [dict(row) for row in rows]
        return bookings
    finally:
        conn.close()


@app.route('/fetch_booking_details')
def fetch_booking_details():
    bookings = get_booking_details()
    html_content = ''
    for booking in bookings:
        html_content += f"<tr>\
            <td class='delivery-status'>{booking['id']}</td>\
            <td class='delivery-status'>{booking['status']}</td>\
            <td class='delivery-status'>{booking['fuelType']}</td>\
            <td class='delivery-status'>{booking['fuelAmount']}</td>\
            <td class='delivery-status'>{booking['timestamp_booked']}</td>\
            <td class='delivery-time'>{booking['timestamp_delivered'] if booking['timestamp_delivered'] else ''}</td>\
             <td class='delivery-status'>{booking['delivered']}</td>\
        </tr>"

    return jsonify(html_content)


@app.route('/accept_booking/<int:booking_id>', methods=['POST'])
def accept_booking(booking_id):
    update_booking_status(booking_id, 'Accepted')
    bookings = get_booking_details()
    stats = {
        'total': len(bookings),
        'pending': sum(1 for b in bookings if b['status'] == 'Pending'),
        'accepted': sum(1 for b in bookings if b['status'] == 'Accepted'),
        'delivered': sum(1 for b in bookings if b['delivered'] == 'Delivered')
    }
    return render_template("manager.html", bookings=bookings, stats=stats)


@app.route('/update_delivery_status', methods=['POST'])
def update_delivery_status():
    data = request.get_json()
    booking_id = data.get('bookingId')
    status = "Delivered"
    delivery_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        sql = "UPDATE bookings SET delivered = ?, timestamp_delivered = ? WHERE id = ?"
        val = (status, delivery_timestamp, booking_id)
        cursor.execute(sql, val)
        conn.commit()
    finally:
        conn.close()

    return jsonify({'message': 'Delivery status updated successfully.'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from datetime import datetime
app = Flask(__name__)

def database_login(tb_name, username, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="fuel"
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        f"SELECT * FROM {tb_name} WHERE username = '{username}' and password = '{password}'")
    myresult = mycursor.fetchall()
    f = False
    for x in myresult:
        f = True
        break
    return f

@app.route('/')
def hello():
    return render_template("home.html", path='/static/fuel3.jpg')

@app.route('/manager', methods=['POST'])
def manager():
    username = request.form.get('Username')
    password = request.form.get('Password')
    f = database_login('manager', username, password)
    if f:
        bookings=get_booking_details()
        return render_template('manager.html',bookings=bookings)
    else:
        return "Login Failed!..."

@app.route('/delivery', methods=['POST'])
def delivery():
    username = request.form.get('Username')
    password = request.form.get('Password')
    f = database_login('delivery', username, password)
    if f:
        bookings=get_booking_details()
        return render_template("delivery.html",bookings=bookings)
    return "Login Failed!..."

@app.route('/customer', methods=['POST'])
def customer():
    username = request.form.get('Username')
    password = request.form.get('Password')
    f = database_login('customer', username, password)
    if f:
        return render_template("customer.html")
    else:
        return "Login Failed!..."
    
def update_booking_status(id,status):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="fuel"
        )
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE bookings SET status = %s WHERE id = %s", (status, id))
        mydb.commit()

def insert_booking_info_into_database(data):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="fuel"
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO bookings (fuelAmount, fuelType, userLocationLat, userLocationLng, petrolBunkLocationLat, petrolBunkLocationLng, timestamp_booked, timestamp_delivered, status, delivered) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    timestamp_booked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    val = (data['fuelAmount'], data['fuelType'], data['userLocation']['lat'], data['userLocation']['lng'], data['petrolBunkLocation']['lat'], data['petrolBunkLocation']['lng'], timestamp_booked, None, 'Pending', 'Not Delivered')

    mycursor.execute(sql, val)

    mydb.commit()

@app.route('/save_booking_info', methods=['POST'])
def save_booking_info():
    data = request.get_json()

    insert_booking_info_into_database(data)

    return redirect(url_for("manager"))
    
booking=[]


def get_booking_details():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="fuel"
    )

    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM bookings")
    bookings = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return bookings

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
            <td class='delivery-time'>{booking['timestamp_delivered']}</td>\
             <td class='delivery-status'>{booking['delivered']}</td>\
        </tr>"

    return jsonify(html_content)

def fetch_delivery_coordinates():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fuel"
        )
        cursor = mydb.cursor()
        cursor.execute("SELECT userLocationLat, userLocationLng, PetrolBunkLocationLat, PetrolBunkLocationLng FROM bookings")
        coordinates = cursor.fetchone()  
        mydb.close()
        return coordinates
    except mysql.connector.Error as error:
        print("Failed to fetch data from MySQL: {}".format(error))
        return None

@app.route('/accept_booking/<int:booking_id>', methods=['POST'])
def accept_booking(booking_id):
    update_booking_status(booking_id, 'Accepted')
    return render_template("manager.html")
    
@app.route('/update_delivery_status', methods=['POST'])
def update_delivery_status():
    data = request.get_json()
    booking_id = data.get('bookingId')
    status = "Delivered"
    delivery_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="fuel"
    )
    mycursor = mydb.cursor()
    
    sql = "UPDATE bookings SET delivered = %s, timestamp_delivered = %s WHERE id = %s"
    val = (status, delivery_timestamp, booking_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return jsonify({'message': 'Delivery status updated successfully.'}), 200

app.run(host='0.0.0.0',port=5050)
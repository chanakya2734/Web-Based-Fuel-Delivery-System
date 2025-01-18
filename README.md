# Web-Based-Fuel-Delivery-System
This project developed a web-based fuel delivery system with three interfaces: customer, manager and delivery boy. Using the google API key, the system captures customer locations for  fuel delivery, which uses a MYSQL database managed user data, orders and delivery status. The manager interface track orders and delivery progress in real-time.
# Objectives of the Project are:
1. The Primary aim is to provide customers with the convenience of fuel delivery directly to their desired location, eliminating the need for them to visit a fuel station.
2. The fuel delivery application enables the customers to get rid of waiting in along queue for fuel it can save time and effort.
3. The application provides fuel at the customer's door step and can offer improved customer services.
4. Integrate GPS into this application to monitor the customer's location and delivery boy location.
# System Configuration:
Hardware requirements:
RAM: 8GB
CPU: Minimum Core i3 processor
Storage: Minimum 256GB SSD should be sufficient
Software requirements:
Operating System: Any modern operating system such as Windows, macOS or a Linux distribution
Technology Stack:
Frontend: HTML, CSS and Javascript
Backend: 
Python: Version 3.x
Flask: Micro web framework for python
Database: MYSQL: MYSQL is a relational database management system for storing customer data and orders
Integrated Development Environment(IDE): Visual Studio Code
Geolocation Services: Google Maps API to provide location-based services for delivery
# The Overview of the Web Application
The process consists of five key steps:
Step 1:Login: Customer, Manager & Delivery Boy must login with valid email and password
Step 2:Find Petrol Pump Near You: Customer has a look to the nearby petrol pump
Step 3:Make an order: He or she can make an order based on its needs
Step 4:Assign Order to Delivery Boy: This is the person who provides the fuel to the customer
Step 5:Customer Delivery: Customers receive fuel according on their needs
The main interface of the project where three options were displayed customer, manager and delivery boy. If a customer opens the page, he or she can select option as customer. If a manager opens the page, he or she can select option as manager. If a delivery boy opens the page, he can select option as delivery boy.
# Customer Interface
The interface of the customer when customer option is selected. There are two options under its customer can enter his username and password for further process.
After customer login, customer's current location will be saved automatically and the fuel will be delivered to that location. Few labels will be displayed in this interface like "Booking ID", "Order Status", "Fuel Type", "Fuel Amount", "Booked Time Stamp", "Delivered Time Stamp" and "Order Status".
Now customer can select the nearby petrol bunk from google map, after selecting the nearby petrol bunk a dialog box will be opened asking which type of fuel should be delivered we can write according to the requirements whether the customer require "Petrol" or "Diesel".
After providing the type of fuel customer required when click ok button, another dialog box will be opened and we need to enter the amount of fuel customer required.
After fuel order by the customer, customer will be able to see the display as petrol pump details. Customer can able to see his or her location details.
# Manager Interface
Manager can login by filling manager's username and manager's password.
Manager receives the booking details by the customer and if the manager accepts the order, then customer can view whether the manager had accepted the order status.
# Delivery Boy Interface
The interface for delivery boy to login and check for the orders.
After successful login of delivery boy, He can able to see the customer's location and his location. According to the location on the google map delivery boy delivers the fuel to the customers.

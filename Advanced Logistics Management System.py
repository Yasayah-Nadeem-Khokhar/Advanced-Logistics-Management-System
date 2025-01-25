import mysql.connector
from mysql.connector import errorcode

# Establish a connection to the MySQL database
try:
    # Connect to MySQL server (no password)
    db = mysql.connector.connect(
        host="127.0.0.1",        # Your MySQL server (default is localhost)
        user="root",          # Your MySQL username
        password="********", 
    )
    
    cursor = db.cursor()

    # Create a database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS logisticCompany")
    
    # Select the database to work with
    cursor.execute("USE logisticCompany")
    
    # SQL query to create a table
    create_table_query = '''

CREATE TABLE IF NOT EXISTS Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    phone_number VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    registration_date DATE,
    customer_type VARCHAR(50),
    status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Delivery_Metrics (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    shipment_id INT NOT NULL UNIQUE,
    vehicle_id INT NOT NULL,
    route_id INT NOT NULL,
    delivery_time DATETIME NOT NULL,
    delay_minutes INT,
    on_time_status VARCHAR(20),
    scheduled_delivery_time DATETIME,
    pickup_time DATETIME,
    delivery_attempts INT,
    delivery_status VARCHAR(50),
    customer_feedback_score INT,
    damage_report TEXT,
    delivery_person_id INT,
    fuel_consumed DECIMAL(10, 2),
    weather_conditions VARCHAR(255),
    additional_notes TEXT
);

CREATE TABLE IF NOT EXISTS Vehicle_Utilization (
    vehicle_id INT PRIMARY KEY,
    total_distance_covered DECIMAL(10, 2),
    total_shipments INT,
    active_hours DECIMAL(5, 2),
    maintenance_hours DECIMAL(5, 2),
    average_speed DECIMAL(5, 2),
    utilization_rate DECIMAL(5, 2),
    idle_time DECIMAL(5, 2),
    operating_cost DECIMAL(10, 2),
    breakdown_count INT,
    emissions_output DECIMAL(10, 2),
    trip_count INT,
    last_service_date DATE,
    route_efficiency DECIMAL(5, 2)
);

CREATE TABLE IF NOT EXISTS Customer_Feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    shipment_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    feedback_date DATE NOT NULL,
    service_quality DECIMAL(5, 2),
    delivery_timeliness DECIMAL(5, 2),
    customer_satisfaction DECIMAL(5, 2),
    issue_reported TEXT,
    resolved_status VARCHAR(20),
    follow_up_date DATE,
    feedback_source VARCHAR(50),
    response_time DECIMAL(5, 2),
    resolved_by INT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (shipment_id) REFERENCES Delivery_Metrics(shipment_id)
);

CREATE TABLE IF NOT EXISTS Support_Staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL,
    assigned_ticket_count INT DEFAULT 0,
    ticket_resolution_rate DECIMAL(5, 2) DEFAULT 0.00,
    average_resolution_time DECIMAL(10, 2) DEFAULT 0.00,
    last_login_time DATETIME,
    performance_rating DECIMAL(3, 2) DEFAULT 0.00,
    supervisor_id INT,
    FOREIGN KEY (supervisor_id) REFERENCES Support_Staff(staff_id)
);

CREATE TABLE IF NOT EXISTS Support_Tickets (
    ticket_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    shipment_id INT NOT NULL,
    issue_type VARCHAR(100) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    opened_date DATETIME NOT NULL,
    closed_date DATETIME,
    resolution_notes TEXT,
    assigned_staff_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (shipment_id) REFERENCES Delivery_Metrics(shipment_id),
    FOREIGN KEY (assigned_staff_id) REFERENCES Support_Staff(staff_id) 
);



CREATE TABLE IF NOT EXISTS Third_Party_Shipments (
    shipment_id INT PRIMARY KEY,
    third_party_name VARCHAR(100) NOT NULL,
    tracking_id VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    estimated_delivery_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Third_Party_Accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    third_party_name VARCHAR(100) NOT NULL,
    api_key VARCHAR(255) NOT NULL UNIQUE,
    account_status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Employee_Records (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    role VARCHAR(50),
    hire_date DATE,
    employment_status VARCHAR(20),
    salary DECIMAL(15, 2),
    department VARCHAR(50),
    manager_id INT,
    performance_review_date DATE,
    benefits TEXT,
    contact_number VARCHAR(15),
    CNIC_number VARCHAR(20) UNIQUE
);

CREATE TABLE IF NOT EXISTS Drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone_number VARCHAR(20),
    license_number VARCHAR(50) NOT NULL,
    years_of_experience INT,
    FOREIGN KEY (employee_id) REFERENCES Employee_Records(employee_id)
);

CREATE TABLE IF NOT EXISTS Vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(100) NOT NULL,
    license_plate VARCHAR(20) NOT NULL,
    capacity INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    fuel_type VARCHAR(50),
    purchase_date DATE,
    service_due_date DATE,
    insurance_expiry_date DATE,
    odometer_reading DECIMAL(10, 2),
    gps_enabled BOOLEAN DEFAULT FALSE,
    driver_assigned_id INT,
    current_location VARCHAR(255),
    avg_fuel_efficiency DECIMAL(5, 2),
    usage_category VARCHAR(50),
    load_sensor_installed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (driver_assigned_id) REFERENCES Drivers(driver_id)
);

CREATE TABLE IF NOT EXISTS Routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    start_location VARCHAR(255) NOT NULL,
    end_location VARCHAR(255) NOT NULL,
    route_distance DECIMAL(10, 2) NOT NULL,
    estimated_time TIME NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    traffic_conditions VARCHAR(255),
    fuel_consumed DECIMAL(10, 2),
    status VARCHAR(50),
    stops TEXT,
    checkpoint_ids TEXT,
    optimized_flag BOOLEAN DEFAULT FALSE,
    weather_conditions VARCHAR(255),
    route_type VARCHAR(100),
    remarks TEXT,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);


CREATE TABLE IF NOT EXISTS Carbon_Emissions (
    vehicle_id INT NOT NULL,
    route_id INT NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    distance_traveled DECIMAL(10, 2) NOT NULL,
    emissions_amount DECIMAL(10, 2) NOT NULL,
    calculation_date DATE NOT NULL,
    PRIMARY KEY (vehicle_id, route_id, calculation_date),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id),
    FOREIGN KEY (route_id) REFERENCES Routes(route_id)
);

CREATE TABLE IF NOT EXISTS Energy_Efficiency (
    vehicle_id INT NOT NULL,
    shipment_count INT NOT NULL,
    fuel_consumption DECIMAL(10, 2) NOT NULL,
    efficiency_rating DECIMAL(5, 2) NOT NULL,
    PRIMARY KEY (vehicle_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);

CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    registration_date DATE,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS Roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS User_Access_Logs (
    log_id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NOT NULL,
    action VARCHAR(255) NOT NULL,
    PRIMARY KEY (log_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS User_Permissions (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    permission_level VARCHAR(50) NOT NULL,
    assigned_date DATE NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

CREATE TABLE IF NOT EXISTS Data_Subjects (
    data_subject_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    phone_number VARCHAR(20),
    date_of_birth DATE,
    address TEXT,
    status VARCHAR(50) DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS Compliance_Records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    compliance_type VARCHAR(100) NOT NULL,
    data_subject_id INT NOT NULL,
    data_request_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (data_subject_id) REFERENCES Data_Subjects(data_subject_id)
);

CREATE TABLE IF NOT EXISTS Delivery_Options (
    option_id INT AUTO_INCREMENT PRIMARY KEY,
    option_name VARCHAR(100) NOT NULL,
    base_fee DECIMAL(10, 2) NOT NULL,
    surcharge DECIMAL(10, 2) DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS Additional_Fees (
    fee_id INT AUTO_INCREMENT PRIMARY KEY,
    fee_type VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS Vehicle_Maintenance (
    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT,
    maintenance_date DATE NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    notes TEXT,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);

CREATE TABLE IF NOT EXISTS Driver_Shifts (
    shift_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT NOT NULL,
    shift_start DATETIME NOT NULL,
    shift_end DATETIME NOT NULL,
    assigned_vehicle_id INT NOT NULL,
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id),
    FOREIGN KEY (assigned_vehicle_id) REFERENCES Vehicles(vehicle_id)
);

CREATE TABLE IF NOT EXISTS Route_Checkpoints (
    route_id INT NOT NULL,
    checkpoint_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    location VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    PRIMARY KEY (route_id, checkpoint_id),
    FOREIGN KEY (route_id) REFERENCES Routes(route_id)
);

CREATE TABLE IF NOT EXISTS Dynamic_Routing (
    route_id INT NOT NULL,
    optimized_start_time DATETIME NOT NULL,
    optimized_end_time DATETIME NOT NULL,
    distance_saved DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (route_id),
    FOREIGN KEY (route_id) REFERENCES Routes(route_id)
);

CREATE TABLE IF NOT EXISTS Hubs (
    hub_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    capacity INT NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Hub_Inventory (
    hub_id INT,
    package_id INT,
    storage_location VARCHAR(255) NOT NULL,
    stored_since_date DATE NOT NULL,
    PRIMARY KEY (hub_id, package_id),
    FOREIGN KEY (hub_id) REFERENCES Hubs(hub_id)
);

CREATE TABLE IF NOT EXISTS Hub_Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    hub_id INT,
    role VARCHAR(255) NOT NULL,
    shift VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255),
    FOREIGN KEY (hub_id) REFERENCES Hubs(hub_id)
);

CREATE TABLE IF NOT EXISTS Shipment_Tracking (
    Shipment_Tracking_id INT AUTO_INCREMENT PRIMARY KEY,
    shipment_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(255),
    status VARCHAR(255),
    estimated_delivery_time DATETIME,
    delivery_person_id INT,
    temperature_reading DECIMAL(5,2),
    humidity_reading DECIMAL(5,2),
    speed DECIMAL(5,2),
    altitude DECIMAL(5,2),
    event_type VARCHAR(255),
    remarks TEXT,
    next_checkpoint VARCHAR(255),
    last_updated_by INT,
    FOREIGN KEY (shipment_id) REFERENCES Delivery_Metrics(shipment_id),
    FOREIGN KEY (delivery_person_id) REFERENCES Drivers(driver_id),
    FOREIGN KEY (last_updated_by) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS IoT_Device_Data (
    device_id INT,
    shipment_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    GPS VARCHAR(255),
    battery_status VARCHAR(50),
    signal_strength DECIMAL(5,2),
    PRIMARY KEY (device_id, shipment_id, timestamp),
    FOREIGN KEY (shipment_id) REFERENCES Delivery_Metrics(shipment_id)
);

CREATE TABLE IF NOT EXISTS Invoices (
    invoice_id INT AUTO_INCREMENT,
    shipment_id INT,
    amount DECIMAL(10, 2),
    status VARCHAR(50),
    payment_method VARCHAR(50),
    tax_amount DECIMAL(10, 2),
    due_date DATE,
    PRIMARY KEY (invoice_id),
    FOREIGN KEY (shipment_id) REFERENCES Delivery_Metrics(shipment_id)
);

CREATE TABLE IF NOT EXISTS Payment_Transactions (
    transaction_id INT AUTO_INCREMENT,
    invoice_id INT,
    payment_date DATETIME,
    amount_paid DECIMAL(10, 2),
    method VARCHAR(50),
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id)
);

CREATE TABLE IF NOT EXISTS Discounts_and_Pos (
    promo_code VARCHAR(50) PRIMARY KEY,
    description TEXT,
    discount_amount DECIMAL(10, 2),
    expiry_date DATE
);

CREATE TABLE IF NOT EXISTS Outsourced_Vehicles (
    outsourcing_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_id INT,
    outsourcing_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    vendor_name VARCHAR(100),
    contract_details TEXT,
    cost DECIMAL(15, 2),
    status VARCHAR(20),
    vehicle_condition VARCHAR(50),
    vehicle_availability VARCHAR(20),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);

CREATE TABLE IF NOT EXISTS Outsourced_Drivers (
    outsourcing_id INT PRIMARY KEY AUTO_INCREMENT,
    driver_id INT,
    outsourcing_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    vendor_name VARCHAR(100),
    contract_details TEXT,
    cost DECIMAL(15, 2),
    status VARCHAR(20),
    driver_availability VARCHAR(20),
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
);

    '''
    
    # Execute the query
    cursor.execute(create_table_query)
    print("DataBase created successfully.")
    
    # Close the connection
    cursor.close()
    db.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your MySQL username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

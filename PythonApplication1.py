import random
import string
import datetime
import MySQLdb
from django import db
from flask import Flask, flash, jsonify, logging, render_template, request, redirect, session, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hms'

db = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    passwd=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

# User Classes
class User:
    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

class Patient(User):
    def __init__(self, userid, password):
        super().__init__(userid, password)

class Admin(User):
    def __init__(self, userid, password):
        super().__init__(userid, password)

# Routes

# Homepage
@app.route('/')
def home():
    return render_template('login.html')

# user screen
@app.route('/userscreen')
def userscreen():
    return render_template('userscreen.html')  # Make sure the 'userscreen.html' template exists

#doctor list
@app.route('/availabledoctor')
def doctor():
    return render_template('availabledoctor.html')

#appointment call
@app.route('/appointmentcall')
def appointmentcall():
    return render_template('appointmentcall.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Registration Form
def generate_random_id(length=8):
    """Generate a random alphanumeric ID of specified length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        action = request.form.get('action')  # Determines whether it's login or register
        patient_name = request.form.get('patient_name')
        gender = request.form.get('gender')
        id_card = request.form.get('idcardnumber')
        password = request.form.get('confirmpass')
        confirmpass = request.form.get('confirmpass')

        cursor = db.cursor()
        try:
            if action == 'register':  # Handle registration
                # Check if all fields are provided
                if not all([patient_name, gender, id_card, password, confirmpass]):
                    error = "All fields are required for registration!"
                    return render_template('register.html', error=error)

                # Insert the user data into the database
                cursor.execute("""
                    INSERT INTO patient_register (Patient_Name, Gender, ID_Card_Number, Password, Confirm_Password)
                    VALUES (%s, %s, %s, %s, %s)
                """, (patient_name, gender, id_card, password, confirmpass))
                db.commit()
                success_message = "User registered successfully! You can now log in."
                return render_template('login.html', success=success_message)

            elif action == 'login':  # Handle login
                # Check if the ID card exists
                cursor.execute("""
                    SELECT * FROM patient_register WHERE ID_Card_Number = %s
                """, (id_card,))
                user = cursor.fetchone()

                if user:
                    # Login successful, save user info in session
                    session['user_id'] = user[0]  # Assuming first column is the user's ID
                    session['user_name'] = user[1]  # Assuming second column is Patient_Name
                    return redirect(url_for('dashboard'))  # Redirect to dashboard
                else:
                    error = "Invalid ID Card Number. Please register first."
                    return render_template('login.html', error=error)

            else:
                error = "Invalid action. Please try again."
                return render_template('login.html', error=error)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
    
    # Generate ID
    patient_id = generate_random_id()
    # Render the login/registration form for GET requests
    return render_template('register.html', patient_id=patient_id)

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        action = request.form.get('action')  # Determines whether it's login or register
        userid = request.form.get('userid')  # User ID (Email for admin or patient ID for regular users)
        password = request.form.get('password')

        cursor = db.cursor()
        try:
            if action == 'login':  # Handle login

                # Check if the entered credentials are for admin
                if userid == 'admin.hospitalmanager@gmail.com' and password == 'HospitalManager@123':
                    return redirect(url_for('dashboard'))  # Redirect to admin portal

                # For non-admin users, check if the user exists in the database
                cursor.execute("""SELECT * FROM patient_register WHERE Patient_Name = %s AND Password = %s""", (userid, password))
                user = cursor.fetchone()

                if user:
                    # Save login data into login_user1 table
                    login_time = datetime.datetime.now()
                    cursor.execute("""
                        INSERT INTO login_user1 (Patient_Name, Password, Login_Time) 
                        VALUES (%s, %s, %s)
                    """, (userid, password, login_time))
                    db.commit()  # Commit the transaction

                    # Login successful, redirect to user screen
                    return redirect(url_for('userscreen'))
                else:
                    error = "Invalid User ID or Password. Please try again."
                    return render_template('login.html', error=error)

            else:
                error = "Invalid action. Please try again."
                return render_template('login.html', error=error)

        except Exception as e:
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()

    # Render the login/registration form for GET requests
    return render_template('login.html')

# Appointment Route
@app.route('/appointment', methods=['GET', 'POST'])
def appointment_patient():
    def generate_random_id(length=8):
        """Generate a random alphanumeric ID of specified length."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    if request.method == 'POST':
        # Retrieve form data
        patient_id = request.form.get('patient_id')
        patient_name = request.form.get('patient_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        appoid = request.form.get('appo_id')
        appodate = request.form.get('appdate')
        appoday = request.form.get('appday')
        appotym = request.form.get('apptym')
        rsnappo = request.form.get('rsnappo')
        constyp = request.form.get('conslt')

        # Validate the fields
        if not all([patient_id, patient_name, age, gender, appoid, appodate, appoday, appotym, rsnappo, constyp]):
            error = "All fields are required for registration!"
            return render_template('appointment.html', error=error)

        # Insert the patient data into the database
        cursor = db.cursor()
        try:
            # Check if Patient_ID and Appointment_ID are unique
            cursor.execute("SELECT * FROM appointment WHERE Patient_ID = %s OR Appointment_ID = %s", (patient_id, appoid))
            if cursor.fetchone():
                error = "Patient ID or Appointment ID already exists!"
                return render_template('appointment.html', error=error)

            # Insert into database
            cursor.execute("""
                INSERT INTO appointment (Patient_ID, Patient_Name, Age, Gender, Appointment_ID, Appointment_Date, Appointment_Day, 
                           Appointment_Time, Reason_of_Appointment, Consultation_Type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (patient_id, patient_name, age, gender, appoid, appodate, appoday, appotym, rsnappo, constyp))
            db.commit()
            return render_template('appointment.html', success=True)

        except Exception as e:
            error = f"Failed to patient appointment. Error: {str(e)}"
            print(error)  # Log the error
            return error

        finally:
            cursor.close()

    # For GET request, pre-generate random IDs
    patient_id = generate_random_id()
    appoid = generate_random_id()
    return render_template('appointment.html', patient_id=patient_id, appoid=appoid)

# ward bed Route
@app.route('/wardbed', methods=['GET', 'POST'])
def ward_bed():
    if request.method == 'POST':
        # Retrieve form data
        ward_name = request.form.get('ward_name')
        ward_type = request.form.get('ward_type')
        floor_no = request.form.get('floor_no')
        bed_id = request.form.get('bed_id')
        bed_type = request.form.get('bed_type')
        patient_id = request.form.get('patient_id')
        booking_date = request.form.get('booking_date')
        discharge_date = request.form.get('dscdate')
        reservation_status = request.form.get('resvsts')

        # Validate the fields
        if not all([ward_name, ward_type, floor_no, bed_id, bed_type, patient_id, booking_date, discharge_date, reservation_status]):
            error = "All fields are required for registration!"
            return render_template('wardbed.html', error=error)

        # Check if Bed ID or Patient ID already exists in the database
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM ward_bed WHERE Bed_ID = %s OR Patient_ID = %s", (bed_id, patient_id))
            if cursor.fetchone():
                error = "Duplicate Bed ID or Patient ID detected! Please refresh the page and try again."
                return render_template('wardbed.html', error=error)

            # Insert the data into the database
            cursor.execute("""
                INSERT INTO ward_bed (Ward_Name, Ward_Type, Floor_No, Bed_ID, Bed_Type, Patient_ID, Booking_Date, Discharge_Date, Reserve_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ward_name, ward_type, floor_no, bed_id, bed_type, patient_id, booking_date, discharge_date, reservation_status))
            db.commit()
            return render_template('wardbed.html', success=True)

        except Exception as e:
            db.rollback()
            error = f"Failed to book a ward. Error: {str(e)}"
            print(error)
            return render_template('wardbed.html', error=error)

        finally:
            cursor.close()

    # Generate random unique IDs for Bed ID and Patient ID
    def generate_random_id(prefix, length=8):
        characters = string.ascii_uppercase + string.digits
        random_id = ''.join(random.choices(characters, k=length))
        return f"{prefix}-{random_id}"

    # Ensure the IDs are unique
    cursor = db.cursor()
    while True:
        bed_id = generate_random_id("BED")
        patient_id = generate_random_id("PAT")
        cursor.execute("SELECT * FROM ward_bed WHERE Bed_ID = %s OR Patient_ID = %s", (bed_id, patient_id))
        if not cursor.fetchone():
            break

    cursor.close()

    # Render the form for GET request with prefilled IDs
    return render_template('wardbed.html', bed_id=bed_id, patient_id=patient_id)

# pharmacy Route
def generate_random_id(length=8):
    """Generate a random alphanumeric string of the given length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_random_batch_no(length=6):
    """Generate a random alphanumeric string of the given length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/pharmacy', methods=['GET', 'POST'])
def pharmacy():
    if request.method == 'POST':
        # Retrieve form data
        medicine_id = request.form.get('medicine_id')
        medicine_name = request.form.get('medicine_name')
        brand = request.form.get('brand_name')
        dosage = request.form.get('dosage_form')
        strength = request.form.get('strength')
        quantity = request.form.get('Quantity_in_Stock')
        expiry_date = request.form.get('expiry_date')
        batch_no = request.form.get('batch_no')
        price = request.form.get('Price_per_Unit')

        # Validate the fields
        if not all([medicine_id, medicine_name, brand, dosage, strength, quantity, expiry_date, batch_no, price]):
            error = "All fields are required for Pharmacy!"
            return render_template('pharmacy.html', error=error)

        # Check uniqueness of IDs
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM pharmacy WHERE Medicine_ID = %s OR Batch_No = %s", (medicine_id, batch_no))
            if cursor.fetchone()[0] > 0:
                error = "Medicine ID or Batch No already exists in the database!"
                return render_template('pharmacy.html', error=error)

            # Insert the data into the database
            cursor.execute("""
                INSERT INTO pharmacy (Medicine_ID, Medicine_Name, Brand_Name, Dosage_Form, Strength, Quantity_In_Stock, Expiry_Date, Batch_No, Price_Per_Unit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (medicine_id, medicine_name, brand, dosage, strength, quantity, expiry_date, batch_no, price))
            db.commit()
            return render_template('pharmacy.html', success=True)

        except Exception as e:
            db.rollback()
            error = f"Failed to insert data. Error: {str(e)}"
            return render_template('pharmacy.html', error=error)

        finally:
            cursor.close()

    # For GET request, pre-generate IDs
    random_medicine_id = generate_random_id()
    random_batch_no = generate_random_batch_no()
    return render_template('pharmacy.html', random_medicine_id=random_medicine_id, random_batch_no=random_batch_no)

# billing Route
def generate_random_patient_id():
    """Generate a random alphanumeric patient ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_random_transaction_id():
    """Generate a random numeric transaction ID."""
    return ''.join(random.choices(string.digits, k=10))

def is_patient_id_unique(patient_id):
    """Check if the patient ID is unique in the database."""
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM billing WHERE Patient_ID = %s", (patient_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count == 0

def is_transaction_id_unique(transaction_id):
    """Check if the transaction ID is unique in the database."""
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM billing WHERE Transaction_ID = %s", (transaction_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count == 0

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        # Retrieve form data
        patient_id = request.form.get('patient_id')
        bill_date = request.form.get('bill_date')
        total_amount = request.form.get('total_amount')
        discount = request.form.get('discount')
        finl_amount = request.form.get('finl_amount')
        payment_mtd = request.form.get('payment_mtd')
        trns_id = request.form.get('trns_id')
        paymt_sts = request.form.get('paymt_sts')
        paymt_date = request.form.get('paymt_date')

        # Validate the fields
        if not all([patient_id, bill_date, total_amount, discount, finl_amount, payment_mtd, trns_id, paymt_sts, paymt_date]):
            error = "All fields are required for billing!"
            return error

        # Ensure unique Patient ID and Transaction ID
        if not is_patient_id_unique(patient_id):
            return "Patient ID already exists in the database!"
        if not is_transaction_id_unique(trns_id):
            return "Transaction ID already exists in the database!"

        # Insert the patient data into the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO billing (Patient_ID, Bill_Date, Total_Amount, Discount, Final_Amount, Payment_Method, Transaction_ID, Payment_Status, Payment_Date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (patient_id, bill_date, total_amount, discount, finl_amount, payment_mtd, trns_id, paymt_sts, paymt_date))
            db.commit()
            return render_template('billing.html', success=True)

        except Exception as e:
            db.rollback()
            error = f"Failed to Billing. Error: {str(e)}"
            print(error)  # Log the error for debugging
            return error

        finally:
            cursor.close()

    # Generate random IDs for the GET request
    while True:
        random_patient_id = generate_random_patient_id()
        random_transaction_id = generate_random_transaction_id()
        if is_patient_id_unique(random_patient_id) and is_transaction_id_unique(random_transaction_id):
            break

    return render_template('billing.html', random_patient_id=random_patient_id, random_transaction_id=random_transaction_id)

# online appo Route
def generate_random_doctor_id():
    """Generate a random alphanumeric Doctor ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_random_patient_id():
    """Generate a random alphanumeric patient ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_random_appointment_id():
    """Generate a random alphanumeric appointment ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def is_doctor_id_unique(doctor_id):
    """Check if the Doctor ID is unique in the database."""
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM onlineappointment WHERE Doctor_ID = %s", (doctor_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count == 0

def is_patient_id_unique(patient_id):
    """Check if the Patient ID is unique in the database."""
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM onlineappointment WHERE Patient_ID = %s", (patient_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count == 0

def is_appointment_id_unique(appo_id):
    """Check if the Appointment ID is unique in the database."""
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM onlineappointment WHERE Appointment_ID = %s", (appo_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count == 0

@app.route('/onlineappointment', methods=['GET', 'POST'])
def onlineappointment():
    if request.method == 'POST':
        # Retrieve form data
        patient_id = request.form.get('patient_id')
        patient_name = request.form.get('patient_name')
        appo_id = request.form.get('appo_id')
        appo_date = request.form.get('appo_date')
        doctor_id = request.form.get('doctor_id')
        doctor_name = request.form.get('doctor_name')
        doctor_spe = request.form.get('doctor_spe')
        rsndis = request.form.get('rsndis')

        # Validate the fields
        if not all([patient_id ,patient_name, appo_id, appo_date, doctor_id, doctor_name, doctor_spe, rsndis]):
            return "All fields are required for Appointment!"

        # Ensure Doctor ID is unique
        if not is_doctor_id_unique(doctor_id):
            return "The generated Doctor ID already exists in the database. Please refresh the page to try again."
        if not is_patient_id_unique(patient_id):
            return "Patient ID already exists in the database!"
        if not is_appointment_id_unique(appo_id):
            return "Appointment ID already exists in the database!"
        
        # Insert the patient data into the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO onlineappointment (Patient_ID ,Patient_Name, Appointment_ID, Appointment_Date, Doctor_ID, Doctor_Name, Doctor_Specialization, Reason_of_Dieases)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (patient_id ,patient_name, appo_id, appo_date, doctor_id, doctor_name, doctor_spe, rsndis))
            db.commit()
            return render_template('onlineappointment.html', success=True)

        except Exception as e:
            db.rollback()
            return f"Failed to save appointment. Error: {str(e)}"

        finally:
            cursor.close()

    # Handle GET request
    random_doctor_id = None
    random_patient_id = None
    random_appo_id = None
    while True:
        random_patient_id = generate_random_patient_id()
        random_doctor_id = generate_random_doctor_id()
        random_appo_id = generate_random_appointment_id()
        if is_doctor_id_unique(random_doctor_id):
            break

    return render_template('onlineappointment.html', random_appo_id=random_appo_id ,random_patient_id=random_patient_id, random_doctor_id=random_doctor_id)

# fetch billing and payment data
@app.route('/billingpayment', methods=['GET', 'POST'])
def billing_payment():
    if request.method == 'POST':
        # Get the patient ID from the form
        bill_date = request.form.get('bill_date')

        # Validate the input
        if not bill_date:
            return render_template('billingpayment.html', error="Bill Date is required!")

        # Fetch the billing data from the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                SELECT Patient_ID, Bill_Date, Total_Amount, Discount, Final_Amount, 
                    Payment_Method, Transaction_ID, Payment_Status, Payment_Date 
                FROM billing WHERE Bill_Date = %s
            """, (bill_date,))

            billing_data = cursor.fetchall()

            if billing_data:
                billing_list = []
                for data in billing_data:
                    print("Row Data:", data)  # Debugging Output
                    billing_dict = {
                        'Patient_ID': data[0],  
                        'Bill_Date': data[1],
                        'Total_Amount': data[2],
                        'Discount': data[3],
                        'Final_Amount': data[4],
                        'Payment_Method': data[5],
                        'Transaction_ID': data[6],
                        'Payment_Status': data[7],
                        'Payment_Date': data[8]
                    }
                    billing_list.append(billing_dict)

                return render_template('billingpayment.html', billing_list=billing_list)


            else:
                return render_template('billingpayment.html', error="No billing record found for this Patient ID.")

        except Exception as e:
            error = f"Failed to fetch billing data. Error: {str(e)}"
            print(error)  # Log the error for debugging
            return render_template('billingpayment.html', error=error)

        finally:
            cursor.close()

    # Render the form for GET request
    return render_template('billingpayment.html')

# fetch appointment data
@app.route('/appointment_date', methods=['GET', 'POST'])
def appointment_date():
    if request.method == 'POST':
        # Get the appointment date from the form
        appointment_date = request.form.get('appointment_date')

        # Validate the input
        if not appointment_date:
            return render_template('appointment_date.html', error="Appointment Date is required!")

        # Fetch the appointment data from the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                SELECT Patient_Name, Age, Gender, Appointment_Date, Appointment_Day, Appointment_Time, Reason_of_Appointment, Consultation_Type
                FROM appointment WHERE Appointment_Date = %s
            """, (appointment_date,))
            appointment_data = cursor.fetchall()

            if appointment_data:
                # Convert the fetched data into a list of dictionaries for easier handling in the template
                appointments = []
                for record in appointment_data:
                    appointments.append({
                        'Patient_Name': record[0],
                        'Age': record[1],
                        'Gender': record[2],
                        'Appointment_Date': record[3],
                        'Appointment_Day': record[4],
                        'Appointment_Time': record[5],
                        'Reason_of_Appointment': record[6],
                        'Consultation_Type': record[7],
                    })

                return render_template('appointment_date.html', appointments=appointments)

            else:
                return render_template('appointment_date.html', error="No appointment record found for this date.")

        except Exception as e:
            error = f"Failed to fetch appointment data. Error: {str(e)}"
            print(error)  # Log the error for debugging
            return render_template('appointment_date.html', error=error)

        finally:
            cursor.close()

    # Render the form for GET request
    return render_template('appointment_date.html')

# fetch online appo data
@app.route('/onlineappo_data', methods=['GET', 'POST'])
def onlineappo_data():
    if request.method == 'POST':
        # Get the appointment date from the form
        appointment_date = request.form.get('appo_date')

        # Validate the input
        if not appointment_date:
            return render_template('onlineappo_data.html', error="Appointment Date is required!")

        # Fetch the appointment data from the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                SELECT Patient_ID, Patient_Name, Appointment_ID, Appointment_Date, Doctor_ID, Doctor_Name, Doctor_Specialization, Reason_of_Dieases
                FROM onlineappointment WHERE Appointment_Date = %s
            """, (appointment_date,))
            onlineappointment_data = cursor.fetchall()

            if onlineappointment_data:
                # Convert the fetched data into a list of dictionaries
                onlineappointments = []
                for record in onlineappointment_data:
                    onlineappointments.append({
                        'Patient_ID': record[0],
                        'Patient_Name': record[1],
                        'Appointment_ID': record[2],
                        'Appointment_Date': record[3],
                        'Doctor_ID': record[4],
                        'Doctor_Name': record[5],
                        'Doctor_Specialization': record[6], 
                        'Reason_of_Dieases': record[7],
                    })

                return render_template('onlineappo_data.html', onlineappointments=onlineappointments)

            else:
                return render_template('onlineappo_data.html', error="No Online Appointment record found for this date.")

        except Exception as e:
            error = f"Failed to Fetch Online Appointment Data. Error: {str(e)}"
            print(error)  # Log the error for debugging
            return render_template('onlineappo_data.html', error=error)

        finally:
            cursor.close()

    # Render the form for GET request
    return render_template('onlineappo_data.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
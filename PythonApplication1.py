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

# Sample users
patients = [Patient('123', '123')]
# admins = [
#     {'userid': 'admin@gmail.com', 'password': '1234'}
# ]

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
    
    # Render the login/registration form for GET requests
    return render_template('register.html')

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
                if userid == 'admin@gmail.com' and password == '1234':
                    return redirect(url_for('dashboard'))  # Redirect to admin portal

                # For non-admin users, check if the user exists in the database
                cursor.execute("""SELECT * FROM login_user1 WHERE Patient_ID = %s AND Password = %s""", (userid, password))
                user = cursor.fetchone()

                if user:
                    # Login successful, save user info in session
                    # session['userid'] = user[0]  # Assuming first column is the user's ID
                    # session['password'] = user[1]  # Assuming second column is the password
                    return redirect(url_for('userscreen'))  # Redirect to user screen
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

# Register Patient Route
@app.route('/registerpatient', methods=['GET', 'POST'])
def register_patient():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        contact = request.form.get('contact')

        # Validate the fields
        if not all([first_name, last_name, age, gender, contact]):
            error = "All fields are required for registration!"
            return render_template('registerpatient.html', error=error)

        # Insert the patient data into the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO register_patient (First_Name, Last_Name, Age, Gender, Contact)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, age, gender, contact))
            db.commit()
            success_message = "Patient registered successfully!"
            return success_message

        except Exception as e:
            error = f"Failed to register patient. Error: {str(e)}"
            print(error)  # Log the error
            return error

        finally:
            cursor.close()

    # Render the form for GET request
    return render_template('registerpatient.html')

# Appointment Patient Route
@app.route('/appointment', methods=['GET', 'POST'])
def appointment_patient():
    if request.method == 'POST':
        # Retrieve form data
        patient_name = request.form.get('patient_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        appodate = request.form.get('appdate')
        appoday = request.form.get('appday')
        appotym = request.form.get('apptym')
        rsnappo = request.form.get('rsnappo')
        constyp = request.form.get('conslt')

        # Validate the fields
        if not all([patient_name, age, gender, appodate, appoday, appotym, rsnappo, constyp]):
            error = "All fields are required for registration!"
            return render_template('appointment.html', error=error)

        # Insert the patient data into the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO appointment (Patient_Name, Age, Gender, Appointment_Date, Appointment_Day, Appointment_Time, Reason_of_Appointment, Consultation_Type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (patient_name, age, gender, appodate, appoday, appotym, rsnappo, constyp))
            db.commit()
            success_message = "Patient appointment successfully!"
            return success_message

        except Exception as e:
            error = f"Failed to patient appointment. Error: {str(e)}"
            print(error)  # Log the error
            return error

        finally:
            cursor.close()

        # Render the form for GET request
    return render_template('appointment.html')

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
            return error

        # Insert the patient data into the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO ward_bed (Ward_Name, Ward_Type, Floor_No, Bed_ID, Bed_Type, Patient_ID, Booking_Date, Discharge_Date, Reserve_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ward_name, ward_type, floor_no, bed_id, bed_type, patient_id, booking_date, discharge_date, reservation_status))
            db.commit()
            success_message = "Ward Booked Successfully!"
            return success_message

        except Exception as e:
            db.rollback()
            error = f"Failed to book a ward. Error: {str(e)}"
            print(error)  # Log the error for debugging
            return error

        finally:
            cursor.close()

    # Render the form for GET request
    return render_template('wardbed.html')

# pharmacy Route
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
        Price = request.form.get('Price_per_Unit')

        # Validate the fields
        if not all([medicine_id, medicine_name, brand, dosage, strength, quantity, expiry_date, batch_no, Price]):
            error = "All fields are required for Pharamacy!"
            return error

        # Insert the patient data into the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO pharamacy (Medicine_ID, Medicine_Name, Brand_Name, Dosage_Form, Strength, Quantity_In_Stock, Expiry_Date, Batch_No, Price_Per_Unit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (medicine_id, medicine_name, brand, dosage, strength, quantity, expiry_date, batch_no, Price))
            db.commit()
            success_message = "Insert Successfully!"
            return success_message

        except Exception as e:
            db.rollback()
            error = f"Failed to Insert. Error: {str(e)}"
            print(error)  # Log the error for debugging
            return error

        finally:
            cursor.close()

        # Render the form for GET request
    return render_template('pharmacy.html')

# billing Route
@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        # Retrieve form data
        patient_id = request.form.get('patient_id')
        # invoice_id = request.form.get('invoice_id')
        bill_date = request.form.get('bill_date')
        total_amount = request.form.get('total_amount')
        discount = request.form.get('discount')
        tax_amount = request.form.get('tax_amount')
        finl_amount = request.form.get('finl_amount')
        payment_mtd= request.form.get('payment_mtd')
        trns_id = request.form.get('trns_id')
        paymt_sts = request.form.get('paymt_sts')
        paymt_date = request.form.get('paymt_date')

        # Validate the fields
        if not all([patient_id, bill_date, total_amount, discount, tax_amount, finl_amount, payment_mtd, trns_id, paymt_sts, paymt_date]):
            error = "All fields are required for billing!"
            return error

        # Insert the patient data into the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO billing (Patient_ID, Bill_Date, Total_Amount, Discount, Tax_Amount, Final_Amount, Payment_Method, Transaction_ID, Payment_Status, Payment_Date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (patient_id, bill_date, total_amount, discount, tax_amount, finl_amount, payment_mtd, trns_id, paymt_sts, paymt_date))
            db.commit()
            success_message = "Billing Successfully!"
            return success_message

        except Exception as e:
            db.rollback()
            error = f"Failed to Billing. Error: {str(e)}"
            print(error)  # Log the error for debugging
            return error

        finally:
            cursor.close()

    return render_template('billing.html')

# online appo Route
@app.route('/onlineappointment', methods=['GET', 'POST'])
def onlineappointment():
    if request.method == 'POST':
        # Retrieve form data
        patient_id = request.form.get('patient_id')
        patient_name = request.form.get('patient_name')
        doctor_id = request.form.get('doctor_id')
        doctor_name = request.form.get('doctor_name')
        doctor_spe = request.form.get('doctor_spe')
        rsndis = request.form.get('rsndis')

        # Validate the fields
        if not all([patient_id, patient_name, doctor_id, doctor_name, doctor_spe, rsndis]):
            error = "All fields are required for Appointment!"
            return error

        # Insert the patient data into the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO onlineappointment (Patient_ID, Patient_Name, Doctor_ID, Doctor_Name, Doctor_Specialization, Reason_of_Dieases)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (patient_id, patient_name, doctor_id, doctor_name, doctor_spe, rsndis))
            db.commit()
            success_message = "Online Appointment Successfully!"
            return success_message

        except Exception as e:
            db.rollback()
            error = f"Failed to Online Appointment. Error: {str(e)}"
            print(error)  # Log the error for debugging
            return error

        finally:
            cursor.close()
        # Render the form for GET request
    return render_template('onlineappointment.html')

# billing and payment Route
@app.route('/billingpayment', methods=['GET', 'POST'])
def billing_payment():
    if request.method == 'POST':
        # Get the patient ID from the form
        patient_id = request.form.get('patient_id')

        # Validate the input
        if not patient_id:
            return render_template('billingpayment.html', error="Patient ID is required!")

        # Fetch the billing data from the database
        cursor = db.cursor()
        try:
            cursor.execute("""
                SELECT * FROM billing WHERE Patient_ID = %s
            """, (patient_id,))
            billing_data = cursor.fetchone()

            if billing_data:
                # Assuming the columns in the "billing" table are:
                # [Patient_ID, Bill_Date, Total_Amount, Discount, Tax_Amount, Final_Amount, Payment_Method, Transaction_ID, Payment_Status, Payment_Date]
                billing_dict = {
                    'Patient_ID': billing_data[0],
                    'Bill_Date': billing_data[1],
                    'Total_Amount': billing_data[2],
                    'Discount': billing_data[3],
                    'Tax_Amount': billing_data[4],
                    'Final_Amount': billing_data[5],
                    'Payment_Method': billing_data[6],
                    'Transaction_ID': billing_data[7],
                    'Payment_Status': billing_data[8],
                    'Payment_Date': billing_data[9]
                }
                return render_template('billingpayment.html', billing=billing_dict)

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
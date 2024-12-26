from flask import Flask, flash, render_template, request, redirect, url_for

app = Flask(__name__)

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
admins = [
    {'userid': 'admin@gmail.com', 'password': '1234'}
]

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

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        
        # Check both admins and patients lists for valid credentials
        for user in admins:
            if user['userid'] == userid and user['password'] == password:
                return redirect(url_for('dashboard'))  # Redirect to dashboard
            else:
                # flash('invalid')
                return redirect(url_for('userscreen'))
        return "Invalid userid or password!"
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Registration Form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        patient_name = request.form['patient_name']
        id = request.form['idcardnumber']
        gender = request.form['gender']
        
        if not all([patient_id, patient_name, id, gender]):
            return "All fields are required!"
        # Here, you can save data to the database
        return f"Registered: {patient_name}"
    
    return render_template('register.html')  # Render the signup form

# Register Patient Route
@app.route('/registerpatient', methods=['GET', 'POST'])
def register_patient():
    if request.method == 'POST':
        # Get data from the form
        patient_id = request.form.get('patient_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        contact = request.form.get('contact')
        gender = request.form.get('gender')
        # Validate the fields
        if not all([patient_id, first_name, last_name, age, gender, contact]):
            return "All fields are required!"
        
        # If everything is fine, save the data or process it
        return f"Patient Registered: {first_name} {last_name}"

    # Render the form for GET request
    return render_template('registerpatient.html')

# Appointment Patient Route
@app.route('/appointment', methods=['GET', 'POST'])
def appointment_patient():
    if request.method == 'POST':
        # Get data from the form
        patient_id = request.form.get('patient_id')
        patient_name = request.form.get('patient_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        appodate = request.form.get('appdate')
        appoday = request.form.get('appday')
        appotym = request.form.get('apptym')
        rsnappo = request.form.get('rsnappo')
        constyp = request.form.get('conslt')
        # Validate the fields
        if not all([patient_id, patient_name, age, gender, appodate, appoday, appotym, rsnappo, constyp]):
            return "All fields are required!"
        
        # If everything is fine, save the data or process it
        return f"Patient Appointment: {patient_id} {patient_name}"

    # Render the form for GET request
    return render_template('appointment.html')

# ward bed Route
@app.route('/wardbed', methods=['GET', 'POST'])
def ward_bed():
    if request.method == 'POST':
        # Get data from the form
        ward_id = request.form.get('ward_id')
        ward_name = request.form.get('ward_name')
        ward_typ = request.form.get('ward_typ')
        floor_no = request.form.get('floor_no')
        bed_id = request.form.get('bed_id')
        bed_typ = request.form.get('bed_typ')
        patient_id = request.form.get('patient_id')
        bkdate = request.form.get('bkdate')
        dscdate = request.form.get('dscdate')
        resvsts = request.form.get('resvsts')
        # Validate the fields
        if not all([ward_id, ward_name, ward_typ, floor_no, bed_id, bed_typ, patient_id, bkdate, dscdate, resvsts]):
            return "All fields are required!"
        
        # If everything is fine, save the data or process it
        return f"ward Registered: {ward_id} {ward_name}"

    # Render the form for GET request
    return render_template('wardbed.html')

# pharmacy Route
@app.route('/pharmacy', methods=['GET', 'POST'])
def pharmacy():
    if request.method == 'POST':
        # Get data from the form
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
            return "All fields are required!"
        
        # If everything is fine, save the data or process it
        return f"Pharmacy Registered: {medicine_id} {medicine_name}"

    # Render the form for GET request
    return render_template('pharmacy.html')

# billing Route
@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        # Get data from the form
        patient_id = request.form.get('patient_id')
        invoice_id = request.form.get('invoice_id')
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
        if not all([patient_id, invoice_id, bill_date, total_amount, discount, tax_amount, finl_amount, payment_mtd, trns_id, paymt_sts, paymt_date]):
            return "All fields are required!"
        
        # If everything is fine, save the data or process it
        return f"Billing Registered: {patient_id} {invoice_id}"

    # Render the form for GET request
    return render_template('billing.html')

# online appo Route
@app.route('/onlineappointment', methods=['GET', 'POST'])
def onlineappointment():
    if request.method == 'POST':
        # Get data from the form
        patient_id = request.form.get('patient_id')
        patient_name = request.form.get('patient_name')
        doctor_id = request.form.get('doctor_id')
        doctor_name = request.form.get('doctor_name')
        doctor_spe = request.form.get('doctor_spe')
        rsndis = request.form.get('rsndis')
        # Validate the fields
        if not all([patient_id, patient_name, doctor_id, doctor_name, doctor_spe, rsndis]):
            return "All fields are required!"
        
        # If everything is fine, save the data or process it
        return f"Online Appointment: {patient_id} {patient_name} {doctor_id} {doctor_name}"

    # Render the form for GET request
    return render_template('onlineappointment.html')

# medical rec Route
@app.route('/medicalrec', methods=['GET', 'POST'])
def medical_rec():
    if request.method == 'POST':
        # Get data from the form
        patient_id = request.form.get('patient_id')
        # Validate the fields
        if not all([patient_id]):
            return "All fields are required!"
        
        # If everything is fine, save the data or process it
        return f"Medical Record: {patient_id}"

    # Render the form for GET request
    return render_template('medicalrec.html')

# billing and payment Route
@app.route('/billingpayment', methods=['GET', 'POST'])
def billing_payment():
    if request.method == 'POST':
        # Get data from the form
        patient_id = request.form.get('patient_id')
        # Validate the fields
        if not all([patient_id]):
            return "All fields are required!"
        
        # If everything is fine, save the data or process it
        return f"Payments: {patient_id}"

    # Render the form for GET request
    return render_template('billingpayment.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
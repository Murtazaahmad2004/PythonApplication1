from msilib.schema import File
from tkinter import *
from tkinter import ttk

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Patient(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.patient_data = {}
        
class Doctor(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        
def login(users):
    while True:
        username = input("Enter The Username: ")
        password = input("Enter The Password: ")

        for u in users:
            if username == u.username and password == u.password:
                print("User Has Been Logged in!")
                return u
        else:
            print("Username or Password is incorrect. Please try again!")
            
#def on_validate(P):
 #   return P.isdigit()

def on_validate(P, data_type):
    if P == "":
        return True  # Allow empty entry
    
    if data_type == "text":
      return P.isalpha()
    elif data_type == "numeric":
      return P.isdigit()
    else:
      return False

def open_registration_window(user):
    registration_window = Toplevel(root)
    registration_window.title("Registration.")

    # Add widgets and layout for the registration window
    label_patient_name = Label(registration_window, text="Patient Name:")
    label_patient_name.grid(row=0, column=0, padx=10, pady=10)
    entry_patient_name = Entry(registration_window, validate="key", validatecommand=(registration_window.register(lambda P: on_validate(P, "text")), '%P'))
    entry_patient_name.grid(row=0, column=1, padx=10, pady=10)

    label_father_name = Label(registration_window, text="Father's Name:")
    label_father_name.grid(row=1, column=0, padx=10, pady=10)
    entry_father_name = Entry(registration_window, validate="key", validatecommand=(registration_window.register(lambda P: on_validate(P, "text")), '%P'))
    entry_father_name.grid(row=1, column=1, padx=10, pady=10)
    
    label_age = Label(registration_window, text="Age:")
    label_age.grid(row=2, column=0, padx=10, pady=10)
    entry_age = Entry(registration_window, validate="key", validatecommand=(registration_window.register(lambda P: on_validate(P, "numeric")), '%P'))
    entry_age.grid(row=2, column=1, padx=10, pady=10)
    
    label_gender = Label(registration_window, text="Gender:")
    label_gender.grid(row=3, column=0, padx=10, pady=10)
    entry_gender = Entry(registration_window, validate="key", validatecommand=(registration_window.register(lambda P: on_validate(P, "text")), '%P'))
    entry_gender.grid(row=3, column=1, padx=10, pady=10)

    label_contact = Label(registration_window, text="Contact:")
    label_contact.grid(row=4, column=0, padx=10, pady=10)
    entry_contact = Entry(registration_window, validate="key", validatecommand=(registration_window.register(lambda P: on_validate(P,"numeric")), '%P'))
    entry_contact.grid(row=4, column=1, padx=10, pady=10)
                   
    def submit_registration():
        # Access the entered data
        patient_name = entry_patient_name.get()
        father_name = entry_father_name.get()
        age = entry_age.get()
        gender = entry_gender.get()
        contact = entry_contact.get()
        
        if any(field == "" for field in [patient_name , father_name, age, gender, contact]):
            print("Error: Please Fill In All Fields.")
        else:
        # You can do something with the collected data, such as saving it to a database
         print("Patient Name:", patient_name)
         print("Father's Name:", father_name)
         print("Age:", age)
         print("Gender:", gender)
         print("Contact:", contact)

        # Close the registration window if needed
        registration_window.destroy()

    # Add a submit button
    submit_button = Button(registration_window, text="Submit", command=submit_registration)
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

def open_appointment_window(user):
    appointment_window = Toplevel(root)
    appointment_window.title("Appointment Scheduling.")

    # Add widgets and layout for the registration window
    
    label_patient_name = Label(appointment_window, text="Patient Name:")
    label_patient_name.grid(row=0, column=0, padx=10, pady=10)
    entry_patient_name = Entry(appointment_window, validate="key", validatecommand=(appointment_window.register(lambda P: on_validate(P, "text")), '%P'))
    entry_patient_name.grid(row=0, column=1, padx=10, pady=10)
    
    label_doctor_name = Label(appointment_window, text="Doctor Name:")
    label_doctor_name.grid(row=1, column=0, padx=10, pady=10)
    entry_doctor_name = Entry(appointment_window, validate="key", validatecommand=(appointment_window.register(lambda P: on_validate(P, "text")), '%P'))
    entry_doctor_name.grid(row=1, column=1, padx=10, pady=10)

    label_doctor_id = Label(appointment_window, text="Doctor Id:")
    label_doctor_id.grid(row=2, column=0, padx=10, pady=10)
    entry_doctor_id = Entry(appointment_window, validate="key", validatecommand=(appointment_window.register(lambda P: on_validate(P, "numeric")), '%P'))
    entry_doctor_id.grid(row=2, column=1, padx=10, pady=10)

    label_date = Label(appointment_window, text="Date:")
    label_date.grid(row=3, column=0, padx=10, pady=10)
    entry_date = Entry(appointment_window, validate="key", validatecommand=(appointment_window.register(lambda P: on_validate(P, "numeric")), '%P'))
    entry_date.grid(row=3, column=1, padx=10, pady=10)

    label_gender = Label(appointment_window, text="Gender:")
    label_gender.grid(row=5, column=0, padx=10, pady=10)
    entry_gender = Entry(appointment_window, validate="key", validatecommand=(appointment_window.register(lambda P: on_validate(P, "text")), '%P'))
    entry_gender.grid(row=5, column=1, padx=10, pady=10)

    def submit_appointment():
        # Access the entered data
        doctor_name = entry_doctor_name.get()
        doctor_id = entry_doctor_id.get()
        patient_name = entry_patient_name.get()
        date = entry_date.get()
        gender = entry_gender.get()

        if any(field == "" for field in [doctor_name, doctor_id, patient_name, date, gender]):
            print("Error: Please Fill In All Fields.")
        else:
        # You can do something with the collected data, such as saving it to a database
         print("Doctor Name:", doctor_name)
         print("Doctor Id:", doctor_id)
         print("Patient Name:", patient_name)
         print("Date:", date)
         print("Gender:", gender)

        # Close the registration window if needed
        appointment_window.destroy()

    # Add a submit button
    submit_button = Button(appointment_window, text="Submit", command=submit_appointment)
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)

def open_medical_records_window(user):
    medical_records_window = Toplevel(root)
    medical_records_window.title("Medical Records")
    # Add widgets and layout for the medical records window as needed

    label_prescription = Label(medical_records_window, text="Prescription:")
    label_prescription.grid(row=0, column=0, padx=10, pady=10)
    
    label_patient_name = Label(medical_records_window, text="Patient Name:")
    label_patient_name.grid(row=1, column=0, padx=10, pady=10)
    entry_patient_name = Entry(medical_records_window, validate="key", validatecommand=(medical_records_window.register(lambda P: on_validate(P, "text")), '%P'))
    entry_patient_name.grid(row=1, column=1, padx=10, pady=10)

    label_date = Label(medical_records_window, text="Date")
    label_date.grid(row=2, column=0, padx=10, pady=10)
    entry_date = Entry(medical_records_window, validate="key", validatecommand=(medical_records_window.register(lambda P: on_validate(P, "numeric")), '%P'))
    entry_date.grid(row=2, column=1, padx=10, pady=10)

    label_med = Label(medical_records_window, text="Medications:")
    label_med.grid(row=3, column=0, padx=10, pady=10)
    entry_med = Entry(medical_records_window, validate="key", validatecommand=(medical_records_window.register(lambda P: on_validate(P, "text")), '%P'))
    entry_med.grid(row=3, column=1, padx=10, pady=10)

    label_dos = Label(medical_records_window, text="Dosage:")
    label_dos.grid(row=4, column=0, padx=10, pady=10)
    entry_dos = Entry(medical_records_window, validate="key", validatecommand=(medical_records_window.register(lambda P: on_validate(P, "numeric")), '%P'))
    entry_dos.grid(row=4, column=1, padx=10, pady=10)
   
    label_fre = Label(medical_records_window, text="Frequency:")
    label_fre.grid(row=5, column=0, padx=10, pady=10)
    entry_fre = Entry(medical_records_window, validate="key", validatecommand=(medical_records_window.register(lambda P: on_validate(P, "text")), '%P'))
    entry_fre.grid(row=5, column=1, padx=10, pady=10)
    
    label_d_day = Label(medical_records_window, text="Duration Days:")
    label_d_day.grid(row=6, column=0, padx=10, pady=10)
    entry_d_day = Entry(medical_records_window, validate="key", validatecommand=(medical_records_window.register(lambda P: on_validate(P, "numeric")), '%P'))
    entry_d_day.grid(row=6, column=1, padx=10, pady=10)
    
    def submit_medical_records():
        # Access the entered data
        patient_name = entry_patient_name.get()
        d_day = entry_d_day.get()
        date = entry_date.get()
        fre = entry_fre.get()
        dos = entry_dos.get()
        med = entry_med.get()
    
        if any(field == "" for field in [patient_name , d_day, fre, date, dos, med]):
            print("Error: Please Fill In All Fields.")
        else:
        # You can do something with the collected data, such as saving it to a database
         print("Patient Name:", patient_name)
         print("Dosage:", dos)
         print("Frequency:", fre)
         print("Medications:", med)
         print("Date:", date)
         print("Duration Day:",d_day)
        # Close the registration window if needed
        medical_records_window.destroy()

    # Add a submit button
    submit_button = Button(medical_records_window, text="Submit", command=submit_medical_records)
    submit_button.grid(row=7, column=0, columnspan=2, pady=10)

def exit_program():
    root.destroy()

# Sample data
patient_user = Patient('123', '123')
doctor_user = Doctor('doctor', 'pass')

# Add the users to the list
users = [patient_user, doctor_user]

# Perform login
user = login(users)

root = Tk()
root.geometry("1920x1080")
root.title("Hospital Management System.")

# Create a menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create a patient menu
patient_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Patient", menu=patient_menu)

# Add menu items to the patient menu
patient_menu.add_command(label="Registration", command=lambda: open_registration_window(user))
patient_menu.add_command(label="Appointment", command=lambda: open_appointment_window(user))
patient_menu.add_command(label="Medical Records", command=lambda: open_medical_records_window(user))
patient_menu.add_command(label="Exit", command=exit_program)

# Use the actual path to your image file
ss = PhotoImage(f='D:/Projects/HMS OOP/PythonApplication1/pin.png')  # Use forward slashes or double backslashes

label = ttk.Label(root, image=ss)
label.photo = ss  # To prevent garbage collection
label.pack()

root.mainloop()
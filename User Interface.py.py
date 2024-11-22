import customtkinter as ctk
from PIL import Image
from tkinter import messagebox, ttk
import re


# Initialize customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class CMUHealthCareSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("CMU Health Care System")
        self.root.geometry("400x500")

        # Data
        self.departments = ["Cardiology", "Dermatology", "Pediatrics", "Neurology"]
        self.doctors = {
            "Cardiology": ["Dr. Smith", "Dr. Johnson"],
            "Dermatology": ["Dr. Brown", "Dr. Davis"],
            "Pediatrics": ["Dr. Miller", "Dr. Wilson"],
            "Neurology": ["Dr. Moore", "Dr. Taylor"]
        }
        self.appointment_times = ["9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM"]
        self.patient_history = {"John Doe": "Flu treated on 01/10/2024", "Jane Smith": "Skin allergy on 01/15/2024"}

        # UI Components
        self.setup_main_ui()

    def setup_main_ui(self):
        """Main screen UI."""
        try:
            cmu_logo = ctk.CTkImage(light_image=Image.open("logo.png"), size=(300, 150))
            ctk.CTkLabel(self.root, image=cmu_logo, text="").pack(pady=10)
        except:
            pass

        ctk.CTkLabel(self.root, text="Welcome to CMU Health Care System", font=("Arial", 18)).pack(pady=10)

        # Regular Login
        self.add_input_field("Username", "user_entry")
        self.add_input_field("Password", "pass_entry", show="*")

        ctk.CTkButton(self.root, text="Login", command=self.open_appointment_screen, width=150).pack(pady=5)
        ctk.CTkButton(self.root, text="Signup", command=self.open_signup_screen, width=150).pack(pady=5)

        # Admin Login
        self.add_input_field("Admin Username", "admin_user_entry")
        self.add_input_field("Admin Password", "admin_pass_entry", show="*")
        ctk.CTkButton(self.root, text="Admin Login", command=self.open_admin_page, fg_color="red", width=150).pack(pady=10)

    def add_input_field(self, label, attr_name, show=None):
        """Helper to add input fields."""
        ctk.CTkLabel(self.root, text=label).pack()
        entry = ctk.CTkEntry(self.root, show=show)
        setattr(self, attr_name, entry)
        entry.pack(pady=5)

    def open_signup_screen(self):
        SignupScreen(self.root)

    def open_appointment_screen(self):
        AppointmentScreen(self.root, self.departments, self.doctors, self.appointment_times)

    def open_admin_page(self):
        username = self.admin_user_entry.get()
        password = self.admin_pass_entry.get()
        if username == "admin" and password == "admin123":
            AdminPage(self.root, self.departments, self.doctors, self.patient_history)
        else:
            self.show_message("Error", "Invalid admin credentials.", is_error=True)

    @staticmethod
    def show_message(title, message, is_error=False):
        """Show info or error messages."""
        if is_error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)


class SignupScreen:
    def __init__(self, parent):
        self.parent = parent
        self.parent.withdraw()
        self.signup_screen = ctk.CTkToplevel(parent)
        self.signup_screen.title("Signup")
        self.signup_screen.geometry("400x400")

        self.add_input_field("Full Name", "full_name_entry")
        self.add_input_field("Email", "email_entry")
        self.add_input_field("Password", "password_entry", show="*")
        self.add_input_field("Phone", "phone_entry")

        ctk.CTkButton(self.signup_screen, text="Register", command=self.register_user).pack(pady=10)
        ctk.CTkButton(self.signup_screen, text="Back", command=self.back_to_main, fg_color="red").pack(pady=5)

    def add_input_field(self, label, attr_name, show=None):
        """Helper to add input fields."""
        ctk.CTkLabel(self.signup_screen, text=label).pack(pady=5)
        entry = ctk.CTkEntry(self.signup_screen, show=show)
        setattr(self, attr_name, entry)
        entry.pack(pady=5)

    def register_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        phone = self.phone_entry.get()
        error = self.validate_inputs(email, password, phone)
        if error:
            CMUHealthCareSystem.show_message("Error", error, is_error=True)
        else:
            CMUHealthCareSystem.show_message("Success", "Registration successful!")
            self.back_to_main()

    @staticmethod
    def validate_inputs(email, password, phone):
        """Validate email, password, and phone inputs."""
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return "Invalid Email: Enter a valid email address."
        if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password) or not any(char in "!@#$%^&*()" for char in password):
            return "Invalid Password: Must include uppercase, lowercase, number, and special character."
        if len(phone) != 10 or not phone.isdigit():
            return "Invalid Phone Number: Must be exactly 10 digits."
        return None

    def back_to_main(self):
        self.signup_screen.destroy()
        self.parent.deiconify()


class AppointmentScreen:
    def __init__(self, parent, departments, doctors, times):
        self.parent = parent
        self.parent.withdraw()
        self.appointment_screen = ctk.CTkToplevel(parent)
        self.appointment_screen.title("Doctor Appointment")
        self.appointment_screen.geometry("400x400")

        self.departments = departments
        self.doctors = doctors

        self.add_dropdown("Department", "department_var", self.departments, self.update_doctors)
        self.add_dropdown("Doctor", "doctor_var", [])
        self.add_dropdown("Time", "time_var", times)

        ctk.CTkButton(self.appointment_screen, text="Book Appointment", command=self.book_appointment).pack(pady=10)
        ctk.CTkButton(self.appointment_screen, text="Patient History", command=self.show_patient_history).pack(pady=10)
        ctk.CTkButton(self.appointment_screen, text="Logout", command=self.logout, fg_color="red").pack(pady=5)

    def add_dropdown(self, label, attr_name, values, command=None):
        """Helper to add dropdown fields."""
        ctk.CTkLabel(self.appointment_screen, text=f"Select {label}").pack(pady=5)
        var = ctk.StringVar()
        dropdown = ctk.CTkComboBox(self.appointment_screen, variable=var, values=values, command=command)
        setattr(self, attr_name, var)
        setattr(self, f"{attr_name}_dropdown", dropdown)
        dropdown.pack(pady=5)

    def update_doctors(self, *_):
        department = self.department_var.get()
        self.doctor_var_dropdown.configure(values=self.doctors.get(department, []))

    def book_appointment(self):
        department, doctor, time = self.department_var.get(), self.doctor_var.get(), self.time_var.get()
        if not (department and doctor and time):
            CMUHealthCareSystem.show_message("Error", "All fields must be selected.", is_error=True)
        else:
            CMUHealthCareSystem.show_message("Appointment Booked", f"Booked with {doctor} ({department}) at {time}")

    def show_patient_history(self):
        # Placeholder for patient history functionality
        CMUHealthCareSystem.show_message("Patient History", "Demo patient history functionality.")

    def logout(self):
        self.appointment_screen.destroy()
        self.parent.deiconify()


class AdminPage:
    def __init__(self, parent, departments, doctors, patient_history):
        self.parent = parent
        self.parent.withdraw()
        self.admin_page = ctk.CTkToplevel(parent)
        self.admin_page.title("Admin Panel")
        self.admin_page.geometry("500x500")

        self.departments = departments
        self.doctors = doctors
        self.patient_history = patient_history

        ctk.CTkLabel(self.admin_page, text="Admin Panel", font=("Arial", 20)).pack(pady=10)

        # Manage Doctor Details
        ctk.CTkLabel(self.admin_page, text="Update Doctor Details", font=("Arial", 16)).pack(pady=5)
        self.add_dropdown("Department", "update_department_var", self.departments, self.update_doctor_dropdown)
        self.add_dropdown("Doctor", "update_doctor_var", [])
        self.add_dropdown("Availability", "availability_var", ["Available", "Unavailable"])
        ctk.CTkButton(self.admin_page, text="Update Doctor", command=self.update_doctor).pack(pady=10)

        # Manage Patient History
        ctk.CTkLabel(self.admin_page, text="Manage Patient History", font=("Arial", 16)).pack(pady=10)
        self.patient_history_text = ctk.CTkTextbox(self.admin_page, width=400, height=150)
        self.patient_history_text.pack(pady=5)
        self.load_patient_history()
        ctk.CTkButton(self.admin_page, text="Update History", command=self.update_patient_history).pack(pady=5)

        ctk.CTkButton(self.admin_page, text="Logout", command=self.logout, fg_color="red").pack(pady=10)

    def add_dropdown(self, label, attr_name, values, command=None):
        """Helper to add dropdown fields."""
        ctk.CTkLabel(self.admin_page, text=f"Select {label}").pack(pady=5)
        var = ctk.StringVar()
        dropdown = ctk.CTkComboBox(self.admin_page, variable=var, values=values, command=command)
        setattr(self, attr_name, var)
        setattr(self, f"{attr_name}_dropdown", dropdown)
        dropdown.pack(pady=5)

    def update_doctor_dropdown(self, *_):
        department = self.update_department_var.get()
        self.update_doctor_var_dropdown.configure(values=self.doctors.get(department, []))

    def update_doctor(self):
        department, doctor, availability = self.update_department_var.get(), self.update_doctor_var.get(), self.availability_var.get()
        if not (department and doctor and availability):
            CMUHealthCareSystem.show_message("Error", "All fields must be selected.", is_error=True)
        else:
            CMUHealthCareSystem.show_message("Doctor Updated", f"{doctor} in {department} set to {availability}")

    def load_patient_history(self):
        """Load patient history into text box."""
        self.patient_history_text.delete("1.0", ctk.END)
        for patient, history in self.patient_history.items():
            self.patient_history_text.insert(ctk.END, f"{patient}: {history}\n")

    def update_patient_history(self):
        """Update patient history from the text box."""
        raw_text = self.patient_history_text.get("1.0", ctk.END).strip()
        new_history = {}
        for line in raw_text.split("\n"):
            if ": " in line:
                patient, history = line.split(": ", 1)
                new_history[patient.strip()] = history.strip()
        self.patient_history = new_history
        CMUHealthCareSystem.show_message("Success", "Patient history updated successfully.")

    def logout(self):
        self.admin_page.destroy()
        self.parent.deiconify()


if __name__ == "__main__":
    root = ctk.CTk()
    CMUHealthCareSystem(root)
    root.mainloop()

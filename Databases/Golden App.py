import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image  

# Database connection
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="",    # Localhost IP
            port="",    # MySQL default port
            user="",    # MySQL username
            password="",# MySQL password
            database="" # MySQL database name
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

class StudentManagementSystem(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Student Management System")
        self.geometry("900x500")
        self.resizable(False, False)

        # Split the main window into two sections (left and right)
        self.left_frame = ctk.CTkFrame(self, width=450, corner_radius=0, fg_color="#0073FF")
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ctk.CTkFrame(self, width=450, corner_radius=0, fg_color="#FFFFFF")
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.logo_image = ctk.CTkImage(Image.open("capaciti.jpg"), size=(300, 300))  
        self.logo_label = ctk.CTkLabel(self.left_frame, image=self.logo_image, text="")
        self.logo_label.pack(pady=50)

        # Heading on the right frame
        self.heading = ctk.CTkLabel(
            self.right_frame,
            text="Candidate Enrollment System - Login",
            font=("Arial", 20, "bold"),
            text_color="#0E6655",
        )
        self.heading.pack(pady=30)

        # Login form on the right frame
        self.form_frame = ctk.CTkFrame(self.right_frame, corner_radius=10)
        self.form_frame.pack(pady=20, padx=50)

        # Username entry
        self.username_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Username",
            corner_radius=10,
            width=300,
        )
        self.username_entry.pack(pady=10)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Password",
            show="*",
            corner_radius=10,
            width=300,
        )
        self.password_entry.pack(pady=15)

        # Show/Hide Password Button
        self.show_password = False
        self.toggle_password_btn = ctk.CTkButton(
            self.form_frame,
            text="Show",
            corner_radius=10,
            command=self.toggle_password,
            fg_color="#0073FF",
            hover_color="#005FCC",
            font=("Arial", 12, "bold"),
        )
        self.toggle_password_btn.pack(pady=5)

        # Login Button
        self.login_btn = ctk.CTkButton(
            self.form_frame,
            text="Login",
            corner_radius=10,
            command=self.login,
            fg_color="#0073FF",
            hover_color="#005FCC",
            font=("Arial", 12, "bold"),
        )
        self.login_btn.pack(pady=10)

        # Exit Button
        self.exit_btn = ctk.CTkButton(
            self.form_frame,
            text="Exit",
            corner_radius=10,
            command=self.exit_app,
            fg_color="#0073FF",
            hover_color="#005FCC",
            font=("Arial", 12, "bold"),
        )
        self.exit_btn.pack(pady=5)

    # Show/Hide Password Function
    def toggle_password(self):
        if self.show_password:
            self.password_entry.configure(show="*")
            self.toggle_password_btn.configure(text="Show")
        else:
            self.password_entry.configure(show="")
            self.toggle_password_btn.configure(text="Hide")
        self.show_password = not self.show_password

    # Exit Application Function
    def exit_app(self):
        self.destroy()

    # Login Function
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Replace with your actual authentication mechanism
        if username == "admin" and password == "admin":
            self.open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    # Function to open the dashboard
    def open_dashboard(self):
        self.withdraw()
        dashboard = DashboardWindow(self)
        dashboard.grab_set()

class DashboardWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure the dashboard window
        self.title("Admin Dashboard")
        self.geometry("1000x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Top bar for title and user info
        self.top_bar = ctk.CTkFrame(self, height=80, fg_color="#343a40", corner_radius=0)
        self.top_bar.pack(side="top", fill="x")

        self.title_label = ctk.CTkLabel(
            self.top_bar,
            text="CapaCiTi",
            font=("Arial", 20, "bold"),
            text_color="#ffffff",
            corner_radius=0
        )
        self.title_label.pack(side="left", padx=20, pady=10)

        self.user_label = ctk.CTkLabel(
            self.top_bar,
            text="Administrator",
            font=("Arial", 18, "bold"),
            text_color="#ffffff",
            corner_radius=0
        )
        self.user_label.pack(side="right", padx=20, pady=10)

        # Sidebar with buttons
        self.sidebar_frame = ctk.CTkFrame(self, width=200, fg_color="#343a40", corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        buttons = ["Dashboard", "Candidate List", "Courses", "Enroll Candidate", "Logout"]
        for btn_name in buttons:
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=btn_name,
                fg_color="#343a40",
                text_color="#ffffff",
                hover_color="#495057",
                font=("Arial", 14, "bold"),
                command=lambda name=btn_name: self.handle_button_click(name)
            )
            btn.pack(fill="x", pady=10)

        self.content_frame = ctk.CTkFrame(self, fg_color="#f8f9fa")
        self.content_frame.pack(side="right", fill="both", expand=True)

    def handle_button_click(self, btn_name):
        if btn_name == "Candidate List":
            self.display_candidate_list()
        elif btn_name == "Courses":
            self.display_courses()
        elif btn_name == "Enroll Candidate":
            self.display_enrollments()
        elif btn_name == "Logout":
            self.on_close()

    def display_candidate_list(self):
        conn = connect_to_database()
        if conn is None:
            return  # Failed to connect to the database

        self.clear_content_frame()

        # Define the columns for the Treeview
        columns = ("StudentID", "FirstName", "LastName", "DOB", "EnrollmentDate", "Actions")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        # Format columns with specific widths and alignment
        self.tree.column("StudentID", anchor="center", width=100)
        self.tree.column("FirstName", anchor="center", width=150)
        self.tree.column("LastName", anchor="center", width=150)
        self.tree.column("DOB", anchor="center", width=100)
        self.tree.column("EnrollmentDate", anchor="center", width=120)
        self.tree.column("Actions", anchor="center", width=80)

        # Define table headings with bold font
        self.tree.heading("StudentID", text="Student ID", anchor="center")
        self.tree.heading("FirstName", text="First Name", anchor="center")
        self.tree.heading("LastName", text="Last Name", anchor="center")
        self.tree.heading("DOB", text="Date of Birth", anchor="center")
        self.tree.heading("EnrollmentDate", text="Enrollment Date", anchor="center")
        self.tree.heading("Actions", text="Actions", anchor="center")

        # Add alternating row colors for better readability
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.map('Treeview', background=[('selected', 'lightblue')])
        style.configure('Treeview', background='white', foreground='black', fieldbackground='white')
        style.layout('Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])

        self.tree.pack(fill="both", expand=True)

        # Fetch data from the students table
        cursor = conn.cursor()
        cursor.execute("SELECT StudentID, FirstName, LastName, DOB, EnrollmentDate FROM students")
        rows = cursor.fetchall()

        # Insert rows and add an edit button for each row
        for row in rows:
            student_id = row[0]
            self.tree.insert("", "end", values=row + ("Edit",))

        # Bind double-click on 'Edit' action
        self.tree.bind('<Double-1>', self.on_edit_click)

        conn.close()

    def on_edit_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_values = self.tree.item(selected_item, "values")
        student_id = item_values[0]

        # Open the edit window with student_id
        EditStudentWindow(self, student_id)

    def display_courses(self):
        conn = connect_to_database()
        if conn is None:
            return

        self.clear_content_frame()

        columns = ("CourseID", "CourseName", "Credits")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        self.tree.heading("CourseID", text="Course ID")
        self.tree.heading("CourseName", text="Course Name")
        self.tree.heading("Credits", text="Credits")

        self.tree.pack(fill="both", expand=True)

        cursor = conn.cursor()
        cursor.execute("SELECT CourseID, CourseName, Credits FROM courses")
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

        conn.close()

    def display_enrollments(self):
        conn = connect_to_database()
        if conn is None:
            return

        self.clear_content_frame()

        columns = ("EnrollmentID", "StudentID", "CourseID", "Results")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        self.tree.heading("EnrollmentID", text="Enrollment ID")
        self.tree.heading("StudentID", text="Student ID")
        self.tree.heading("CourseID", text="Course ID")
        self.tree.heading("Results", text="Results")

        self.tree.pack(fill="both", expand=True)

        cursor = conn.cursor()
        cursor.execute("SELECT EnrollmentID, StudentID, CourseID, Results FROM enrollments")
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

        conn.close()

    def display_enrollments(self):
        self.clear_content_frame()

        # Form for adding a new student
        self.enroll_frame = ctk.CTkFrame(self.content_frame)
        self.enroll_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.enroll_frame, text="Enroll New Student", font=("Arial", 18, "bold")).pack(pady=10)

        # Input fields
        self.entry_first_name = ctk.CTkEntry(self.enroll_frame, placeholder_text="First Name")
        self.entry_first_name.pack(pady=5)

        self.entry_last_name = ctk.CTkEntry(self.enroll_frame, placeholder_text="Last Name")
        self.entry_last_name.pack(pady=5)

        self.entry_dob = ctk.CTkEntry(self.enroll_frame, placeholder_text="Date of Birth (YYYY-MM-DD)")
        self.entry_dob.pack(pady=5)

        self.entry_enrollment_date = ctk.CTkEntry(self.enroll_frame, placeholder_text="Enrollment Date (YYYY-MM-DD)")
        self.entry_enrollment_date.pack(pady=5)

        # Save button
        self.save_button = ctk.CTkButton(self.enroll_frame, text="Enroll Student", command=self.add_student)
        self.save_button.pack(pady=10)

    def add_student(self):
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        dob = self.entry_dob.get()
        enrollment_date = self.entry_enrollment_date.get()

        conn = connect_to_database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO students (FirstName, LastName, DOB, EnrollmentDate) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, dob, enrollment_date)
            )
            conn.commit()
            messagebox.showinfo("Success", "Student enrolled successfully!")
            self.clear_content_frame()
            self.display_candidate_list()  # Refresh candidate list
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error adding student: {err}")

        conn.close()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def on_close(self):
        self.destroy()

class EditStudentWindow(ctk.CTkToplevel):
    def __init__(self, parent, student_id):
        super().__init__(parent)

        self.title("Edit Student")
        self.geometry("400x300")

        self.student_id = student_id
        self.parent = parent

        self.create_widgets()
        self.load_student_data()

    def create_widgets(self):
        self.label_id = ctk.CTkLabel(self, text="Student ID:")
        self.label_id.pack(pady=10)

        self.entry_id = ctk.CTkEntry(self, state="disabled")
        self.entry_id.pack(pady=10)

        self.label_first_name = ctk.CTkLabel(self, text="First Name:")
        self.label_first_name.pack(pady=10)

        self.entry_first_name = ctk.CTkEntry(self)
        self.entry_first_name.pack(pady=10)

        self.label_last_name = ctk.CTkLabel(self, text="Last Name:")
        self.label_last_name.pack(pady=10)

        self.entry_last_name = ctk.CTkEntry(self)
        self.entry_last_name.pack(pady=10)

        self.label_dob = ctk.CTkLabel(self, text="Date of Birth:")
        self.label_dob.pack(pady=10)

        self.entry_dob = ctk.CTkEntry(self)
        self.entry_dob.pack(pady=10)

        self.label_enrollment_date = ctk.CTkLabel(self, text="Enrollment Date:")
        self.label_enrollment_date.pack(pady=10)

        self.entry_enrollment_date = ctk.CTkEntry(self)
        self.entry_enrollment_date.pack(pady=10)

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_changes)
        self.save_button.pack(pady=20)

    def load_student_data(self):
        conn = connect_to_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute("SELECT FirstName, LastName, DOB, EnrollmentDate FROM students WHERE StudentID = %s", (self.student_id,))
        student_data = cursor.fetchone()

        if student_data:
            self.entry_id.insert(0, self.student_id)
            self.entry_first_name.insert(0, student_data[0])
            self.entry_last_name.insert(0, student_data[1])
            self.entry_dob.insert(0, student_data[2])
            self.entry_enrollment_date.insert(0, student_data[3])

        conn.close()

    def save_changes(self):
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        dob = self.entry_dob.get()
        enrollment_date = self.entry_enrollment_date.get()

        conn = connect_to_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET FirstName = %s, LastName = %s, DOB = %s, EnrollmentDate = %s WHERE StudentID = %s",
            (first_name, last_name, dob, enrollment_date, self.student_id)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student data updated successfully!")
        self.destroy()
        self.parent.display_candidate_list()

if __name__ == "__main__":
    app = StudentManagementSystem()
    app.mainloop()

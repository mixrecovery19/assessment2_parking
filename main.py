import tkinter as tk
from tkinter import simpledialog, messagebox
from student_manager import open_student_manager_ui
from campus_manager import open_campus_manager_ui
from student_parking_manager import open_student_parking_manager
from student_parking_manager_db import open_student_parking_manager_db
from handlers import styles
from config import get_db_connection
import mysql.connector, json
# --- a basic program to demonstrate a simple student parking management system for the handling of data through both json & database ---
PASSWORD = "admin123"

def load_students():
    with open("students.json", "r") as f:
        return json.load(f)

def load_students_db():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        connection.close()
        return students
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error accessing database: {err}")
        return []

def student_access():
    student_number = simpledialog.askstring("Student Access", "Enter your Student Number:")
    
    if not student_number:
        messagebox.showerror("Error", "You must enter a student number.")
        return    
    students = load_students()    
    student = next((s for s in students if s["student_number"] == student_number), None)

    if student:       
        messagebox.showinfo("Access Granted", 
            f"Welcome {student['student_first_name']} {student['student_last_name']}!\n"
            f"Email: {student['student_email']}\nRego: {student['student_rego']}")
        
        open_student_parking_manager(student)
    else:       
        messagebox.showerror("Access Denied", "Student number not found.")

def student_access_db():
    student_number = simpledialog.askstring("Student Access", "Enter your Student Number:")
    if not student_number:
        messagebox.showerror("Error", "You must enter a student number.")
        return
    students = load_students_db()
    student = next((s for s in students if s["student_number"] == student_number), None)

    if student:        
        messagebox.showinfo("Access Granted", 
            f"Welcome {student['student_first_name']} {student['student_last_name']}!\n"
            f"Email: {student['student_email']}\nRego: {student['student_rego']}")        
        
        open_student_parking_manager_db(student)

    else:        
        messagebox.showerror("Access Denied", "Student number not found.")
    
def staff_access_student():
    password = simpledialog.askstring("Password", "Enter staff password:", show='*')
    if password == PASSWORD:
        messagebox.showinfo("Access Granted", "Welcome to the staff area.")
        open_student_manager_ui()
    else:
        messagebox.showerror("Access Denied", "Invalid password.")

def staff_access_campus():
    password = simpledialog.askstring("Password", "Enter staff password:", show='*')
    if password == PASSWORD:
        messagebox.showinfo("Access Granted", "Welcome to the staff area.")
        open_campus_manager_ui()
    else:
        messagebox.showerror("Access Denied", "Invalid password.")

def main():
    root = tk.Tk()
    root.title("MP Car Park Management")
    root.geometry("600x600")

    tk.Label(root, text="Welcome to MP Car Park Management System", font=("Arial", 14)).pack(pady=20)

    tk.Button(root, text="Student Parking Management", bg=styles.MAIN_PAGE_BUTTON_COLOR_STUDENT_PARKING, command=student_access, width=30).pack(pady=10)
    tk.Button(root, text="Student Parking Management(DB)", bg=styles.MAIN_PAGE_BUTTON_COLOR_STUDENT_PARKING_DB, command=student_access_db, width=30).pack(pady=10)
    tk.Button(root, text="Campus Manager", bg=styles.MAIN_PAGE_BUTTON_COLOR_CAMPUS, command=staff_access_campus, width=20).pack(pady=10)
    tk.Button(root, text="Student Manager", bg=styles.MAIN_PAGE_BUTTON_COLOR_STUDENT, command=staff_access_student, width=20).pack(pady=10)
    tk.Button(root, text="Exit", command=root.destroy, width=20).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

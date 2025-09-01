import tkinter as tk
from tkinter import messagebox, ttk
from config import get_db_connection

class StudentParkingManagerSearchDB:
    def __init__(self):        
        self.connection = self.mk_connect_db()

    def mk_connect_db(self):
        try:
            conn = get_db_connection()
            return conn
        except Exception as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            return None     

    def mk_load_students(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students")
            return cursor.fetchall()
        except Exception as err:
            messagebox.showerror("Database Error", f"Error loading students: {err}")
            return []

    def mk_search_student_parking_manager_db(self, student_number):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT spr.receipt_number,
                    s.student_number,
                    s.student_first_name,
                    s.student_last_name,
                    s.student_email,
                    s.added_on,
                    c.campus_name,
                    spr.total_cost,
                    spr.receipt_timestamp,
                    spr.duration
                FROM student_parking_receipt spr
                JOIN students s ON spr.student_id = s.student_id
                JOIN campus c ON spr.campus_id = c.campus_id
                WHERE s.student_number = %s
            """, (student_number,))
            return cursor.fetchall()
        except Exception as err:
            messagebox.showerror("Database Error", f"Error searching student parking: {err}")
            return []

def open_student_parking_search_db():
    search_window = tk.Toplevel()
    search_window.title("Search Student Parking")
    search_window.geometry("400x300")

    tk.Label(search_window, text="Enter Student Number:", font=("Arial", 12)).pack(pady=10)
    student_number_entry = tk.Entry(search_window)
    student_number_entry.pack(pady=5)

    def search_student_parking():
        student_number = student_number_entry.get()
        if not student_number:
            messagebox.showerror("Error", "You must enter a student number.")
            return
        search_db = StudentParkingManagerSearchDB()
        results = search_db.mk_search_student_parking_manager_db(student_number)

        if results:
            result_window = tk.Toplevel()
            result_window.title("Search Results")
            tk.Button(result_window, text="Close", command=result_window.destroy).pack(pady=10)
            result_window.geometry("800x900")
           
            columns = (
                "receipt_number", "student_number", "student_first_name", 
                "student_last_name", "student_email", "campus_name", 
                "total_cost", "receipt_timestamp", "duration"
            )
            tree = ttk.Treeview(result_window, columns=columns, show="headings", height=15)
          
            tree.heading("receipt_number", text="Receipt #")
            tree.heading("student_number", text="Student #")
            tree.heading("student_first_name", text="First Name")
            tree.heading("student_last_name", text="Last Name")
            tree.heading("student_email", text="Email")
            tree.heading("campus_name", text="Campus")
            tree.heading("total_cost", text="Total Cost")
            tree.heading("receipt_timestamp", text="Timestamp")
            tree.heading("duration", text="Duration (hrs)")

            tree.column("receipt_number", width=80)
            tree.column("student_number", width=100)
            tree.column("student_first_name", width=100)
            tree.column("student_last_name", width=100)
            tree.column("student_email", width=150)
            tree.column("campus_name", width=100)
            tree.column("total_cost", width=120)
            tree.column("receipt_timestamp", width=150)
            tree.column("duration", width=80)

            for result in results:
                tree.insert("", "end", values=(
                    result["receipt_number"],
                    result["student_number"],
                    result["student_first_name"],
                    result["student_last_name"],
                    result["student_email"],
                    result["campus_name"],
                    result["total_cost"],
                    result["receipt_timestamp"],
                    result["duration"]
                ))

            scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        else:
            messagebox.showinfo("No Results", "No parking information found for this student.")

    tk.Button(search_window, text="Search", command=search_student_parking).pack(pady=10)
    tk.Button(search_window, text="Close", command=search_window.destroy).pack(pady=10)

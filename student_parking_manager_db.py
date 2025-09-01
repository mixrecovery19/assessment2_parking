import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from config import get_db_connection


class StudentParkingManagerDB:
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
    
class StudentParkingCampusDB:
    def __init__(self):
        self.connection = get_db_connection()
        self.campuses = self.mk_load_campuses()

    def mk_load_campuses(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM campus")
            return cursor.fetchall()
        except Exception as err:
            messagebox.showerror("Database Error", f"Error loading campuses: {err}")
            return [] 

def open_student_parking_manager_db(students):
    campus_manager = StudentParkingCampusDB()

    mk_root = tk.Tk()
    mk_root.title("MP Student Car Park Activation")
    mk_root.geometry("700x600")

    tk.Label(mk_root, text="Select Campus:").pack()
    campus_names = [c["campus_name"] for c in campus_manager.campuses]
    mk_campus_combo = ttk.Combobox(mk_root, values=campus_names, state="readonly")
    mk_campus_combo.pack(pady=5)
    
    tk.Label(mk_root, text="Student Number:").pack()
    mk_student_number = tk.Label(mk_root, text=students["student_number"])
    mk_student_number.pack()

    tk.Label(mk_root, text="Student First Name:").pack()
    mk_student_first_name = tk.Label(mk_root, text=students["student_first_name"])
    mk_student_first_name.pack()

    tk.Label(mk_root, text="Student Last Name:").pack()
    mk_student_last_name = tk.Label(mk_root, text=students["student_last_name"])
    mk_student_last_name.pack()

    tk.Label(mk_root, text="Student Email:").pack()
    mk_student_email = tk.Label(mk_root, text=students["student_email"])
    mk_student_email.pack()

    tk.Label(mk_root, text="Car Registration:").pack()
    mk_student_rego_entry = tk.Entry(mk_root)
    mk_student_rego_entry.insert(0, students["student_rego"])  
    mk_student_rego_entry.pack()
    
    tk.Label(mk_root, text="Select Parking Duration (Hours):").pack(pady=10)
    durations = [1, 2, 4, 8]  
    duration_var = tk.IntVar(value=1)  

    mk_duration_combo = ttk.Combobox(
        mk_root,
        values=durations,
        state="readonly"
    )
    mk_duration_combo.current(0) 
    mk_duration_combo.pack(pady=5)
   
    tk.Label(mk_root, text="Selected Duration:").pack()
    mk_selected_duration_label = tk.Label(mk_root, text=str(duration_var.get()))
    mk_selected_duration_label.pack()
    
    tk.Label(mk_root, text="Total Cost:").pack()
    mk_total_cost_label = tk.Label(mk_root, text="$0.00")
    mk_total_cost_label.pack()
    
    def update_total_cost():
        campus_name = mk_campus_combo.get()
        hours = duration_var.get()

        if not campus_name:
            mk_total_cost_label.config(text="$0.00")
            return

        selected_campus = next((c for c in campus_manager.campuses if c["campus_name"] == campus_name), None)
        if not selected_campus:
            mk_total_cost_label.config(text="$0.00")
            return

        price_per_hour = selected_campus.get("price_per_hour") or 0
        total_cost = hours * price_per_hour
        mk_total_cost_label.config(text=f"${total_cost:.2f}")

    
    def update_selected_duration_label_db(event=None):
        selected = mk_duration_combo.get()
        if selected:
            duration_var.set(int(selected))
            mk_selected_duration_label.config(text=str(duration_var.get()))
            update_total_cost()

    mk_duration_combo.bind("<<ComboboxSelected>>", update_selected_duration_label_db)
    mk_campus_combo.bind("<<ComboboxSelected>>", lambda e: update_total_cost())

    def submit_parking_db():
        campus_name = mk_campus_combo.get()
        hours = duration_var.get()
        rego = mk_student_rego_entry.get()

        if not campus_name:
            messagebox.showwarning("Missing Data", "Please select a campus.")
            return

        selected_campus = next((c for c in campus_manager.campuses if c["campus_name"] == campus_name), None)
        if not selected_campus:
            messagebox.showwarning("Missing Data", "Selected campus not found.")
            return

        campus_id = selected_campus["campus_id"]
        price_per_hour = selected_campus.get("price_per_hour", 0)
        total_cost = hours * price_per_hour

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO student_parking_receipt
                (student_id, campus_id, duration, total_cost, receipt_timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                students["student_id"],
                campus_id,              
                hours,
                total_cost,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as err:
            messagebox.showerror("Database Error", f"Error saving receipt: {err}")
            return

        messagebox.showinfo(
            "Parking Confirmed",
            f"Parking booked for {students['student_number']}.\n"
            f"Campus: {campus_name}\n"
            f"Rego: {rego}\n"
            f"Duration: {hours} hours\n\n"
            f"Total Cost: ${total_cost:.2f}\n\n"
            f"Receipt saved to database"
        )

    tk.Button(mk_root, text="Submit", command=submit_parking_db).pack(pady=30)
    tk.Button(mk_root, text="Exit", command=mk_root.destroy).pack(pady=10)

    mk_root.mainloop()

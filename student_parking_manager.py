import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class StudentParkingManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = self.mk_load_students()

    def mk_load_students(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        

class StudentParkingCampus:
    def __init__(self, filename="campus.json"):
        self.filename = filename
        self.campuses = self.mk_load_campuses()

    def mk_load_campuses(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []       


def open_student_parking_manager(student):    
    campus_manager = StudentParkingCampus()

    mk_root = tk.Tk()
    mk_root.title("MP Student Car Park Activation")
    mk_root.geometry("500x500")
   
    tk.Label(mk_root, text="Select Campus:").pack()
    campus_names = [c["campus_name"] for c in campus_manager.campuses]
    mk_campus_combo = ttk.Combobox(mk_root, values=campus_names, state="readonly")
    mk_campus_combo.pack(pady=5)
    
    tk.Label(mk_root, text="Student Number:").pack()
    mk_student_number = tk.Label(mk_root, text=student["student_number"])
    mk_student_number.pack()

    tk.Label(mk_root, text="Student First Name:").pack()
    mk_student_first_name = tk.Label(mk_root, text=student["student_first_name"])
    mk_student_first_name.pack()

    tk.Label(mk_root, text="Student Last Name:").pack()
    mk_student_last_name = tk.Label(mk_root, text=student["student_last_name"])
    mk_student_last_name.pack()

    tk.Label(mk_root, text="Student Email:").pack()
    mk_student_email = tk.Label(mk_root, text=student["student_email"])
    mk_student_email.pack()

    tk.Label(mk_root, text="Car Registration:").pack()
    mk_student_rego_entry = tk.Entry(mk_root)
    mk_student_rego_entry.insert(0, student["student_rego"])  # prefill rego from student_rego
    mk_student_rego_entry.pack()
   
    tk.Label(mk_root, text="Select Parking Duration (Hours):").pack(pady=10)
    durations = [1, 2, 4, 8]  # directly as numbers
    duration_var = tk.IntVar(value=1)  # default selection

    mk_duration_combo = ttk.Combobox(
        mk_root,
        values=durations,
        state="readonly"
    )
    mk_duration_combo.current(0)  # the zero-based index simply defaults to the first item
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

        price_per_hour = selected_campus.get("price_per_hour", 0)
        total_cost = hours * price_per_hour
        mk_total_cost_label.config(text=f"${total_cost:.2f}")
    
    def update_selected_duration_label(event=None):
        selected = mk_duration_combo.get()
        if selected:
            duration_var.set(int(selected))
            mk_selected_duration_label.config(text=str(duration_var.get()))
            update_total_cost()

    mk_duration_combo.bind("<<ComboboxSelected>>", update_selected_duration_label)
    mk_campus_combo.bind("<<ComboboxSelected>>", lambda e: update_total_cost())

   # --- submit button speaks for itself
    def submit_parking():
        campus = mk_campus_combo.get()
        hours = duration_var.get()
        rego = mk_student_rego_entry.get()

        if not campus:
            messagebox.showwarning("Missing Data", "Please select a campus.")
            return

        selected_campus = next((c for c in campus_manager.campuses if c["campus_name"] == campus), None)
        if not selected_campus:
            messagebox.showwarning("Missing Data", "Selected campus not found.")
            return

        price_per_hour = selected_campus.get("price_per_hour", 0)
        total_cost = hours * price_per_hour

       # builds what you would like to display to the receipt, should you wish to actually handle a form of receipt processing delivery/printing
        receipt = {
            "student_number": student["student_number"],
            "student_first_name": student["student_first_name"],
            "student_last_name": student["student_last_name"],
            "student_email": student["student_email"],
            "car_registration": rego,
            "campus": campus,
            "duration": hours,
            "total_cost": total_cost,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
       # kept the son data relevance as a way to demonstrate both json and database variations of data handling
        receipts_file = "student_parking_receipt.json"
        try:
            if os.path.exists(receipts_file):
                with open(receipts_file, "r") as f:
                    receipts = json.load(f)
            else:
                receipts = []
        except json.JSONDecodeError:
            receipts = []

        receipts.append(receipt)

        with open(receipts_file, "w") as f:
            json.dump(receipts, f, indent=4)
        
        messagebox.showinfo(
            "Parking Confirmed",
            f"Parking booked for {student['student_first_name']} {student['student_last_name']}.\n"
            f"Campus: {campus}\n"
            f"Rego: {rego}\n"
            f"Duration: {hours} hours\n\n"
            f"Total Cost: ${total_cost:.2f}\n\n"
            f"Receipt saved to {receipts_file}"
        )

    tk.Button(mk_root, text="Submit", command=submit_parking).pack(pady=20)
    tk.Button(mk_root, text="Exit", command=mk_root.destroy).pack(pady=10)

    mk_root.mainloop()

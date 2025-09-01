import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = self.mk_load_students()

    def mk_load_students(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return [] 

    def mk_save_students(self):
        with open(self.filename, 'w') as file:
            json.dump(self.students, file, indent=4)

    def mk_add_student(self, mk_student_number, mk_student_first_name, mk_student_last_name, mk_student_email, mk_student_rego):
        item = {
            "student_id": len(self.students) + 1,
            "student_number": mk_student_number,
            "student_first_name": mk_student_first_name,
            "student_last_name": mk_student_last_name,
            "student_email": mk_student_email,
            "student_rego": mk_student_rego,
            "added_on": datetime.now().isoformat()
        }
        
        self.students.append(item)
        self.mk_save_students()
        print(f"✅ Added '{mk_student_first_name} {mk_student_last_name}' to students")
        return item
    
def load_student_details():
    manager = StudentManager()
    students = manager.mk_load_students()
    return students

def open_create_student_manager():
    manager = StudentManager()

    mk_root = tk.Tk()
    mk_root.title("MP Student Car Park Activation")
    mk_root.geometry("500x500")

    #search existing students    
    tk.Label(mk_root, text="Select Existing Student:").pack()
    student_names = [f"{c['student_id']}: {c['student_first_name']} {c['student_last_name']}" for c in manager.students]
    student_var = tk.StringVar()
    mk_student_combo = ttk.Combobox(mk_root, values=student_names, state="readonly", textvariable=student_var)
    mk_student_combo.pack(pady=5)

    tk.Button(
        mk_root,
        text="Select This Student To Update",
        command=lambda: load_student_details()
    ).pack(pady=5)
    
    tk.Label(mk_root, text="Student Number:").pack()
    mk_student_number_entry = tk.Entry(mk_root)
    mk_student_number_entry.pack()

    tk.Label(mk_root, text="Student First Name:").pack()
    mk_student_first_name_entry = tk.Entry(mk_root)
    mk_student_first_name_entry.pack()

    tk.Label(mk_root, text="Student Last Name:").pack()
    mk_student_last_name_entry = tk.Entry(mk_root)
    mk_student_last_name_entry.pack()

    tk.Label(mk_root, text="Student Email:").pack()
    mk_student_email_entry = tk.Entry(mk_root)
    mk_student_email_entry.pack()

    tk.Label(mk_root, text="Car Registration:").pack()
    mk_student_rego_entry = tk.Entry(mk_root)
    mk_student_rego_entry.pack()
    
    mk_listbox = tk.Listbox(mk_root, width=50)
    mk_listbox.pack(pady=10)
    
    def create_student_from_form():
        num = mk_student_number_entry.get().strip()
        first = mk_student_first_name_entry.get().strip()
        last = mk_student_last_name_entry.get().strip()
        email = mk_student_email_entry.get().strip()
        rego = mk_student_rego_entry.get().strip()

        if not (num and first and last and email and rego):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        item = manager.mk_add_student(num, first, last, email, rego)
       
        mk_listbox.insert(tk.END, f"{item['student_id']}: {first} {last} ({rego})")
       
        mk_student_number_entry.delete(0, tk.END)
        mk_student_first_name_entry.delete(0, tk.END)
        mk_student_last_name_entry.delete(0, tk.END)
        mk_student_email_entry.delete(0, tk.END)
        mk_student_rego_entry.delete(0, tk.END)

    def load_student_details(*args):
        selection = student_var.get()
        if not selection:
            return
        student_id = int(selection.split(":")[0])
        student = next((s for s in manager.students if s["student_id"] == student_id), None)
        if student:
            mk_student_number_entry.delete(0, tk.END)
            mk_student_number_entry.insert(0, student["student_number"])

            mk_student_first_name_entry.delete(0, tk.END)
            mk_student_first_name_entry.insert(0, student["student_first_name"])

            mk_student_last_name_entry.delete(0, tk.END)
            mk_student_last_name_entry.insert(0, student["student_last_name"])

            mk_student_email_entry.delete(0, tk.END)
            mk_student_email_entry.insert(0, student["student_email"])

            mk_student_rego_entry.delete(0, tk.END)
            mk_student_rego_entry.insert(0, student["student_rego"])

        student_var.trace_add("w", load_student_details)
    
    tk.Button(mk_root, text="Add Student", command=create_student_from_form).pack(pady=5)    
    tk.Button(mk_root, text="Exit Student Manager", command=mk_root.destroy).pack(pady=5)
    
    mk_root.mainloop()

import tkinter as tk
from tkinter import messagebox
import json

class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = self.mk_load_students()

    def mk_load_students(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # empty if no file yet

    def mk_save_students(self):
        with open(self.filename, 'w') as file:
            json.dump(self.students, file, indent=4)

    def mk_update_students(self, mk_student_id, mk_student_number, mk_student_first_name, mk_student_last_name, mk_student_email, mk_student_rego):
        for item in self.students:
            if item["student_id"] == mk_student_id:
                item["student_number"] = mk_student_number
                item["student_first_name"] = mk_student_first_name
                item["student_last_name"] = mk_student_last_name
                item["student_email"] = mk_student_email
                item["student_rego"] = mk_student_rego
                self.mk_save_students()
                print(f"✅ Updated student ID {mk_student_id}")
                return item
        print(f"❌ Student ID {mk_student_id} not found")
        return None

def open_update_student_manager():
    manager = StudentManager()

    mk_root = tk.Tk()
    mk_root.title("MP Student Update Manager")
    mk_root.geometry("500x500")

    # --- Dropdown to select student ---
    student_var = tk.StringVar()
    student_dropdown = tk.OptionMenu(
        mk_root,
        student_var,
        *[f"{s['student_id']}: {s['student_first_name']} {s['student_last_name']}" for s in manager.students]
    )
    student_dropdown.pack(pady=10)

    # --- Form fields ---
    tk.Label(mk_root, text="Student Number:").pack()
    mk_student_number_entry = tk.Entry(mk_root)
    mk_student_number_entry.pack()

    tk.Label(mk_root, text="First Name:").pack()
    mk_student_first_name_entry = tk.Entry(mk_root)
    mk_student_first_name_entry.pack()

    tk.Label(mk_root, text="Last Name:").pack()
    mk_student_last_name_entry = tk.Entry(mk_root)
    mk_student_last_name_entry.pack()

    tk.Label(mk_root, text="Email:").pack()
    mk_student_email_entry = tk.Entry(mk_root)
    mk_student_email_entry.pack()

    tk.Label(mk_root, text="Car Registration:").pack()
    mk_student_rego_entry = tk.Entry(mk_root)
    mk_student_rego_entry.pack()

    # --- Populate form when student selected ---
    def load_student_details(*args):
        selection = student_var.get()
        print(f"Variable changed! New Value: {selection}")
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

    # ✅ trace binding should be here, not inside the function
    student_var.trace_add("write", load_student_details)

    # --- Update function ---
    def update_student_from_form():
        selection = student_var.get()
        if not selection:
            messagebox.showerror("Error", "Please select a student first.")
            return

        student_id = int(selection.split(":")[0])
        updated = manager.mk_update_students(
            student_id,
            mk_student_number_entry.get().strip(),
            mk_student_first_name_entry.get().strip(),
            mk_student_last_name_entry.get().strip(),
            mk_student_email_entry.get().strip(),
            mk_student_rego_entry.get().strip()
        )

        if updated:
            messagebox.showinfo("Success", f"Student ID {student_id} updated successfully!")
        else:
            messagebox.showerror("Error", f"Failed to update student ID {student_id}.")

    # --- Buttons ---
    tk.Button(mk_root, text="Update Selected Student", command=update_student_from_form).pack(pady=5)
    tk.Button(mk_root, text="Exit", command=mk_root.destroy).pack(pady=5)

    mk_root.mainloop()

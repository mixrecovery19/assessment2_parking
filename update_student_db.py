import tkinter as tk
from tkinter import messagebox
import mysql.connector
from dotenv import load_dotenv
import os

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "carpark")
DB_USER = os.getenv("DB_USER", "Michael-MP")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

class StudentManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.students = self.mk_load_students()

    def mk_load_students(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        cursor.close()
        return result

    def mk_update_student(self, mk_student_id, mk_student_number, mk_first_name, mk_last_name, mk_email, mk_rego):
        cursor = self.connection.cursor()
        sql = """
        UPDATE students
        SET student_number=%s,
            student_first_name=%s,
            student_last_name=%s,
            student_email=%s,
            student_rego=%s
        WHERE student_id=%s
        """
        cursor.execute(sql, (mk_student_number, mk_first_name, mk_last_name, mk_email, mk_rego, mk_student_id))
        self.connection.commit()
        cursor.close()

        # Update local list
        for item in self.students:
            if item["student_id"] == mk_student_id:
                item["student_number"] = mk_student_number
                item["student_first_name"] = mk_first_name
                item["student_last_name"] = mk_last_name
                item["student_email"] = mk_email
                item["student_rego"] = mk_rego
                break

        print(f"✅ Updated student ID {mk_student_id}")
        return True

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()

# -----------------------------
# Tkinter GUI
# -----------------------------
def open_update_student_manager_db():
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

    student_var.trace_add("write", load_student_details)

    # --- Update function ---
    def update_student_from_form():
        selection = student_var.get()
        if not selection:
            messagebox.showerror("Error", "Please select a student first.")
            return

        student_id = int(selection.split(":")[0])
        success = manager.mk_update_student(
            student_id,
            mk_student_number_entry.get().strip(),
            mk_student_first_name_entry.get().strip(),
            mk_student_last_name_entry.get().strip(),
            mk_student_email_entry.get().strip(),
            mk_student_rego_entry.get().strip()
        )

        if success:
            messagebox.showinfo("Success", f"Student ID {student_id} updated successfully!")
        else:
            messagebox.showerror("Error", f"Failed to update student ID {student_id}.")

    # --- Buttons ---
    tk.Button(mk_root, text="Update Selected Student", command=update_student_from_form).pack(pady=5)
    tk.Button(mk_root, text="Exit", command=lambda: [manager.close_connection(), mk_root.destroy()]).pack(pady=5)

    mk_root.mainloop()

# Run the GUI
if __name__ == "__main__":
    open_update_student_manager_db()

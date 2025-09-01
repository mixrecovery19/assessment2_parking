import tkinter as tk
from tkinter import messagebox, ttk
from config import get_db_connection

class StudentManager:
    def __init__(self):
        self.connection = get_db_connection()
        self.students = self.mk_load_students() 

    def mk_load_students(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")  
        students = cursor.fetchall()
        cursor.close()
        return students

    def mk_add_student(self, student_number, first_name, last_name, email, rego):
        cursor = self.connection.cursor()
        sql = """
        INSERT INTO students (student_number, student_first_name, student_last_name, student_email, student_rego, added_on)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(sql, (student_number, first_name, last_name, email, rego))
        self.connection.commit()
        student_id = cursor.lastrowid
        cursor.close()

        student = {
            "student_id": student_id,
            "student_number": student_number,
            "student_first_name": first_name,
            "student_last_name": last_name,
            "student_email": email,
            "student_rego": rego
        }
        self.students.append(student)
        print(f"✅ Added '{first_name} {last_name}' to database with ID {student_id}")
        return student

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()

def open_create_student_manager_db():
    manager = StudentManager()

    mk_root = tk.Tk()
    mk_root.title("MP Student Car Park Activation")
    mk_root.geometry("600x600")
    
    tk.Label(mk_root, text="Select Existing Student:").pack()
    student_var = tk.StringVar()
    student_names = [f"{c['student_id']}: {c['student_first_name']} {c['student_last_name']}" for c in manager.students]
    mk_student_combo = ttk.Combobox(mk_root, values=student_names, state="readonly", textvariable=student_var)
    mk_student_combo.pack(pady=5)
    
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
       
        student_names.append(f"{item['student_id']}: {first} {last}")
        mk_student_combo['values'] = student_names

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
    
    tk.Button(mk_root, text="Add Student", command=create_student_from_form).pack(pady=5)
    tk.Button(mk_root, text="Exit Student Manager", command=lambda: (manager.close_connection(), mk_root.destroy())).pack(pady=5)

    mk_root.mainloop()

if __name__ == "__main__":
    open_create_student_manager_db()

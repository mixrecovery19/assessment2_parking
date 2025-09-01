import tkinter as tk
from create_student import open_create_student_manager
from create_student_db import open_create_student_manager_db
from update_student import open_update_student_manager
from update_student_db import open_update_student_manager_db
from student_parking_search_db import open_student_parking_search_db

def open_student_manager():
    open_create_student_manager()
    open_create_student_manager_db()
    open_update_student_manager()
    open_update_student_manager_db()
    open_student_parking_search_db()

def open_student_manager_ui():
    root = tk.Tk()
    root.title("MP Student Management")
    root.geometry("600x600")

    tk.Label(root, text="Welcome to the Student Management System", font=("Arial", 14)).pack(pady=20)

    tk.Button(root, text="Create Student Manager", command=open_create_student_manager, width=30).pack(pady=10)
    tk.Button(root, text="Create Student Manager (DB)", command=open_create_student_manager_db, width=30).pack(pady=10)
    tk.Button(root, text="Update Student Manager", command=open_update_student_manager, width=30).pack(pady=10)
    tk.Button(root, text="Update Student Manager (DB)", command=open_update_student_manager_db, width=30).pack(pady=10)
    tk.Button(root, text="Students Parking Search (DB)", command=open_student_parking_search_db, width=30).pack(pady=10)
    tk.Button(root, text="Exit", command=root.destroy, width=30).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    open_student_manager_ui()

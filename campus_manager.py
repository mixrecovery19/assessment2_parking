import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from create_campus import open_create_campus_manager
from update_campus import open_update_campus_manager
from create_campus_db import open_create_campus_manager_db
from update_campus_db import open_update_campus_manager_db

def open_campus_manager():
    open_create_campus_manager()
    open_update_campus_manager()
    open_create_campus_manager_db()
    open_update_campus_manager_db()

def open_campus_manager_ui():
    root = tk.Tk()
    root.title("MP Car Park Management")
    root.geometry("400x300")

    tk.Label(root, text="Welcome to the Car Park Management System", font=("Arial", 14)).pack(pady=20)

    tk.Button(root, text="Create Campus Manager", command=open_create_campus_manager, width=30).pack(pady=10)
    tk.Button(root, text="Create Campus Manager (DB)", command=open_create_campus_manager_db, width=30).pack(pady=10)
    tk.Button(root, text="Update Campus Manager", command=open_update_campus_manager, width=30).pack(pady=10)
    tk.Button(root, text="Update Campus Manager (DB)", command=open_update_campus_manager_db, width=30).pack(pady=10)
    tk.Button(root, text="Exit", command=root.destroy, width=30).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    open_campus_manager_ui()

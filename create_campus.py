import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

CampusTotalCarparks = 100

class CampusManager:
    def __init__(self, filename="campus.json"):
        self.filename = filename
        self.campus = self.mk_load_campus()

    def mk_load_campus(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # empty if no file yet

    def mk_save_campus(self):
        with open(self.filename, 'w') as file:
            json.dump(self.campus, file, indent=4)

    def mk_add_campus(self, mk_campus_name, mk_campus_location):
        item = {
            "campus_id": len(self.campus) + 1,
            "campus_total_carparks": CampusTotalCarparks,
            "campus_name": mk_campus_name,
            "campus_location": mk_campus_location,
            "available_carparks": CampusTotalCarparks,  # Initially all carparks are available
            "occupied_carparks": 0,
            "price_per_hour": 0,
            "added_on": datetime.now().isoformat()
        }

        self.campus.append(item)
        self.mk_save_campus()
        print(f"✅ Added '{mk_campus_name}' to campuses")
        return item  # so we can update the UI with this record

def open_create_campus_manager():
    manager = CampusManager()

    mk_root = tk.Tk()
    mk_root.title("MP Campus Management")
    mk_root.geometry("500x500")

    # Form fields
    tk.Label(mk_root, text="Campus Name:").pack()
    mk_campus_name_entry = tk.Entry(mk_root)
    mk_campus_name_entry.pack()

    tk.Label(mk_root, text="Campus Location:").pack()
    mk_campus_location_entry = tk.Entry(mk_root)
    mk_campus_location_entry.pack()

    tk.Label(mk_root, text="Total Car Parks:").pack()
    mk_campus_total_carparks_entry = tk.Entry(mk_root)
    mk_campus_total_carparks_entry.pack()    

    tk.Label(mk_root, text="Price Per Hour:").pack()
    mk_campus_price_per_hour_entry = tk.Entry(mk_root)
    mk_campus_price_per_hour_entry.pack()

    # Listbox to display records
    mk_listbox = tk.Listbox(mk_root, width=50)
    mk_listbox.pack(pady=10)

    # Function to add campus from form
    def create_campus_from_form():
        name = mk_campus_name_entry.get().strip()
        location = mk_campus_location_entry.get().strip()

        if not (name and location):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        item = manager.mk_add_campus(name, location)
        
        mk_listbox.insert(tk.END, f"{item['campus_id']}: {name} ({location})")
        
        mk_campus_name_entry.delete(0, tk.END)
        mk_campus_location_entry.delete(0, tk.END)

    # Button
    tk.Button(mk_root, text="Create Campus", command=create_campus_from_form).pack(pady=5)
    tk.Button(mk_root, text="Exit Campus Manager", command=mk_root.destroy).pack(pady=5)

    # Start GUI loop
    mk_root.mainloop()

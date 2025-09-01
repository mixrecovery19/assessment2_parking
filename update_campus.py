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

    def mk_update_campus(self, mk_campus_id, mk_campus_name, mk_campus_location, mk_total_carparks, mk_price_per_hour):
        for item in self.campus:
            if item["campus_id"] == mk_campus_id:
                item["campus_name"] = mk_campus_name
                item["campus_location"] = mk_campus_location
                item["total_carparks"] = mk_total_carparks
                item["price_per_hour"] = mk_price_per_hour
                self.mk_save_campus()
                print(f"✅ Updated campus ID {mk_campus_id}")
                return item
        print(f"❌ Campus ID {mk_campus_id} not found")
        return None


def open_update_campus_manager():
    manager = CampusManager()

    mk_root = tk.Tk()
    mk_root.title("MP Campus Management")
    mk_root.geometry("500x500")
    
    campus_var = tk.StringVar()
    campus_dropdown = tk.OptionMenu(mk_root, campus_var, *[f"{c['campus_id']}: {c['campus_name']}" for c in manager.campus])
    campus_dropdown.pack(pady=10)
    
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
    
    def load_campus_details(*args):
        selection = campus_var.get()
        if not selection:
            return
        campus_id = int(selection.split(":")[0])
        campus = next((c for c in manager.campus if c["campus_id"] == campus_id), None)
        if campus:
            mk_campus_name_entry.delete(0, tk.END)
            mk_campus_name_entry.insert(0, campus["campus_name"])

            mk_campus_location_entry.delete(0, tk.END)
            mk_campus_location_entry.insert(0, campus["campus_location"])

            mk_campus_total_carparks_entry.delete(0, tk.END)
            mk_campus_total_carparks_entry.insert(0, campus.get("total_carparks", ""))

            mk_campus_price_per_hour_entry.delete(0, tk.END)
            mk_campus_price_per_hour_entry.insert(0, campus.get("price_per_hour", ""))

    campus_var.trace_add("write", load_campus_details)
    
    def update_campus_from_form():
        selection = campus_var.get()
        if not selection:
            messagebox.showerror("Error", "Please select a campus first.")
            return

        campus_id = int(selection.split(":")[0])
        name = mk_campus_name_entry.get().strip()
        location = mk_campus_location_entry.get().strip()
        total_carparks = mk_campus_total_carparks_entry.get().strip()
        price_per_hour = mk_campus_price_per_hour_entry.get().strip()

        if not (name and location and total_carparks and price_per_hour):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        item = manager.mk_update_campus(campus_id, name, location, int(total_carparks), float(price_per_hour))
        if item:
            messagebox.showinfo("Success", f"Campus {campus_id} updated successfully!")
   
    tk.Button(mk_root, text="Update Selected Campus", command=update_campus_from_form).pack(pady=5)
    tk.Button(mk_root, text="Exit Campus Update Manager", command=mk_root.destroy).pack(pady=5)

    mk_root.mainloop()

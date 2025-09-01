import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "carpark")
DB_USER = os.getenv("DB_USER", "Michael-MP")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

CampusTotalCarparks = 100

class CampusManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.campus = self.mk_load_campus()

    def mk_load_campus(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM campus")
        result = cursor.fetchall()
        cursor.close()
        return result

    def mk_update_campus(self, mk_campus_id, mk_campus_name, mk_campus_location, mk_total_carparks, mk_price_per_hour):
        cursor = self.connection.cursor()
        sql = """
        UPDATE campus
        SET campus_name=%s,
            campus_location=%s,
            campus_total_carparks=%s,
            price_per_hour=%s
        WHERE campus_id=%s
        """
        cursor.execute(sql, (mk_campus_name, mk_campus_location, mk_total_carparks, mk_price_per_hour, mk_campus_id))
        self.connection.commit()
        cursor.close()

        # Update local list
        for item in self.campus:
            if item["campus_id"] == mk_campus_id:
                item["campus_name"] = mk_campus_name
                item["campus_location"] = mk_campus_location
                item["campus_total_carparks"] = mk_total_carparks
                item["price_per_hour"] = mk_price_per_hour
                break

        print(f"✅ Updated campus ID {mk_campus_id}")
        return True

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()

# -----------------------------
# Tkinter GUI
# -----------------------------
def open_update_campus_manager_db():
    manager = CampusManager()

    mk_root = tk.Tk()
    mk_root.title("MP Campus Update Manager")
    mk_root.geometry("500x500")

    # Dropdown to select campus
    campus_var = tk.StringVar()
    campus_dropdown = tk.OptionMenu(mk_root, campus_var, *[f"{c['campus_id']}: {c['campus_name']}" for c in manager.campus])
    campus_dropdown.pack(pady=10)

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

    # Populate form when campus selected
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
            mk_campus_total_carparks_entry.insert(0, campus.get("campus_total_carparks", ""))

            mk_campus_price_per_hour_entry.delete(0, tk.END)
            mk_campus_price_per_hour_entry.insert(0, campus.get("price_per_hour", ""))

    campus_var.trace_add("write", load_campus_details)

    # Update function
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

        success = manager.mk_update_campus(campus_id, name, location, int(total_carparks), float(price_per_hour))
        if success:
            messagebox.showinfo("Success", f"Campus {campus_id} updated successfully!")

    # Buttons
    tk.Button(mk_root, text="Update Selected Campus", command=update_campus_from_form).pack(pady=5)
    tk.Button(mk_root, text="Exit Campus Update Manager", command=lambda: [manager.close_connection(), mk_root.destroy()]).pack(pady=5)

    mk_root.mainloop()

# Run the GUI
if __name__ == "__main__":
    open_update_campus_manager_db()

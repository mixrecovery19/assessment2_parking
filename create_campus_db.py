import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from config import get_db_connection

CampusTotalCarparks = 100

class CampusManager:
    def __init__(self):
        self.connection = get_db_connection()            
        self.campus = self.mk_load_campus()

    def mk_load_campus(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM campus")
        result = cursor.fetchall()
        cursor.close()
        return result             

    def mk_add_campus(self, mk_campus_name, mk_campus_location, mk_total_carparks, mk_price_per_hour):
        cursor = self.connection.cursor()
        sql = """
        INSERT INTO campus (
            campus_name, campus_location, campus_total_carparks,
            available_carparks, occupied_carparks, price_per_hour, added_on
        )
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(sql, (
            mk_campus_name,
            mk_campus_location,
            mk_total_carparks,
            mk_total_carparks,   
            0,                   
            mk_price_per_hour
        ))
        self.connection.commit()
        campus_id = cursor.lastrowid
        cursor.close()

        campus = {
            "campus_id": campus_id,
            "campus_total_carparks": mk_total_carparks,
            "campus_name": mk_campus_name,
            "campus_location": mk_campus_location,
            "available_carparks": mk_total_carparks,
            "occupied_carparks": 0,
            "price_per_hour": mk_price_per_hour,
            "added_on": datetime.now().isoformat()
        }

        self.campus.append(campus)        
        print(f"✅ Added '{mk_campus_name}' to campus")
        return campus


    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()


def open_create_campus_manager_db():
    manager = CampusManager()

    mk_root = tk.Tk()
    mk_root.title("MP Campus Management")
    mk_root.geometry("500x500")
    
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
   
    mk_listbox = tk.Listbox(mk_root, width=50)
    mk_listbox.pack(pady=10)
   
    def create_campus_from_form():
        name = mk_campus_name_entry.get().strip()
        location = mk_campus_location_entry.get().strip()
        total_carparks = int(mk_campus_total_carparks_entry.get().strip())
        price_per_hour = float(mk_campus_price_per_hour_entry.get().strip())

        if not (name and location):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        item = manager.mk_add_campus(name, location, total_carparks, price_per_hour)
        
        mk_listbox.insert(tk.END, f"{item['campus_id']}: {name} ({location}) - ${price_per_hour}/hr")

        mk_campus_name_entry.delete(0, tk.END)
        mk_campus_location_entry.delete(0, tk.END)
        mk_campus_total_carparks_entry.delete(0, tk.END)
        mk_campus_price_per_hour_entry.delete(0, tk.END)
    
    tk.Button(mk_root, text="Create Campus", command=create_campus_from_form).pack(pady=5)
    tk.Button(mk_root, text="Exit Campus Manager", command=mk_root.destroy).pack(pady=5)
    
    mk_root.mainloop()

    if __name__ == "__main__":
        open_create_campus_manager_db()
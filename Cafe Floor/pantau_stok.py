import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def pantau_stok():
    win = tk.Toplevel()
    win.title("Pantauan Stok Bahan")
    win.geometry("500x400") # 
    win.configure(bg="#f8f9fa")

    tk.Label(win, text="Pantauan Stok Bahan", font=("Segoe UI", 16, "bold"),
             bg="#198754", fg="white", pady=10).pack(fill=tk.X)

    tree = ttk.Treeview(win, columns=("nama", "stok", "satuan"), show="headings")
    tree.heading("nama", text="Nama Bahan")
    tree.heading("stok", text="Stok")
    tree.heading("satuan", text="Satuan")
    
    # Atur lebar kolom
    tree.column("nama", anchor="w", width=200)
    tree.column("stok", anchor="center", width=100)
    tree.column("satuan", anchor="center", width=100)
    
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
        cursor = conn.cursor()
        
        cursor.execute("SELECT nama_bahan, stok, satuan FROM bahan") 
        
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Terjadi kesalahan database: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan tak terduga: {e}")

# Contoh penggunaan
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 

    pantau_stok()

    root.mainloop()
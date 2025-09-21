import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def lihat_menu_pelanggan():
    win = tk.Toplevel()
    win.title("Daftar Menu")
    win.geometry("600x400")
    win.configure(bg="#f8f9fa")

    tk.Label(win, text="Daftar Menu", font=("Segoe UI", 16, "bold"),
             bg="#198754", fg="white", pady=10).pack(fill=tk.X)

    tree = ttk.Treeview(win, columns=("nama", "harga", "kategori"), show="headings")
    tree.heading("nama", text="Nama Menu")
    tree.heading("harga", text="Harga")
    tree.heading("kategori", text="Kategori")
    tree.column("nama", anchor="center")
    tree.column("harga", anchor="center")
    tree.column("kategori", anchor="center")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
        cursor = conn.cursor()
        cursor.execute("SELECT nama_menu, harga, kategori FROM menu")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))
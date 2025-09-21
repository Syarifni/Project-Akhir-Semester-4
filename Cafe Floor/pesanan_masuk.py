import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def lihat_pesanan_kasir():
    win = tk.Toplevel()
    win.title("Daftar Pesanan Hari Ini")
    win.geometry("750x500")

    tree = ttk.Treeview(win, columns=("id", "tanggal", "pelanggan", "total", "status"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="cafe_floor"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_pesanan, p.tanggal, u.username, t.total_bayar, p.status
            FROM pesanan p
            JOIN pengguna u ON p.id_pengguna = u.id_pengguna
            JOIN transaksi t ON p.id_pesanan = t.id_pesanan
            ORDER BY p.tanggal DESC
        """)
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal ambil pesanan: {e}")
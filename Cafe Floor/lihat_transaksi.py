import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

def lihat_transaksi_kasir():
    win = tk.Toplevel()
    win.title("Transaksi Penjualan")
    win.geometry("750x500")
    win.configure(bg="#f8f9fa")

    tk.Label(win, text="Transaksi Penjualan Hari Ini", font=("Segoe UI", 16, "bold"),
             bg="#198754", fg="white", pady=10).pack(fill=tk.X)

    # Filter tanggal
    filter_frame = tk.Frame(win, bg="#f8f9fa")
    filter_frame.pack(pady=10)

    tk.Label(filter_frame, text="Tanggal (YYYY-MM-DD):", font=("Segoe UI", 11), bg="#f8f9fa").pack(side=tk.LEFT, padx=5)
    entry_tanggal = tk.Entry(filter_frame, font=("Segoe UI", 11), width=15)
    entry_tanggal.insert(0, datetime.now().strftime("%Y-%m-%d"))
    entry_tanggal.pack(side=tk.LEFT, padx=5)

    # Table
    tree = ttk.Treeview(win, columns=("id", "tanggal", "total", "metode", "status"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_transaksi():
        tanggal = entry_tanggal.get().strip()
        if not tanggal:
            messagebox.showwarning("Input Salah", "Masukkan tanggal.")
            return

        tree.delete(*tree.get_children())

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.id_transaksi, t.tanggal_pembayaran, t.total_bayar, t.metode_pembayaran, p.status
                FROM transaksi t
                JOIN pesanan p ON t.id_pesanan = p.id_pesanan
                WHERE DATE(t.tanggal_pembayaran) = %s
                ORDER BY t.tanggal_pembayaran DESC
            """, (tanggal,))
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(filter_frame, text="Tampilkan", font=("Segoe UI", 11), bg="#198754", fg="white",
              command=load_transaksi).pack(side=tk.LEFT, padx=5)

    load_transaksi()
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

def show_laporan_penjualan():
    def load_data():
        tanggal = tanggal_entry.get()
        if not tanggal:
            messagebox.showwarning("Input Error", "Masukkan tanggal terlebih dahulu.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="cafe_floor"
            )
            cursor = conn.cursor()

            query = """
                SELECT p.tanggal, m.nama_menu, pi.jumlah, pi.subtotal 
                FROM pesanan p
                JOIN pesanan_item pi ON p.id_pesanan = pi.id_pesanan
                JOIN menu m ON pi.id_menu = m.id_menu
                WHERE DATE(p.tanggal) = %s
            """
            cursor.execute(query, (tanggal,))
            rows = cursor.fetchall()

            for i in tree.get_children():
                tree.delete(i)
            for row in rows:
                tree.insert("", "end", values=row)

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data: {e}")

    window = tk.Toplevel()
    window.title("Laporan Penjualan Harian")
    window.geometry("750x500")
    window.configure(bg="#e9fbe5")

    title = tk.Label(window, text="Laporan Penjualan", font=("Segoe UI", 18, "bold"), bg="#198754", fg="white", pady=15)
    title.pack(fill=tk.X)

    tanggal_frame = tk.Frame(window, bg="#e9fbe5")
    tanggal_frame.pack(pady=10)

    tk.Label(tanggal_frame, text="Tanggal (YYYY-MM-DD):", font=("Segoe UI", 11), bg="#e9fbe5").pack(side=tk.LEFT, padx=5)
    tanggal_entry = tk.Entry(tanggal_frame, font=("Segoe UI", 11), width=15)
    tanggal_entry.insert(0, str(date.today()))
    tanggal_entry.pack(side=tk.LEFT, padx=5)

    tk.Button(tanggal_frame, text="Tampilkan", command=load_data, font=("Segoe UI", 11), bg="#198754", fg="white").pack(side=tk.LEFT, padx=5)

    columns = ("tanggal", "menu", "jumlah", "subtotal")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    tree.heading("tanggal", text="Tanggal")
    tree.heading("menu", text="Nama Menu")
    tree.heading("jumlah", text="Jumlah")
    tree.heading("subtotal", text="Subtotal (Rp)")

    for col in columns:
        tree.column(col, anchor="center")

    tree.pack(pady=20, fill=tk.BOTH, expand=True)
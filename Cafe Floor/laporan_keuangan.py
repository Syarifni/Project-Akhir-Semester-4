import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

def show_laporan_keuangan():
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

            # Penjualan
            cursor.execute("""
                SELECT SUM(total_bayar) FROM transaksi t
                JOIN pesanan p ON t.id_pesanan = p.id_pesanan
                WHERE DATE(p.tanggal) = %s
            """, (tanggal,))
            penjualan = cursor.fetchone()[0] or 0

            # Pengeluaran
            cursor.execute("SELECT SUM(jumlah) FROM pengeluaran WHERE DATE(tanggal) = %s", (tanggal,))
            pengeluaran = cursor.fetchone()[0] or 0

            # Bersih
            hasil = penjualan - pengeluaran

            for i in tree.get_children():
                tree.delete(i)

            tree.insert("", "end", values=("Total Penjualan", f"Rp{penjualan:,}"))
            tree.insert("", "end", values=("Total Pengeluaran", f"- Rp{pengeluaran:,}"))
            tree.insert("", "end", values=("Laba Bersih", f"Rp{hasil:,}"))

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data: {e}")

    window = tk.Toplevel()
    window.title("Laporan Keuangan Harian")
    window.geometry("500x400")
    window.configure(bg="#e9fbe5")

    title = tk.Label(window, text="Laporan Keuangan Harian", font=("Segoe UI", 18, "bold"), bg="#198754", fg="white", pady=15)
    title.pack(fill=tk.X)

    tanggal_frame = tk.Frame(window, bg="#e9fbe5")
    tanggal_frame.pack(pady=10)

    tk.Label(tanggal_frame, text="Tanggal (YYYY-MM-DD):", font=("Segoe UI", 11), bg="#e9fbe5").pack(side=tk.LEFT, padx=5)
    tanggal_entry = tk.Entry(tanggal_frame, font=("Segoe UI", 11), width=15)
    tanggal_entry.insert(0, str(date.today()))
    tanggal_entry.pack(side=tk.LEFT, padx=5)

    tk.Button(tanggal_frame, text="Tampilkan", command=load_data, font=("Segoe UI", 11), bg="#198754", fg="white").pack(side=tk.LEFT, padx=5)

    tree = ttk.Treeview(window, columns=("keterangan", "nilai"), show="headings")
    tree.heading("keterangan", text="Keterangan")
    tree.heading("nilai", text="Nilai")

    tree.column("keterangan", anchor="w", width=200)
    tree.column("nilai", anchor="e", width=200)

    tree.pack(pady=20, fill=tk.BOTH, expand=True)
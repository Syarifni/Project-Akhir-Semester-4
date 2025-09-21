import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def analisis_produk():
    win = tk.Toplevel()
    win.title("Analisis Produk Terlaris")
    win.geometry("850x550")
    win.configure(bg="#f8f9fa")

    # Header
    tk.Label(win, text="Analisis Menu Terlaris", font=("Segoe UI", 16, "bold"),
             bg="#198754", fg="white", pady=10).pack(fill=tk.X)

    # Filter Tanggal (Otomatis Hari Ini)
    filter_frame = tk.Frame(win, bg="#f8f9fa")
    filter_frame.pack(pady=10)

    tk.Label(filter_frame, text="Tanggal (YYYY-MM-DD):", font=("Segoe UI", 11), bg="#f8f9fa").pack(side=tk.LEFT)
    tanggal_entry = tk.Entry(filter_frame, font=("Segoe UI", 11), width=15)
    tanggal_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))  # Set default hari ini
    tanggal_entry.pack(side=tk.LEFT, padx=5)

    # Canvas Grafik
    canvas_frame = tk.Frame(win, bg="#f8f9fa")
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    global_fig = None  # untuk ekspor grafik

    # Ambil Data dari DB
    def ambil_data():
        tanggal = tanggal_entry.get().strip()
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="cafe_floor"
            )
            cursor = conn.cursor()

            query = """
                SELECT m.nama_menu, SUM(pi.jumlah) as total_terjual
                FROM pesanan_item pi
                JOIN menu m ON pi.id_menu = m.id_menu
                JOIN pesanan p ON pi.id_pesanan = p.id_pesanan
                WHERE DATE(p.tanggal) = %s
                GROUP BY m.nama_menu ORDER BY total_terjual DESC LIMIT 10
            """
            cursor.execute(query, (tanggal,))
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data:\n{e}")
            return []

    # Tampilkan Grafik
    def tampilkan_grafik():
        nonlocal global_fig
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        data = ambil_data()
        if not data:
            messagebox.showinfo("Kosong", "Tidak ada data untuk ditampilkan.")
            return

        nama_menu = [row[0] for row in data]
        total = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(nama_menu[::-1], total[::-1], color="#6f42c1")
        ax.set_title("TOP 10 MENU TERLARIS")
        ax.set_xlabel("Jumlah Terjual")

        global_fig = fig

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Export PNG
    def export_png():
        if not global_fig:
            messagebox.showwarning("Kosong", "Tampilkan grafik terlebih dahulu.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if file:
            global_fig.savefig(file)
            messagebox.showinfo("Berhasil", f"Disimpan sebagai {file}")

    # Export PDF
    def export_pdf():
        if not global_fig:
            messagebox.showwarning("Kosong", "Tampilkan grafik terlebih dahulu.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if file:
            global_fig.savefig(file)
            messagebox.showinfo("Berhasil", f"PDF berhasil disimpan: {file}")

    # Export Excel
    def export_excel():
        data = ambil_data()
        if not data:
            messagebox.showwarning("Kosong", "Tidak ada data untuk diekspor.")
            return
        df = pd.DataFrame(data, columns=["Nama Menu", "Total Terjual"])
        file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel File", "*.xlsx")])
        if file:
            df.to_excel(file, index=False)
            messagebox.showinfo("Berhasil", f"Excel berhasil disimpan: {file}")

    # Tombol Aksi
    btn_frame = tk.Frame(win, bg="#f8f9fa")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Tampilkan Grafik", bg="#6f42c1", fg="white", font=("Segoe UI", 11, "bold"),
              command=tampilkan_grafik).pack(side=tk.LEFT, padx=10)

    tk.Button(btn_frame, text="Export PNG", bg="#0d6efd", fg="white", font=("Segoe UI", 11, "bold"),
              command=export_png).pack(side=tk.LEFT, padx=5)

    tk.Button(btn_frame, text="Export PDF", bg="#dc3545", fg="white", font=("Segoe UI", 11, "bold"),
              command=export_pdf).pack(side=tk.LEFT, padx=5)

    tk.Button(btn_frame, text="Export Excel", bg="#198754", fg="white", font=("Segoe UI", 11, "bold"),
              command=export_excel).pack(side=tk.LEFT, padx=5)
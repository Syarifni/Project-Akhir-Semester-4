import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import mysql.connector
import pandas as pd
from fpdf import FPDF

def get_data_penjualan_per_menu(tanggal, kategori=None):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cafe_floor"
        )
        cursor = conn.cursor()
        query = """
            SELECT 
                m.nama_menu, 
                m.kategori,
                SUM(pi.jumlah) AS total_terjual 
            FROM 
                pesanan_item pi
            JOIN 
                menu m ON pi.id_menu = m.id_menu
            JOIN 
                pesanan p ON pi.id_pesanan = p.id_pesanan
            WHERE 
                DATE(p.tanggal) = %s AND p.status = 'Selesai'
        """
        params = [tanggal]
        if kategori and kategori != "Semua":
            query += " AND m.kategori = %s"
            params.append(kategori)

        query += " GROUP BY m.nama_menu, m.kategori ORDER BY total_terjual DESC"
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        print("Database Error:", e)
        return []
    finally:
        if conn: conn.close()

def show_laporan_menu():
    root = tk.Toplevel()
    root.title("Laporan Penjualan Menu")
    root.geometry("850x600")
    root.configure(bg="#f0fff0")

    tk.Label(root, text="Laporan Penjualan Menu", font=("Segoe UI", 18, "bold"),
             bg="#198754", fg="white", pady=12).pack(fill=tk.X)

    # Form Input 
    form_frame = tk.LabelFrame(root, text="Filter Laporan", font=("Segoe UI", 12, "bold"), bg="#f0fff0")
    form_frame.pack(padx=20, pady=10, fill=tk.X)

    tk.Label(form_frame, text="Tanggal (YYYY-MM-DD):", font=("Segoe UI", 11), bg="#f0fff0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tanggal_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=15)
    tanggal_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
    tanggal_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Kategori:", font=("Segoe UI", 11), bg="#f0fff0").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    kategori_var = tk.StringVar()
    kategori_dropdown = ttk.Combobox(form_frame, textvariable=kategori_var, font=("Segoe UI", 11), width=20, state="readonly")
    kategori_dropdown.grid(row=0, column=3, padx=5, pady=5)

    def load_kategori():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="cafe_floor"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT kategori FROM menu")
            result = cursor.fetchall()
            kategori_list = [r[0] for r in result]
            kategori_dropdown['values'] = ["Semua"] + kategori_list
            kategori_var.set("Semua")
        except Exception as e:
            print("Gagal ambil kategori:", e)
        finally:
            if conn: conn.close()

    # Table 
    table_frame = tk.Frame(root, bg="#f0fff0")
    table_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    table = ttk.Treeview(table_frame, columns=("Nama Menu", "Kategori", "Total Terjual"), show="headings")
    for col in ("Nama Menu", "Kategori", "Total Terjual"):
        table.heading(col, text=col)
        table.column(col, anchor="center", width=200)
    table.pack(fill=tk.BOTH, expand=True)

    # Logic & Export 
    def tampilkan_data():
        tanggal = tanggal_entry.get()
        kategori = kategori_var.get()
        data = get_data_penjualan_per_menu(tanggal, kategori)

        table.delete(*table.get_children())
        if not data:
            messagebox.showinfo("Info", "Data tidak ditemukan.")
            return

        for item in data:
            table.insert("", tk.END, values=item)

    def export_excel():
        tanggal = tanggal_entry.get()
        kategori = kategori_var.get()
        data = get_data_penjualan_per_menu(tanggal, kategori)
        if not data:
            messagebox.showwarning("Kosong", "Tidak ada data untuk diekspor.")
            return
        df = pd.DataFrame(data, columns=["Nama Menu", "Kategori", "Total Terjual"])
        file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file:
            df.to_excel(file, index=False)
            messagebox.showinfo("Berhasil", f"Data berhasil disimpan ke: {file}")

    def export_pdf():
        tanggal = tanggal_entry.get()
        kategori = kategori_var.get()
        data = get_data_penjualan_per_menu(tanggal, kategori)
        if not data:
            messagebox.showwarning("Kosong", "Tidak ada data untuk diekspor.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Laporan Penjualan Menu", ln=True, align="C")
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 10, f"Tanggal: {tanggal}    Kategori: {kategori}", ln=True)

        pdf.set_font("Arial", "B", 10)
        pdf.cell(80, 8, "Nama Menu", 1)
        pdf.cell(50, 8, "Kategori", 1)
        pdf.cell(30, 8, "Total Terjual", 1)
        pdf.ln()

        pdf.set_font("Arial", "", 10)
        for nama, kat, jumlah in data:
            pdf.cell(80, 8, str(nama), 1)
            pdf.cell(50, 8, str(kat), 1)
            pdf.cell(30, 8, str(jumlah), 1)
            pdf.ln()

        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file:
            pdf.output(file)
            messagebox.showinfo("Berhasil", f"PDF disimpan: {file}")

    # Tombol Aksi 
    btn_frame = tk.Frame(root, bg="#f0fff0")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Tampilkan Data", font=("Segoe UI", 11, "bold"),
              bg="#198754", fg="white", command=tampilkan_data, width=20).pack(side=tk.LEFT, padx=10)

    tk.Button(btn_frame, text="Export Excel", font=("Segoe UI", 11, "bold"),
              bg="#20c997", fg="white", command=export_excel, width=20).pack(side=tk.LEFT, padx=10)

    tk.Button(btn_frame, text="Export PDF", font=("Segoe UI", 11, "bold"),
              bg="#dc3545", fg="white", command=export_pdf, width=20).pack(side=tk.LEFT, padx=10)

    load_kategori()
    root.mainloop()
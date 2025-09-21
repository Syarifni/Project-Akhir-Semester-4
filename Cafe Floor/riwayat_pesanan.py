import tkinter as tk
from tkinter import messagebox, ttk
from koneksi import connect_db

def show_riwayat_pesanan(user_id):
    riwayat_win = tk.Toplevel()
    riwayat_win.title("Riwayat Pesanan Saya")
    riwayat_win.geometry("900x600")
    riwayat_win.configure(bg="#f8f9fa")

    tk.Label(riwayat_win, text="Riwayat Pesanan Pelanggan", font=("Segoe UI", 18, "bold"),
             bg="#198754", fg="white", pady=10).pack(fill=tk.X)

    frame = tk.Frame(riwayat_win, bg="#f8f9fa")
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("id_pesanan", "tanggal", "total_bayar", "metode_pembayaran", "status_pesanan"), show="headings", height=15)
    
    tree.heading("id_pesanan", text="ID Pesanan")
    tree.heading("tanggal", text="Tanggal Pesanan")
    tree.heading("total_bayar", text="Total Bayar")
    tree.heading("metode_pembayaran", text="Metode Pembayaran")
    tree.heading("status_pesanan", text="Status")

    tree.column("id_pesanan", width=100, anchor=tk.CENTER)
    tree.column("tanggal", width=180, anchor=tk.CENTER)
    tree.column("total_bayar", width=150, anchor=tk.E)
    tree.column("metode_pembayaran", width=150, anchor=tk.CENTER)
    tree.column("status_pesanan", width=100, anchor=tk.CENTER)
    
    tree.pack(fill=tk.BOTH, expand=True)

    def load_riwayat_pesanan():
        conn = None
        try:
            conn = connect_db()
            cursor = conn.cursor()
            
            # Mengambil riwayat pesanan spesifik untuk user_id yang login
            cursor.execute("""
                SELECT p.id_pesanan, p.tanggal, t.total_bayar, t.metode_pembayaran, p.status
                FROM pesanan p
                LEFT JOIN transaksi t ON p.id_pesanan = t.id_pesanan
                WHERE p.id_pengguna = %s
                ORDER BY p.tanggal DESC
            """, (user_id,))
            
            rows = cursor.fetchall()

            # Bersihkan treeview sebelum mengisi ulang
            for item in tree.get_children():
                tree.delete(item)

            if not rows:
                messagebox.showinfo("Informasi", "Anda belum memiliki riwayat pesanan.")
                return

            for row in rows:
                # Format total_bayar
                total_bayar_formatted = f"Rp{row[2]:,.0f}" if row[2] is not None else "N/A"
                tree.insert("", tk.END, values=(row[0], row[1], total_bayar_formatted, row[3], row[4]))

        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memuat riwayat pesanan: {e}")
        finally:
            if conn:
                conn.close()

    load_riwayat_pesanan()

    riwayat_win.mainloop()

# Bagian ini hanya untuk pengujian modul secara terpisah
if __name__ == '__main__':
    root_test = tk.Tk()
    root_test.withdraw()
    # Contoh pemanggilan untuk user_id 4
    show_riwayat_pesanan(4)
    root_test.mainloop()
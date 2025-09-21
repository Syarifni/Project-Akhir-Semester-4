import tkinter as tk
from tkinter import messagebox
from koneksi import connect_db
from cetak_struk import tampilkan_struk # Mengimpor tampilkan_struk

def cetak_ulang_struk_kasir():
    win = tk.Toplevel()
    win.title("Cetak Ulang Struk")
    win.geometry("500x300")
    win.configure(bg="#f8f9fa")

    tk.Label(win, text="CETAK ULANG STRUK PESANAN", font=("Segoe UI", 16, "bold"),
             bg="#198754", fg="white", pady=10).pack(fill=tk.X)

    form_frame = tk.Frame(win, bg="#f8f9fa", padx=20, pady=20)
    form_frame.pack(pady=20, padx=20)

    tk.Label(form_frame, text="Masukkan ID Pesanan:", font=("Segoe UI", 12), bg="#f8f9fa").grid(row=0, column=0, sticky="w", pady=10, padx=5)
    id_pesanan_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=25)
    id_pesanan_entry.grid(row=0, column=1, pady=10, padx=5)
    id_pesanan_entry.focus_set()

    def proses_cetak_ulang():
        pesanan_id_str = id_pesanan_entry.get()
        if not pesanan_id_str:
            messagebox.showwarning("Input Kosong", "Mohon masukkan ID Pesanan.")
            return

        conn = None
        try:
            pesanan_id = int(pesanan_id_str)
            conn = connect_db()
            cursor = conn.cursor(dictionary=True) # Mengambil hasil sebagai dictionary

            # Ambil data pesanan utama dan transaksi
            # Mengambil t.total_bayar sebagai 'total'
            cursor.execute("""
                SELECT 
                    p.id_pesanan, p.tanggal, p.status AS status_pesanan, 
                    t.total_bayar AS total, -- Mengambil total_bayar dan meng-alias-nya sebagai 'total'
                    peng.nama AS nama_pelanggan,
                    t.metode_pembayaran
                FROM pesanan p
                JOIN pengguna peng ON p.id_pengguna = peng.id_pengguna
                LEFT JOIN transaksi t ON p.id_pesanan = t.id_pesanan
                WHERE p.id_pesanan = %s
            """, (pesanan_id,))
            data_pesanan_db = cursor.fetchone()

            if not data_pesanan_db:
                messagebox.showwarning("Tidak Ditemukan", f"Pesanan dengan ID {pesanan_id} tidak ditemukan.")
                return

            # Ambil item-item pesanan
            cursor.execute("""
                SELECT 
                    m.nama_menu AS nama, 
                    pi.jumlah AS qty, 
                    m.harga AS harga_satuan, 
                    pi.subtotal
                FROM pesanan_item pi
                JOIN menu m ON pi.id_menu = m.id_menu
                WHERE pi.id_pesanan = %s
            """, (pesanan_id,))
            item_data_db = cursor.fetchall()

            if not item_data_db:
                messagebox.showwarning("Tidak Ada Item", f"Pesanan ID {pesanan_id} tidak memiliki item. Struk tidak dapat dicetak.")
                return

            # Siapkan data untuk tampilkan_struk
            data_pesanan_for_struk = {
                "id_pesanan": data_pesanan_db['id_pesanan'],
                "nama_pelanggan": data_pesanan_db['nama_pelanggan'],
                "total": data_pesanan_db['total'], # Menggunakan 'total' dari alias SQL
                "metode_pembayaran": data_pesanan_db.get('metode_pembayaran', 'N/A'),
                "status_pembayaran": data_pesanan_db['status_pesanan'],
                "diskon": 0, # Placeholder
                "pajak": 0,   # Placeholder
                "tanggal": data_pesanan_db['tanggal'] # Pastikan tanggal dikirim sebagai objek datetime
            }

            tampilkan_struk(data_pesanan_for_struk, item_data_db)
            messagebox.showinfo("Sukses", f"Struk untuk Pesanan ID {pesanan_id} berhasil dicetak ulang.")
            win.destroy()
            
        except ValueError:
            messagebox.showwarning("Input Invalid", "ID Pesanan harus berupa angka.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
            print(f"Error detail: {e}")
        finally:
            if conn:
                conn.close()

    tk.Button(form_frame, text="Cetak Struk", font=("Segoe UI", 12, "bold"),
              bg="#198754", fg="white", command=proses_cetak_ulang).grid(row=1, columnspan=2, pady=20)

    id_pesanan_entry.bind("<Return>", lambda event: proses_cetak_ulang())

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    cetak_ulang_struk_kasir()
    root.mainloop()
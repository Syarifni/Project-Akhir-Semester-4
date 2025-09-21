import tkinter as tk
from tkinter import messagebox, ttk
from koneksi import connect_db
import datetime
from cetak_struk import tampilkan_struk

def show_pembayaran(user_id):
    pembayaran_win = tk.Toplevel()
    pembayaran_win.title("Form Pembayaran")
    pembayaran_win.geometry("700x500")
    pembayaran_win.configure(bg="#f8f9fa")

    tk.Label(pembayaran_win, text=f"Pembayaran Pesanan (Pelanggan ID: {user_id})", font=("Segoe UI", 16, "bold"), bg="#f8f9fa").pack(pady=10)

    tk.Label(pembayaran_win, text="Pilih Pesanan yang Akan Dibayar:", bg="#f8f9fa").pack(pady=5)
    
    pesanan_options = []
    pesanan_data_map = {}

    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        # Mengambil total_bayar dari tabel transaksi (t.total_bayar)
        cursor.execute("""
            SELECT p.id_pesanan, p.tanggal, t.total_bayar, t.metode_pembayaran
            FROM pesanan p
            LEFT JOIN transaksi t ON p.id_pesanan = t.id_pesanan
            WHERE p.id_pengguna = %s AND p.status = 'Menunggu' -- Mencari status 'Menunggu'
            ORDER BY p.tanggal DESC
        """, (user_id,))
        for row in cursor.fetchall():
            id_p, tgl_p, total_p, metode_p = row
            # Fallback jika total_bayar di transaksi masih None (belum diisi sempurna)
            if total_p is None:
                sub_cursor = conn.cursor()
                sub_cursor.execute("SELECT SUM(subtotal) FROM pesanan_item WHERE id_pesanan = %s", (id_p,))
                sum_subtotal = sub_cursor.fetchone()[0]
                total_p = sum_subtotal if sum_subtotal is not None else 0
                sub_cursor.close()
                
            display_text = f"ID: {id_p} - Tgl: {tgl_p.strftime('%Y-%m-%d')} - Total: Rp{total_p:,.0f}"
            pesanan_options.append(display_text)
            pesanan_data_map[display_text] = {'id': id_p, 'total': total_p, 'metode_awal': metode_p, 'tanggal': tgl_p} # Tambahkan tanggal
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memuat daftar pesanan: {e}")
        print(f"Error detail: {e}")
    finally:
        if conn:
            conn.close()

    if not pesanan_options:
        tk.Label(pembayaran_win, text="Tidak ada pesanan yang perlu dibayar.", bg="#f8f9fa", fg="red").pack()
        tk.Button(pembayaran_win, text="Tutup", command=pembayaran_win.destroy).pack(pady=20)
        return

    selected_pesanan_text = tk.StringVar(pembayaran_win)
    selected_pesanan_text.set(pesanan_options[0])

    pesanan_dropdown = ttk.Combobox(pembayaran_win, textvariable=selected_pesanan_text, values=pesanan_options, state="readonly", font=("Segoe UI", 12))
    pesanan_dropdown.pack(pady=5)

    tk.Label(pembayaran_win, text="Jumlah Pembayaran (Rp):", bg="#f8f9fa").pack(pady=5)
    jumlah_bayar_entry = tk.Entry(pembayaran_win, font=("Segoe UI", 12), width=20)
    jumlah_bayar_entry.pack(pady=5)

    tk.Label(pembayaran_win, text="Metode Pembayaran:", bg="#f8f9fa").pack(pady=5)
    metode_bayar_var = tk.StringVar(pembayaran_win)
    metode_bayar_var.set("Tunai")
    metode_bayar_dropdown = ttk.Combobox(pembayaran_win, textvariable=metode_bayar_var, values=["Tunai", "QRIS", "Debit", "Transfer"], state="readonly", font=("Segoe UI", 12))
    metode_bayar_dropdown.pack(pady=5)

    def proses_pembayaran():
        try:
            pesanan_text = selected_pesanan_text.get()
            pesanan_info = pesanan_data_map.get(pesanan_text)
            
            if not pesanan_info:
                messagebox.showwarning("Validasi", "Pilih pesanan yang akan dibayar.")
                return

            id_pesanan_to_pay = pesanan_info['id']
            total_harga_pesanan = pesanan_info['total']
            
            jumlah_bayar = float(jumlah_bayar_entry.get())
            metode_pembayaran = metode_bayar_var.get()

            if jumlah_bayar <= 0:
                messagebox.showwarning("Validasi", "Jumlah pembayaran harus positif.")
                return
            
            if jumlah_bayar < total_harga_pesanan:
                messagebox.showwarning("Pembayaran Kurang", f"Jumlah pembayaran kurang dari total harga pesanan (Rp{total_harga_pesanan:,.0f}).")
                return
            
            conn = None
            try:
                conn = connect_db()
                cursor = conn.cursor()
                
                # Update status pesanan di tabel 'pesanan' menjadi 'Selesai'
                cursor.execute("UPDATE pesanan SET status = %s WHERE id_pesanan = %s", ("Selesai", id_pesanan_to_pay))
                
                # Update transaksi di tabel 'transaksi'
                # Asumsi transaksi sudah dibuat di pemesanan.py, jadi kita UPDATE saja
                tanggal_transaksi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    UPDATE transaksi 
                    SET tanggal_pembayaran = %s, total_bayar = %s, metode_pembayaran = %s 
                    WHERE id_pesanan = %s
                """, (tanggal_transaksi, jumlah_bayar, metode_pembayaran, id_pesanan_to_pay))
                
                conn.commit()
                messagebox.showinfo("Sukses", "Pembayaran berhasil diproses.")
                pembayaran_win.destroy()

                # Panggil tampilkan_struk dengan data yang diformat
                _data_pesanan, _item_data = _get_data_for_struk(id_pesanan_to_pay)
                if _data_pesanan and _item_data:
                    tampilkan_struk(_data_pesanan, _item_data)

            except Exception as e:
                messagebox.showerror("Gagal Pembayaran", f"Terjadi kesalahan saat memproses pembayaran: {e}")
                print(f"Error detail: {e}")
                if conn: conn.rollback()
            finally:
                if conn:
                    conn.close()
        except ValueError:
            messagebox.showwarning("Validasi", "Jumlah pembayaran harus berupa angka.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan tak terduga: {e}")

    def _get_data_for_struk(id_pesanan):
        conn = None
        data_pesanan_struk = None
        item_data_struk = []
        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)

            # Ambil detail pesanan utama (menggunakan t.total_bayar sebagai 'total')
            cursor.execute("""
                SELECT 
                    p.id_pesanan, p.tanggal, p.status AS status_pesanan, 
                    t.total_bayar AS total,
                    peng.nama AS nama_pelanggan,
                    t.metode_pembayaran
                FROM pesanan p
                JOIN pengguna peng ON p.id_pengguna = peng.id_pengguna
                LEFT JOIN transaksi t ON p.id_pesanan = t.id_pesanan
                WHERE p.id_pesanan = %s
            """, (id_pesanan,))
            data_pesanan_db = cursor.fetchone()

            if not data_pesanan_db:
                return None, None

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
            """, (id_pesanan,))
            item_data_db = cursor.fetchall()

            data_pesanan_struk = {
                "id_pesanan": data_pesanan_db['id_pesanan'],
                "tanggal": data_pesanan_db['tanggal'], # Objek datetime dari DB
                "nama_pelanggan": data_pesanan_db['nama_pelanggan'],
                "total": data_pesanan_db['total'],
                "metode_pembayaran": data_pesanan_db.get('metode_pembayaran', 'N/A'),
                "status_pembayaran": data_pesanan_db['status_pesanan'],
                "diskon": 0,
                "pajak": 0
            }
            item_data_struk = item_data_db

            return data_pesanan_struk, item_data_struk

        except Exception as e:
            messagebox.showerror("Error Struk", f"Gagal mengambil data untuk struk: {e}")
            print(f"Error detail _get_data_for_struk: {e}")
            return None, None
        finally:
            if conn:
                conn.close()

    tk.Button(pembayaran_win, text="Proses Pembayaran", font=("Segoe UI", 12, "bold"), bg="#198754", fg="white", command=proses_pembayaran).pack(pady=20)
    pembayaran_win.mainloop()
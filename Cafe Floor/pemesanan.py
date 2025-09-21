import tkinter as tk
from tkinter import messagebox, ttk
import datetime
from koneksi import connect_db
from cetak_struk import tampilkan_struk 

def show_pemesanan(user_id):
    pemesanan_win = tk.Toplevel()
    pemesanan_win.title("Pemesanan Pelanggan")
    pemesanan_win.geometry("800x700")
    pemesanan_win.configure(bg="#f8f9fa")

    tk.Label(pemesanan_win, text="Pemesanan Pelanggan", font=("Segoe UI", 18, "bold"),
             bg="#198754", fg="white", pady=10).pack(fill=tk.X)

    frame = tk.Frame(pemesanan_win, bg="#f8f9fa")
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def get_menu_data():
        conn = None
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_menu, nama_menu, harga FROM menu WHERE status='tersedia'")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error Menu", f"Gagal memuat daftar menu: {e}")
            return []
        finally:
            if conn:
                conn.close()

    daftar_menu = get_menu_data()

    # Membuat map dari nama_menu ke ID dan harga untuk pencarian cepat
    menu_name_to_info = {item[1]: {'id': item[0], 'harga': item[2]} for item in daftar_menu}
    menu_names_with_price = [f"{item[1]} - Rp{item[2]:,.0f}" for item in daftar_menu]

    tree = ttk.Treeview(frame, columns=("id_menu", "nama_menu", "harga_satuan", "qty", "subtotal"), show="headings", height=12)
    tree.heading("id_menu", text="ID Menu")
    tree.heading("nama_menu", text="Nama Menu")
    tree.heading("harga_satuan", text="Harga Satuan")
    tree.heading("qty", text="Jumlah")
    tree.heading("subtotal", text="Subtotal")

    tree.column("id_menu", width=80, anchor=tk.CENTER)
    tree.column("nama_menu", width=200, anchor=tk.W)
    tree.column("harga_satuan", width=120, anchor=tk.E)
    tree.column("qty", width=80, anchor=tk.CENTER)
    tree.column("subtotal", width=150, anchor=tk.E)
    tree.pack(fill=tk.BOTH, expand=True)

    def update_total():
        total = 0
        for child in tree.get_children():
            total += float(tree.item(child)["values"][4])
        total_label.config(text=f"Total: Rp{total:,.0f}")
        return total

    def tambah_item():
        selected_text = combo_menu.get()
        if not selected_text:
            messagebox.showwarning("Validasi", "Pilih menu terlebih dahulu.")
            return

        menu_name_only = selected_text.split(" - Rp")[0]
        menu_info = menu_name_to_info.get(menu_name_only)
        
        if not menu_info:
            messagebox.showerror("Error", "Menu tidak ditemukan. Silakan refresh aplikasi atau hubungi admin.")
            return

        menu_id = menu_info['id']
        nama_menu = menu_name_only # Gunakan nama menu tanpa harga
        harga_satuan = float(menu_info['harga'])

        try:
            qty_str = qty_entry.get().strip()
            if not qty_str:
                messagebox.showwarning("Input Salah", "Jumlah tidak boleh kosong.")
                return

            qty = int(qty_str)
            if qty <= 0:
                messagebox.showwarning("Input Salah", "Jumlah harus lebih dari 0.")
                return
        except ValueError:
            messagebox.showwarning("Input Salah", "Jumlah harus berupa angka.")
            return
        
        subtotal = harga_satuan * qty
        
        # Periksa apakah item sudah ada di treeview
        item_exists = False
        for child in tree.get_children():
            current_id = tree.item(child)["values"][0]
            if current_id == menu_id:
                current_qty = tree.item(child)["values"][3]
                current_subtotal = tree.item(child)["values"][4]
                new_qty = current_qty + qty
                new_subtotal = current_subtotal + subtotal
                tree.item(child, values=(menu_id, nama_menu, harga_satuan, new_qty, new_subtotal))
                item_exists = True
                break
        
        if not item_exists:
            tree.insert("", tk.END, values=(menu_id, nama_menu, harga_satuan, qty, subtotal))
        
        update_total()

        qty_entry.delete(0, tk.END)
        qty_entry.insert(0, "1")

    def hapus_item():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih item yang ingin dihapus.")
            return
        for item in selected_item:
            tree.delete(item)
        update_total()

    def update_stok_otomatis(pesanan_id, cursor):
        # Ambil item-item pesanan dari database, bukan dari treeview (untuk keamanan dan konsistensi)
        cursor.execute("""
            SELECT pi.id_menu, pi.jumlah 
            FROM pesanan_item pi
            WHERE pi.id_pesanan = %s
        """, (pesanan_id,))
        items = cursor.fetchall()

        for id_menu, jumlah_pesanan in items:
            cursor.execute("SELECT id_bahan, jumlah FROM menu_bahan WHERE id_menu = %s", (id_menu,))
            bahan_menu = cursor.fetchall()
            
            for id_bahan, jumlah_bahan_per_item in bahan_menu:
                total_kurang = jumlah_bahan_per_item * jumlah_pesanan
                cursor.execute("UPDATE bahan SET stok = stok - %s WHERE id_bahan = %s", (total_kurang, id_bahan))
                
                cursor.execute("""
                    INSERT INTO log_stock (id_bahan, perubahan, keterangan, waktu)
                    VALUES (%s, %s, %s, NOW())
                """, (id_bahan, -total_kurang, f'Digunakan untuk pesanan {pesanan_id}'))

        try:
            # Pastikan kolom 'batas_minimum' ada di tabel 'bahan'
            cursor.execute("SELECT nama_bahan, stok, satuan FROM bahan WHERE stok <= batas_minimum")
            data_stok_menipis = cursor.fetchall()
            if data_stok_menipis:
                pesan = "Stok bahan berikut menipis:\n"
                for nama, stok, satuan in data_stok_menipis:
                    pesan += f"- {nama} sisa {stok} {satuan}\n"
                messagebox.showwarning("Peringatan Stok", pesan)
        except Exception as e:
            # Jika kolom 'batas_minimum' belum ada, peringatan akan muncul di sini
            messagebox.showwarning("Peringatan Stok", 
                                   f"Tidak dapat memeriksa batas minimum stok. Pastikan kolom 'batas_minimum' ada di tabel 'bahan'. Error: {e}")

    def simpan_pesanan():
        if not tree.get_children():
            messagebox.showwarning("Validasi", "Belum ada item pesanan.")
            return
        
        conn = None
        try:
            conn = connect_db()
            cursor = conn.cursor()

            nama_pengguna_struk = "Anonim"
            # Ambil nama pengguna berdasarkan user_id
            cursor.execute("SELECT nama FROM pengguna WHERE id_pengguna = %s", (user_id,))
            user_result = cursor.fetchone()
            if user_result:
                nama_pengguna_struk = user_result[0]

            total_keseluruhan = update_total()
            tanggal_pesanan_obj = datetime.datetime.now()
            tanggal_pesanan_str = tanggal_pesanan_obj.strftime("%Y-%m-%d %H:%M:%S")
            metode_pembayaran_final = metode_var.get()

            # Insert ke tabel pesanan
            # Total harga tidak dimasukkan di sini karena akan dihitung di transaksi akhir
            cursor.execute(
                "INSERT INTO pesanan (id_pengguna, tanggal, status) VALUES (%s, %s, %s)",
                (user_id, tanggal_pesanan_str, "Menunggu") # Status awal "Menunggu"
            )
            id_pesanan_baru = cursor.lastrowid # Dapatkan ID pesanan yang baru saja dibuat

            if not id_pesanan_baru:
                raise Exception("Gagal mendapatkan ID pesanan baru.")

            # Masukkan item pesanan ke tabel pesanan_item
            for child in tree.get_children():
                menu_id, nama_menu, harga_satuan, qty, subtotal = tree.item(child)["values"]
                cursor.execute(
                    "INSERT INTO pesanan_item (id_pesanan, id_menu, jumlah, subtotal) VALUES (%s, %s, %s, %s)",
                    (id_pesanan_baru, menu_id, qty, subtotal)
                )
            
            # Insert ke tabel transaksi dengan total_bayar awal
            # Total_bayar di sini adalah estimasi awal, bisa diupdate di pembayaran.py
            cursor.execute(
                "INSERT INTO transaksi (id_pesanan, tanggal_pembayaran, total_bayar, metode_pembayaran) VALUES (%s, %s, %s, %s)",
                (id_pesanan_baru, tanggal_pesanan_str, total_keseluruhan, metode_pembayaran_final)
            )

            # Update stok bahan otomatis
            update_stok_otomatis(id_pesanan_baru, cursor)
            
            conn.commit()

            messagebox.showinfo("Berhasil", f"Pesanan Anda berhasil disimpan. ID Pesanan: {id_pesanan_baru}. Silakan lanjutkan ke pembayaran.")
            
            # Siapkan data untuk tampilkan_struk
            data_pesanan_for_struk = {
                "id_pesanan": id_pesanan_baru,
                "nama_pelanggan": nama_pengguna_struk, # Menggunakan nama pengguna yang diambil dari DB
                "total": total_keseluruhan,
                "metode_pembayaran": metode_pembayaran_final,
                "status_pembayaran": "Menunggu Pembayaran", # Status awal saat struk dicetak
                "diskon": 0, # Belum ada diskon di sini
                "pajak": 0,  # Belum ada pajak di sini
                "tanggal": tanggal_pesanan_obj
            }
            item_data_for_struk = []
            for item in tree.get_children():
                menu_id, nama_menu, harga_satuan, qty, subtotal = item['values']
                item_data_for_struk.append({
                    "nama": nama_menu,
                    "qty": qty,
                    "harga_satuan": harga_satuan,
                    "subtotal": subtotal
                })

            tampilkan_struk(data_pesanan_for_struk, item_data_for_struk)

            # Kosongkan treeview setelah pesanan disimpan
            tree.delete(*tree.get_children())
            update_total()
            
            # pemesanan_win.destroy() # Opsional: tutup jendela setelah simpan

        except Exception as e:
            messagebox.showerror("Gagal Menyimpan Pesanan", f"Terjadi kesalahan: {e}")
            print(f"Error detail in simpan_pesanan: {e}")
            if conn: conn.rollback() # Rollback transaksi jika ada kesalahan
        finally:
            if conn:
                conn.close()

    # Frame input menu dan jumlah
    input_frame = tk.Frame(pemesanan_win, bg="#f5f5dc")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Pilih Menu", font=("Segoe UI", 11), bg="#f5f5dc").grid(row=0, column=0, padx=5, pady=5)
    combo_menu = ttk.Combobox(input_frame, font=("Segoe UI", 11), width=30,
                              values=menu_names_with_price, state="readonly")
    combo_menu.grid(row=0, column=1, padx=5, pady=5)
    if menu_names_with_price:
        combo_menu.set(menu_names_with_price[0])
    else:
        combo_menu.config(state="disabled")

    tk.Label(input_frame, text="Jumlah", font=("Segoe UI", 11), bg="#f5f5dc").grid(row=0, column=2, padx=5, pady=5)
    qty_entry = tk.Entry(input_frame, font=("Segoe UI", 11), width=5)
    qty_entry.insert(0, "1")
    qty_entry.grid(row=0, column=3, padx=5, pady=5)

    tk.Button(input_frame, text="Tambah", bg="#198754", fg="white", font=("Segoe UI", 11, "bold"),
              command=tambah_item).grid(row=0, column=4, padx=10, pady=5)
    
    tk.Button(input_frame, text="Hapus Item Terpilih", bg="#dc3545", fg="white", font=("Segoe UI", 11),
              command=hapus_item).grid(row=1, column=0, columnspan=5, pady=5) # Tombol hapus

    bottom_frame = tk.Frame(pemesanan_win, bg="#f8f9fa")
    bottom_frame.pack(pady=10)

    metode_var = tk.StringVar(value="Tunai")
    tk.Label(bottom_frame, text="Metode Pembayaran:", font=("Segoe UI", 11), bg="#f8f9fa").grid(row=0, column=0, padx=5)
    metode_menu = ttk.Combobox(bottom_frame, font=("Segoe UI", 11), textvariable=metode_var,
                               values=["Tunai", "Transfer", "QRIS", "Debit"], width=10, state="readonly")
    metode_menu.grid(row=0, column=1, padx=5)
    metode_menu.set("Tunai")

    total_label = tk.Label(bottom_frame, text="Total: Rp0", font=("Segoe UI", 14, "bold"),
                           bg="#f8f9fa", fg="#212529")
    total_label.grid(row=0, column=2, padx=20)

    tk.Button(bottom_frame, text="Simpan Pesanan", font=("Segoe UI", 12, "bold"),
              bg="#198754", fg="white", command=simpan_pesanan).grid(row=0, column=3, padx=10)
    
    update_total()
    pemesanan_win.mainloop()

# Bagian ini hanya untuk pengujian modul secara terpisah
if __name__ == '__main__':
   
    root_test = tk.Tk()
    root_test.withdraw() # Sembunyikan jendela root utama
    print("Menjalankan Pemesanan untuk user_id 4...")
    show_pemesanan(4) 
    root_test.mainloop()
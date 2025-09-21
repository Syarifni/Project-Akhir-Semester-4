import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def tampilkan_struk(data_pesanan, item_list):
    """
    Menampilkan struk pesanan dalam jendela Tkinter dengan format teks yang rapi.

    Args:
        data_pesanan (dict): Kamus berisi detail pesanan global (id_pesanan, nama_pelanggan,
                             total, metode_pembayaran, status_pembayaran, diskon, pajak, tanggal).
                             Bisa juga mencakup 'jumlah_bayar' dan 'kembalian' dari modul pembayaran.
        item_list (list): Daftar kamus, setiap kamus berisi detail item pesanan
                          (nama, qty, harga_satuan, subtotal).
    """
    struk_win = tk.Toplevel()
    struk_win.title(f"Struk Pesanan #{data_pesanan.get('id_pesanan', 'N/A')}")
    struk_win.geometry("400x700") # Sesuaikan ukuran jendela
    struk_win.resizable(False, False)
    struk_win.configure(bg="#ffffff")

    canvas = tk.Canvas(struk_win, bg="#ffffff")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(struk_win, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

    struk_frame = tk.Frame(canvas, bg="#ffffff", padx=20, pady=20)
    canvas.create_window((0, 0), window=struk_frame, anchor="nw")

    # --- Generate Struk Lines ---
    lines = []
    
    # Header
    lines.append("        CAFE FLOOR JAYA SELALU")
    lines.append("      Jl. Gatot Subroto, Bengkalis")
    lines.append("         Telp: 0823-9024-7313")
    lines.append("=" * 38)

    # Detail Pesanan
    tanggal_obj = data_pesanan.get("tanggal", datetime.now())
    display_date = tanggal_obj.strftime("%d/%m/%Y %H:%M:%S")

    lines.append(f"Tanggal   : {display_date}")
    lines.append(f"ID Pesanan: {data_pesanan.get('id_pesanan', 'N/A')}")
    lines.append(f"Pelanggan : {data_pesanan.get('nama_pelanggan', 'Anonim')}")
    lines.append("-" * 38)

    # Item Header
    lines.append(f"{'Item':<15}{'Qty':>4}{'Harga':>9}{'Total':>10}")
    lines.append("-" * 38)

    # Item List
    for item in item_list:
        try:
            nama = item.get('nama', '')
            qty = int(item.get('qty', 0))
            harga = float(item.get('harga_satuan', 0.0))
            subtotal = float(item.get('subtotal', 0.0))
        except (ValueError, TypeError):
            # Ini akan dicetak ke konsol, tidak ke struk GUI
            print(f"Peringatan: Item struk dengan data tidak valid dilewati: {item}")
            continue
        
        # Format harga dan subtotal dengan pemisah ribuan
        formatted_harga = f"{int(harga):,}".replace(",", ".")
        formatted_subtotal = f"{int(subtotal):,}".replace(",", ".")

        # Potong nama jika terlalu panjang
        display_nama = (nama[:13] + '..') if len(nama) > 15 else nama
        lines.append(f"{display_nama:<15}{qty:>4}{formatted_harga:>9}{formatted_subtotal:>10}")

    lines.append("-" * 38)

    # Ringkasan Pembayaran
    if 'diskon' in data_pesanan and data_pesanan['diskon'] > 0:
        formatted_diskon = f"{int(data_pesanan['diskon']):,}".replace(",", ".")
        lines.append(f"{'Diskon':<15}{'-Rp' + formatted_diskon:>23}")
    if 'pajak' in data_pesanan and data_pesanan['pajak'] > 0:
        formatted_pajak = f"{int(data_pesanan['pajak']):,}".replace(",", ".")
        lines.append(f"{'Pajak':<15}{'+Rp' + formatted_pajak:>23}")

    total = int(data_pesanan.get("total", 0))
    formatted_total = f"{total:,}".replace(",", ".")
    lines.append(f"{'TOTAL BAYAR':<15}{'Rp' + formatted_total:>23}")
    
    lines.append(f"{'Metode Bayar':<15}{data_pesanan.get('metode_pembayaran', ''):>23}")
    lines.append(f"{'Status':<15}{data_pesanan.get('status_pembayaran', 'Belum Bayar'):>23}")

    # Detail pembayaran tambahan dari pembayaran.py
    jumlah_bayar = data_pesanan.get('jumlah_bayar') 
    if jumlah_bayar is not None:
        kembalian = data_pesanan.get('kembalian', 0)
        formatted_jumlah_bayar = f"{int(jumlah_bayar):,}".replace(",", ".")
        formatted_kembalian = f"{int(kembalian):,}".replace(",", ".")
        lines.append(f"{'Jumlah Bayar':<15}{'Rp' + formatted_jumlah_bayar:>23}")
        lines.append(f"{'Kembalian':<15}{'Rp' + formatted_kembalian:>23}")


    lines.append("=" * 38)
    lines.append("     TERIMA KASIH ATAS KUNJUNGAN")
    lines.append("      Simpan struk ini sebagai")
    lines.append("        bukti pembayaran")
    lines.append("") # Baris kosong di akhir


    # --- Display Lines in Tkinter ---
    # Menggunakan font Courier New agar spasi antar karakter konsisten
    # dan alignment sesuai dengan string formatting
    for line in lines:
        tk.Label(struk_frame, text=line, font=("Courier New", 10), bg="#ffffff", justify=tk.LEFT, anchor="w").pack(fill=tk.X)
    
    # --- Tombol Cetak ---
    def cetak_dokumen():
        messagebox.showinfo("Cetak Struk", "Fitur cetak (print) akan diimplementasikan di sini. Anda bisa menghubungkannya ke printer fisik.")

    cetak_button = tk.Button(struk_frame, text="Cetak Struk", command=cetak_dokumen, 
                             bg="#0d6efd", fg="white", font=("Segoe UI", 10, "bold"))
    cetak_button.pack(pady=15)

    struk_win.mainloop()

# Bagian ini hanya untuk pengujian modul secara terpisah
if __name__ == '__main__':
    root_test = tk.Tk()
    root_test.withdraw() # Sembunyikan jendela root utama
    
    # Contoh data pesanan (seperti dari pemesanan.py setelah insert)
    sample_data_pemesanan = {
        "id_pesanan": 101,
        "nama_pelanggan": "Pelanggan A",
        "total": 55000,
        "metode_pembayaran": "Tunai",
        "status_pembayaran": "Menunggu Pembayaran",
        "diskon": 0,
        "pajak": 0,
        "tanggal": datetime.now()
    }
    sample_items_pemesanan = [
        {"nama": "Kopi Latte", "qty": 2, "harga_satuan": 25000, "subtotal": 50000},
        {"nama": "Croissant", "qty": 1, "harga_satuan": 5000, "subtotal": 5000},
        {"nama": "Lemon Tea", "qty": 1, "harga_satuan": 15000, "subtotal": 15000}
    ]
    
    print("Menampilkan struk dari pemesanan (tanpa detail pembayaran)...")
    tampilkan_struk(sample_data_pemesanan, sample_items_pemesanan)

    # Contoh data pesanan (setelah pembayaran berhasil dari pembayaran.py)
    sample_data_pembayaran = {
        "id_pesanan": 102,
        "nama_pelanggan": "Pelanggan B",
        "total": 75000,
        "metode_pembayaran": "QRIS",
        "status_pembayaran": "Lunas",
        "diskon": 0,
        "pajak": 0,
        "jumlah_bayar": 80000, # Tambahan dari pembayaran
        "kembalian": 5000,    # Tambahan dari pembayaran
        "tanggal": datetime.now()
    }
    sample_items_pembayaran = [
        {"nama": "Nasi Goreng", "qty": 1, "harga_satuan": 40000, "subtotal": 40000},
        {"nama": "Es Teh", "qty": 1, "harga_satuan": 10000, "subtotal": 10000},
        {"nama": "Brownies", "qty": 1, "harga_satuan": 25000, "subtotal": 25000},
        {"nama": "Air Mineral", "qty": 2, "harga_satuan": 5000, "subtotal": 10000}
    ]
    
    print("Menampilkan struk dari pembayaran (dengan detail pembayaran)...")
    tampilkan_struk(sample_data_pembayaran, sample_items_pembayaran)
    
    root_test.mainloop()
import tkinter as tk
from tkinter import messagebox

from laporan_penjualan import show_laporan_penjualan
from laporan_pengeluaran import show_laporan_pengeluaran
from laporan_menu import show_laporan_menu
from pantau_stok import pantau_stok
from peringatan_stok import tampilkan_peringatan_stok
from analisis_produk import analisis_produk
from laporan_keuangan import show_laporan_keuangan

def main(user_name, user_id): # Signature fungsi sudah benar
    root = tk.Tk()
    root.title("Dashboard Pemilik")
    root.geometry("800x700")
    root.configure(bg="#e9fbe5")
    root.resizable(True, True)

    # ==== HEADER ====
    tk.Label(root, text="DASHBOARD PEMILIK", font=("Segoe UI", 24, "bold"),
             bg="#198754", fg="white", pady=20).pack(fill=tk.X)

    # PERUBAHAN DI SINI: Menampilkan user_name
    tk.Label(root, text=f"Login sebagai : Pemilik ({user_name}, (ID: {user_id}))", font=("Segoe UI", 12),
             bg="#e9fbe5", fg="#333").pack(pady=(10, 5))

    # ==== FRAME TOMBOL ====
    frame = tk.Frame(root, bg="#e9fbe5")
    frame.pack(pady=10)

    # ==== TOMBOL FUNGSI ====
    def create_button(text, command, color="#198754"):
        return tk.Button(
            frame, text=text, command=command,
            bg=color, fg="white",
            font=("Segoe UI", 12, "bold"),
            width=25, height=2,
            relief="flat", bd=0
        )

    # ==== DATA TOMBOL ====
    buttons = [
        ("Laporan Penjualan", show_laporan_penjualan, "#829707"),
        ("Laporan Pengeluaran", show_laporan_pengeluaran, "#dc3545"),
        ("Laporan Menu", show_laporan_menu, "#fd7e14"),
        ("Pantau Stok", pantau_stok, "#20c997"),
        ("Peringatan Stok", tampilkan_peringatan_stok, "#6f42c1"),
        ("Analisis Produk", analisis_produk, "#0d6efd"),
        ("Laporan Keuangan", show_laporan_keuangan, "#343a40")
    ]

    # ==== GRIDING TOMBOL ====
    for idx, (label, func, color) in enumerate(buttons):
        row = idx // 2
        col = idx % 2
        create_button(label, func, color).grid(row=row, column=col, padx=10, pady=10)

    # ==== LOGOUT BUTTON ====
    def logout():
        if messagebox.askyesno("Logout", "Yakin ingin logout?"):
            root.destroy()
            from login import show_login
            from __main__ import on_login_success
            show_login(on_login_success)

    tk.Button(
        root, text="Logout", command=logout,
        bg="#dc3545", fg="white",
        font=("Segoe UI", 12, "bold"),
        width=20, height=2,
        relief="flat", bd=0
    ).pack(pady=20)

    # ==== EXIT (X) WINDOW ====
    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy() if messagebox.askokcancel("Keluar", "Yakin ingin keluar?") else None)
    root.mainloop()

# ==== Pemanggilan awal login ====
if __name__ == "__main__":
    from login import show_login

    def after_login(peran, user_id):
        if peran == "pemilik":
            main(user_id)
        else:
            messagebox.showerror("Akses Ditolak", "Hanya kasir yang bisa mengakses dashboard ini.")

    show_login(after_login)

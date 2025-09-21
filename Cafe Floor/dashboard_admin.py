import tkinter as tk
from tkinter import messagebox

from manajemen_menu import show_manajemen_menu
from manajemen_pengguna import kelola_pengguna
from laporan_menu import show_laporan_menu
from laporan_penjualan import show_laporan_penjualan
from laporan_pengeluaran import show_laporan_pengeluaran
from peringatan_stok import tampilkan_peringatan_stok
from lihat_transaksi import lihat_transaksi_kasir

def main(user_name, user_id):
    root = tk.Tk()
    root.title("Dashboard Admin")
    root.geometry("800x600")
    root.configure(bg="#e9fbe5")
    root.resizable(True, True)

    tk.Label(root, text="DASHBOARD ADMIN", font=("Segoe UI", 24, "bold"),
             bg="#198754", fg="white", pady=20).pack(fill=tk.X)

    # PERUBAHAN DI SINI: Menampilkan user_name
    tk.Label(root, text=f"Login sebagai : Admin ({user_name}, (ID: {user_id}))", font=("Segoe UI", 12),
             bg="#e9fbe5", fg="#333").pack(pady=(10, 5))

    # ==== Frame untuk tombol grid ====
    frame = tk.Frame(root, bg="#e9fbe5")
    frame.pack(pady=10)

    def create_button(text, command, color="#198754"):
        return tk.Button(
            frame, text=text, command=command,
            bg=color, fg="white",
            font=("Segoe UI", 12, "bold"),
            width=30, height=2,
            relief="flat", bd=0
        )

    buttons = [
        ("Manajemen Menu", show_manajemen_menu, "#6EF8B8"),
        ("Manajemen Pengguna", kelola_pengguna, "#842029"),
        ("Laporan Menu", show_laporan_menu, "#04eeff"),
        ("Laporan Penjualan", show_laporan_penjualan, "#fd7e14"),
        ("Laporan Pengeluaran", show_laporan_pengeluaran, "#ffc107"),
        ("Peringatan Stok", tampilkan_peringatan_stok, "#0d6efd")
    ]

    for index, (label, func, color) in enumerate(buttons):
        row = index // 2
        col = index % 2
        create_button(label, func, color).grid(row=row, column=col, padx=10, pady=10)

    # ==== Tombol dalam 2 kolom ====
    buttons = [
        ("Manajemen Menu", show_manajemen_menu, "#E74FCE"),
        ("Manajemen Pengguna", kelola_pengguna, "#20c997"),
        ("Lihat Transaksi", lihat_transaksi_kasir, "#6f42c1"),
        ("Laporan Menu", show_laporan_menu, "#04eeff"),
        ("Laporan Penjualan", show_laporan_penjualan, "#fd7e14"),
        ("Laporan Pengeluaran", show_laporan_pengeluaran, "#ffc107"),
        ("Peringatan Stok", tampilkan_peringatan_stok, "#0d6efd")
    ]

    for index, (label, func, color) in enumerate(buttons):
        row = index // 2
        col = index % 2
        create_button(label, func, color).grid(row=row, column=col, padx=10, pady=10)

    # ==== Tombol Logout di bawah ====
    def logout():
        if messagebox.askyesno("Logout", "Yakin ingin logout?"):
            root.destroy()
            from login import show_login
            from __main__ import on_login_success
            show_login(on_login_success)

    logout_btn = tk.Button(root, text="Logout", command=logout,
                           bg="#dc3545", fg="white", font=("Segoe UI", 12, "bold"),
                           width=20, height=2, relief="flat", bd=0)
    logout_btn.pack(pady=20)

    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy() if messagebox.askokcancel("Keluar", "Yakin ingin keluar?") else None)
    root.mainloop()

# ==== Pemanggilan awal login ====
if __name__ == "__main__":
    from login import show_login

    def after_login(peran, user_id):
        if peran == "admin":
            main(user_id)
        else:
            messagebox.showerror("Akses Ditolak", "Hanya admin yang bisa mengakses dashboard ini.")

    show_login(after_login)
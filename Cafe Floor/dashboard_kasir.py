import tkinter as tk
from tkinter import messagebox

from pesanan_masuk import lihat_pesanan_kasir
from cetak_ulang_struk import cetak_ulang_struk_kasir
from lihat_transaksi import lihat_transaksi_kasir
from laporan_menu import show_laporan_menu
from laporan_penjualan import show_laporan_penjualan

def main(user_name, user_id):
    root = tk.Tk()
    root.title("Dashboard Kasir")
    root.geometry("700x700")
    root.configure(bg="#e9fbe5")
    root.resizable(True, True)

    tk.Label(root, text="DASHBOARD KASIR", font=("Segoe UI", 24, "bold"),
             bg="#198754", fg="white", pady=20).pack(fill=tk.X)

    tk.Label(root, text=f"Login sebagai : Kasir ({user_name}, (ID: {user_id}))", font=("Segoe UI", 12),
             bg="#e9fbe5", fg="#333").pack(pady=(10, 5))


    frame = tk.Frame(root, bg="#e9fbe5")
    frame.pack(pady=20)

    def create_button(text, command, color="#198754"):
        return tk.Button(
            frame, text=text, command=command,
            bg=color, fg="white",
            font=("Segoe UI", 12, "bold"),
            width=30, height=2,
            relief="flat", bd=0
        )

    create_button("Pesanan Masuk", lihat_pesanan_kasir, "#6EF8B8").pack(pady=8)
    create_button("Cetak Ulang Struk", cetak_ulang_struk_kasir, "#f390ee").pack(pady=8)
    create_button("Lihat Transaksi", lihat_transaksi_kasir, "#20c997").pack(pady=8)
    create_button("Laporan Menu", show_laporan_menu, "#fd7e14").pack(pady=8)
    create_button("Laporan Penjualan", show_laporan_penjualan, "#ffc107").pack(pady=8)

    def logout():
        if messagebox.askyesno("Logout", "Yakin ingin logout?"):
            root.destroy()
            from login import show_login
            from __main__ import on_login_success
            show_login(on_login_success)

    create_button("Logout", logout, "#dc3545").pack(pady=20)

    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy() if messagebox.askokcancel("Keluar", "Yakin ingin keluar?") else None)
    root.mainloop()

# ==== Pemanggilan awal login ====
if __name__ == "__main__":
    from login import show_login

    def after_login(peran, user_id):
        if peran == "kasir":
            main(user_id)
        else:
            messagebox.showerror("Akses Ditolak", "Hanya kasir yang bisa mengakses dashboard ini.")

    show_login(after_login)
import tkinter as tk
from tkinter import messagebox
from lihat_menu import lihat_menu_pelanggan
from pemesanan import show_pemesanan
from riwayat_pesanan import show_riwayat_pesanan
from pembayaran import show_pembayaran


def main(user_name, user_id): 
    root = tk.Tk()
    root.title("Dashboard Pelanggan")
    root.geometry("600x750")  
    root.configure(bg="#e8f5e9")
    root.resizable(True, True)

    # ========== Header ==========
    tk.Label(root, text="DASHBOARD PELANGGAN", font=("Segoe UI", 26, "bold"),
             bg="#198754", fg="white", pady=25).pack(fill=tk.X)

    # ========== Info Login ==========
    # PERUBAHAN DI SINI: Menampilkan user_name
    tk.Label(root, text=f"Login sebagai : {user_name}, (ID: {user_id}))", font=("Segoe UI", 13),
             bg="#e8f5e9", fg="#333").pack(pady=(10, 20))

    # ========== Fungsi Membuat Tombol ==========
    def create_button(text, command, color="#198754"):
        return tk.Button(
            root, text=text, command=command,
            font=("Segoe UI", 12, "bold"), bg=color, fg="white",
            width=30, height=2, relief="flat", bd=0,
            activebackground=color
        )

    # ========== Tombol Fitur ==========
    create_button("Lihat Menu", lihat_menu_pelanggan, color="#20c997").pack(pady=8)
    create_button("Pemesanan", lambda: show_pemesanan(user_id), color="#6f42c1").pack(pady=8)
    create_button("Riwayat Pesanan", lambda: show_riwayat_pesanan(user_id), color="#fd7e14").pack(pady=8)
    create_button("Pembayaran", lambda: show_pembayaran(user_id), color="#ffc107").pack(pady=8)

    # ========== Logout ==========
    def logout():
        if messagebox.askyesno("Logout", "Yakin ingin logout?"):
            root.destroy()
            from login import show_login
            from __main__ import on_login_success
            show_login(on_login_success)

    create_button("Logout", logout, color="#dc3545").pack(pady=20)

    # ========== Konfirmasi Saat Klik X ==========
    def on_exit():
        if messagebox.askokcancel("Keluar", "Yakin ingin keluar?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_exit)
    root.mainloop()

# ==== Pemanggilan awal login ====
if __name__ == "__main__":
    from login import show_login

    def after_login(peran, user_id):
        if peran == "pelanggan":
            main(user_id)
        else:
            messagebox.showerror("Akses Ditolak", "Hanya kasir yang bisa mengakses dashboard ini.")

    show_login(after_login)
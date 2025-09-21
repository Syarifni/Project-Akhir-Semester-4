import tkinter as tk
from tkinter import messagebox
from login import show_login
from dashboard_admin import main as show_admin_dashboard
from dashboard_kasir import main as show_kasir_dashboard
from dashboard_pemilik import main as show_pemilik_dashboard
from dashboard_pelanggan import main as show_pelanggan_dashboard

# Fungsi yang dipanggil setelah login berhasil
def on_login_success(peran, user_name, user_id):
    if peran == "admin":
        show_admin_dashboard(user_name, user_id) 
    elif peran == "kasir":
        show_kasir_dashboard(user_name, user_id) 
    elif peran == "pemilik":
        show_pemilik_dashboard(user_name, user_id) 
    elif peran == "pelanggan":
        show_pelanggan_dashboard(user_name, user_id) 
    else:
        messagebox.showerror("Error Peran", "Peran pengguna tidak dikenali. Silakan hubungi administrator.")

# Panggil fungsi show_login untuk memulai aplikasi
show_login(on_login_success)
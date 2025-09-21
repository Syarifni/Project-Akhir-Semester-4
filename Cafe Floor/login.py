# login.py
import tkinter as tk
from tkinter import messagebox
from koneksi import connect_db 
import hashlib

def show_login(on_login_success_callback):
    win = tk.Tk()
    win.title("LOGIN - CAFE FLOOR")
    win.geometry("360x480")
    win.configure(bg="#f8f9fa")
    win.resizable(True, True) 

    # Header
    header = tk.Label(
        win, text="CAFE FLOOR", font=("Segoe UI", 22, "bold"),
        bg="#198754", fg="white", pady=15
    )
    header.pack(fill=tk.X, pady=(0, 10))

    subheader = tk.Label(
        win, text="Silakan Login", font=("Segoe UI", 14),
        bg="#f8f9fa", fg="#333"
    )
    subheader.pack()

    # Frame Form Login
    form_frame = tk.Frame(win, bg="#f8f9fa")
    form_frame.pack(pady=40)

    # Username
    tk.Label(form_frame, text="Username", font=("Segoe UI", 12), bg="#f8f9fa").grid(row=0, column=0, sticky="w", pady=(0, 5))
    username_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=30)
    username_entry.grid(row=1, column=0, pady=(0, 20))

    # Password
    tk.Label(form_frame, text="Password", font=("Segoe UI", 12), bg="#f8f9fa").grid(row=2, column=0, sticky="w", pady=(0, 5))
    password_entry = tk.Entry(form_frame, show="*", font=("Segoe UI", 12), width=30)
    password_entry.grid(row=3, column=0, pady=(0, 20))

    # Fungsi Login
    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Validasi", "Harap isi username dan password.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = None 
        try:
            conn = connect_db() 
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id_pengguna, username, id_role FROM pengguna WHERE username=%s AND password=%s",
                (username, hashed_password)
            )
            result = cursor.fetchone()
            
            if result:
                user_id_from_db, user_name, role_id = result
                role_map = {1: "admin", 2: "kasir", 3: "pemilik", 4: "pelanggan"}
                peran = role_map.get(role_id, "pelanggan")
                win.destroy() # Tutup jendela login
                on_login_success_callback(peran, user_name, user_id_from_db) 
            else: 
                messagebox.showerror("Login Gagal", "Username atau password salah.")
        except Exception as e:
            # Ini akan menangkap error dari connect_db() atau error database lainnya
            messagebox.showerror("Error Koneksi/Login", f"Gagal koneksi database atau query error:\n{e}")
        finally:
            if conn:
                conn.close() # Pastikan koneksi ditutup

    # Tombol Login
    login_btn = tk.Button(
        form_frame, text="Login", font=("Segoe UI", 12, "bold"),
        bg="#198754", fg="white", width=25, height=2, command=login
    )
    login_btn.grid(row=4, column=0, pady=10)

    # Footer
    footer = tk.Label(
        win, text="© 2025 Cafe Floor App", font=("Segoe UI", 9),
        bg="#f8f9fa", fg="#888"
    )
    footer.pack(side=tk.BOTTOM, pady=10)

    win.mainloop()
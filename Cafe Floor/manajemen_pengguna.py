import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def kelola_pengguna():
    win = tk.Toplevel()
    win.title("Manajemen Pengguna & Hak Akses")
    win.geometry("850x630")
    win.configure(bg="#f8f9fa")

    # HEADER 
    tk.Label(win, text="MANAJEMEN PENGGUNA & HAK AKSES", font=("Segoe UI", 18, "bold"),
             bg="#198754", fg="white", pady=12).pack(fill=tk.X)

    # TABEL PENGGUNA
    pengguna_frame = tk.LabelFrame(win, text="Daftar Pengguna", bg="#f8f9fa", font=("Segoe UI", 11, "bold"))
    pengguna_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=(15, 5))

    tree = ttk.Treeview(pengguna_frame, columns=("id", "username", "role"), show="headings", height=8)
    tree.heading("id", text="ID")
    tree.heading("username", text="Username")
    tree.heading("role", text="Role")
    for col, w in zip(("id", "username", "role"), (50, 200, 150)):
        tree.column(col, width=w, anchor="center")
    tree.pack(padx=10, pady=5, fill=tk.X)

    # FORM TAMBAH/EDIT
    form_frame = tk.LabelFrame(win, text="Form Pengguna", bg="#f8f9fa", font=("Segoe UI", 11, "bold"))
    form_frame.pack(fill=tk.X, padx=10, pady=(5, 10))

    def form_label(entry_text, row):
        tk.Label(form_frame, text=entry_text, bg="#f8f9fa", font=("Segoe UI", 10)).grid(
            row=row, column=0, padx=5, pady=5, sticky="e"
        )

    form_label("Username:", 0)
    username_entry = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    form_label("Password:", 1)
    password_entry = tk.Entry(form_frame, font=("Segoe UI", 10), show="*", width=30)
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    form_label("Role:", 2)
    role_combo = ttk.Combobox(form_frame, font=("Segoe UI", 10), state="readonly", width=28)
    role_combo.grid(row=2, column=1, padx=5, pady=5)

    btn_simpan = tk.Button(form_frame, text="Tambah Pengguna", font=("Segoe UI", 10, "bold"),
                           bg="#198754", fg="white", width=30)
    btn_simpan.grid(row=3, column=0, columnspan=2, pady=10)

    # FUNGSI PENGGUNA
    def reset_form():
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        role_combo.set("")
        btn_simpan.config(text="Tambah Pengguna", command=tambah_pengguna)

    def load_role():
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
            cursor = conn.cursor()
            cursor.execute("SELECT nama_role FROM role")
            roles = [r[0] for r in cursor.fetchall()]
            role_combo["values"] = roles
            if roles: role_combo.current(0)
            conn.close()
        except Exception as e:
            messagebox.showerror("Gagal Ambil Role", str(e))

    def load_pengguna():
        tree.delete(*tree.get_children())
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
            cursor = conn.cursor()
            cursor.execute("SELECT u.id_pengguna, u.username, r.nama_role FROM pengguna u JOIN role r ON u.id_role = r.id_role")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Gagal Load Pengguna", str(e))

    def tambah_pengguna():
        uname = username_entry.get().strip()
        pwd = password_entry.get()
        role = role_combo.get()
        if not uname or not pwd or not role:
            return messagebox.showwarning("Input", "Lengkapi semua data!")
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
            cursor = conn.cursor()
            cursor.execute("SELECT id_role FROM role WHERE nama_role=%s", (role,))
            id_role = cursor.fetchone()[0]
            cursor.execute("INSERT INTO pengguna (username, password, id_role) VALUES (%s, %s, %s)", (uname, pwd, id_role))
            conn.commit()
            conn.close()
            load_pengguna()
            reset_form()
            messagebox.showinfo("Berhasil", "Pengguna berhasil ditambahkan.")
        except Exception as e:
            messagebox.showerror("Gagal Tambah", str(e))

    def edit_pengguna():
        selected = tree.focus()
        if not selected:
            return messagebox.showwarning("Pilih", "Pilih data yang akan diedit.")
        row = tree.item(selected)["values"]
        pengguna_id, uname, role = row
        username_entry.delete(0, tk.END)
        username_entry.insert(0, uname)
        role_combo.set(role)

        def simpan_edit():
            new_uname = username_entry.get().strip()
            new_pwd = password_entry.get()
            new_role = role_combo.get()
            if not new_uname or not new_role:
                return messagebox.showwarning("Input", "Lengkapi semua data!")
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
                cursor = conn.cursor()
                cursor.execute("SELECT id_role FROM role WHERE nama_role=%s", (new_role,))
                id_role = cursor.fetchone()[0]
                if new_pwd:
                    cursor.execute("UPDATE pengguna SET username=%s, password=%s, id_role=%s WHERE id_pengguna=%s",
                                   (new_uname, new_pwd, id_role, pengguna_id))
                else:
                    cursor.execute("UPDATE pengguna SET username=%s, id_role=%s WHERE id_pengguna=%s",
                                   (new_uname, id_role, pengguna_id))
                conn.commit()
                conn.close()
                load_pengguna()
                reset_form()
                messagebox.showinfo("Berhasil", "Data pengguna diperbarui.")
            except Exception as e:
                messagebox.showerror("Gagal Edit", str(e))

        btn_simpan.config(text="Simpan Perubahan", command=simpan_edit)

    def hapus_pengguna():
        selected = tree.focus()
        if not selected:
            return messagebox.showwarning("Pilih", "Pilih data untuk dihapus.")
        pengguna_id = tree.item(selected)["values"][0]
        if messagebox.askyesno("Konfirmasi", "Hapus pengguna ini?"):
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pengguna WHERE id_pengguna=%s", (pengguna_id,))
                conn.commit()
                conn.close()
                load_pengguna()
                messagebox.showinfo("Sukses", "Pengguna dihapus.")
            except Exception as e:
                messagebox.showerror("Gagal", str(e))

    btn_frame = tk.Frame(win, bg="#f8f9fa")
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Edit", font=("Segoe UI", 10, "bold"), bg="#ffc107", command=edit_pengguna).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Hapus", font=("Segoe UI", 10, "bold"), bg="#dc3545", fg="white", command=hapus_pengguna).pack(side=tk.LEFT, padx=5)

    # HAK AKSES
    akses_frame = tk.LabelFrame(win, text="Manajemen Hak Akses", bg="#f8f9fa", font=("Segoe UI", 11, "bold"))
    akses_frame.pack(fill=tk.BOTH, padx=10, pady=10)

    tree_akses = ttk.Treeview(akses_frame, columns=("id", "nama"), show="headings", height=5)
    tree_akses.heading("id", text="ID")
    tree_akses.heading("nama", text="Nama Role")
    tree_akses.column("id", width=60, anchor="center")
    tree_akses.column("nama", width=200, anchor="center")
    tree_akses.pack(padx=10, pady=5, fill=tk.X)

    entry_role = tk.Entry(akses_frame, font=("Segoe UI", 10), width=25)
    entry_role.pack(pady=5, side=tk.LEFT, padx=10)

    def load_hak_akses():
        tree_akses.delete(*tree_akses.get_children())
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
            cursor = conn.cursor()
            cursor.execute("SELECT id_role, nama_role FROM role")
            for row in cursor.fetchall():
                tree_akses.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Gagal", str(e))

    def tambah_role():
        nama_role = entry_role.get().strip()
        if not nama_role:
            return messagebox.showwarning("Input", "Masukkan nama role.")
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO role (nama_role) VALUES (%s)", (nama_role,))
            conn.commit()
            conn.close()
            entry_role.delete(0, tk.END)
            load_hak_akses()
            load_role()
            messagebox.showinfo("Sukses", "Role berhasil ditambahkan.")
        except Exception as e:
            messagebox.showerror("Gagal", str(e))

    def edit_role():
        selected = tree_akses.focus()
        if not selected:
            return messagebox.showwarning("Pilih", "Pilih role untuk diedit.")
        role_id, nama_role = tree_akses.item(selected)["values"]
        entry_role.delete(0, tk.END)
        entry_role.insert(0, nama_role)

        def simpan_role():
            new_name = entry_role.get().strip()
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
                cursor = conn.cursor()
                cursor.execute("UPDATE role SET nama_role=%s WHERE id_role=%s", (new_name, role_id))
                conn.commit()
                conn.close()
                load_hak_akses()
                load_role()
                entry_role.delete(0, tk.END)
                btn_role.config(text="Tambah Role", command=tambah_role)
                messagebox.showinfo("Berhasil", "Role diperbarui.")
            except Exception as e:
                messagebox.showerror("Gagal", str(e))

        btn_role.config(text="Simpan Role", command=simpan_role)

    def hapus_role():
        selected = tree_akses.focus()
        if not selected:
            return messagebox.showwarning("Pilih", "Pilih role yang akan dihapus.")
        role_id = tree_akses.item(selected)["values"][0]
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus role ini?"):
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="", database="cafe_floor")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM role WHERE id_role=%s", (role_id,))
                conn.commit()
                conn.close()
                load_hak_akses()
                load_role()
                messagebox.showinfo("Berhasil", "Role berhasil dihapus.")
            except Exception as e:
                messagebox.showerror("Gagal", str(e))

    btn_role = tk.Button(akses_frame, text="Tambah Role", font=("Segoe UI", 10), bg="#0d6efd", fg="white", command=tambah_role)
    btn_role.pack(pady=5, side=tk.LEFT)
    tk.Button(akses_frame, text="Edit", font=("Segoe UI", 10), bg="#ffc107", command=edit_role).pack(pady=5, side=tk.LEFT, padx=5)
    tk.Button(akses_frame, text="Hapus", font=("Segoe UI", 10), bg="#dc3545", fg="white", command=hapus_role).pack(pady=5, side=tk.LEFT, padx=5)

    # LOAD SEMUA
    load_pengguna()
    load_role()
    load_hak_akses()
    win.mainloop()
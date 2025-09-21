import tkinter as tk
from tkinter import ttk, messagebox
from koneksi import connect_db

def show_manajemen_menu():
    win = tk.Toplevel()
    win.title("Manajemen Menu")
    win.geometry("750x550")
    win.configure(bg="#e9fbe5")

    # Header
    tk.Label(win, text="Manajemen Menu", font=("Segoe UI", 20, "bold"),
             bg="#198754", fg="white", pady=10).pack(fill=tk.X)

    # Form Input
    form = tk.LabelFrame(win, text="Form Tambah / Edit Menu", font=("Segoe UI", 12, "bold"),
                         bg="#e9fbe5", padx=15, pady=10)
    form.pack(padx=20, pady=15, fill=tk.X)

    tk.Label(form, text="Nama Menu", bg="#e9fbe5", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
    nama_entry = tk.Entry(form, font=("Segoe UI", 11), width=30)
    nama_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form, text="Harga", bg="#e9fbe5", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w")
    harga_entry = tk.Entry(form, font=("Segoe UI", 11), width=20)
    harga_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(form, text="Kategori", bg="#e9fbe5", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w")
    kategori_combo = ttk.Combobox(form, values=["makanan berat", "minuman", "cemilan"],
                                  font=("Segoe UI", 11), width=27)
    kategori_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    def reset_form():
        nama_entry.delete(0, tk.END)
        harga_entry.delete(0, tk.END)
        kategori_combo.set("")

    def simpan_menu():
        nama = nama_entry.get().strip()
        harga = harga_entry.get().strip()
        kategori = kategori_combo.get()

        if not nama or not harga or not kategori:
            messagebox.showwarning("Validasi", "Harap lengkapi semua data!")
            return

        try:
            harga = float(harga)
        except:
            messagebox.showwarning("Validasi", "Harga harus berupa angka!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO menu (nama_menu, harga, kategori) VALUES (%s, %s, %s)",
                           (nama, harga, kategori))
            conn.commit()
            messagebox.showinfo("Berhasil", "Menu berhasil ditambahkan")
            reset_form()
            load_data()
        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal menambahkan menu:\n{e}")
        finally:
            conn.close()

    simpan_btn = tk.Button(form, text="Simpan Menu", command=simpan_menu,
                           font=("Segoe UI", 11, "bold"), bg="#198754", fg="white", width=20)
    simpan_btn.grid(row=3, column=0, columnspan=2, pady=15)

    # Tabel 
    tabel_frame = tk.LabelFrame(win, text="Daftar Menu", font=("Segoe UI", 12, "bold"),
                                bg="#e9fbe5", padx=10, pady=10)
    tabel_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

    table = ttk.Treeview(tabel_frame, columns=("id_menu", "nama_menu", "harga", "kategori"), show="headings")
    table.heading("id_menu", text="ID")
    table.heading("nama_menu", text="Nama Menu")
    table.heading("harga", text="Harga")
    table.heading("kategori", text="Kategori")

    for col in table["columns"]:
        table.column(col, anchor="center", width=150)
    table.pack(fill=tk.BOTH, expand=True)

    def load_data():
        for row in table.get_children():
            table.delete(row)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_menu, nama_menu, harga, kategori FROM menu")
            for row in cursor.fetchall():
                table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def hapus_menu():
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Pilih", "Pilih menu yang ingin dihapus.")
            return
        item = table.item(selected[0])
        menu_id = item["values"][0]
        if messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus menu '{item['values'][1]}'?"):
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM menu WHERE id_menu = %s", (menu_id,))
                conn.commit()
                load_data()
                messagebox.showinfo("Berhasil", "Menu berhasil dihapus.")
            except Exception as e:
                messagebox.showerror("Gagal", str(e))
            finally:
                conn.close()

    def edit_menu():
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Pilih", "Pilih menu yang ingin diedit.")
            return
        item = table.item(selected[0])
        menu_id, nama, harga, kategori = item["values"]

        nama_entry.delete(0, tk.END)
        nama_entry.insert(0, nama)
        harga_entry.delete(0, tk.END)
        harga_entry.insert(0, harga)
        kategori_combo.set(kategori)

        def simpan_edit():
            new_nama = nama_entry.get().strip()
            new_harga = harga_entry.get().strip()
            new_kategori = kategori_combo.get()

            if not new_nama or not new_harga or not new_kategori:
                messagebox.showwarning("Validasi", "Harap lengkapi semua data!")
                return

            try:
                new_harga = float(new_harga)
            except:
                messagebox.showwarning("Validasi", "Harga harus berupa angka!")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE menu 
                    SET nama_menu=%s, harga=%s, kategori=%s 
                    WHERE id_menu=%s
                """, (new_nama, new_harga, new_kategori, menu_id))
                conn.commit()
                messagebox.showinfo("Berhasil", "Menu berhasil diperbarui")
                reset_form()
                load_data()
                simpan_btn.config(command=simpan_menu, text="Simpan Menu")
            except Exception as e:
                messagebox.showerror("Gagal", str(e))
            finally:
                conn.close()

        simpan_btn.config(command=simpan_edit, text="Simpan Perubahan")

    # Tombol Edit / Hapus
    btn_frame = tk.Frame(win, bg="#e9fbe5")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Edit Menu", bg="#ffc107", font=("Segoe UI", 11, "bold"),
              width=15, command=edit_menu).pack(side=tk.LEFT, padx=10)

    tk.Button(btn_frame, text="Hapus Menu", bg="#dc3545", fg="white", font=("Segoe UI", 11, "bold"),
              width=15, command=hapus_menu).pack(side=tk.LEFT, padx=10)

    load_data()
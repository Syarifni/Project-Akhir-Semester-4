import mysql.connector
from tkinter import messagebox

def cek_stok_minimum():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cafe_floor"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nama_bahan, stok, batas_minimum 
            FROM bahan 
            WHERE stok <= batas_minimum
        """)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("Gagal cek stok minimum:", e)
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()

def tampilkan_peringatan_stok():
    data_stok = cek_stok_minimum()
    if data_stok:
        pesan = "Stok bahan berikut menipis:\n\n"
        for nama, stok, batas in data_stok:
            pesan += f"- {nama}: {stok} (Minimum: {batas})\n"
        messagebox.showwarning("Peringatan Stok Minimum", pesan)
    else:
        messagebox.showinfo("Stok Aman", "Semua bahan berada di atas batas minimum.")
import tkinter as tk
from tkinter import font, messagebox
from gui.ekle import filmdizi_ekle
from gui.arsiv import arsivim
from database_manager import DatabaseManager





def cikis_yap():
    messagebox.showinfo("Çıkış", "Program kapatılıyor, iyi günler :)")
    menü.destroy()

# Veritabanı bağlantısı
try:
    db = DatabaseManager(host="localhost", user="root", password="Burak416041.", database="film_dizi", port=3307)
    db.connect()
except Exception as e:
    messagebox.showerror("Veritabanı Hatası", f"Veritabanı bağlantısı kurulamadı: {e}")
    exit()

menü = tk.Tk()
menü.title("MENÜ")
menü.geometry("400x300")
menü.configure(bg="#121212")

for i in range(6):
    menü.grid_rowconfigure(i, weight=1)

menü.grid_columnconfigure(0, weight=1)

baslik = tk.Label(menü, text="Ana Menü", font=("Comic Sans MS", 30), bg="#121212", fg="#E50914")
baslik.grid(row=0, column=0, pady=10, sticky="n")

l1 = tk.Label(menü, text="Hoşgeldiniz, lütfen yapmak istediğiniz işlemi seçiniz.", 
              font=("Segoe UI", 9), bg="#121212", fg="white")
l1.grid(row=1, column=0, pady=5, sticky="n")

ortak_font = font.Font(family="Helvetica", size=9, weight="bold")

btnekleme = tk.Button(menü, text="Film/Dizi Ekle", width=20, height=2, fg="#ffffff", bg="#E50914", 
                      command=lambda: filmdizi_ekle(menü, db), font=ortak_font)
btnekleme.grid(row=2, column=0, pady=5)

btnoneri = tk.Button(menü, text="Önerilen Filmler/Diziler", width=20, height=2, fg="#ffffff", bg="#E50914", 
                     font=ortak_font)
btnoneri.grid(row=3, column=0, pady=5)

btnarsiv = tk.Button(menü, text="Filmlerim/Dizilerim", width=20, height=2, fg="#ffffff", bg="#E50914", 
                     command=lambda: arsivim(menü, db), font=ortak_font)
btnarsiv.grid(row=4, column=0, pady=5)

btncikis = tk.Button(menü, text="Çıkış", width=20, height=2, bg="#E50914", fg="#ffffff", 
                      command=cikis_yap, font=ortak_font)
btncikis.grid(row=5, column=0, pady=5)

menü.mainloop()

# Veritabanı bağlantısını kapat
if db:
    db.close()

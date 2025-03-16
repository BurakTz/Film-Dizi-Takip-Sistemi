import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import DatabaseManager

def silinenleri_goster(arsiv_penceresi, db):
    # Veritabanından silinen içerikleri çek
    silinen_icerikler = db.fetch_all("SELECT * FROM deleted_content")

    # Silinen içerik kontrolü
    if not silinen_icerikler:
        messagebox.showinfo("Bilgi", "Henüz hiçbir içerik silinmedi.")
        return

    # Arşiv penceresini gizle
    arsiv_penceresi.withdraw()

    # Yeni pencere oluştur
    silinen_pencere = tk.Toplevel()
    silinen_pencere.title("Silinen İçerikler")
    silinen_pencere.geometry("750x400")
    silinen_pencere.configure(bg="#121212")

    # Grid yapılandırması
    silinen_pencere.grid_rowconfigure(0, weight=1)  # Başlık için
    silinen_pencere.grid_rowconfigure(1, weight=1)  # Bilgilendirme etiketi için
    silinen_pencere.grid_rowconfigure(2, weight=8)  # Tablo için
    silinen_pencere.grid_rowconfigure(3, weight=1)  # Butonlar için
    silinen_pencere.grid_columnconfigure(0, weight=1)

    # Başlık
    baslik = tk.Label(
        silinen_pencere,
        text="Silinen İçerikler",
        font=("Comic Sans MS", 24, "bold"),
        bg="#121212",
        fg="#E50914"
    )
    baslik.grid(row=0, column=0, pady=10, sticky="n")

    # Bilgilendirme etiketi
    bilgi_etiketi = tk.Label(
        silinen_pencere,
        text="Silinenler listesi 1 hafta sonra otomatik silinir",
        font=("Helvetica", 10, "italic"),
        bg="#121212",
        fg="white"
    )
    bilgi_etiketi.grid(row=1, column=0, pady=5, sticky="n")

    # Tablo oluştur
    sütunlar = ("Ad", "Kategori", "Tür", "Süre", "Durum", "Yıldız", "Notlar")
    tree_silinen = ttk.Treeview(silinen_pencere, columns=sütunlar, show="headings")
    tree_silinen.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # Sütun başlıkları
    for sütun in sütunlar:
        tree_silinen.heading(sütun, text=sütun)
        tree_silinen.column(sütun, anchor="center", width=100)

    # Silinen içerikleri tabloya ekle
    for icerik in silinen_icerikler:
        tree_silinen.insert("", "end", values=(
            icerik["ad"], icerik["kategori"], icerik["tür"], icerik["süre"],
            icerik["durum"], icerik["yildiz"], icerik["notlar"]
        ))

    # Geri alma işlevi
    def geri_al():
        secilen = tree_silinen.selection()
        if not secilen:
            messagebox.showerror("Hata", "Lütfen geri almak için bir içerik seçiniz.")
            return

        sonuc = messagebox.askyesno(
            "Geri Alma Onayı",
            "Seçilen içerikleri geri almak istediğinize emin misiniz?"
        )
        if not sonuc:
            return

        for id in secilen:
            degerler = tree_silinen.item(id, "values")
            try:
                # Geri alınan kaydı ana tabloya ekle
                db.insert("content", {
                    "ad": degerler[0],
                    "kategori": degerler[1],
                    "tür": degerler[2],
                    "süre": degerler[3],
                    "durum": degerler[4],
                    "yildiz": degerler[5],
                    "notlar": degerler[6]
                })

                # Geri alınan kaydı silinen tablodan kaldır
                db.delete("deleted_content", {"ad": degerler[0]})
                tree_silinen.delete(id)

                messagebox.showinfo("Başarı", "Seçilen içerikler başarıyla geri alındı.")

            except Exception as e:
                messagebox.showerror("Hata", f"Geri alma işlemi başarısız: {e}")

    def tamamen_sil():
        secilen = tree_silinen.selection()
        if not secilen:
            messagebox.showerror("Hata", "Lütfen silmek için bir içerik seçiniz.")
            return

        sonuc = messagebox.askyesno(
            "Silme Onayı",
            "Seçilen içerikleri tamamen silmek istediğinize emin misiniz?"
        )
        if not sonuc:
            return

        for id in secilen:
            degerler = tree_silinen.item(id, "values")
            try:
                # Seçilen kayıtları tamamen sil
                db.delete("deleted_content", {"ad": degerler[0]})
                tree_silinen.delete(id)

                messagebox.showinfo("Başarı", "Seçilen içerikler başarıyla silindi.")

            except Exception as e:
                messagebox.showerror("Hata", f"Silme işlemi başarısız: {e}")

    # Geri alma butonu
    geri_al_buton = tk.Button(
        silinen_pencere,
        text="Geri Al",
        bg="#E50914",
        fg="white",
        font=("Helvetica", 10, "bold"),
        command=geri_al,
        width=15
    )
    geri_al_buton.grid(row=3, column=0, padx=10, pady=10, sticky="se")

    tamamen_sil_buton = tk.Button(
        silinen_pencere,
        text="Tamamen Sil",
        bg="#E50914",
        fg="white",
        font=("Helvetica", 10, "bold"),
        command=tamamen_sil,
        width=15
    )
    tamamen_sil_buton.grid(row=3, column=0, pady=10, sticky="s")

    # Geri dön işlevi
    def geri_don():
        silinen_pencere.destroy()
        arsiv_penceresi.deiconify()  # Arşiv penceresini tekrar göster

    # Geri dön butonu
    geri_buton = tk.Button(
        silinen_pencere,
        text="Arşive Dön",
        bg="#E50914",
        fg="white",
        font=("Helvetica", 10, "bold"),
        command=geri_don,
        width=15
    )
    geri_buton.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

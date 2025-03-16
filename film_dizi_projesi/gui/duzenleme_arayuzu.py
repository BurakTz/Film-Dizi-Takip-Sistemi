import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import DatabaseManager

def duzenleme_arayuzu(arsiv_penceresi, tree, db):
    # Seçili öğeyi al
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Hata", "Lütfen düzenlemek için bir içerik seçiniz.")
        return

    # Seçili öğenin değerlerini al
    item_values = tree.item(selected_item, "values")

    # Düzenleme penceresi oluştur
    duzenleme_penceresi = tk.Toplevel(arsiv_penceresi)
    duzenleme_penceresi.title("Düzenleme")
    duzenleme_penceresi.geometry("400x400")
    duzenleme_penceresi.configure(bg="#121212")

    # Ad düzenleme
    tk.Label(duzenleme_penceresi, text="Ad:", bg="#2C2C2C", fg="white", width=18, anchor="center", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=10, pady=10)
    ad_entry = tk.Entry(duzenleme_penceresi)
    ad_entry.grid(row=0, column=1, padx=10, pady=10)
    ad_entry.insert(0, item_values[0])

    # Tür düzenleme
    tk.Label(duzenleme_penceresi, text="Tür:", bg="#2C2C2C", fg="white", width=18, anchor="center", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=10, pady=10)
    tür_combobox = ttk.Combobox(duzenleme_penceresi, state="readonly", values=["Korku", "Komedi", "Dram", "Aksiyon", "Aşk", "Bilim Kurgu"])
    tür_combobox.grid(row=1, column=1, padx=10, pady=10)
    tür_combobox.set(item_values[1])

    # Kategori düzenleme
    tk.Label(duzenleme_penceresi, text="Kategori:", bg="#2C2C2C", fg="white", width=18, anchor="center", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=10, pady=10)
    kategori_combobox = ttk.Combobox(duzenleme_penceresi, state="readonly", values=["Film", "Dizi"])
    kategori_combobox.grid(row=2, column=1, padx=10, pady=10)
    kategori_combobox.set(item_values[2])

    # Süre düzenleme
    tk.Label(duzenleme_penceresi, text="Süre:", bg="#2C2C2C", fg="white", width=18, anchor="center", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=10, pady=10)
    sure_entry = tk.Entry(duzenleme_penceresi)
    sure_entry.grid(row=3, column=1, padx=10, pady=10)
    sure_entry.insert(0, item_values[3])

    # Durum düzenleme
    tk.Label(duzenleme_penceresi, text="Durum:", bg="#2C2C2C", fg="white", width=18, anchor="center", font=("Helvetica", 10, "bold")).grid(row=4, column=0, padx=10, pady=10)
    durum_combobox = ttk.Combobox(duzenleme_penceresi, state="readonly", values=["İzlenmedi", "İzleniyor", "İzlendi"])
    durum_combobox.grid(row=4, column=1, padx=10, pady=10)
    durum_combobox.set(item_values[4])

    # Yıldız düzenleme
    tk.Label(duzenleme_penceresi, text="Yıldız:", bg="#2C2C2C", fg="white", width=18, anchor="center", font=("Helvetica", 10, "bold")).grid(row=5, column=0, padx=10, pady=10)
    yildiz_combobox = ttk.Combobox(duzenleme_penceresi, state="readonly", values=[str(i) for i in range(1, 6)])
    yildiz_combobox.grid(row=5, column=1, padx=10, pady=10)
    yildiz_combobox.set(item_values[5])

    # Notlar düzenleme
    tk.Label(duzenleme_penceresi, text="Notlar:", bg="#2C2C2C", fg="white", width=18, anchor="center", font=("Helvetica", 10, "bold")).grid(row=6, column=0, padx=10, pady=10)
    notlar_entry = tk.Entry(duzenleme_penceresi)
    notlar_entry.grid(row=6, column=1, padx=10, pady=10)
    notlar_entry.insert(0, item_values[6])

    # Kaydet butonu
    def kaydet():
        yeni_veriler = {
            "ad": ad_entry.get(),
            "tür": tür_combobox.get(),
            "kategori": kategori_combobox.get(),
            "süre": sure_entry.get(),
            "durum": durum_combobox.get(),
            "yildiz": yildiz_combobox.get(),
            "notlar": notlar_entry.get()
        }

        try:
            # MySQL'de güncelleme yap
            db.update("content", yeni_veriler, {"ad": item_values[0]})
            # Treeview'de güncelle
            tree.item(selected_item, values=(
                yeni_veriler["ad"],
                yeni_veriler["tür"],
                yeni_veriler["kategori"],
                yeni_veriler["süre"],
                yeni_veriler["durum"],
                yeni_veriler["yildiz"],
                yeni_veriler["notlar"]
            ))
            messagebox.showinfo("Başarı", "Kayıt başarıyla güncellendi!")
            duzenleme_penceresi.destroy()
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt güncellenemedi: {e}")

    kaydet_buton = tk.Button(duzenleme_penceresi, text="Kaydet", command=kaydet, bg="#E50914", fg="white", width=15)
    kaydet_buton.grid(row=7, column=0, columnspan=2, pady=10)

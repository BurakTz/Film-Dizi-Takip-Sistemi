import tkinter as tk
from tkinter import ttk, messagebox
from gui.silinenler import silinenleri_goster
from gui.filtreleme_arayuzu import filtreleme_arayuzu
from gui.duzenleme_arayuzu import duzenleme_arayuzu
from database_manager import DatabaseManager

def duzenleme_arayuzu(arsiv_penceresi, tree, db):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Hata", "Lütfen düzenlemek için bir içerik seçiniz.")
        return

    item_values = tree.item(selected_item, "values")

    duzenleme_penceresi = tk.Toplevel(arsiv_penceresi)
    duzenleme_penceresi.title("Düzenleme")
    duzenleme_penceresi.geometry("400x400")
    duzenleme_penceresi.configure(bg="#121212")

    def create_label_and_entry(row, label_text, default_value, options=None):
        tk.Label(
            duzenleme_penceresi,
            text=label_text,
            bg="#2C2C2C",
            fg="white",
            width=18,
            anchor="center",
            font=("Helvetica", 10, "bold")
        ).grid(row=row, column=0, padx=10, pady=10)

        if options:
            entry_widget = ttk.Combobox(
                duzenleme_penceresi,
                state="readonly",
                values=options
            )
            entry_widget.set(default_value)
        else:
            entry_widget = tk.Entry(duzenleme_penceresi)
            entry_widget.insert(0, default_value)

        entry_widget.grid(row=row, column=1, padx=10, pady=10)
        return entry_widget

    ad_entry = create_label_and_entry(0, "Ad:", item_values[0])
    tür_combobox = create_label_and_entry(1, "Tür:", item_values[1], ["Korku", "Komedi", "Dram", "Aksiyon", "Aşk", "Bilim Kurgu"])
    kategori_combobox = create_label_and_entry(2, "Kategori:", item_values[2], ["Film", "Dizi"])
    süre_entry = create_label_and_entry(3, "Süre:", item_values[3])
    durum_combobox = create_label_and_entry(4, "Durum:", item_values[4], ["İzlenmedi", "İzleniyor", "İzlendi"])
    yildiz_combobox = create_label_and_entry(5, "Yıldız:", item_values[5], [str(i) for i in range(1, 6)])
    notlar_entry = create_label_and_entry(6, "Notlar:", item_values[6])

    def kaydet():
        yeni_veriler = {
            "ad": ad_entry.get(),
            "tür": tür_combobox.get(),
            "kategori": kategori_combobox.get(),
            "süre": süre_entry.get(),
            "durum": durum_combobox.get(),
            "yildiz": yildiz_combobox.get(),
            "notlar": notlar_entry.get()
        }

        try:
            db.ensure_connection()
            db.update("content", yeni_veriler, {"ad": item_values[0]})
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

    kaydet_buton = tk.Button(
        duzenleme_penceresi,
        text="Kaydet",
        command=kaydet,
        bg="#E50914",
        fg="white",
        width=15
    )
    kaydet_buton.grid(row=7, column=0, columnspan=2, pady=10)

def arsivim(menü, db):
    db.connect()

    menü.withdraw()
    arsiv_penceresi = tk.Toplevel()
    arsiv_penceresi.title("Arşiv")
    arsiv_penceresi.geometry("750x400")
    arsiv_penceresi.configure(bg="#121212")

    arsiv_penceresi.grid_rowconfigure(0, weight=1)
    arsiv_penceresi.grid_rowconfigure(1, weight=0)
    arsiv_penceresi.grid_rowconfigure(2, weight=0)
    arsiv_penceresi.grid_rowconfigure(3, weight=0)
    arsiv_penceresi.grid_columnconfigure(0, weight=1)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#121212", foreground="white", fieldbackground="#121212")
    style.configure("Treeview.Heading", background="#E50914", foreground="white", font=("Helvetica", 10, "bold"))

    sütunlar = ("Ad", "Kategori", "Tür", "Süre", "Durum", "Yıldız", "Notlar")
    tree = ttk.Treeview(arsiv_penceresi, columns=sütunlar, show="headings")

    for sütun in sütunlar:
        tree.heading(sütun, text=sütun)
        tree.column(sütun, anchor="center", width=100)

    def tabloyu_doldur():
        for item in tree.get_children():
            tree.delete(item)
        rows = db.fetch_all("SELECT * FROM content")
        for row in rows:
            tree.insert("", "end", values=(row["ad"], row["kategori"], row["tür"], row["süre"], row["durum"], row["yildiz"], row["notlar"]))

    tabloyu_doldur()

    scrollbar = ttk.Scrollbar(arsiv_penceresi, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    filtre_buton = tk.Button(
        arsiv_penceresi,
        text="Filtreleme",
        bg="#E50914",
        fg="white",
        command=lambda: filtreleme_arayuzu(arsiv_penceresi, tree),
        width=15
    )
    filtre_buton.grid(row=1, column=0, pady=10, sticky="n")

    duzenle_buton = tk.Button(
        arsiv_penceresi,
        text="Düzenleme",
        bg="#E50914",
        fg="white",
        command=lambda: duzenleme_arayuzu(arsiv_penceresi, tree, db),
        width=15
    )
    duzenle_buton.grid(row=2, column=0, pady=10, sticky="n")

    def sil(tree):
        secilen = tree.selection()
        if not secilen:
            messagebox.showerror("Hata", "Lütfen silmek için içerik seçiniz.")
            return

        for id in secilen:
            values = tree.item(id, "values")
            db.insert("deleted_content", {
                "ad": values[0],
                "kategori": values[1],
                "tür": values[2],
                "süre": values[3],
                "durum": values[4],
                "yildiz": values[5],
                "notlar": values[6]
            })
            db.execute_query("DELETE FROM content WHERE ad = %s", (values[0],))
            tree.delete(id)

        messagebox.showinfo("Bilgi", "Seçilen içerikler başarıyla silindi.")

    sil_buton = tk.Button(
        arsiv_penceresi,
        text="Sil",
        bg="#E50914",
        fg="white",
        command=lambda: sil(tree),
        width=15
    )
    sil_buton.grid(row=1, column=1, pady=10, sticky="e")

    yenile_buton = tk.Button(
        arsiv_penceresi,
        text="Yenile",
        bg="#E50914",
        fg="white",
        command=tabloyu_doldur,
        width=15
    )
    yenile_buton.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    silinenler_buton = tk.Button(
        arsiv_penceresi,
        text="Silinenler",
        bg="#E50914",
        fg="white",
        command=lambda: silinenleri_goster(arsiv_penceresi, db),
        width=15
    )
    silinenler_buton.grid(row=3, column=0, pady=10, sticky="n")

    geri_buton = tk.Button(
        arsiv_penceresi,
        text="Menüye Dön",
        bg="#E50914",
        fg="white",
        width=15,
        command=lambda: geri_don(arsiv_penceresi, menü, db)
    )
    geri_buton.grid(row=3, column=1, pady=10, sticky="e")

    def geri_don(pencere, menü, db):
        db.close()
        pencere.destroy()
        menü.deiconify()

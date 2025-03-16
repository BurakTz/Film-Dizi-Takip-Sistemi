class content:
    def __init__(self, ad, kategori, tür, süre, durum, yildiz, notlar):
        self.ad = ad
        self.kategori = kategori
        self.tür = tür
        self.süre = süre
        self.durum = durum
        self.yildiz = yildiz
        self.notlar = notlar

    def __str__(self):  # toString metoduna benziyor
        return (f"Ad: {self.ad}\n"
                f"Kategori: {self.kategori}\n"
                f"Tür: {self.tür}\n"
                f"Süre(dakika): {self.süre}\n"
                f"Durum: {self.durum}\n"
                f"Yıldız: {self.yildiz}\n"
                f"Notlar: {self.notlar}")

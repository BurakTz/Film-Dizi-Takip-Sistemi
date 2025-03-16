import tkinter as tk

def filtreleme_arayuzu(ana_pencere, nesneler, tree):
    filtre_penceresi = tk.Toplevel(ana_pencere)
    filtre_penceresi.title("Filtreleme")
    filtre_penceresi.geometry("400x300")
    filtre_penceresi.configure(bg="#121212")
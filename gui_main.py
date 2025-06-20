from tkinter import *
from tkinter import messagebox
import tkintermapview
from utils import CoordinateFetcher

placowki = []
markery = []

def open_main_app():
    def odswiez_liste():
        listbox.delete(0, END)
        for plac in placowki:
            listbox.insert(END, f"{plac['nazwa']} - {plac['miasto']}")

    def dodaj_placowke():
        nazwa = entry_nazwa.get()
        miasto = entry_miasto.get()
        if not nazwa or not miasto:
            messagebox.showwarning("Brak danych", "Podaj nazwę i miasto.")
            return

        coords = CoordinateFetcher(miasto.replace(" ", "_")).get_coordinates()
        if coords is None:
            messagebox.showerror("Błąd", "Nie udało się pobrać współrzędnych.")
            return

        lat, lon = coords
        nowa = {"nazwa": nazwa, "miasto": miasto, "lat": lat, "lon": lon}
        placowki.append(nowa)
        marker = mapa.set_marker(lat, lon, text=nazwa)
        markery.append(marker)
        odswiez_liste()
        entry_nazwa.delete(0, END)
        entry_miasto.delete(0, END)

    def aktualizuj_placowke():
        idx = listbox.curselection()
        if not idx:
            messagebox.showwarning("Brak wyboru", "Wybierz placówkę do aktualizacji.")
            return

        nazwa = entry_nazwa.get()
        miasto = entry_miasto.get()
        if not nazwa or not miasto:
            messagebox.showwarning("Brak danych", "Podaj nową nazwę i miasto.")
            return

        coords = CoordinateFetcher(miasto.replace(" ", "_")).get_coordinates()
        if coords is None:
            messagebox.showerror("Błąd", "Nie udało się pobrać nowych współrzędnych.")
            return

        lat, lon = coords
        i = idx[0]

        # Zaktualizuj dane placówki
        placowki[i] = {"nazwa": nazwa, "miasto": miasto, "lat": lat, "lon": lon}

        # Usuń WSZYSTKIE stare markery
        for m in markery:
            m.delete()
        markery.clear()

        # Odtwórz znaczniki zaktualizowane
        for p in placowki:
            marker = mapa.set_marker(p["lat"], p["lon"], text=p["nazwa"])
            markery.append(marker)

        odswiez_liste()
        entry_nazwa.delete(0, END)
        entry_miasto.delete(0, END)

    def usun_placowke():
        idx = listbox.curselection()
        if not idx:
            return

        i = idx[0]
        placowki.pop(i)
        markery[i].delete()
        markery.pop(i)

        odswiez_liste()
        mapa.set_address("Polska")

        # Odtwórz znaczniki
        for m in markery:
            m.delete()
        markery.clear()
        for p in placowki:
            marker = mapa.set_marker(p["lat"], p["lon"], text=p["nazwa"])
            markery.append(marker)

    def pokaz_na_mapie(event):
        idx = listbox.curselection()
        if not idx:
            return
        plac = placowki[idx[0]]
        mapa.set_position(plac["lat"], plac["lon"])
        mapa.set_zoom(10)

        # Wczytaj dane do pól edycji
        entry_nazwa.delete(0, END)
        entry_nazwa.insert(0, plac["nazwa"])
        entry_miasto.delete(0, END)
        entry_miasto.insert(0, plac["miasto"])

    root = Toplevel()
    root.title("System Zarządzania Bankiem")
    root.geometry("1000x600")

    frame_left = Frame(root)
    frame_left.pack(side=LEFT, fill=Y, padx=10, pady=10)

    Label(frame_left, text="Lista placówek").pack()
    listbox = Listbox(frame_left, width=40)
    listbox.pack(pady=5)
    listbox.bind("<<ListboxSelect>>", pokaz_na_mapie)

    Button(frame_left, text="Usuń", command=usun_placowke).pack(pady=5)

    Label(frame_left, text="Nazwa:").pack()
    entry_nazwa = Entry(frame_left)
    entry_nazwa.pack(pady=2)

    Label(frame_left, text="Miasto:").pack()
    entry_miasto = Entry(frame_left)
    entry_miasto.pack(pady=2)

    Button(frame_left, text="Dodaj placówkę", command=dodaj_placowke).pack(pady=10)
    Button(frame_left, text="Aktualizuj placówkę", command=aktualizuj_placowke).pack(pady=5)

    frame_right = Frame(root)
    frame_right.pack(side=RIGHT, expand=True, fill=BOTH, padx=10, pady=10)

    mapa = tkintermapview.TkinterMapView(frame_right, width=700, height=550, corner_radius=0)
    mapa.pack()
    mapa.set_position(52.2297, 21.0122)
    mapa.set_zoom(6)



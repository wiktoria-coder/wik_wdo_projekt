from tkinter import *
from tkinter import messagebox
import tkintermapview
from utils import CoordinateFetcher

placowki = []
markery_placowek = {}
markery_pracownikow = {}
markery_klientow = {}
pracownicy = []
klienci = []


def open_main_app():
    root = Toplevel()
    root.title("System Zarzadzania Bankiem")
    root.geometry("1200x850")

    tryb_widoku = StringVar(value="wszyscy")

    def odswiez_liste():
        listbox.delete(0, END)
        for plac in placowki:
            listbox.insert(END, f"{plac['nazwa']} - {plac['miasto']}")

    def odswiez_markery():
        for m in markery_placowek.values():
            m.delete()
        for m in markery_pracownikow.values():
            m.delete()
        for m in markery_klientow.values():
            m.delete()

        markery_placowek.clear()
        markery_pracownikow.clear()
        markery_klientow.clear()

        for plac in placowki:
            # lista pracowników tej placówki
            pracownicy_tekst = "\n".join(
                f"{p['imie']} {p['nazwisko']} ({p['stanowisko']})"
                for p in pracownicy if p.get("placowka") == plac["nazwa"]
            )

            # lista klientów tej placówki
            klienci_tekst = "\n".join(
                f"{k['imie']} {k['nazwisko']} (Klient)"
                for k in klienci if k.get("placowka") == plac["nazwa"]
            )

            popup_text = f"{plac['nazwa']} ({plac['miasto']})"
            if pracownicy_tekst:
                popup_text += f"\n--- Pracownicy ---\n{pracownicy_tekst}"
            if klienci_tekst:
                popup_text += f"\n--- Klienci ---\n{klienci_tekst}"


            marker = mapa.set_marker(plac["lat"], plac["lon"], text=popup_text)
            markery_placowek[plac["nazwa"]] = marker

            # Markery dla wszystkich pracowników
            for prac in pracownicy:
                klucz = f"{prac['imie']}_{prac['nazwisko']}"
                tekst = f"{prac['imie']} {prac['nazwisko']} ({prac['stanowisko']})"

                if prac.get("placowka") in [p["nazwa"] for p in placowki]:
                    # Pracownik przypisany do istniejącej placówki — pomijamy, bo już jest pokazany w dymku placówki
                    continue

                # Inaczej: pokazujemy jego własny znacznik
                marker = mapa.set_marker(prac.get("lat", 52.2297), prac.get("lon", 21.0122), text=tekst)
                markery_pracownikow[klucz] = marker

            # Markery dla wszystkich klientów
            for klient in klienci:
                klucz = f"{klient['imie']}_{klient['nazwisko']}"
                tekst = f"{klient['imie']} {klient['nazwisko']} (Klient)"

                if klient.get("placowka") in [p["nazwa"] for p in placowki]:
                    # Klient przypisany do istniejącej placówki — pomijamy, bo już jest pokazany w dymku placówki
                    continue

                # Inaczej: pokazujemy jego własny znacznik
                marker = mapa.set_marker(klient.get("lat", 52.2297), klient.get("lon", 21.0122), text=tekst)
                markery_klientow[klucz] = marker

    def odswiez_liste_pracownikow():
        listbox_prac.delete(0, END)
        wybrane = listbox.curselection()
        if tryb_widoku.get() == "wszyscy":
            for p in pracownicy:
                listbox_prac.insert(END, f"{p['imie']} {p['nazwisko']} - {p['stanowisko']} ({p.get('placowka', 'brak')})")
        elif tryb_widoku.get() == "z_placowki" and wybrane:
            nazwa_plac = placowki[wybrane[0]]["nazwa"]
            for p in pracownicy:
                if p.get("placowka") == nazwa_plac:
                    listbox_prac.insert(END, f"{p['imie']} {p['nazwisko']} - {p['stanowisko']}")

    def odswiez_liste_klientow():
        listbox_klienci.delete(0, END)
        wybrane = listbox.curselection()
        if tryb_widoku.get() == "wszyscy":
            for k in klienci:
                listbox_klienci.insert(END, f"{k['imie']} {k['nazwisko']} - {k.get('placowka', 'brak')}")
        elif tryb_widoku.get() == "z_placowki" and wybrane:
            nazwa_plac = placowki[wybrane[0]]["nazwa"]
            for k in klienci:
                if k.get("placowka") == nazwa_plac:
                    listbox_klienci.insert(END, f"{k['imie']} {k['nazwisko']}")

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
        odswiez_liste()
        odswiez_markery()
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
        placowki[i] = {"nazwa": nazwa, "miasto": miasto, "lat": lat, "lon": lon}
        odswiez_liste()
        odswiez_markery()
        entry_nazwa.delete(0, END)
        entry_miasto.delete(0, END)

    def usun_placowke():
        idx = listbox.curselection()
        if not idx:
            return

        i = idx[0]
        usuwana_placowka = placowki[i]["nazwa"]
        placowki.pop(i)

        # Odejmij przypisanie placówki pracownikom i klientom
        for p in pracownicy:
            if p.get("placowka") == usuwana_placowka:
                p["placowka"] = None

        for k in klienci:
            if k.get("placowka") == usuwana_placowka:
                k["placowka"] = None

        #nie usuwają się klienci ani pracownicy - TYLKO placówka

        odswiez_liste()
        odswiez_liste_pracownikow()
        odswiez_liste_klientow()
        odswiez_markery()

    def pokaz_na_mapie(event):
        idx = listbox.curselection()
        if not idx:
            return
        plac = placowki[idx[0]]
        mapa.set_position(plac["lat"], plac["lon"])
        mapa.set_zoom(10)
        entry_nazwa.delete(0, END)
        entry_nazwa.insert(0, plac["nazwa"])
        entry_miasto.delete(0, END)
        entry_miasto.insert(0, plac["miasto"])
        odswiez_liste_pracownikow()



    def dodaj_pracownika():
        imie = entry_imie.get()
        nazwisko = entry_nazwisko.get()
        stanowisko = entry_stanowisko.get()

        if not imie or not nazwisko or not stanowisko:
            messagebox.showwarning("Brak danych", "Uzupełnij wszystkie dane pracownika.")
            return

        wybrane = listbox.curselection()
        if not wybrane:
            messagebox.showwarning("Brak placówki", "Wybierz placówkę, do której przypisany będzie pracownik.")
            return

        wybrana_plac = placowki[wybrane[0]]
        placowka_nazwa = wybrana_plac["nazwa"]
        lat = wybrana_plac["lat"]
        lon = wybrana_plac["lon"]

        nowy = {
            "imie": imie,
            "nazwisko": nazwisko,
            "stanowisko": stanowisko,
            "placowka": placowka_nazwa,
            "lat": lat,
            "lon": lon
        }
        pracownicy.append(nowy)
        odswiez_liste_pracownikow()
        odswiez_markery()

        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        entry_stanowisko.delete(0, END)

    def usun_pracownika():
        idx = listbox_prac.curselection()
        if not idx:
            return

        pracownik = pracownicy.pop(idx[0])
        klucz = f"{pracownik['imie']}_{pracownik['nazwisko']}"

        # Usuń znacznik pracownika z mapy, jeśli istnieje
        if klucz in markery_pracownikow:
            markery_pracownikow[klucz].delete()
            del markery_pracownikow[klucz]

        odswiez_liste_pracownikow()
        odswiez_markery()

    def aktualizuj_pracownika():
        idx = listbox_prac.curselection()
        if not idx:
            messagebox.showwarning("Brak wyboru", "Wybierz pracownika do aktualizacji.")
            return

        imie = entry_imie.get()
        nazwisko = entry_nazwisko.get()
        stanowisko = entry_stanowisko.get()

        if not imie or not nazwisko or not stanowisko:
            messagebox.showwarning("Brak danych", "Uzupełnij wszystkie dane.")
            return

        stary = pracownicy[idx[0]]
        wybrane_plac = listbox.curselection()
        placowka = placowki[wybrane_plac[0]]["nazwa"] if wybrane_plac else stary.get("placowka")

        pracownicy[idx[0]] = {
            "imie": imie,
            "nazwisko": nazwisko,
            "stanowisko": stanowisko,
            "placowka": placowka,
            "lat": stary.get("lat"),
            "lon": stary.get("lon")
        }
        odswiez_liste_pracownikow()
        odswiez_markery()

        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        entry_stanowisko.delete(0, END)



    def dodaj_klienta():
        imie = entry_klient_imie.get()
        nazwisko = entry_klient_nazwisko.get()

        if not imie or not nazwisko:
            messagebox.showwarning("Brak danych", "Uzupełnij imię i nazwisko klienta.")
            return

        wybrane = listbox.curselection()
        if not wybrane:
            messagebox.showwarning("Brak placówki", "Wybierz placówkę, do której przypisany będzie klient.")
            return

        wybrana_plac = placowki[wybrane[0]]
        placowka_nazwa = wybrana_plac["nazwa"]
        lat = wybrana_plac["lat"]
        lon = wybrana_plac["lon"]

        nowy = {
            "imie": imie,
            "nazwisko": nazwisko,
            "placowka": placowka_nazwa,
            "lat": lat,
            "lon": lon
        }
        klienci.append(nowy)
        odswiez_liste_klientow()
        odswiez_markery()

        entry_klient_imie.delete(0, END)
        entry_klient_nazwisko.delete(0, END)

    def usun_klienta():
        idx = listbox_klienci.curselection()
        if not idx:
            return

        klient = klienci.pop(idx[0])
        klucz = f"{klient['imie']}_{klient['nazwisko']}"

        if klucz in markery_klientow:
            markery_klientow[klucz].delete()
            del markery_klientow[klucz]

        odswiez_liste_klientow()
        odswiez_markery()

    def aktualizuj_klienta():
        idx = listbox_klienci.curselection()
        if not idx:
            messagebox.showwarning("Brak wyboru", "Wybierz klienta do aktualizacji.")
            return

        imie = entry_klient_imie.get()
        nazwisko = entry_klient_nazwisko.get()
        stary = klienci[idx[0]]

        wybrane_plac = listbox.curselection()
        placowka = placowki[wybrane_plac[0]]["nazwa"] if wybrane_plac else stary.get("placowka")

        klienci[idx[0]] = {
            "imie": imie,
            "nazwisko": nazwisko,
            "placowka": placowka,
            "lat": stary.get("lat"),
            "lon": stary.get("lon")
        }

        odswiez_liste_klientow()
        odswiez_markery()

        entry_klient_imie.delete(0, END)
        entry_klient_nazwisko.delete(0, END)



    # === GUI ===
#RAMKA LISTY PLACÓWEK BANKU
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
    frame_right.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

#RAMKA MAPY
    mapa = tkintermapview.TkinterMapView(frame_right, width=700, height=400, corner_radius=0)
    mapa.pack()
    mapa.set_position(52.2297, 21.0122)
    mapa.set_zoom(6)

#RAMKA LISTA PRACOWNIKÓW I KLIENTÓW
    #Pracownicy
    frame_dolny = Frame(root)
    frame_dolny.pack(side=BOTTOM, fill=X, padx=10, pady=10)

    frame_pracownicy = Frame(frame_dolny)
    frame_pracownicy.grid(row=0, column=0, sticky="n")

    frame_klienci = Frame(frame_dolny)
    frame_klienci.grid(row=0, column=1, sticky="n", padx=20)

    Label(frame_pracownicy, text="Lista pracowników").grid(row=0, column=0, sticky=W, columnspan=2)

    listbox_prac = Listbox(frame_pracownicy, width=40, height=6)
    listbox_prac.grid(row=1, column=0, rowspan=4, padx=5)

    right_panel = Frame(frame_pracownicy)
    right_panel.grid(row=1, column=1, padx=10, sticky=N)

    Label(right_panel, text="Stanowisko:").grid(row=0, column=0, sticky=W)
    entry_stanowisko = Entry(right_panel)
    entry_stanowisko.grid(row=1, column=0)

    Button(right_panel, text="Dodaj", command=dodaj_pracownika).grid(row=2, column=0, sticky="ew", pady=2)
    Button(right_panel, text="Usuń", command=usun_pracownika).grid(row=3, column=0, sticky="ew", pady=2)
    Button(right_panel, text="Aktualizuj", command=aktualizuj_pracownika).grid(row=4, column=0, sticky="ew", pady=2)

    Label(frame_pracownicy, text="Imię:").grid(row=5, column=0, sticky=W)
    entry_imie = Entry(frame_pracownicy)
    entry_imie.grid(row=5, column=0, sticky=E, padx=(50, 5))

    Label(frame_pracownicy, text="Nazwisko:").grid(row=6, column=0, sticky=W)
    entry_nazwisko = Entry(frame_pracownicy)
    entry_nazwisko.grid(row=6, column=0, sticky=E, padx=(50, 5))

    frame_widok = Frame(frame_pracownicy)
    frame_widok.grid(row=0, column=1, sticky=E)

    Radiobutton(frame_widok, text="Wszyscy", variable=tryb_widoku, value="wszyscy", command=odswiez_liste_pracownikow).pack(side=LEFT)
    Radiobutton(frame_widok, text="Z placówki", variable=tryb_widoku, value="z_placowki", command=odswiez_liste_pracownikow).pack(side=LEFT)

    #Klienci
    Label(frame_klienci, text="Lista klientów").grid(row=0, column=0, sticky=W, columnspan=2)

    listbox_klienci = Listbox(frame_klienci, width=40, height=6)
    listbox_klienci.grid(row=1, column=0, rowspan=4, padx=5)

    right_panel_klient = Frame(frame_klienci)
    right_panel_klient.grid(row=1, column=1, padx=10, sticky=N)

    Label(right_panel_klient, text="Imię:").grid(row=0, column=0, sticky=W)
    entry_klient_imie = Entry(right_panel_klient)
    entry_klient_imie.grid(row=1, column=0)

    Label(right_panel_klient, text="Nazwisko:").grid(row=2, column=0, sticky=W)
    entry_klient_nazwisko = Entry(right_panel_klient)
    entry_klient_nazwisko.grid(row=3, column=0)

    Button(right_panel_klient, text="Dodaj", command=dodaj_klienta).grid(row=4, column=0, sticky="ew", pady=2)
    Button(right_panel_klient, text="Usuń", command=usun_klienta).grid(row=5, column=0, sticky="ew", pady=2)
    Button(right_panel_klient, text="Aktualizuj", command=aktualizuj_klienta).grid(row=6, column=0, sticky="ew", pady=2)

    frame_widok_klienci = Frame(frame_klienci)
    frame_widok_klienci.grid(row=0, column=1, sticky=E)

    Radiobutton(frame_widok_klienci, text="Wszyscy", variable=tryb_widoku, value="wszyscy",command=odswiez_liste_klientow).pack(side=LEFT)
    Radiobutton(frame_widok_klienci, text="Z placówki", variable=tryb_widoku, value="z_placowki",command=odswiez_liste_klientow).pack(side=LEFT)

    odswiez_liste()
    odswiez_liste_pracownikow()
    odswiez_markery()
    odswiez_liste_klientow()

    root.mainloop()

from tkinter import *
import tkintermapview

def pokaz_mapke_bankow(lista_placowek):
    okno = Toplevel()
    okno.title("Mapa wszystkich banków")
    okno.geometry("800x600")

    mapa = tkintermapview.TkinterMapView(okno, width=800, height=600, corner_radius=0)
    mapa.pack(fill="both", expand=True)

    mapa.set_position(52.2297, 21.0122)  # Centrum Polski
    mapa.set_zoom(6)

    lokalizacje = {}
    for plac in lista_placowek:
        key = (plac["lat"], plac["lon"])
        lokalizacje.setdefault(key, []).append(plac)

    for (lat, lon), placowki_na_miejscu in lokalizacje.items():
        opis = "\n".join(f"{p['nazwa']} ({p['miasto']})" for p in placowki_na_miejscu)
        mapa.set_marker(lat, lon, text=opis)


def pokaz_mapke_pracownikow(pracownicy):
    okno = Toplevel()
    okno.title("Mapa wszystkich pracowników")
    okno.geometry("800x600")

    mapa = tkintermapview.TkinterMapView(okno, width=800, height=600, corner_radius=0)
    mapa.pack(fill="both", expand=True)

    mapa.set_position(52.2297, 21.0122)
    mapa.set_zoom(6)

    lokalizacje = {}
    for prac in pracownicy:
        key = (prac.get("lat", 52.2297), prac.get("lon", 21.0122))
        lokalizacje.setdefault(key, []).append(prac)

    for (lat, lon), pracownicy_na_miejscu in lokalizacje.items():
        opis = "\n".join(f"{p['imie']} {p['nazwisko']} ({p['stanowisko']})" for p in pracownicy_na_miejscu)
        mapa.set_marker(lat, lon, text=opis)


def pokaz_mapke_pracownikow_z_placowki(lista_pracownikow, nazwa_placowki):
    okno = Toplevel()
    okno.title(f"Mapa pracowników z placówki: {nazwa_placowki}")
    okno.geometry("800x600")

    mapa = tkintermapview.TkinterMapView(okno, width=800, height=600, corner_radius=0)
    mapa.pack(fill="both", expand=True)

    mapa.set_position(52.2297, 21.0122)
    mapa.set_zoom(6)

    lokalizacje = {}
    for prac in lista_pracownikow:
        if prac.get("placowka") != nazwa_placowki:
            continue
        key = (prac.get("lat", 52.2297), prac.get("lon", 21.0122))
        lokalizacje.setdefault(key, []).append(prac)

    for (lat, lon), pracownicy_na_miejscu in lokalizacje.items():
        opis = "\n".join(f"{p['imie']} {p['nazwisko']} ({p['stanowisko']})" for p in pracownicy_na_miejscu)
        mapa.set_marker(lat, lon, text=opis)


def pokaz_mapke_klientow_z_placowki(lista_klientow, nazwa_placowki):
    okno = Toplevel()
    okno.title(f"Mapa klientów z placówki: {nazwa_placowki}")
    okno.geometry("800x600")

    mapa = tkintermapview.TkinterMapView(okno, width=800, height=600, corner_radius=0)
    mapa.pack(fill="both", expand=True)

    mapa.set_position(52.2297, 21.0122)  # Centrum Polski
    mapa.set_zoom(6)

    lokalizacje = {}
    for klient in lista_klientow:
        if klient.get("placowka") != nazwa_placowki:
            continue
        key = (klient.get("lat", 52.2297), klient.get("lon", 21.0122))
        lokalizacje.setdefault(key, []).append(klient)

    for (lat, lon), klienci_na_miejscu in lokalizacje.items():
        opis = "\n".join(f"{k['imie']} {k['nazwisko']} (Klient)" for k in klienci_na_miejscu)
        mapa.set_marker(lat, lon, text=opis)
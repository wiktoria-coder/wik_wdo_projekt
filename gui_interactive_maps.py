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

    # Dodaj znaczniki z przekazanej listy
    for plac in lista_placowek:
        tekst = f"{plac['nazwa']} ({plac['miasto']})"
        mapa.set_marker(plac["lat"], plac["lon"], text=tekst)

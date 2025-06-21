from gui_login import start_login
from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Ukryj główne puste okno
    start_login()
    root.mainloop()

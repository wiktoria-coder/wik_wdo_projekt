from tkinter import *
from tkinter import messagebox
from gui_main import open_main_app

users = {
    "admin": "admin123",
    "pracownik": "haslo"
}

def start_login():
    def login():
        username = entry_username.get()
        password = entry_password.get()

        if username in users and users[username] == password:
            messagebox.showinfo("Sukces", "Zalogowano pomyślnie!")
            login_window.destroy()
            open_main_app()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło.")

    login_window = Toplevel()
    login_window.title("Logowanie do systemu bankowego")
    login_window.geometry("400x250")

    Label(login_window, text="Login:").pack(pady=5)
    entry_username = Entry(login_window)
    entry_username.pack(pady=5)

    Label(login_window, text="Hasło:").pack(pady=5)
    entry_password = Entry(login_window, show="*")
    entry_password.pack(pady=5)

    Button(login_window, text="Zaloguj", command=login).pack(pady=20)



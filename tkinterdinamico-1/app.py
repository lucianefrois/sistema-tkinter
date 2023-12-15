import tkinter as tk
from login import LoginWindow
from menu import DatabaseMenu
from database import DatabaseManager

def open_main_menu():
    root = tk.Tk()
    app = DatabaseMenu(root)
    root.mainloop()

def main():
    db_name = 'tcc_top3'  # Substitua pelo nome real do seu banco de dados
    db_manager = DatabaseManager(db_name=db_name)
    login_window = LoginWindow(db_manager, open_main_menu)
    login_window.mainloop()

if __name__ == "__main__":
    main()

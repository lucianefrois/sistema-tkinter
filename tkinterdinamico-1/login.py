import tkinter as tk
from tkinter import messagebox
from database import DatabaseManager

# Configurações globais
BUTTON_WIDTH = 5
BUTTON_HEIGHT = 1
DATABASE_NAME = "tcc_top3"
BUTTON_BACKGROUND_COLOR = "#84C54A"
BACKGROUND_COLOR = "#4A5B8A"
COMMON_FONT = ("Arial", 14)
FONT_COLOR = "#FFFFFF"

class LoginWindow(tk.Tk):
    def __init__(self, db_manager, open_main_menu_callback):
        super().__init__()
        self.title("Login")
        self.geometry("500x500")
        self.configure(bg=BACKGROUND_COLOR)
        self.db_manager = db_manager
        self.open_main_menu_callback = open_main_menu_callback  # Callback para abrir o menu principal
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Usuário:", bg=BACKGROUND_COLOR, fg=FONT_COLOR, font=COMMON_FONT).pack(pady=5)
        self.username_entry = tk.Entry(self, font=COMMON_FONT)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Senha:", bg=BACKGROUND_COLOR, fg=FONT_COLOR, font=COMMON_FONT).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", font=COMMON_FONT)
        self.password_entry.pack(pady=5)

        login_button = tk.Button(
            self,
            text="Login",
            command=self.login,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            bg=BUTTON_BACKGROUND_COLOR,
            font=COMMON_FONT,
        )
        login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db_manager.authenticate_user(username, password):
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.destroy()  # Fecha a janela de login
            self.open_main_menu_callback()  # Chama a função para abrir o menu principal
        else:
            messagebox.showerror("Login", "Login falhou. Tente novamente.")

# Exemplo de uso
if __name__ == "__main__":
    db_manager = DatabaseManager(DATABASE_NAME)
    login_window = LoginWindow(db_manager, lambda: print("Abrir menu principal"))
    login_window.mainloop()

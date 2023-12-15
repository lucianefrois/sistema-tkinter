import tkinter as tk
from tkinter import PhotoImage
from database import DatabaseManager
from gui import DynamicGUI
from config import *
import os

class DatabaseMenu(BaseWindow):
    def __init__(self, root):
        super().__init__(root, "Menu FluidOps", BACKGROUND_COLOR, fullscreen=True)
        self.db_manager = DatabaseManager(DATABASE_NAME)
        self.dynamic_gui = None
        self.dynamic_gui_instances = {}
        self.report_windows = {}
        self.create_buttons()

    def get_db_manager(self):
        return self.db_manager

    def create_buttons(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_relatorio_geral_path = os.path.join(current_dir, "assets", "images", "icon_relatorio2.png")
        icon_relatorio_individual_path = os.path.join(current_dir, "assets", "images", "icon_relatorio1.png")

        # Crie um frame para os botões superiores
        top_buttons_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        top_buttons_frame.pack(side="top")

        # Botões da parte de cima
        top_buttons = ["Cadastrar Cliente", "Serviço Clientes", "Caixa", "Registrar Despesas"]

        for table_name in top_buttons:
            button_frame = tk.Frame(top_buttons_frame, bg=BACKGROUND_COLOR)

            # Carregue o ícone como PhotoImage e redimensione
            icon_filename = table_icons[table_name]
            icon = PhotoImage(file=icon_filename)
            icon = icon.subsample(14)  # Redimensione o ícone (ajuste o valor conforme necessário)

            # Crie botões com ícones e texto
            button = tk.Button(
                button_frame,
                text=table_name,
                image=icon,
                compound="top",
                bg=BUTTON_BACKGROUND_COLOR,
                font=COMMON_FONT,
                command=lambda t=table_name: self.open_menu_option(t)
            )
            button.image = icon
            button["width"] = BUTTON_WIDTH
            button["height"] = BUTTON_HEIGHT
            button.pack(side="left", padx=20, pady=20)
            button_frame.pack(side="left")

        # Imagem
        image_path = os.path.join(current_dir, "assets", "images", "top_nordeste.png")
        image = PhotoImage(file=image_path)
        image_label = tk.Label(self.root, image=image, bg=BACKGROUND_COLOR, width=350, height=350)
        image_label.image = image
        image_label.pack(pady=5)

        # Crie um frame para os botões inferiores
        bottom_buttons_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        bottom_buttons_frame.pack(side="bottom")

        image_path = os.path.join(current_dir, "assets", "images", "icon_laudo.png")
        icon_relatorio_individual = PhotoImage(file=icon_relatorio_individual_path)
        icon_relatorio_individual = icon_relatorio_individual.subsample(14)


        report_button_individual = tk.Button(
            bottom_buttons_frame,
            text="Relatório Individual",
            image=icon_relatorio_individual,
            compound="top",
            command=lambda: self.open_report("individual"),
            bg=BUTTON_BACKGROUND_COLOR,
            font=COMMON_FONT
        )
        report_button_individual.image = icon_relatorio_individual
        report_button_individual["width"] = BUTTON_WIDTH
        report_button_individual["height"] = BUTTON_HEIGHT
        report_button_individual.pack(side="left", padx=20, pady=30)

        image_path = os.path.join(current_dir, "assets", "images", "logo_nordeste.png")
        icon_relatorio_geral = PhotoImage(file=icon_relatorio_geral_path)
        icon_relatorio_geral = icon_relatorio_geral.subsample(14)
        report_button_geral = tk.Button(
            bottom_buttons_frame,
            text="Relatório Geral",
            image=icon_relatorio_geral,
            compound="top",
            command=lambda: self.open_report("geral"),
            bg=BUTTON_BACKGROUND_COLOR,
            font=COMMON_FONT
        )
        report_button_geral.image = icon_relatorio_geral
        report_button_geral["width"] = BUTTON_WIDTH
        report_button_geral["height"] = BUTTON_HEIGHT
        report_button_geral.pack(side="left", padx=20)

        # Botões da parte de baixo
        bottom_buttons = ["Sair"]
        for table_name in bottom_buttons:
            button_frame = tk.Frame(bottom_buttons_frame, bg=BACKGROUND_COLOR)

            # Carregue o ícone como PhotoImage e redimensione
            icon_filename = table_icons[table_name]
            icon = PhotoImage(file=icon_filename)
            icon = icon.subsample(14)

            # Crie botões com ícones e texto
            button = tk.Button(
                button_frame,
                text=table_name,
                image=icon,
                compound="top",
                bg=BUTTON_BACKGROUND_COLOR,
                font=COMMON_FONT,
                command=lambda t=table_name: self.open_menu_option(t)
            )
            button.image = icon
            button["width"] = BUTTON_WIDTH
            button["height"] = BUTTON_HEIGHT
            button.pack(side="left", padx=20, pady=10)
            button_frame.pack(side="left")

    def open_report(self, report_type):
        report_window = tk.Toplevel(self.root)
        if report_type == "individual":
            report = ReportIndividualWindow(report_window, self.db_manager)
        elif report_type == "geral":
            report = GeneralReportWindow(report_window, self.db_manager)
        self.report_windows[report_type] = report
    

    def open_gui(self, table_name, selected_window):
        table_menu = tk.Toplevel(self.root)
        table_menu.title(f"Operações em {table_name}")
        self.db_manager.set_id_column_name(table_name)
        dynamic_gui = DynamicGUI(table_menu, table_name, self.db_manager, selected_window)
        dynamic_gui.return_to_menu = lambda: self.close_gui(table_menu, table_name)
        self.dynamic_gui_instances[table_name] = dynamic_gui

    def close_gui(self, window, table_name):
        window.destroy()
        del self.dynamic_gui_instances[table_name]

    def open_menu_option(self, option_name):
        if option_name == "Cadastrar Cliente":
            self.open_gui("cliente", option_name)
        elif option_name == "Serviço Clientes":
            self.open_gui("servico_cliente", option_name)
        elif option_name == "Caixa":
            self.open_gui("entrada", option_name)
        elif option_name == "Registrar Despesas":
            self.open_gui("saida", option_name)
        elif option_name == "Sair":
            self.root.quit()

from reports import ReportIndividualWindow, GeneralReportWindow

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseMenu(root)
    root.mainloop()
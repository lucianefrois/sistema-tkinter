#Configurações globais
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 150
DATABASE_NAME = "tcc_top3"
BUTTON_BACKGROUND_COLOR = "#84C54A"
BACKGROUND_COLOR = "#4A5B8A"
COMMON_FONT = ("Arial", 14)
FONT_COLOR = "#FFFFFF"

# Dicionário associando nomes de tabelas aos nomes dos arquivos de ícone
table_icons = {
    "Cadastrar Cliente": "assets/images/user_add.png",
    "Cadastrar Despachante": "assets/images/icon_despachante.png",
    "Serviço Clientes": "assets/images/icon_laudo.png",
    "Caixa": "assets/images/icon_pagamento.png",
    "Registrar Despesas": "assets/images/icon_despesa.png",
    "Relatório Individual": "assets/images/icon_relatorio1.png",
    "Relatório Geral": "assets/images/icon_relatorio2.png",
    "Sair": "assets/images/icon_saida.png",
}


class BaseWindow:
    def __init__(self, root, title, background_color, fullscreen=True):
        self.root = root
        self.root.title(title)
        self.root.configure(bg=background_color)
        # Obtem o tamanho da tela
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        # Iniciar Maximizado
        self.root.state('zoomed')
        # Defina o tamanho da janela como tela cheia
        WINDOW_SIZE = f"{screen_width}x{screen_height}"
        root.geometry(WINDOW_SIZE)
        
        
    
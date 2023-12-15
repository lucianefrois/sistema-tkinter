import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry #calendario
from database import DatabaseManager #banco de dados
import datetime #database
from config import * #configurações
import re # para realizar a conversão das datas 
from PIL import Image, ImageTk # para carregamento de imagem
from pdf import ReportIndividualPDF,GeneralReportsPDF #para gerar o pdf
import subprocess #para abrir o pdf

class ReportIndividualWindow(BaseWindow):
    def __init__(self, root, db_manager):
        super().__init__(root, "Relatório Individual", BACKGROUND_COLOR, fullscreen=True)
        self.report_type = "individual"
        self.db_manager = db_manager
        self.data_entrada = None
        # Cria campos de consulta
        self.create_report_fields()
        # Cria um Treeview 
        self.create_treeview()
        self.create_treeview_saida()

    def create_report_fields(self):
        # Frame 30% à esquerda
        left_frame = tk.Frame(self.root, width=0.3 * self.root.winfo_screenwidth(), 
                              height=self.root.winfo_screenheight(), bg=BACKGROUND_COLOR)
        left_frame.pack(side="left", fill="y")
        
        tk.Label(left_frame, text="Relatório Individual", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5, pady=10)

        # Adicione uma imagem usando PIL (Pillow)
        image = Image.open("assets/images/icon_relatorio1.png")  # Substitua pelo caminho da sua imagem
        image = image.resize((100, 100))  # Redimensione a imagem conforme necessário
        photo = ImageTk.PhotoImage(image)

        # Label para exibir a imagem
        image_label = tk.Label(left_frame, image=photo, bg=BACKGROUND_COLOR)
        image_label.image = photo
        image_label.pack(pady=50, padx=100)
        
        # Labels e ComboBox para campos de consulta
        tk.Label(left_frame, text="Nome:", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5, pady=5)
        self.name_combobox = ttk.Combobox(left_frame)
        self.name_combobox.pack(padx=5, pady=5)
        self.name_combobox.set("Escolha o Despachante")

        # Carregar clientes no ComboBox
        clientes = self.db_manager.get_all_clientes()
        self.name_combobox['values'] = clientes
        print(clientes)

        # DateEntry para seleção de datas
        tk.Label(left_frame, text="Data de Início:", font=COMMON_FONT, fg=FONT_COLOR, bg=BACKGROUND_COLOR).pack(padx=5, pady=5)
        self.start_date_entry = DateEntry(left_frame, date_pattern='dd/mm/yyyy')
        self.start_date_entry.pack(padx=5, pady=5)

        tk.Label(left_frame, text="Data de Fim:", font=COMMON_FONT, fg=FONT_COLOR, bg=BACKGROUND_COLOR).pack(padx=5, pady=5)
        self.end_date_entry = DateEntry(left_frame, date_pattern='dd/mm/yyyy')
        self.end_date_entry.pack(padx=5, pady=5)

        # Botão para gerar o relatório
        generate_button = tk.Button(left_frame, text="Gerar Relatório", command=self.generate_report)
        generate_button.pack(padx=5, pady=10)
        
        # Label para exibir o valor total
        self.total_label = tk.Label(left_frame, text="Total R$: 0.00",font=COMMON_FONT, fg="white", bg=BACKGROUND_COLOR)
        self.total_label.pack(padx=5, pady=10)

        # Botão de voltar
        back_button = tk.Button(left_frame, text="Voltar para o Menu", command=self.return_to_menu)
        back_button.pack(padx=10, pady=10)

        # Botão de imprimir
        print_button = tk.Button(left_frame, text="Imprimir Relatório", command=self.print_report)
        print_button.pack(padx=10, pady=10)

    def create_treeview(self):
        # Frame 50% à direita
        right_frame = tk.Frame(self.root, width=0.5 * self.root.winfo_screenwidth(),
                        height=0.5 * self.root.winfo_screenwidth(), bg=BACKGROUND_COLOR)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        columns = [
            ("ID", 100),
            ("Data", 100),
            ("Cliente", 150),
            ("Tipo Veiculo", 100),
            ("Placa", 100),
            ("Valor", 75),
            ("Status", 100),
            ("Op. Caixa", 100)
        ]

        self.tree = ttk.Treeview(right_frame, columns=[column[0] for column in columns])
        # Configuração das colunas e cabeçalhos do Treeview
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("#0", text="")
        
        for i, (text, width) in enumerate(columns, 1):
            self.tree.column(f"#{i}", width=width, anchor="center")
            self.tree.heading(f"#{i}", text=text)
        
        self.tree.pack(fill=tk.BOTH, expand=1, padx=40, pady=20)

        # Configurar barras de rolagem
        scrollbar_y = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")
        
    def generate_report(self):
        name = self.name_combobox.get()  # Obtém o valor selecionado na combobox
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()
        
        # Use o valor real do nome, não a string "{name}"
        cleaned_name = re.sub(r'[{}]', '', name)
        
        print("Nome:", cleaned_name)
        print("Data de Início:", start_date_str)
        print("Data de Fim:", end_date_str)

        # Conversão das datas
        start_date = datetime.datetime.strptime(start_date_str, "%d/%m/%Y").date()
        end_date = datetime.datetime.strptime(end_date_str, "%d/%m/%Y").date()

        # Consulta SQL
        query = """
        SELECT * FROM relatorio_individual
        WHERE
            (Data_servico BETWEEN %s AND %s) AND Cliente_Despachante = %s;
        """
        parameters = (start_date, end_date, cleaned_name)


        try:
            self.db_manager.cursor.execute(query, parameters)
            results = self.db_manager.cursor.fetchall()
            print("Results:", results)
            self.db_manager.conn.commit()
        except Exception as e:
            print(f"Erro ao executar consulta: {e}")
            results = []
        
        total_value = 0
        
        # Limpa a exibição anterior no Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Preencha o Treeview com os resultados
        for row in results:
            self.tree.insert("", "end", values=row)
            print(row)

            # Cálculo do total_value dentro do loop
            if len(row) > 6 and isinstance(row[5], float):
                try:
                    valor = float(row[5])
                    print(f"O valor é : {valor}") #debug
                    total_value += valor
                except (ValueError, TypeError):
                    pass

        # Atualize o valor total na Label
        self.total_label.config(text=f"Total R$: {total_value:.2f}")
        print(total_value)
        
        # Armazena os resultados e total_value como atributos da instância
        self.report_results = results
        self.report_total_value = total_value
        self.report_cleaned_name = cleaned_name
        self.report_start_date_str = start_date_str
        self.report_end_date_str = end_date_str
        

    def return_to_menu(self):
        # Ocultar a janela atual
        self.root.destroy()
        # Tornar a janela do menu visível
        menu_window = DatabaseMenu(self.root)

    def print_report(self):
        # Somente chama a função para abrir o PDF se o relatório foi gerado
        if hasattr(self, 'report_results') and hasattr(self, 'report_total_value'):
            # Criação do arquivo PDF utilizando a nova classe ReportIndividualPDF
            pdf_generator = ReportIndividualPDF()
            pdf_filename = f"relatorio_{self.report_cleaned_name}_{self.report_start_date_str.replace('/', '_')}_{self.report_end_date_str.replace('/', '_')}.pdf"
            
            # Chama a função para criar o PDF e imprimir/abrir o relatório (abrir o PDF)
            pdf_generator.create_pdf(
                pdf_filename,
                self.report_cleaned_name,
                self.report_start_date_str,
                self.report_end_date_str,
                self.report_results,
                self.report_total_value
            )
            print(f"Relatório gerado em: {pdf_filename}")

from menu import DatabaseMenu
# isso faz com que o menu não funcione
class GeneralReportWindow(BaseWindow):
    def __init__(self, root, db_manager):
        super().__init__(root, "Relatório Geral", BACKGROUND_COLOR, fullscreen=True)
        self.db_manager = db_manager
        self.report_type = "geral"
        self.create_report_fields()
        self.create_treeview_saida()
        self.create_treeview_entrada()
        self.start_date = None
        self.end_date = None
        self.pdf_generator = GeneralReportsPDF()

    def create_report_fields(self):
        # Frame 30% à esquerda
        left_frame = tk.Frame(self.root, width=0.3 * self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg=BACKGROUND_COLOR)
        left_frame.pack(side="left", fill="y")
        
        tk.Label(left_frame, text="Relatório Geral", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5, pady=10)
        
        # Adicione uma imagem usando PIL (Pillow)
        image = Image.open("assets/images/icon_relatorio2.png")  # Substitua pelo caminho da sua imagem
        image = image.resize((100, 100))  # Redimensione a imagem conforme necessário
        photo = ImageTk.PhotoImage(image)

        #Label para exibir a imagem
        image_label = tk.Label(left_frame, image=photo, bg=BACKGROUND_COLOR)
        image_label.image = photo
        image_label.pack(pady=50, padx=100)

        # Título
        tk.Label(left_frame, text="Selecione um período", font=COMMON_FONT, fg=FONT_COLOR, bg=BACKGROUND_COLOR, width=30).pack(pady=5)

        # Datas
        tk.Label(left_frame, text="Data de Entrada:", font=COMMON_FONT, fg=FONT_COLOR, bg=BACKGROUND_COLOR, width=30).pack(pady=5)
        self.start_date_entry = DateEntry(left_frame, date_pattern='dd/mm/yyyy', width=30)
        self.start_date_entry.pack(pady=5, padx=20)
        tk.Label(left_frame, text="Data de Saída:", font=COMMON_FONT, fg=FONT_COLOR, bg=BACKGROUND_COLOR, width=30).pack(pady=5)
        self.end_date_entry = DateEntry(left_frame, date_pattern='dd/mm/yyyy', width=30)
        self.end_date_entry.pack(pady=5, padx=20)

        # Botão para gerar o relatório
        generate_button = tk.Button(left_frame, text="Gerar Relatório", command=self.generate_report, width=30)
        generate_button.pack(pady=10, padx=20)

        # Label para exibir o valor total de entradas
        self.total_entrada_label = tk.Label(left_frame, text="Total Entradas R$: 0.00", fg="white", font=COMMON_FONT, bg=BACKGROUND_COLOR, width=30)
        self.total_entrada_label.pack(pady=5, padx=20)
        # Label para exibir o valor total
        self.total_saida_label = tk.Label(left_frame, text="Total Saidas R$: 0.00", fg="white", font=COMMON_FONT, bg=BACKGROUND_COLOR, width=30)
        self.total_saida_label.pack(pady=5, padx=20)
        # Label para exibir o valor total
        self.total_label = tk.Label(left_frame, text="Total R$: 0.00", fg="white", font=COMMON_FONT, bg=BACKGROUND_COLOR, width=30)
        self.total_label.pack(pady=5, padx=20)

        # Botão de imprimir
        print_button = tk.Button(left_frame, text="Imprimir Relatório", command=self.print_report, width=30)
        print_button.pack(padx=50, pady=10)

        # Botão de voltar
        back_button = tk.Button(left_frame, text="Voltar para o Menu", command=self.return_to_menu, width=30)
        back_button.pack(pady=50, padx=20)
    
    def create_treeview_entrada(self):
        # Frame para o novo treeview
        right_frame_entrada = tk.Frame(self.root, width=0.5 * self.root.winfo_screenwidth(),
                                height=0.5 * self.root.winfo_screenheight(), bg=BACKGROUND_COLOR)
        right_frame_entrada.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        columns_entrada = [
            ("ID", 50),
            ("Data Entrada", 100),
            ("Cliente/Despachante", 150),
            ("Valor Entrada", 100),
            ("Status", 100),
        ]
        self.tree_entrada = ttk.Treeview(right_frame_entrada, columns=[column[0] for column in columns_entrada])

        # Configuração das colunas e cabeçalhos do Treeview de saída
        self.tree_entrada.column("#0", width=0, stretch=tk.NO)
        self.tree_entrada.heading("#0", text="")

        for i, (text, width) in enumerate(columns_entrada, 1):
            self.tree_entrada.heading(f"#{i}", text=text)
            self.tree_entrada.column(f"#{i}", width=width, anchor="center")

        self.tree_entrada.pack(fill=tk.BOTH, expand=1, padx=40, pady=20)

        # Configurar barras de rolagem para o treeview de saída
        scrollbar_y_entrada = ttk.Scrollbar(self.tree_entrada, orient="vertical", command=self.tree_entrada.yview)
        self.tree_entrada.configure(yscrollcommand=scrollbar_y_entrada.set)
        scrollbar_y_entrada.pack(side="right", fill="y")

        scrollbar_x_entrada = ttk.Scrollbar(self.tree_entrada, orient="horizontal", command=self.tree_entrada.xview)
        self.tree_entrada.configure(xscrollcommand=scrollbar_x_entrada.set)
        scrollbar_x_entrada.pack(side="bottom", fill="x")
        
    def create_treeview_saida(self):
        # Frame para o novo treeview
        right_frame_saida = tk.Frame(self.root, width=0.5 * self.root.winfo_screenwidth(),
                                height=0.5 * self.root.winfo_screenheight(), bg=BACKGROUND_COLOR)
        right_frame_saida.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        columns_saida = [
            ("ID", 50),
            ("Data Saída", 100),
            ("Descrição", 150),
            ("Valor Saída", 100),
            ("Op caixa", 100)
        ]
        self.tree_saida = ttk.Treeview(right_frame_saida, columns=[column[0] for column in columns_saida])

        # Configuração das colunas e cabeçalhos do Treeview de saída
        self.tree_saida.column("#0", width=0, stretch=tk.NO)
        self.tree_saida.heading("#0", text="")

        for i, (text, width) in enumerate(columns_saida, 1):
            self.tree_saida.heading(f"#{i}", text=text)
            self.tree_saida.column(f"#{i}", width=width, anchor="center")

        self.tree_saida.pack(fill=tk.BOTH, expand=1, padx=40, pady=20)

        # Configurar barras de rolagem para o treeview de saída
        scrollbar_y_saida = ttk.Scrollbar(self.tree_saida, orient="vertical", command=self.tree_saida.yview)
        self.tree_saida.configure(yscrollcommand=scrollbar_y_saida.set)
        scrollbar_y_saida.pack(side="right", fill="y")

        scrollbar_x_saida = ttk.Scrollbar(self.tree_saida, orient="horizontal", command=self.tree_saida.xview)
        self.tree_saida.configure(xscrollcommand=scrollbar_x_saida.set)
        scrollbar_x_saida.pack(side="bottom", fill="x")

    def generate_report(self):
        # Obtenha as datas de entrada e saída dos campos de entrada
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        # Verifique se as datas foram preenchidas
        if not start_date or not end_date:
            # Mostre uma mensagem de erro se as datas não forem preenchidas
            tk.messagebox.showerror("Erro", "Por favor, insira datas de entrada e saída.")
            return

        # Converta as datas para o formato 'YYYY-MM-DD'
        self.formatted_start_date = start_date.strftime('%Y-%m-%d')
        self.formatted_end_date = end_date.strftime('%Y-%m-%d')

        # Consulta SQL para relatorio_geral
        query_geral = "SELECT * FROM relatorio_geral WHERE Data_Servico BETWEEN %s AND %s"
        results_geral = self.db_manager.execute_query(query_geral, self.formatted_start_date, self.formatted_end_date)
        # Consulta SQL para view_saidas
        query_saidas = "SELECT * FROM view_saidas WHERE data_saida BETWEEN %s AND %s"
        results_saidas = self.db_manager.execute_query(query_saidas, self.formatted_start_date, self.formatted_end_date)

        # Limpe a exibição anterior no Treeview de entrada
        for item in self.tree_entrada.get_children():
            self.tree_entrada.delete(item)

        # Preencha o Treeview de entrada com os resultados de relatorio_geral
        for row in results_geral:
            self.tree_entrada.insert("", "end", values=row)
            
        # Limpe a exibição anterior no Treeview de saída
        for item in self.tree_saida.get_children():
            self.tree_saida.delete(item)

        # Preencha o Treeview de saída com os resultados de view_saidas
        for row in results_saidas:
            self.tree_saida.insert("", "end", values=row)

            
        total_entrada = 0
        total_saida = 0
        total_value = 0

        # Cálculo dos valores de entrada com base nos dados do Treeview de entrada
        for row in self.tree_entrada.get_children():
            values = self.tree_entrada.item(row)['values']
            try:
                valor_entrada = float(values[3]) if values[3] else 0  # Valor de entrada convertido para float
                total_entrada += valor_entrada  # Adiciona o valor de entrada
            except (ValueError, TypeError):  
                pass  

        # Cálculo dos valores de saída com base nos dados do Treeview de saída
        for row in self.tree_saida.get_children():
            values = self.tree_saida.item(row)['values']
            try:
                valor_saida = float(values[3]) if values[3] else 0  # Valor de saída convertido para float
                total_saida += valor_saida  # Adiciona o valor de saída   
            except (ValueError, TypeError):  
                pass  

        # Cálculo do total líquido
        total_value = total_entrada - total_saida

        # Atualize os valores totais nas Labels
        self.total_entrada_label.config(text=f"Total Entradas R$: {total_entrada:.2f}")
        self.total_saida_label.config(text=f"Total Saidas R$: -{total_saida:.2f}")
        self.total_label.config(text=f"Total Liquido R$: {total_value:.2f}")
        print(f"Total Calculado: {total_value}")

        # Armazena os resultados e total_value como atributos da instância
        self.report_results = results_geral
        self.report_total_entrada = total_entrada
        self.report_total_saida = total_saida
        self.report_total_value = total_value

    def print_report(self):
        # Verifica se o relatório foi gerado
        if hasattr(self, 'report_results') and hasattr(self, 'report_total_value'):
            # Chama a função para gerar e imprimir/abrir o relatório (abrir o PDF)
            self.pdf_generator.create_pdf(self.formatted_start_date, self.formatted_end_date, 
                                          self.report_results, self.report_total_entrada, 
                                          self.report_total_saida, self.report_total_value)



    def return_to_menu(self):
        # Ocultar a janela atual
        self.root.destroy()
        # Tornar a janela do menu visível
        menu_window = DatabaseMenu(self.root)

from menu import DatabaseMenu

if __name__ == "__main__":
    root = tk.Tk()
    db_manager = DatabaseManager(DATABASE_NAME)
    general_report_window = GeneralReportWindow(root, db_manager)
    report_individual_window = ReportIndividualWindow(root, db_manager)
    root.mainloop()
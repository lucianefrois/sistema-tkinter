import tkinter as tk
from tkinter import ttk,messagebox
from database import DatabaseManager
from config import *
from PIL import Image, ImageTk

class ServicesWindow(BaseWindow):
    def __init__(self, root, db_manager,table_name):
        super().__init__(root, "Cadastrar Serviço", BACKGROUND_COLOR, fullscreen=True)
        self.service_type = "servico"
        self.table_name = table_name #o problema tb está aqui
        self.db_manager = db_manager
        
        # Cria os rótulos (labels) e as entradas (inputs) com base nos campos da tabela
        #O problema está aqui
        self.labels = []
        self.inputs = []
        self.create_service_fields ()
        self.create_treeview()
        self.selected_item = None
    
    def create_service_fields(self):
        left_frame = tk.Frame(self.root, width=0.3*self.root.winfo_screenwidth(), 
                              height=self.root.winfo_screenheight(), bg=BACKGROUND_COLOR)
        left_frame.pack(side="left", fill="y")
        
        tk.Label(left_frame, text="Serviços", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5, pady=10)
        
        image = Image.open("assets/images/icon_laudo.png")
        image = image.resize((75,75))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(left_frame, image=photo, bg=BACKGROUND_COLOR)
        image_label.image = photo
        image_label.pack(pady=5,padx=100)
        
        # Clientes 
        label_clientes = tk.Label(left_frame, text="Nome Clientes", font=COMMON_FONT, fg=FONT_COLOR, 
                bg=BACKGROUND_COLOR)
        label_clientes.pack(padx=5, pady=5)
        self.labels.append(label_clientes)
        
        self.input_clientes = ttk.Combobox(left_frame)
        self.input_clientes.pack(padx=5, pady=5)
        self.input_clientes.set("Escolha o cliente")
        self.inputs.append(self.input_clientes)  
        
        clientes = self.db_manager.get_all_clientes()
        self.input_clientes['values'] = clientes
        print(clientes)
        
        # Despachantes
        label_despachantes = tk.Label(left_frame, text="Nome Despachantes:", font=COMMON_FONT, fg=FONT_COLOR, 
                bg=BACKGROUND_COLOR)
        label_despachantes.pack(padx=5,pady=5)
        self.labels.append(label_despachantes)
        
        self.input_despachantes = ttk.Combobox(left_frame)
        self.input_despachantes.pack(padx=5, pady=5)
        self.input_despachantes.set("Escolha o Despachante")
        self.inputs.append(self.input_despachantes)

        # Carregar despachantes no ComboBox
        despachantes = self.db_manager.get_all_despachantes()
        self.input_despachantes['values'] = despachantes
        print(despachantes)
        
        # Tipos de veículos
        label_type = tk.Label(left_frame, text="Tipo de Veiculo:", font=COMMON_FONT, fg=FONT_COLOR, 
                bg=BACKGROUND_COLOR)
        label_type.pack(padx=5, pady=5)
        self.labels.append(label_type)
        
        self.input_type = ttk.Combobox(left_frame)
        self.input_type.pack(padx=5, pady=5)
        self.input_type.set("Escolha o tipo")
        self.inputs.append(self.input_type)
        
        type_auto = self.db_manager.get_type_auto()
        self.input_type['values'] = type_auto
        
        # Operator
        label_operator = tk.Label(left_frame, text="Tipo de Veiculo:", font=COMMON_FONT, fg=FONT_COLOR, 
                bg=BACKGROUND_COLOR)
        label_operator.pack(padx=5, pady=5)
        self.labels.append(label_operator)
        
        self.input_operator = ttk.Combobox(left_frame)
        self.input_operator.pack(padx=5, pady=5)
        self.input_operator.set("Escolha o tipo")
        self.inputs.append(self.input_operator)
        
        operator = self.db_manager.get_all_operator()
        self.input_operator['values'] = operator
        
        # Placa
        label_auto_plate = tk.Label(left_frame, text="Placa do Veiculo:", font=COMMON_FONT, fg=FONT_COLOR, 
                bg=BACKGROUND_COLOR)
        label_auto_plate.pack(padx=5, pady=5)
        self.labels.append(label_auto_plate)
        
        self.input_auto_plate = ttk.Entry(left_frame)
        self.input_auto_plate.pack(padx=5, pady=5)
        self.inputs.append(self.input_auto_plate)
        
        #Valor
        label_value = tk.Label(left_frame, text="Valor R$:", font=COMMON_FONT, fg=FONT_COLOR, 
                bg=BACKGROUND_COLOR)
        label_value.pack(padx=5, pady=5)
        self.labels.append(label_value)
        
        self.input_value = ttk.Entry(left_frame)
        self.input_value.pack(padx=5, pady=5)
        self.inputs.append(self.input_value)
        
        # Label para exibir o valor total
        self.total_label = tk.Label(left_frame, text="Total R$: 0.00", fg="white", font=COMMON_FONT, bg=BACKGROUND_COLOR, width=30)
        self.total_label.pack(pady=10, padx=5)
        
        #Botões
        btn_create = tk.Button(left_frame, text="Salvar", command=self.create, bg='green', width=15)
        btn_create.pack(padx=10, pady=5)

        btn_update = tk.Button(left_frame, text="Atualizar", command=self.update, bg='orange', width=15)
        btn_update.pack(padx=10, pady=5)

        btn_delete = tk.Button(left_frame, text="Excluir", command=self.delete, bg='red', width=15)
        btn_delete.pack(padx=10, pady=5)

        btn_clear = tk.Button(left_frame, text="Limpar", command=self.limpar_campos, bg='yellow', width=15)
        btn_clear.pack(padx=10, pady=5)
        back_button = tk.Button(left_frame, text="Voltar para o Menu", command=self.return_to_menu, width=30)
        back_button.pack(padx=20,pady=5)
    
    def create_treeview(self):
        # Frame 50% à direita
        right_frame = tk.Frame(self.root, width=0.5 * self.root.winfo_screenwidth(),
                        height=0.5 * self.root.winfo_screenwidth(), bg=BACKGROUND_COLOR)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        columns = [
            # ('ID', 50),
            ("Cliente", 100),
            ("Despachante", 100),
            ("Tipo Veiculo", 100),
            ("Op. Caixa", 50),
            ("Placa Veiculo", 100),
            ("Valor", 100),
            ("Data", 100),
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
        
        # Configurar a função OnSelect para ser chamada quando um item do Treeview for selecionado
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Inicializar os dados no Treeview
        self.read()
    
    # def calculate_total(self):
    #     # Inicializa o total como zero
    #     total = 0.0
        
    #     # Obtém os valores dos campos de entrada e os soma ao total
    #     for entry in self.input_values:  # Supondo que self.input_values seja a lista que contém os campos de valor
    #         try:
    #             value = float(entry.get())
    #             total += value
    #         except ValueError:
    #             pass  # Ignora valores inválidos que não podem ser convertidos em float
    
    #     # Exibe o total no label
    #     self.total_label.config(text=f"Total R$: {total:.2f}")


    #O PROBLEMA ESTÁ AQUI    
    def create(self):
        data = {}
        for label, entry in zip(self.labels, self.inputs):
            field_name = label["text"].lower()  # Ajuste aqui para pegar o texto do rótulo
            field_value = entry.get()
            data[field_name] = field_value

        if not all(data.values()):
            messagebox.showerror("Cadastro em Tabela", "Por favor, preencha todos os campos.")
            return

        # Use db_manager para realizar operações no banco de dados
        try:
            self.db_manager.insert(self.table_name, data)
            messagebox.showinfo("Cadastro em Tabela", "Registro criado com sucesso.")
            self.limpar_campos()
            self.read()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir registro: {e}")
    # O PROBLEMA ESTÁ NESSAS FUNÇÕES
    def delete(self):
        if not self.selected_item:
            messagebox.showerror("Cadastro em Tabela", "Por favor, selecione um registro para excluir.")
            return
        
        result = messagebox.askquestion('Cadastro em Tabela', 'Você tem certeza que deseja excluir o registro?', icon="warning")
        if result == 'yes':
            condition = {self.db.id_column_name: self.selected_item}
            self.db.delete(self.table_name, condition)
            messagebox.showinfo("Cadastro em Tabela", "Registro excluído com sucesso.")
            self.limpar_campos()
            self.selected_item = None
            self.read()

    def limpar_campos(self):
        for entry in self.inputs:
            entry.delete(0, tk.END)

    def on_select(self, event):
        selected_item = self.tree.item(self.tree.selection())
        if selected_item and 'values' in selected_item:
            values = selected_item['values']
            # Certifique-se de que existem pelo menos 8 valores na lista
            if values and len(values) >= 7:  
                self.input_clientes.set(values[1])  
                self.input_despachantes.set(values[2])  
                self.input_type.set(values[3]) 
                self.input_operator.set(values[4])  
                self.input_auto_plate.delete(0, tk.END)
                self.input_auto_plate.insert(0, values[5])  
                self.input_value.delete(0, tk.END)
                self.input_value.insert(0, values[6])
            # Aqui, o índice 7 corresponderia à coluna da data, se necessário
                for entry, value in zip(self.inputs, values[0:]):
                    entry.delete(0, tk.END)
                    entry.insert(0, value)
                    
    def read(self):
        data = self.db_manager.select_all(self.table_name)
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert('', 'end', values=row[1:])

    def update(self):
        if not self.selected_item:
            messagebox.showerror("Cadastro em Tabela", "Por favor, selecione um registro para atualizar.")
            return
        data = {}
        for label, entry in zip(self.labels, self.inputs): ## O PROBLEMA ESTÁ AQUI
            field_name = label.cget("text").lower()
            field_value = entry.get()
            data[field_name] = field_value

        if not all(data.values()):
            messagebox.showerror("Cadastro em Tabela", "Por favor, preencha todos os campos.")
            return

        # Modifique a linha abaixo para obter o nome da coluna de identificação do DatabaseManager
        id_column_name = self.db.id_column_name

        # Atualize o registro com base na coluna de identificação
        self.db.update(self.table_name, data, {id_column_name: self.selected_item})
        messagebox.showinfo("Cadastro em Tabela", "Registro atualizado com sucesso.")
        self.limpar_campos()
        self.selected_item = None
        self.read()

    def return_to_menu(self):
        # Ocultar a janela atual
        self.root.withdraw()
        # Tornar a janela do menu visível
        menu_window = DatabaseMenu(self.root)

class PaymentWindow(BaseWindow):
    def __init__(self, root, db_manager):
        super().__init__(root, "Caixa", BACKGROUND_COLOR, fullscreen=True)
        self.service_type = "servico"
        self.db_manager = db_manager
        self.create_service_fields ()
        self.create_treeview()
    
    def create_service_fields(self):
        left_frame = tk.Frame(self.root, width=0.3*self.root.winfo_screenwidth(), 
                              height=self.root.winfo_screenheight(), bg=BACKGROUND_COLOR)
        left_frame.pack(side="left", fill="y")
        
        tk.Label(left_frame, text="Pagamento", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5, pady=10)
        
        image = Image.open("assets/images/icon_pagamento.png")
        image = image.resize((100,100))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(left_frame, image=photo, bg=BACKGROUND_COLOR)
        image_label.image = photo
        image_label.pack(pady=5,padx=100)
        
        #Clientes 
        tk.Label(left_frame, text="Nome Clientes", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5, pady=5)
        self.name_combobox = ttk.Combobox(left_frame)
        self.name_combobox.pack(padx=5, pady=5)
        self.name_combobox.set("Escolha o cliente")
        
        clientes = self.db_manager.get_all_clientes()
        self.name_combobox['values'] = clientes
        print(clientes)
        
        #despachantes
        tk.Label(left_frame, text="Nome Despachantes:", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5,pady=5)
        self.despachantes_name_combobox = ttk.Combobox(left_frame)
        self.despachantes_name_combobox.pack(padx=5, pady=5)
        self.despachantes_name_combobox.set("Escolha o Despachante")

        # Carregar despachantes no ComboBox
        despachantes = self.db_manager.get_all_despachantes()
        self.despachantes_name_combobox['values'] = despachantes
        print(despachantes)
        
        #Tipos de veiculos
        tk.Label(left_frame, text="Tipo de Veiculo:", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5, pady=5)
        self.type_combobox = ttk.Combobox(left_frame)
        self.type_combobox.pack(padx=5, pady=5)
        self.type_combobox.set("Escolha o tipo")
        
        type_auto = self.db_manager.get_type_auto()
        self.type_combobox['values'] = type_auto
        
        tk.Label(left_frame, text="Placa do Veiculo:", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5, pady=5)
        self.auto_plate = ttk.Entry(left_frame)
        self.auto_plate.pack(padx=5, pady=5)
        
        tk.Label(left_frame, text="Valor R$:", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5, pady=5)
        self.valor = ttk.Entry(left_frame)
        self.valor.pack(padx=5, pady=5)
        
        # Label para exibir o valor total
        self.total_label = tk.Label(left_frame, text="Total: 0.00", fg="white", font=COMMON_FONT, bg=BACKGROUND_COLOR, width=30)
        self.total_label.pack(pady=10, padx=20)
        
        #Botões
        btn_create = tk.Button(left_frame, text="Salvar", bg='green', width=15)
        btn_create.pack(padx=10, pady=10)
        btn_update = tk.Button(left_frame, text="Atualizar", bg='orange', width=15)
        btn_update.pack(padx=10, pady=10)
        btn_delete = tk.Button(left_frame, text="Excluir", bg='red', width=15 )
        btn_delete.pack(padx=10, pady=10)
        btn_clear = tk.Button(left_frame, text="Limpar",  bg='yellow', width=15)
        btn_clear.pack(padx=10, pady=10)
        back_button = tk.Button(left_frame, text="Voltar para o Menu", command=self.return_to_menu, width=30)
        back_button.pack(pady=10, padx=20)
    
    def create_treeview(self):
        # Frame 50% à direita
        right_frame = tk.Frame(self.root, width=0.5 * self.root.winfo_screenwidth(),
                        height=0.5 * self.root.winfo_screenwidth(), bg=BACKGROUND_COLOR)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        columns = [
            ("Data", 100),
            ("Cliente", 100),
            ("Despachante", 100),
            ("Tipo Veiculo", 100),
            ("Placa Veiculo", 100),
            ("Valor", 100),
            ("Op. Caixa", 50),
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
    
    def return_to_menu(self):
        # Ocultar a janela atual
        self.root.withdraw()
        # Tornar a janela do menu visível
        menu_window = DatabaseMenu(self.root)

    
from menu import DatabaseMenu        
if __name__ == "__main__":
    root = tk.Tk()
    db_manager = DatabaseManager(DATABASE_NAME)
    table_name = 'servico'
    services_window = ServicesWindow(root, db_manager,table_name)
    #payment_window = PaymentWindow(root, db_manager)
    
    # data_to_insert = {
    # 'id_cliente': 1,
    # 'id_despachante': 2,
    # 'id_tipo_veiculo': 3,
    # 'id_op_caixa': 4,
    # 'placa': 'ABC1234',
    # 'valor_servico': 100.00,
    # 'data_entrada': '2023-11-26'
    # }
    # # Agora, supondo que você tenha uma instância da classe DatabaseManager chamada db_manager
    # # Você chamaria a função insert assim:
    # table_name = 'servico'
    # db_manager.insert(table_name, data_to_insert)
    # print (db_manager)
    root.mainloop()

    
import tkinter as tk
from tkinter import ttk,messagebox
from database import DatabaseManager
from config import *
from PIL import Image, ImageTk

class ServicesWindow(BaseWindow):
    def __init__(self, root, db_manager,table_name):
        super().__init__(root, "Cadastrar Serviço", BACKGROUND_COLOR, fullscreen=True)
        self.table_name = "servico_cliente" #o problema tb está aqui
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
        btn_create = tk.Button(left_frame, text="Salvar",  bg='green', width=15)
        btn_create.pack(padx=10, pady=5)

        btn_update = tk.Button(left_frame, text="Atualizar",  bg='orange', width=15)
        btn_update.pack(padx=10, pady=5)

        btn_delete = tk.Button(left_frame, text="Excluir",  bg='red', width=15)
        btn_delete.pack(padx=10, pady=5)

        btn_clear = tk.Button(left_frame, text="Limpar",  bg='yellow', width=15)
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
    
    


    def on_select(self, event):
            selected_item = self.tree.item(self.tree.selection())
            if selected_item and 'values' in selected_item:
                values = selected_item['values']
                if values:  # Verifica se a lista de valores não está vazia
                    self.selected_item = values[0]
                    for entry, value in zip(self.inputs, values[0:]):
                        entry.delete(0, tk.END)
                        entry.insert(0, value)
                        
    # Função para criar um novo registro
    def create(self, data):
        query = """
        INSERT INTO servico_cliente (id_cliente, id_tipo_veiculo_cliente, id_op_caixa_cliente, placa, valor_servico)
        VALUES (%s, %s, %s, %s, %s)
        """
        data = {
        # Outros campos...
        'id_cliente': self.selected_client_id,  # Usando o ID selecionado
        # Mais campos...
        }
        try:
            self.db_manager.execute_query(query, data)
            messagebox.showinfo("Cadastro em Tabela", "Registro criado com sucesso.")
            self.limpar_campos()
            self.read()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir registro: {e}")

    # Função para ler os registros da tabela
    def read(self):
        query = "SELECT * FROM view_servico_cliente"
        data = self.db_manager.select(query)
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert('', 'end', values=row)

    # Função para atualizar um registro
    def update(self, data, condition):
        query = """
        UPDATE servico_cliente
        SET id_cliente = %s, id_tipo_veiculo_cliente = %s,
            id_op_caixa_cliente = %s, placa = %s, valor_servico = %s
        WHERE id_servico_cliente = %s
        """
        try:
            self.db_manager.execute_query(query, data + condition)
            messagebox.showinfo("Cadastro em Tabela", "Registro atualizado com sucesso.")
            self.limpar_campos()
            self.selected_item = None
            self.read()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar registro: {e}")

    # Função para excluir um registro
    def delete(self, condition):
        query = "DELETE FROM servico_cliente WHERE id_servico_cliente = %s"
        try:
            self.db_manager.execute_query(query, condition)
            messagebox.showinfo("Cadastro em Tabela", "Registro excluído com sucesso.")
            self.limpar_campos()
            self.selected_item = None
            self.read()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir registro: {e}")

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

    
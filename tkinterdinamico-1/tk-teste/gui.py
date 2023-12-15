#Esse código cria um combobox que puxa dados do banco

import tkinter as tk
from tkinter import ttk, messagebox
from database import *
from config import *
from PIL import Image, ImageTk
import time

class DynamicGUI(BaseWindow):
    def __init__(self, root, table_name, db_manager, selected_window):
        super().__init__(root, f"Cadastro em Tabela: {table_name}", BACKGROUND_COLOR, fullscreen=True)
        self.table_name = table_name
        self.db_manager = db_manager
        self.table_structure = self.db_manager.get_table_structure(table_name)
        # Variáveis
        self.selected_item = None
        self.selected_window = selected_window
        # Cria os rótulos (labels) e as entradas (inputs) com base nos campos da tabela
        self.labels = []
        self.inputs = []
        # Cria campos de consulta
        self.create_report_fields()
        # Cria um Treeview
        self.create_treeview()

    def create_report_fields(self):
        self.selected_client_id = None
        # Frame 30% à esquerda
        left_frame = tk.Frame(self.root, width=0.3 * self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), bg=BACKGROUND_COLOR)
        left_frame.pack(side="left", fill="y")
        combobox = None 
        tk.Label(left_frame, text=f"{self.table_name}", font=COMMON_FONT, fg=FONT_COLOR, 
                 bg=BACKGROUND_COLOR).pack(padx=5, pady=10)
        
        # Exiba a imagem da janela selecionada
        if self.selected_window in table_icons:
            image_path = table_icons[self.selected_window]
            image = Image.open(image_path)
            image = image.resize((50, 50))
            photo = ImageTk.PhotoImage(image)

            # Label para exibir a imagem
            image_label = tk.Label(left_frame, image=photo, bg=BACKGROUND_COLOR)
            image_label.image = photo
            image_label.pack(pady=5, padx=100)

        # Verifica se a estrutura da tabela é uma lista e a converte em uma lista de nomes de campos
        if isinstance(self.table_structure, list):
            self.field_names = [field[0] for field in self.table_structure]
            data_atual = time.strftime('%Y-%m-%d', time.localtime())
            data_atual_str = str(data_atual)

        for i, field_name in enumerate(self.field_names[1:], start=1):
            label = tk.Label(left_frame, text=field_name.capitalize(), font=COMMON_FONT, fg=FONT_COLOR, bg=BACKGROUND_COLOR, width=15)
            label.pack(padx=5, pady=5)
            
            if field_name == 'id_cliente' and self.table_name == 'servico_cliente':
                combobox = ttk.Combobox(left_frame, values=self.get_client_values(), width=27)
                combobox.pack(padx=5, pady=5)
                combobox.bind("<<ComboboxSelected>>", self.on_cliente_selection)
                self.labels.append(label)
                self.inputs.append(combobox)  # Adiciona o ComboBox às entradas
            else:
                entry = tk.Entry(left_frame, width=30)
                entry.pack(padx=5, pady=5)
                self.labels.append(label)
                self.inputs.append(entry)
                
        btn_create = tk.Button(left_frame, text="Salvar", command=self.create, bg='green', width=15)
        btn_create.pack(padx=10, pady=5)
        btn_update = tk.Button(left_frame, text="Atualizar", command=self.update, bg='orange', width=15)
        btn_update.pack(padx=10, pady=5)
        btn_delete = tk.Button(left_frame, text="Excluir", command=self.delete, bg='red', width=15)
        btn_delete.pack(padx=10, pady=5)
        btn_clear = tk.Button(left_frame, text="Limpar", command=self.limpar_campos, bg='yellow', width=15)
        btn_clear.pack(padx=10, pady=5)
        # Botão de voltar
        back_button = tk.Button(left_frame, text="Voltar para o Menu", command=self.return_to_menu, width=15)
        back_button.pack(padx=10, pady=5)

    def create_treeview(self):
        right_frame = tk.Frame(self.root, width=0.5 * self.root.winfo_screenwidth(),
                        height=self.root.winfo_screenwidth(), bg=BACKGROUND_COLOR)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Treeview
        self.tree = ttk.Treeview(right_frame, columns=(self.field_names), show="headings", selectmode="browse")
        
        for field_name in self.field_names:
            self.tree.heading(field_name, text=field_name.capitalize(), anchor='center')
            self.tree.column(field_name, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=1, padx=20, pady=15)

        # Configurar uma barra de rolagem vertical para o Treeview
        scrollbar_y = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y", padx=20)

        # Configurar uma barra de rolagem horizontal para o Treeview
        scrollbar_x = ttk.Scrollbar(right_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x", pady=20)

        # Configurar a função OnSelect para ser chamada quando um item do Treeview for selecionado
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Inicializar os dados no Treeview
        self.read()

    def get_client_id(self, nome_cliente):
        selected_cliente = self.inputs[1].get()  # Obtém o valor do ComboBox

        if selected_cliente:
            # Obtém o id_cliente com base no nome do cliente
            id_cliente = self.db_manager.get_client_id(selected_cliente)
            return self.db_manager.get_client_id(nome_cliente)
        else:
            return None
        
    def create(self):
        data = {}
        for label, entry in zip(self.labels, self.inputs):
            field_name = label.cget("text").lower()
            field_value = entry.get()

            if field_name == 'id_cliente' and self.table_name == 'servico_cliente':
                # Obtém o id_cliente com base no nome do cliente
                client_id = self.get_client_id(field_value)

                if client_id is not None:
                    field_value = client_id
                else:
                    print("Por favor, selecione um cliente.")
                    return

            if self.table_name == 'servico_cliente' and field_name == 'data_entrada':
                data_atual = time.localtime()
                field_value = f"{data_atual.tm_year}-{data_atual.tm_mon:02d}-{data_atual.tm_mday:02d}"

            data[field_name] = field_value

        if not all(data.values()):
            messagebox.showerror("Cadastro em Tabela", "Por favor, preencha todos os campos.")
            return

        self.db_manager.insert(self.table_name, data)
        messagebox.showinfo("Cadastro em Tabela", "Registro criado com sucesso.")
        self.limpar_campos()
        self.read()

    def delete(self):
        if not self.selected_item:
            messagebox.showerror("Cadastro em Tabela", "Por favor, selecione um registro para excluir.")
            return

        result = messagebox.askquestion('Cadastro em Tabela', 'Você tem certeza que deseja excluir o registro?', icon="warning")
        if result == 'yes':
            condition = {self.db_manager.id_column_name: self.selected_item}
            self.db_manager.delete(self.table_name, condition)
            messagebox.showinfo("Cadastro em Tabela", "Registro excluído com sucesso.")
            self.limpar_campos()
            self.selected_item = None
            self.read()

    def limpar_campos(self):
        for entry in self.inputs:
            entry.delete(0, tk.END)

    def get_client_values(self):
        try:
            # Substitua 'seu_usuario', 'sua_senha' e 'tcc_top3' pelas credenciais do seu banco de dados
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='tcc_top3'
            )
            cursor = connection.cursor()

            # Execute uma consulta para obter os nomes dos clientes
            cursor.execute("SELECT nome_cliente FROM cliente")
            result = cursor.fetchall()

            # Feche a conexão com o banco de dados
            connection.close()

            # Extraia os nomes dos clientes da lista de tuplas
            nome_clientes = [row[0] for row in result]

            return nome_clientes
        
        except Exception as e:
            print(f"Erro ao obter valores de clientes: {e}")
            return []
    

    def on_select(self, event):
        selected_item = self.tree.item(self.tree.selection())
        if selected_item and 'values' in selected_item:
            values = selected_item['values']
            if values:
                self.selected_item = values[0]
                for entry, value in zip(self.inputs, values[1:]):
                    entry.delete(0, tk.END)
                    entry.insert(0, value)


    def on_cliente_selection(self, event):
        selected_cliente = self.inputs[1].get()  # Agora, pegamos o valor do ComboBox

        if selected_cliente:
            # Ajuste: passe o nome do cliente como condição
            data = self.db_manager.select_related_data('cliente', 'nome_cliente', selected_cliente)
            
            self.tree.delete(*self.tree.get_children())

            for row in data:
                self.tree.insert('', 'end', values=row)

    def read(self):
        if self.table_name == 'servico_cliente':
            self.read_view()
        else:
            data = self.db_manager.select_all(self.table_name)
            self.tree.delete(*self.tree.get_children())
            for row in data:
                self.tree.insert('', 'end', values=row)

    def read_view(self):
        if self.table_name == 'servico_cliente':
            query = "SELECT * FROM view_servico_cliente"
        data = self.db_manager.execute_query(query)
        self.tree.delete(*self.tree.get_children())

        for row in data:
            self.tree.insert('', 'end', values=row)

    def update(self):
        if not self.selected_item:
            messagebox.showerror("Cadastro em Tabela", "Por favor, selecione um registro para atualizar.")
            return
        data = {}
        for label, entry in zip(self.labels, self.inputs):
            field_name = label.cget("text").lower()
            field_value = entry.get()
            data[field_name] = field_value

        if not all(data.values()):
            messagebox.showerror("Cadastro em Tabela", "Por favor, preencha todos os campos.")
            return

        id_column_name = self.db_manager.id_column_name
        data = {key: value for key, value in data.items() if value}

        self.db_manager.update(self.table_name, data, {id_column_name: self.selected_item})
        messagebox.showinfo("Cadastro em Tabela", "Registro atualizado com sucesso.")
        self.limpar_campos()
        self.selected_item = None
        self.read()

    def return_to_menu(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    db_manager_manager = DatabaseManager(DATABASE_NAME)
    #app = DynamicGUI(root, "cliente", db_manager_manager, "nome_da_sua_janela")
    root.mainloop()



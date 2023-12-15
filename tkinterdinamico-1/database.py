import mysql.connector

class DatabaseManager:
    def __init__(self, db_name):
        self.report_windows = {'individual': None, 'geral': None}
        self.services_windos = {'servico': None, 'entrada': None}
        self.conn = mysql.connector.connect(
            host='localhost', user='root', password='')
        self.cursor = self.conn.cursor()
        self.db_name = db_name
        self.create_database()
        self.conn.database = db_name
        self.id_column_name = 'id'
        self.id_column_names = {
            'cliente': 'id_cliente',
            'entrada': 'id_entrada',
            'forma_pagamento': 'id_forma_pagamento',
            'operador_caixa': 'id_op_caixa',
            'saida': 'id_saida',
            'servico_cliente': 'id_servico_cliente',
            'tipo_veiculo': 'id_tipo_veiculo'    
        }

    def select_related_data(self, table_name, related_column, condition_value):
        try:
            id_column_name = self.get_id_column_name(table_name)
            # Verifique se a tabela é 'cliente' e ajuste a coluna relacionada
            if table_name == 'cliente':
                related_column = 'nome_cliente'
            query = f"SELECT * FROM {table_name} WHERE {related_column} = %s"
            values = (condition_value,)
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao selecionar dados relacionados de {table_name}: {e}")
            return []

    def create_database(self):
        try:
            self.cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
        except Exception as e:
            print(f"Erro ao criar banco de dados: {e}")

    def create_table(self, table_name, table_definition):
        try:
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ({table_definition})")
        except Exception as e:
            print(f"Erro ao criar tabela {table_name}: {e}")

    def create_all_tables(self):
        # Define as tabelas e suas estruturas aqui
        tables = {
            'cliente': (
                'id_cliente INT NOT NULL PRIMARY KEY AUTO_INCREMENT',
                'nome_cliente VARCHAR(50) NOT NULL',
                'doc_cliente VARCHAR(14) NOT NULL',
                'tipo_cliente Varchar(11) NOT NULL'
            ),
            'entrada': (
                'id_entrada INT NOT NULL PRIMARY KEY AUTO_INCREMENT',
                'id_servico_cliente INT',
                'id_forma_pagamento INT',
                'valor FLOAT',
                'status_p TINYINT(1)',
            ),
            'forma_pagamento': (
                'id_forma_pagamento INT NOT NULL PRIMARY KEY AUTO_INCREMENT',
                'nome_forma_pagamento VARCHAR(45) DEFAULT NULL'
            ),
            'operador_caixa': (
                'id_op_caixa INT NOT NULL PRIMARY KEY AUTO_INCREMENT',
                'nome_op_caixa VARCHAR(30)',
                'id_usuario INT'
            ),
            'saida': (
                'id_saida INT NOT NULL PRIMARY KEY AUTO_INCREMENT',
                'data_saida DATE',
                'descricao_saida TEXT',
                'valor_saida float ',
                'id_op_caixa INT'
            ),
            'tipo_veiculo': (
                'id_tipo_veiculo INT NOT NULL PRIMARY KEY AUTO_INCREMENT',
                'nome VARCHAR(20) NOT NULL'
            ),
            'servico_cliente': (
                'id_servico_cliente INT AUTO_INCREMENT PRIMARY KEY',
                'id_cliente INT',
                'id_tipo_veiculo_cliente INT',
                'id_op_caixa_cliente INT',
                'placa VARCHAR(7) NOT NULL',
                'valor_servico Float NOT NULL',
                'data_entrada DATE'
            ),
            'tipo_veiculo': (
                'id_tipo_veiculo INT NOT NULL PRIMARY KEY AUTO_INCREMENT',
                'nome VARCHAR(20) NOT NULL',
            ),
            'usuario': (
                'id_usuario INT NOT NULL PRIMARY KEY AUTO_INCREMENT',
                'username VARCHAR(30)',
                'senha VARCHAR(16)'
            )
        }
        for table_name, table_definition in tables.items():
            self.create_table(table_name, ', '.join(table_definition))
    def authenticate_user(self, username, password):
        try:
            query = "SELECT * FROM usuario WHERE username = %s AND senha = %s"
            values = (username, password)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"Erro ao autenticar usuário: {e}")
            return False


    def insert(self, table_name, data):
        try:
            placeholders = ', '.join(['%s'] * len(data))
            columns = ', '.join(data.keys())
            values = tuple(data.values())
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            print(f"Query SQL: {query}")
            print(f"Valores: {values}")
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erro ao inserir registro em {table_name}: {e}")
            self.conn.rollback()

    def update(self, table_name, data, condition):
        try:
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            print(set_clause)
            condition_clause = ' AND '.join(
                [f"{key} = %s" for key in condition.keys()])
            print(condition_clause)
            values = tuple(list(data.values()) + list(condition.values()))
            print(data.values())
            print(condition.values())
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_clause}"
            print ()
            print (values)
            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar registro em {table_name}: {e}")
            self.conn.rollback()

    def read(self, table_name, condition=None):
        try:
            if condition:
                condition_clause = ' AND '.join(
                    [f"{key} = %s" for key in condition.keys()])
                values = tuple(condition.values())
                query = f"SELECT * FROM {table_name} WHERE {condition_clause}"
                self.cursor.execute(query, values)
            else:
                query = f"SELECT * FROM {table_name}"
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao ler registros de {table_name}: {e}")

    def delete(self, table_name, condition):
        try:
            condition_clause = ' AND '.join(
                [f"{key} = %s" for key in condition.keys()])
            values = tuple(condition.values())
            query = f"DELETE FROM {table_name} WHERE {condition_clause}"
            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao excluir registro de {table_name}: {e}")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def get_table_structure(self, table_name):
        try:
            self.cursor.execute(f"DESCRIBE {table_name}")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao obter estrutura da tabela {table_name}: {e}")
            return []

    def get_id_column_name(self, table_name):
        return self.id_column_names.get(table_name, 'id')

    def set_id_column_name(self, table_name):
        self.id_column_name = self.id_column_names.get(table_name, 'id')

    def select_all(self, table_name):
        try:
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(
                f"Erro ao selecionar todos os registros de {table_name}: {e}")
            
    #Este método faz uma consulta para obter o id_clientea com base no nome_cliente fornecido.
    def get_client_id(self, client_name):
        try:
            query = "SELECT id_cliente FROM cliente WHERE nome_cliente = %s"
            values = (client_name,)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Erro ao obter id_cliente: {e}")
            return None
        
     #Este método faz uma consulta para obter o id_op_caixa com base no nome fornecido.   
    def get_op_caixa_id(self, nome_op_caixa):
        try:
            query = f"SELECT id_op_caixa FROM op_caixa WHERE nome_op_caixa = '{nome_op_caixa}'"
            result = self.execute_query(query)
            return result[0][0] if result else None
        except Exception as e:
            print(f"Erro ao obter id_op_caixa: {e}")
            return None

    #Este método faz uma consulta para obter o id_tipo_veiculo base no tipo_veiculo fornecido.    
    def get_tipo_veiculo_id(self, nome):
        try:
            query = f"SELECT id_tipo_veiculo FROM tipo_veiculo WHERE nome = '{nome}'"
            result = self.execute_query(query)
            return result[0][0] if result else None
        except Exception as e:
            print(f"Erro ao obter id_tipo_veiculo: {e}")
            return None
        
    #Este método faz uma consulta para obter o id_forma_pagamento base no nome_forma_pagamento fornecido.
    def get_forma_pagamento_id(self, nome_forma_pagamento):
        try:
            query = f"SELECT id_forma_pagamento FROM forma_pagamento WHERE nome_forma_pagamento = '{nome_forma_pagamento}'"
            result = self.execute_query(query)
            return result[0][0] if result else None
        except Exception as e:
            print(f"Erro ao obter id_forma_pagamento: {e}")
            return None

    #Este método faz uma consulta para obter o id_forma_pagamento base no nome_forma_pagamento fornecido.
    def get_servico_cliente_id(self, nome_cliente):
        try:
            query = f"SELECT id_servico_cliente FROM servico_cliente INNER JOIN cliente ON servico_cliente.id_cliente = cliente.id_cliente WHERE cliente.nome_cliente = '{nome_cliente}'"
            result = self.execute_query(query)
            return result[0][0] if result else None
        except Exception as e:
            print(f"Erro ao obter id_servico_cliente: {e}")
            return None

    

    def get_all_clientes(self):
        try:
            query = "SELECT nome_cliente FROM cliente"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Erro ao buscar os clientes: {e}")
            return []
    
    def get_type_auto(self):
        try:
            query = "SELECT nome FROM tipo_veiculo"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Erro ao buscar o tipo de veículo: {e}")
            return []
    
    def get_all_operator(self):
        try:
            query = "SELECT nome_op_caixa FROM op_caixa"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Erro ao buscar o tipo de veículo: {e}")
            return []
        
    def get_all_exits(self):
        try:
            query = "SELECT * FROM op_caixa"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Erro ao buscar o tipo de veículo: {e}")
            return []
        
    def execute_query(self, query, *params):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results
    
if __name__ == "__main__":
    db_name = 'tcc_top3'
    db_manager = DatabaseManager(db_name)
    db_manager.create_all_tables()

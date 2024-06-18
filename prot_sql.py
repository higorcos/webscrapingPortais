import sqlite3

# Conecte-se ao banco de dados SQLite (criará um novo banco de dados se não existir)
conn = sqlite3.connect('Diários/DiárioOficial-TecnologiaUpdate/exemplo.db')

# Crie um cursor para executar comandos SQL
cursor = conn.cursor()

# Defina uma instrução SQL para criar uma tabela (opcional)
create_table_query = '''
CREATE TABLE IF NOT EXISTS diario_oficial (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    tipo_modulo TEXT,
    tipo_arquivo TEXT,
    link TEXT,
    caminho TEXT,
    status TEXT
)
'''


cursor.execute(create_table_query)

# Defina os dados para inserir
dados_usuario = ('nome-1','Arquivo de licitação','Anexo','https','/pasta/pasta','sucesso')

# Defina uma instrução SQL para inserir dados na tabela
insert_query = '''
INSERT INTO diario_oficial (nome,tipo_modulo,tipo_arquivo,link,caminho,status)
VALUES (?,?,?,?,?,?)
'''

# Execute a instrução SQL para inserir os dados
cursor.execute(insert_query, dados_usuario)

# Faça o commit para salvar as alterações no banco de dados
conn.commit()

# Feche a conexão com o banco de dados
conn.close()



from ePCA.Model.db import create_connection

def inserir_cidade(conn, value):
    """ Verificar """
    result = cidade_existe(conn,value)
    if result:
        print(f"A cidade {value} existe na tabela.")
        return result
    else:
        print(f"A cidade {value} não existe na tabela.")
        """ Insert """
        sql = '''INSERT INTO Cidade(Nome) VALUES(?)'''
        cur = conn.cursor()
        cur.execute(sql, value)
        conn.commit()
        return cur.lastrowid
def cidade_existe(conn,ano):
    sql = '''SELECT Cidade.Id FROM Cidade WHERE Nome = ?'''
    cur = conn.cursor()
    cur.execute(sql, ano)
    result = cur.fetchone()
    if result is not None:
        result = result[0]
    return result
def selecionar_cidades(conn):
    """ Query all rows in the employees table """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Cidade")

    rows = cur.fetchall()

    for row in rows:
        print(row)
def update_cidades(conn, employee):
    """ Update age and department of an employee """
    sql = ''' UPDATE employees
              SET age = ? ,
                  department = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, employee)
    conn.commit()

def main():
    database = "test2.db"

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        cidade = ['São Luis']
        resultInsert = inserir_cidade(conn, cidade)
        print("ID CIDADE: ", resultInsert)

        #selecionar_cidades(conn)

    else:
        print("Error! Cannot create the database connection.")


if __name__ == '__main__':
    main()

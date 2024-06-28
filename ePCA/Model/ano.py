from ePCA.Model.db import create_connection

def inserir_ano(conn, value):
    """ Verificar """
    result = ano_existe(conn, value)
    if result:
        #print(f"O ano {value} existe na tabela.")
        return result
    else:
        print(f"O ano {value} não existe na tabela.")
        """ Insert """
        sql = '''INSERT INTO Ano(ANO) VALUES(?)'''
        cur = conn.cursor()
        cur.execute(sql, value)
        conn.commit()
        return cur.lastrowid
def ano_existe(conn,ano):
    sql = '''SELECT Ano.Id FROM Ano WHERE ANO = ?'''
    cur = conn.cursor()
    cur.execute(sql, ano)
    result = cur.fetchone()
    if result is not None:
        result = result[0]
    return result
def selecionar_anos(conn):
    """ Query all rows in the employees table """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Ano")

    rows = cur.fetchall()
    return rows
def update_ano(conn, employee):
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
        ano_1 = [2032]
        resultInsert = inserir_ano(conn, ano_1)
        print('ID ANO: ',resultInsert)
        #selecionar_anos(conn)

    else:
        print("Error! Cannot create the database connection.")


if __name__ == '__main__':
    main()

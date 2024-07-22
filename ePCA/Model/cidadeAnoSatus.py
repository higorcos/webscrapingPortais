from ePCA.Model.db import create_connection

def inserir_cidadeAnoStatus(conn, value):
    """ Verificar """
    result = cidadeAnoStatus_existe(conn,value)
    if result:
        #print(f"O {value} já existe na tabela.")
        return result

    """ Insert """
    sql = '''INSERT INTO CidadeAnoStatus (idCidade, idAno, status) VALUES(?, ?, 'adicionou e iniciou') '''
    cur = conn.cursor()
    cur.execute(sql, value)
    conn.commit()
    return cur.lastrowid
def cidadeAnoStatus_existe(conn,ano):
    sql = '''SELECT CidadeAnoStatus.idCidadeAnoStatus FROM CidadeAnoStatus WHERE idCidade= ? AND idAno = ?'''
    cur = conn.cursor()
    cur.execute(sql, ano)
    result = cur.fetchone()
    if result is not None:
        result = result[0]
    return result
def cidadeAnoStatus_existeStatus(conn,ano):
    sql = '''SELECT CidadeAnoStatus.idCidadeAnoStatus FROM CidadeAnoStatus WHERE idCidade= ? AND idAno = ? AND status='finalizado' '''
    cur = conn.cursor()
    cur.execute(sql, ano)
    result = cur.fetchone()
    if result is not None:
        result = result[0]
    return result
def selecionar_cidadesAnoStatus(conn):
    """ Query all rows in the employees table """
    cur = conn.cursor()
    cur.execute('''SELECT cas.idCidadeAnoStatus, c.Nome, a.Ano, cas.status 
                FROM CidadeAnoStatus cas
                inner join Cidade c 
                on c.Id = cas.idCidade 
                inner JOIN Ano a 
                on a.Id = cas.idAno ''')

    rows = cur.fetchall()
    return rows
def selecionar_cidadesAnoStatusEspecifico(conn,dados):
    """ Query all rows in the employees table """
    cur = conn.cursor()
    cur.execute('''
        SELECT 
            CidadeAnoStatus.idCidadeAnoStatus as id,
            Cidade.Nome AS NomeCidade,
            Ano.ANO AS Ano,
            CidadeAnoStatus.status AS Status
        FROM 
            CidadeAnoStatus
        JOIN 
            Cidade ON CidadeAnoStatus.idCidade = Cidade.Id
        JOIN 
            Ano ON CidadeAnoStatus.idAno = Ano.Id
        WHERE 
            Cidade.Nome = ? 
            AND Ano.ANO = ? 
            ''', dados)

    rows = cur.fetchall()

    return rows
def selecionar_cidadesAnoStatusEspecificoID(conn,dados):
    """ Query all rows in the employees table """
    cur = conn.cursor()
    cur.execute('''
        SELECT 
            Cidade.Nome AS NomeCidade,
            Ano.ANO AS Ano,
            CidadeAnoStatus.status AS Status
        FROM 
            CidadeAnoStatus
        JOIN 
            Cidade ON CidadeAnoStatus.idCidade = Cidade.Id
        JOIN 
            Ano ON CidadeAnoStatus.idAno = Ano.Id
        WHERE 
            CidadeAnoStatus.idCidadeAnoStatus = ?
            ''', dados)

    rows = cur.fetchall()

    return rows
def update_cidadesAnoStatus(conn, employee):
    """ Update age and department of an employee """
    sql = '''
            UPDATE CidadeAnoStatus
            SET status = ?
            WHERE CidadeAnoStatus.idCidadeAnoStatus = ?;
        '''
    cur = conn.cursor()
    cur.execute(sql, employee)
    conn.commit()
    print('Atualizou status ')
def main():
    database = "test2.db"

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        CidadeAnoStatus = [1,3]
        resultInsert = inserir_cidadeAnoStatus(conn, CidadeAnoStatus)
        print(resultInsert)
        resultadoVerificarSeExiste=cidadeAnoStatus_existe(conn,[1,1])
        #print(resultadoVerificarSeExiste)
        a1 = selecionar_cidadesAnoStatus(conn)
        a2 = selecionar_cidadesAnoStatusEspecifico(conn, ['São Luis', 2222])
        a3 = selecionar_cidadesAnoStatusEspecificoID(conn, [2]);

        #update_cidadesAnoStatus(conn,['ad',2])

    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()

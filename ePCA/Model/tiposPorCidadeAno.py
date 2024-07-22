from ePCA.Model.db import create_connection


def inserir_tipoEsubtipoPorCidadeEano(conn, value):
    """ Verificar """
    result = tipoEsubtipoPorCidadeEano_existe(conn, value)
    if result:
        return result

    """ Insert """
    sql = '''INSERT INTO tipoEsubtipoPorCidadeEano (idCidadeAnoStatus, status, nomeTipo, nomeSubtipo) VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, value)
    conn.commit()
    return cur.lastrowid


def tipoEsubtipoPorCidadeEano_existe(conn, tipo):
    sql = '''SELECT idtipo FROM tipoEsubtipoPorCidadeEano WHERE idCidadeAnoStatus = ? AND nomeTipo = ? AND nomeSubtipo = ?'''
    cur = conn.cursor()
    cur.execute(sql, tipo)
    result = cur.fetchone()
    if result is not None:
        result = result[0]
    return result


def selecionar_tiposEsubtiposPorCidadeEano(conn):
    """ Query all rows in the tipoEsubtipoPorCidadeEano table """
    cur = conn.cursor()
    cur.execute('''
        SELECT 
            t.idtipo, 
            cas.idCidadeAnoStatus, 
            t.status, 
            t.nomeTipo, 
            t.nomeSubtipo
        FROM 
            tipoEsubtipoPorCidadeEano t
        INNER JOIN 
            CidadeAnoStatus cas ON t.idCidadeAnoStatus = cas.idCidadeAnoStatus
    ''')
    rows = cur.fetchall()
    return rows


def selecionar_tiposEsubtiposPorCidadeEanoEspecifico(conn, dados):
    """ Query specific rows in the tipoEsubtipoPorCidadeEano table """
    cur = conn.cursor()
    cur.execute('''
        SELECT 
            t.idtipo, 
            cas.idCidadeAnoStatus, 
            t.status, 
            t.nomeTipo, 
            t.nomeSubtipo
        FROM 
            tipoEsubtipoPorCidadeEano t
        INNER JOIN 
            CidadeAnoStatus cas ON t.idCidadeAnoStatus = cas.idCidadeAnoStatus
        WHERE 
            t.nomeTipo = ? AND t.nomeSubtipo = ?
    ''', dados)
    rows = cur.fetchall()
    return rows


def update_tipoEsubtipoPorCidadeEano(conn, tipo):
    """ Update status, nomeTipo, and nomeSubtipo of a tipoEsubtipoPorCidadeEano """
    sql = '''
            UPDATE tipoEsubtipoPorCidadeEano
            SET status = ?, nomeTipo = ?, nomeSubtipo = ?
            WHERE idtipo = ?;
        '''
    cur = conn.cursor()
    cur.execute(sql, tipo)
    conn.commit()
    print('Atualizou tipo e subtipo por cidade e ano')


def main():
    database = "test2.db"

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        tipoEsubtipo = [1, 'ativo', 'Tipo1', 'Subtipo1']
        resultInsert = inserir_tipoEsubtipoPorCidadeEano(conn, tipoEsubtipo)
        print(resultInsert)
        resultadoVerificarSeExiste = tipoEsubtipoPorCidadeEano_existe(conn, [1, 'Tipo1', 'Subtipo1'])
        print(resultadoVerificarSeExiste)
        a1 = selecionar_tiposEsubtiposPorCidadeEano(conn)
        a2 = selecionar_tiposEsubtiposPorCidadeEanoEspecifico(conn, ['Tipo1', 'Subtipo1'])

        # Atualizar exemplo
        update_tipoEsubtipoPorCidadeEano(conn, ['finalizado', 'Tipo1Atualizado', 'Subtipo1Atualizado', 1])

    else:
        print("Error! Cannot create the database connection.")


if __name__ == '__main__':
    main()

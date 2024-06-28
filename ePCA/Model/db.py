import sqlite3


def create_connection(db_file="model_EPCA.db"):
    """ create a database connection to the SQLite database
        specified by db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
    except sqlite3.Error as e:
        print(e)
    return conn


def create_tables(conn):
    """ create a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Cidade (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Nome TEXT NOT NULL
                    );''')
        c.execute('''
                    CREATE TABLE IF NOT EXISTS Ano (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ANO INTEGER NOT NULL
                    );
                    ''')
        c.execute('''
                CREATE TABLE IF NOT EXISTS CidadeAnoStatus (
                idCidadeAnoStatus INTEGER PRIMARY KEY AUTOINCREMENT,
                idCidade INTEGER NOT NULL,
                idAno INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (idCidade) REFERENCES Cidade (Id),
                FOREIGN KEY (idAno) REFERENCES Ano (Id)
                );
                ''')
        print("Table created successfully")
    except sqlite3.Error as e:
        print(e)


def main():
    # create a database connection
    conn = create_connection()

    if conn is not None:
        # create employees table
        create_tables(conn)
        #print('\t Tabelas Criadas')
    else:
        print("Error! Cannot create the database connection.")


#if __name__ == '__main__':
main()
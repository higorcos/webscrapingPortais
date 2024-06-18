import sqlite3


def create_connection(db_file):
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


def create_table(conn):
    """ create a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS employees (
                     id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     age INTEGER,
                     department TEXT
                     )''')
        print("Table created successfully")
    except sqlite3.Error as e:
        print(e)


def insert_employee(conn, employee):
    """ Insert a new employee into the employees table """
    sql = ''' INSERT INTO employees(name, age, department)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, employee)
    conn.commit()
    return cur.lastrowid


def select_all_employees(conn):
    """ Query all rows in the employees table """
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def update_employee(conn, employee):
    """ Update age and department of an employee """
    sql = ''' UPDATE employees
              SET age = ? ,
                  department = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, employee)
    conn.commit()


def main():
    database = "test.db"

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        # create employees table
        create_table(conn)

        # insert employees
        employee_1 = ('John Doe', 30, 'HR')
        employee_2 = ('Jane Smith', 25, 'IT')

        insert_employee(conn, employee_1)
        insert_employee(conn, employee_2)

        print("\nAll employees:")
        select_all_employees(conn)

        # update employee
        updated_employee = (35, 'HR', 1)
        update_employee(conn, updated_employee)

        print("\nEmployees after update:")
        select_all_employees(conn)

    else:
        print("Error! Cannot create the database connection.")


if __name__ == '__main__':
    main()

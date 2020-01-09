import sqlite3


class Database:
    DB_PATH = 'data/database.db'

    def __init__(self, path=DB_PATH):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def commit(self):
        self.connection.commit()
        self.connection.close()

    def create_table(self):
        create_table = """
            CREATE TABLE IF NOT EXISTS employees (
                id TEXT PRIMARY KEY,
                employee_name TEXT NOT NULL,
                dob TEXT NOT NULL,
                doj TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                salary INTEGER NOT NULL,
                gender INTEGER NOT NULL ,
                age INTEGER NOT NULL,
                company_age INTEGER NOT NULL,
                weight INTEGER NOT NULL);"""
        self.cursor.execute(create_table)

    def add_employee(self, values):
        add_employee = """
            INSERT INTO employees 
            (id, employee_name, dob, doj, phone, email, 
            salary, gender, age, company_age, weight) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(add_employee, values)

    def remove_employee(self, employee_id):
        remove_employee = """DELETE FROM employees WHERE id=?"""
        self.cursor.execute(remove_employee, [employee_id])

    def print_table(self):
        get_all_employees = """SELECT * FROM employees"""
        self.cursor.execute(get_all_employees)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

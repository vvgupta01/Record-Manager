from Employee import Employee
from Record import Record
from Modeler import Modeler
from datetime import datetime
import mysql.connector


def main():
    file_name = 'EmployeeFile.txt'
    record_name = 'EmployeeRecords.csv'
    grade_name = 'EmployeeGrades.csv'
    grade_path = 'C:/Users/vvgup/Downloads/EmployeeGrades.csv'

    db_name = 'employee_db'
    table_name = 'employees'

    records = Record(file_name, record_name)

    action = ''
    while action != 'E':
        print('\nADD EMPLOYEE[A] REMOVE EMPLOYEE[R] PRINT EMPLOYEES[P] GO TO MODELER[M] EXIT[E]')
        action = input('ENTER ACTION: ').upper()

        if action == 'A':
            name = input('ENTER EMPLOYEE NAME: ').upper()
            dob = input('ENTER DOB (MM/DD/YYYY): ')

            try:
                datetime.strptime(dob, '%m/%d/%Y').date()
                records.add_employee(name, dob)
            except ValueError:
                print('INVALID DATE')
        elif action == 'R':
            ID = input('ENTER EMPLOYEE ID: ')
            records.remove_employee(ID)
        elif action == 'P':
            records.print_employees()
        elif action == 'M':
            Modeler(grade_path, grade_name)
        elif action == 'E':
            save(records, db_name, table_name)
        else:
            print('INVALID ACTION')

def save(records, db_name, table_name):
    records.save()
    db = mysql.connector.connect(host='localhost', user='root', passwd='vaibhav')
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))

    db = mysql.connector.connect(host='localhost', user='root', passwd='vaibhav', database=db_name)
    cursor = db.cursor()

    drop_table = 'DROP TABLE IF EXISTS {}'.format(table_name)
    create_table = """CREATE TABLE {} (
    name VARCHAR(50) NOT NULL,
    id CHAR({}) PRIMARY KEY NOT NULL,
    dob CHAR(10) NOT NULL,
    email VARCHAR(70) NOT NULL);""".format(table_name, Employee.ID_LENGTH)

    cursor.execute(drop_table)
    cursor.execute(create_table)

    rec = records.employees
    for i in range(len(rec['NAME'])):
        add_employee = 'INSERT INTO {} (name, id, dob, email) VALUES(%s, %s, %s, %s)'.format(table_name)
        val = [rec['NAME'][i], rec['ID'][i], rec['DOB'][i], rec['EMAIL'][i]]
        cursor.execute(add_employee, val)

    # cursor.execute('SELECT * FROM {}'.format(table_name))
    # table = cursor.fetchall()
    # for row in table:
    #     print(row)

    db.commit()
    db.close()
    print('SUCCESSFULLY SAVED RECORDS TO DATABASE')

if __name__ == '__main__':
    main()

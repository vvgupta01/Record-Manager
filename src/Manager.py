from src.Records import Records
from src.Modeler import Modeler
from src import Utils


def main():
    records = Records()

    action = ''
    while action != 'Q':
        if records.is_empty():
            print('\nADD EMPLOYEE[A] MODELER[M] QUIT[Q]')
        else:
            print('\nADD EMPLOYEE[A] REMOVE EMPLOYEE[R] '
                  'SEARCH EMPLOYEE[S]\nMODELER[M] QUIT[Q]')

        action = input('SELECT ACTION: ').upper()
        if action == 'A':
            name, gender, dob, weight, phone, email, salary = get_employee_info()
            records.add_employee(name, gender, dob, weight, phone, email, salary)
        elif action == 'R' and not records.is_empty():
            employee_id = input('ENTER EMPLOYEE ID: ')
            records.remove_employee(employee_id)
        elif action == 'S' and not records.is_empty():
            column, search = get_search(records)
            records.search_employee(search, column)
        elif action == 'M':
            Modeler(records.df).main()
        elif action == 'Q':
            records.save()
        else:
            print('INVALID ACTION')


def get_search(records):
    columns = records.df.columns
    column_text = Utils.get_columns_text(records.df.columns)
    while True:
        print(column_text)
        try:
            index = int(input('SEARCH BY INDEX: '))
            if not 0 <= index < len(columns):
                raise ValueError

            search = input('SEARCH: ').upper()
            return columns[index], search
        except ValueError:
            print('INVALID INDEX')


def get_employee_info():
    name = Utils.get_str_value('ENTER EMPLOYEE NAME: ', 'INVALID NAME',
                               None, Utils.NAME_REGEX)
    gender = Utils.get_str_value('ENTER GENDER (M/F): ', 'INVALID GENDER',
                                 Utils.is_valid_gender, None)
    gender = 0 if gender == 'F' else 1
    dob = Utils.get_str_value('ENTER DOB (MM/DD/YYYY): ', 'INVALID DOB',
                              Utils.is_valid_date, None)
    weight = Utils.get_int_value('ENTER WEIGHT (KG): ', 'INVALID WEIGHT',
                                 Utils.is_pos_int)
    phone = Utils.get_str_value('ENTER PHONE NUMBER (XXX-XXX-XXXX): ',
                                'INVALID PHONE NUMBER',
                                None, Utils.PHONE_REGEX)
    email = Utils.get_str_value('ENTER EMAIL: ', 'INVALID EMAIL',
                                None, Utils.EMAIL_REGEX)
    salary = Utils.get_int_value('ENTER SALARY: ', 'INVALID SALARY',
                                 Utils.is_pos_int)
    return name, gender, dob, weight, phone, email, salary


if __name__ == '__main__':
    main()

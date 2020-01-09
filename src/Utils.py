import os
import re
import random
from datetime import datetime


NAME_REGEX = '[A-Z]+\s+[A-Z]+'
EMAIL_REGEX = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
PHONE_REGEX = '^\d{3}-\d{3}-\d{4}$'


def get_str_value(prompt, error, criteria, regex):
    while True:
        value = input(prompt).upper()
        if regex is not None:
            if matches_regex(value, regex):
                return value
        else:
            if criteria(value):
                return value
        print(error)


def get_int_value(prompt, error, criteria):
    while True:
        try:
            value = int(input(prompt))
            if not criteria(value):
                raise ValueError
            return value
        except ValueError:
            print(error)


def matches_regex(string, regex):
    return re.search(regex, string)


def is_valid_gender(gender):
    return gender == 'M' or gender == 'F'


def is_valid_date(date):
    try:
        datetime.strptime(date, '%m/%d/%Y').date()
        return True
    except ValueError:
        return False


def is_pos_int(nbr):
    try:
        if int(nbr) <= 0:
            raise ValueError
        return True
    except ValueError:
        return False


def is_valid_size(size):
    return 0 < size < 100


def get_date():
    return datetime.today()


def get_age(dob):
    dob = datetime.strptime(dob, '%m/%d/%Y')
    return (get_date() - dob).days // 365


def get_columns_text(columns):
    text = ''
    for i, name in enumerate(columns):
        if i % 4 == 0:
            text += '\n'
        text += '{}[{}] '.format(columns[i], i)
    return text


def get_variables(columns):
    column_text = get_columns_text(columns)
    while True:
        print(column_text)
        var = input('SELECT VARIABLE(S) (EX. 123): ')
        try:
            for char in var:
                if not 0 <= int(char) < len(columns):
                    raise ValueError
                var = list(dict.fromkeys(list(var)))
                for i in range(len(var)):
                    var[i] = columns[int(var[i])]
                print('VARIABLE(S) SELECTED:', var)
                return var
        except ValueError:
            print('INVALID VARIABLE(S)')


def get_values(var):
    value_dict = dict()
    for i in var:
        while True:
            try:
                value = int(input('ENTER {}: '.format(i.upper())))
                value_dict[i] = value
                break
            except ValueError:
                print('INVALID VALUE')
    return value_dict


def generate_id(length):
    employee_id = str(random.randrange(10 ** length))
    employee_id.zfill(length)
    return employee_id


def get_next_index(dir_path):
    return len(os.listdir(dir_path)) // 2 + 1

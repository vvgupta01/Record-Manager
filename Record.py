import pickle
import random
import pandas as pd
import os
from Employee import Employee

class Record:

    def __init__(self, f_name, r_name):
        self.f_name = f_name
        self.r_name = r_name
        self.employees = {'NAME': [], 'ID': [], 'DOB': [], 'EMAIL': []}
        self.load()

    def load(self):
        try:
            file = open(self.f_name, 'rb')
            if os.stat(self.f_name).st_size > 0:
                self.employees = pickle.load(file)
                print('SUCCESSFULLY LOADED RECORDS')
        except FileNotFoundError:
            file = open(self.f_name, 'wb')
        file.close()

    def save(self):
        file = open(self.f_name, 'wb')
        pickle.dump(self.employees, file)
        file.close()

        df = pd.DataFrame(self.employees)
        df.to_csv(self.r_name, index=False)
        print('SUCCESSFULLY SAVED RECORDS')

    def add_employee(self, name, dob):
        employee = Employee(name, dob)
        self.assign_ID(employee)
        self.assign_email(employee)
        self.employees['NAME'].append(employee.name)
        self.employees['ID'].append(employee.ID)
        self.employees['DOB'].append(employee.dob)
        self.employees['EMAIL'].append(employee.email)
        print('SUCCESSFULLY ADDED EMPLOYEE')
        self.save()

    def remove_employee(self, ID):
        for i in range(len(self.employees['ID'])):
            if ID == self.employees['ID'][i]:
                del self.employees['NAME'][i]
                del self.employees['ID'][i]
                del self.employees['DOB'][i]
                del self.employees['EMAIL'][i]
                print('SUCCESSFULLY REMOVED EMPLOYEE')
                self.save()
                return
        print('INVALID ID')

    def print_employees(self):
        try:
            df = pd.read_csv(self.r_name)
            if len(df) == 0:
                print("NO EMPLOYEES FOUND")
            else:
                print()
                print(df)
        except FileNotFoundError:
            print('NO RECORDS FOUND')

    def assign_ID(self, employee):
        ID = ''
        while ID == '':
            for i in range(Employee.ID_LENGTH):
                ID += str(random.randrange(10))

            for id in self.employees['ID']:
                if ID == id:
                    ID = ''
                    break
        employee.ID = ID

    def assign_email(self, employee):
        email = ''
        count = -1
        while email == '':
            email = employee.name.replace(' ', '').lower()
            if count > -1:
                email += str(count)
            for eml in self.employees['EMAIL']:
                if email == eml[:len(email)]:
                    email = ''
                    count += 1
                    break

        email += '@mycompany.com'
        employee.email = email



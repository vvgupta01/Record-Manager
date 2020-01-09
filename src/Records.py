import pandas as pd

from src import Utils
from src.Database import Database


class Records:
    DATA_PATH = 'data/employee_data.csv'
    ID_LENGTH = 6

    def __init__(self, path=DATA_PATH):
        self.database = Database()
        self.df = pd.read_csv(path)
        self.update_df()
        print('SUCCESSFULLY LOADED RECORDS')

    def update_df(self):
        self.df = self.df.astype(str)
        self.df['DOB'] = pd.to_datetime(self.df['DOB'])
        self.df['DOJ'] = pd.to_datetime(self.df['DOJ'])

        date = Utils.get_date()
        self.df['AGE'] = (date - self.df['DOB']).dt.components.days // 365
        self.df['COMPANY_AGE'] = (date - self.df['DOJ']).dt.components.days // 365

    def save(self, path=DATA_PATH):
        self.df['DOB'] = self.df['DOB'].dt.strftime('%m/%d/%Y')
        self.df['DOJ'] = self.df['DOJ'].dt.strftime('%m/%d/%Y')

        self.df.to_csv(path, index=False)
        self.database.sync_df(self.df)
        # self.database.print_table()
        self.database.commit()
        print('SUCCESSFULLY SAVED RECORDS')

    def add_employee(self, name, gender, dob, weight, phone, email, salary):
        employee_id = self.assign_id()
        doj = Utils.get_date()
        age = Utils.get_age(dob)

        row = [employee_id, name, dob, doj, phone,
               email, salary, gender, age, 0, weight]
        self.df.loc[self.df.shape[0]] = row
        print('SUCCESSFULLY ADDED EMPLOYEE')

    def remove_employee(self, employee_id):
        row = self.df[self.df['ID'] == employee_id].index
        if not row.empty:
            self.df.drop(row, inplace=True)
            print('SUCCESSFULLY REMOVED EMPLOYEE')
        else:
            print('INVALID EMPLOYEE ID')

    def search_employee(self, search, column):
        results = self.df[self.df[column].str.contains(search)]
        if not results.empty:
            print(results)
        else:
            print('NO EMPLOYEES FOUND')

    def assign_id(self, length=ID_LENGTH):
        while True:
            employee_id = Utils.generate_id(length)
            if employee_id not in self.df.ID.values:
                return employee_id

    def is_empty(self):
        return self.df.shape[0] == 0

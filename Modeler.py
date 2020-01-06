import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class Modeler:

    def __init__(self, grade_path, grade_name):
        self.grade_path = grade_path
        self.grade_name = grade_name
        self.df = pd.DataFrame()
        self.lm = linear_model.LinearRegression()
        self.load()

    def load(self):
        try:
            df = pd.read_csv(self.grade_name)
        except FileNotFoundError:
            df = pd.read_csv(self.grade_path)
            df.dropna(inplace=True)
            df.drop(columns=['Unnamed: 0'], inplace=True)
            df.rename(columns={'groups': 'group', 'healthy_eating': 'healthy',
                               'active_lifestyle': 'active', 'TechGrade': 'grade'}, inplace=True)
            df['group'].replace({'A': 0, 'B': 1, 'AB': 2, 'O': 3}, inplace=True)
            df['grade'] = df['salary'] // 1000
            df['grade'].replace(0, 1, inplace=True)
            df = df.reindex(columns=['id', 'group', 'age', 'healthy', 'active', 'grade', 'salary'])
            df = df.astype(int)
            df.set_index('id', inplace=True)
        self.df = df
        print('SUCCESSFULLY LOADED MODELER')
        self.main()

    def main(self):
        action = ''
        while action != 'E':
            print('\nGENERATE MODEL[G] EXIT MODELER[E]')
            action = input('ENTER ACTION: ').upper()
            if action == 'G':
                var = None
                valid_var = False
                while not valid_var:
                    var = input('SELECT VARIABLES - GROUP[0] AGE[1] HEALTHY[2] ACTIVE[3] GRADE[4]: ')
                    try:
                        for char in var:
                            if int(char) not in range(0, 5):
                                raise ValueError
                        valid_var = True
                    except ValueError:
                        print('INVALID VARIABLE LIST')
                var = list(var)
                var = list(dict.fromkeys(var))
                for i in range(len(var)):
                    var[i] = self.df.columns[int(var[i])]
                print('VARIABLES SELECTED:', var)

                size = None
                valid_size = False
                while not valid_size:
                    try:
                        size = int(input('ENTER TEST SIZE (%): '))
                        if not 0 < size < 100:
                            raise ValueError
                        valid_size = True
                    except ValueError:
                        print('INVALID TEST SIZE')

                X = self.df[var]
                Y = self.df['salary']
                self.generate_model(X, Y, size)

                while action != 'E':
                    print('PREDICT VALUE[P] RETURN TO MODELER[E]')
                    action = input('ENTER ACTION: ').upper()
                    if action == 'P':
                        df_dict = dict()
                        for v in var:
                            valid_value = False
                            while not valid_value:
                                try:
                                    value = int(input('ENTER {}: '.format(v.upper())))
                                    df_dict[v] = value
                                    valid_value = True
                                except ValueError:
                                    print('INVALID VALUE')

                        df = pd.DataFrame(df_dict, index=[0])
                        print(df)
                        print('PREDICTED SALARY={}'.format(round(self.lm.predict(df), 2)))
                    elif action == 'E':
                        action = ''
                        break
            elif action == 'E':
                self.save()
                return
            else:
                print('INVALID ACTION')

    def generate_model(self, X, Y, size):
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=size/100)
        self.lm = linear_model.LinearRegression()
        self.lm.fit(x_train, y_train)
        y_hat = self.lm.predict(x_test)

        print('\nMEAN ABSOLUTE ERROR:', round(mean_absolute_error(y_test, y_hat), 4))
        print('COEFFICIENT OF DETERMINATION:', round(self.lm.score(X, Y), 4))

        model = 'MODEL: SALARY=({})+'.format(round(self.lm.intercept_, 2))
        for i, c in enumerate(X.columns):
            model += '({}){}'.format(round(self.lm.coef_[i], 2), c.upper())
            if i != len(X.columns)-1:
                model += '+'
        print(model)
        self.plot_model(x_train, y_train)
        self.plot_residual(x_test, y_test-y_hat)
        print('SUCCESSFULLY GENERATED MODEL\n')

    def plot_model(self, X, Y):
        fig, ax = plt.subplots()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        colors = ['b', 'r', 'g', 'orange', 'y']
        for i, c in enumerate(X.columns):
            c_norm = X[c] / X[c].max()
            plt.scatter(c_norm, Y, color=colors[i], alpha=0.5, s=20, label=c.upper())
            plt.plot(np.unique(c_norm), np.poly1d(np.polyfit(c_norm, Y, 1))(np.unique(c_norm)),
                     color=colors[i], linewidth=3)

        plt.title('SALARY VS NORMALIZED FACTORS (N={})'.format(len(X)), fontsize=10, weight='bold')
        plt.xlabel('NORMALIZED FACTORS', fontsize=10)
        plt.ylabel('SALARY', fontsize=10)
        plt.legend(loc='upper left', fontsize=8)

    def plot_residual(self, X, Y):
        fig, ax = plt.subplots()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        colors = ['b', 'r', 'g', 'orange', 'y']
        for i, c in enumerate(X.columns):
            c_norm = X[c] / X[c].max()
            plt.scatter(c_norm, Y, color=colors[i], alpha=0.5, s=20, label=c.upper())

        plt.axhline(y=0, color='k', linestyle='--')
        plt.title('SALARY RESIDUAL VS NORMALIZED FACTORS (N={})'.format(len(X)), fontsize=10, weight='bold')
        plt.xlabel('NORMALIZED FACTORS', fontsize=10)
        plt.ylabel('SALARY RESIDUAL', fontsize=10)
        plt.legend(loc='upper left', fontsize=8)
        plt.show()

    def save(self):
        self.df.to_csv(self.grade_name, index=False)
        print('SUCCESSFULLY SAVED MODELER')
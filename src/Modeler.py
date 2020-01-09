import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from src import Utils


class Modeler:
    GRAPHS_PATH = 'data/graphs'

    def __init__(self, df):
        self.df = df[df.columns[-5:]].astype(int)
        self.lm = None
        print('SUCCESSFULLY LOADED MODELER')

    def main(self):
        action = ''
        var = None
        while action != 'Q':
            if var is None:
                print('\nNEW MODEL[N] STATS[S] QUIT[Q]')
            else:
                print('\nNEW MODEL[N] STATS[S] PREDICT VALUE[P] QUIT[Q]')

            action = input('ENTER ACTION: ').upper()
            if action == 'N':
                var = Utils.get_variables(self.df.columns[-4:])
                size = Utils.get_int_value('ENTER TEST SIZE (%): ',
                                           'INVALID SIZE',
                                           Utils.is_valid_size)
                x = self.df[var]
                y = self.df['SALARY']
                self.generate_model(x, y, size)
            elif action == 'S':
                print(round(self.df.describe(), 2))
            elif action == 'P' and var is not None:
                df = pd.DataFrame(Utils.get_values(var), index=[0])
                print(df)

                y_predict = round(self.lm.predict(df)[0], 2)
                print('PREDICTED SALARY={}'.format(y_predict))
            elif action != 'Q':
                print('INVALID ACTION')

    def generate_model(self, x, y, size, path=GRAPHS_PATH):
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size / 100)
        self.lm = linear_model.LinearRegression()
        self.lm.fit(x_train, y_train)
        y_hat = self.lm.predict(x_test)

        print('\nMEAN ABSOLUTE ERROR:', round(mean_absolute_error(y_test, y_hat), 4))
        print('COEFFICIENT OF DETERMINATION (R2):', round(self.lm.score(x, y), 4))

        model = 'MODEL: SALARY=({})+'.format(round(self.lm.intercept_, 2))
        for i, c in enumerate(x.columns):
            model += '({}){}'.format(round(self.lm.coef_[i], 2), c.upper())
            if i < len(x.columns) - 1:
                model += '+'
        print(model)

        index = Utils.get_next_index(path)
        self.plot_model(x_train, y_train, index)
        self.plot_residual(x_test, y_test-y_hat, index)
        plt.show()
        print('SUCCESSFULLY GENERATED MODEL')

    @staticmethod
    def plot_model(x, y, index, path=GRAPHS_PATH):
        fig, ax = plt.subplots()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        colors = ['b', 'r', 'g', 'orange', 'y']
        for i, c in enumerate(x.columns):
            c_norm = x[c] / x[c].max()
            plt.scatter(c_norm, y, color=colors[i], alpha=0.5, s=20, label=c.upper())
            plt.plot(np.unique(c_norm), np.poly1d(np.polyfit(c_norm, y, 1))(np.unique(c_norm)),
                     color=colors[i], linewidth=3)

        plt.title('SALARY VS NORMALIZED FACTORS (N={})'.format(len(x)), fontsize=10, weight='bold')
        plt.xlabel('NORMALIZED FACTORS', fontsize=10)
        plt.ylabel('SALARY', fontsize=10)
        plt.legend(loc='upper left', fontsize=8)
        plt.savefig(path + '/model_graph_{}.png'.format(index))

    @staticmethod
    def plot_residual(x, y, index, path=GRAPHS_PATH):
        fig, ax = plt.subplots()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        colors = ['b', 'r', 'g', 'orange', 'y']
        for i, c in enumerate(x.columns):
            c_norm = x[c] / x[c].max()
            plt.scatter(c_norm, y, color=colors[i], alpha=0.5, s=20, label=c.upper())

        plt.axhline(y=0, color='k', linestyle='--')
        plt.title('SALARY RESIDUAL VS NORMALIZED FACTORS (N={})'.format(len(x)), fontsize=10, weight='bold')
        plt.xlabel('NORMALIZED FACTORS', fontsize=10)
        plt.ylabel('SALARY RESIDUAL', fontsize=10)
        plt.legend(loc='upper left', fontsize=8)
        plt.savefig(path + '/residual_graph_{}.png'.format(index))

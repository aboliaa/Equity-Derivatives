import os
import matplotlib.pyplot as plt

from utils import remove_fileglob

class Table(object):
    def __init__(self, path):
        self.path = path

    def plot_only_text(self, text, path):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.axis('off')
        plt.text(0.3, 0.8, text)
        plt.savefig(path)

    def plot_report4(self, data):
        remove_fileglob(os.path.join(self.path, "report3*"))
        for i in range(len(data)):
            self._plot_report4(data[i], i)

    def _plot_report4(self, data, ii):
        plt.clf()
        ax = plt.gca()
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        columns = ['No.', 'Symbol', 'Percentage Movement', 'Increase/Decrease']

        cell_text_1 = []
        i = 0
        for d in data[0]:
            i += 1
            cell_text_1.append([str(i), d['scrip'], d['move_percent'], "Increase"])

        cell_text_2 = []
        i = 0
        for d in data[1]:
            i += 1
            cell_text_2.append([str(i), d['scrip'], d['move_percent'], "Decrease"])

        plt.title("OI Movement")
        table1 = plt.table(cellText=cell_text_1, colLabels=columns, loc='upper center')
        table2 = plt.table(cellText=cell_text_2, colLabels=columns, loc='lower center')
        name = "report4_%d.png" % (ii+1,)
        plt.savefig(os.path.join(self.path, name))

    def plot_report5(self, data):
        remove_fileglob(os.path.join(self.path, "report5*"))
        self._plot_report5(data['highest'], ii=1)
        self._plot_report5(data['lowest'], ii=2)

    def _plot_report5(self, data, ii):
        plt.clf()
        
        if not data:
            text = 'No scrips found.'
            path = os.path.join(self.path, "report5_%d.png"%ii)
            self.plot_only_text(text, path)
            return

        columns = ['No.', 'Symbol']
        cell_text = []
        i = 0
        for d in data:
            i += 1
            cell_text.append([str(i), d])
        num_rows = len(cell_text)
        num_cols = len(columns)
        hcell, wcell = 1, 0.1
        hpad, wpad = 0.3, 0
        xsize = num_cols*wcell+wpad
        ysize = num_rows*hcell+hpad
        if xsize < ysize:
            xsize = ysize
        else:
            ysize = xsize
        fig = plt.figure(figsize=(xsize, ysize))
        ax = fig.add_subplot(111)
        ax.axis('off')

        ax.table(cellText=cell_text, colLabels=columns, loc='upper center')
        plt.savefig(os.path.join(self.path, "report5_%d.png"%ii))

    def plot_report6(self, data):
        remove_fileglob(os.path.join(self.path, "report6*"))
        self._plot_report6(data['calls'], ii=1)
        self._plot_report6(data['puts'], ii=2)

    def _plot_report6(self, data, ii):
        plt.clf()
        columns = ['No.', 'Symbol', 'Contracts', 'Strike price', 'Expiry series']

        cell_text = []
        i = 0
        for d in data:
            i += 1
            cell_text.append([str(i), d['scrip'], d['max_contracts'], d['strike_pr'], d['exp_dt']])

        num_rows = i
        num_cols = len(columns)
        hcell, wcell = 1, 0.1
        hpad, wpad = 0.5, 0
        xsize = num_cols*wcell+wpad
        ysize = num_rows*hcell+hpad
        if xsize < ysize:
            xsize = ysize
        else:
            ysize = xsize
        fig = plt.figure(figsize=(xsize, ysize))
        ax = fig.add_subplot(111)
        ax.axis('off')

        ax.table(cellText=cell_text, colLabels=columns, loc='upper center')
        plt.savefig(os.path.join(self.path, "report6_%d.png"%ii))

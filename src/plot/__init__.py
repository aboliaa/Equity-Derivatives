from const import *
import plotly
from graph import Graph
from table import Table

class Plot(object):
    def __init__(self, path=PLOT_PATH):
        self.graph = Graph(path)
        self.table = Table(path)
        self.plotly = plotly

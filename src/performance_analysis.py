import pandas as pd
import matplotlib.pyplot as plt

class PerformanceAnalysis:
    def __init__(self):
        self.data = []

    def analyze(self, results):
        self.data.append(results)

    def generate_report(self):
        df = pd.DataFrame(self.data)
        return df.describe()

    def visualize(self):
        df = pd.DataFrame(self.data)
        df.plot(kind='bar')
        plt.show()


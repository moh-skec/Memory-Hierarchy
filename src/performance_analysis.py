# src/performance_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.DEBUG)


class PerformanceAnalysis:
    def __init__(self):
        self.data = []

    def analyze(self, results):
        self.data.append(results)
        logging.debug(f"Results Analyzed: {results}")

    def generate_report(self):
        df = pd.DataFrame(self.data)
        logging.debug(f"Generated Report: {df.describe()}")
        return df.describe()

    def visualize(self):
        df = pd.DataFrame(self.data)
        df.plot(kind='bar')
        plt.show()
        logging.debug("Visualization Created")

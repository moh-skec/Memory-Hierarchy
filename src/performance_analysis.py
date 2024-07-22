# src/performance_analysis.py
import matplotlib.pyplot as plt
import pandas as pd


class PerformanceAnalysis:
    def __init__(self, simulator):
        self.total_hits = 0
        self.total_misses = 0
        self.total_accesses = 0
        self.simulator = simulator

    def update_metrics(self, hits, misses, accesses):
        self.total_hits += hits
        self.total_misses += misses
        self.total_accesses += accesses

    def visualize(self, data):
        df = pd.DataFrame(data)
        df.plot(kind='bar')
        plt.title('Access Resault')
        plt.show()

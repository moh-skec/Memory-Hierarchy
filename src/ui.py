# src/ui.py
import tkinter as tk
from tkinter import ttk
from memory_hierarchy import CacheMemory, MainMemory, ExternalMemory
from simulation import MemoryAccessSimulation
from performance_analysis import PerformanceAnalysis
from cache_policies import LRU, FIFO, Random, MRU, SecondChance, LFU


class MemoryHierarchySimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Hierarchy Simulator")

        # Add UI components for configuration and display
        self.create_widgets()

        # Set up default memory hierarchy
        external_memory = ExternalMemory("External Memory", 64, 1000)
        main_memory = MainMemory(
            "Main Memory", 32, 100, lower_level=external_memory)
        l3_cache = CacheMemory("L3 Cache", 16, 10, Random,
                               lower_level=main_memory)
        l2_cache = CacheMemory("L2 Cache", 8, 5, FIFO, lower_level=l3_cache)
        l1_cache = CacheMemory("L1 Cache", 4, 1, LRU, lower_level=l2_cache)

        self.memory_hierarchy = [l1_cache, l2_cache,
                                 l3_cache, main_memory, external_memory]
        self.simulator = MemoryAccessSimulation(self.memory_hierarchy)
        self.performance_analyzer = PerformanceAnalysis()

    def create_widgets(self):
        self.settings_frame = ttk.Frame(self.root)
        self.settings_frame.grid(row=0, column=0, padx=10, pady=10)

        self.label_cache_size = ttk.Label(
            self.settings_frame, text="Cache Size (L1, L2, L3):")
        self.label_cache_size.grid(row=0, column=0, sticky="W")
        self.entry_cache_size = ttk.Entry(self.settings_frame)
        self.entry_cache_size.grid(row=0, column=1, padx=5)

        self.label_replacement_policy = ttk.Label(
            self.settings_frame, text="Replacement Policy (LRU, FIFO, Random, MRU, SecondChance, LFU):")
        self.label_replacement_policy.grid(row=1, column=0, sticky="W")
        self.entry_replacement_policy = ttk.Entry(self.settings_frame)
        self.entry_replacement_policy.grid(row=1, column=1, padx=5)

        self.label_access_pattern = ttk.Label(
            self.settings_frame, text="Access Pattern (sequential, random):")
        self.label_access_pattern.grid(row=2, column=0, sticky="W")
        self.entry_access_pattern = ttk.Entry(self.settings_frame)
        self.entry_access_pattern.grid(row=2, column=1, padx=5)

        self.label_access_count = ttk.Label(
            self.settings_frame, text="Number of Accesses:")
        self.label_access_count.grid(row=3, column=0, sticky="W")
        self.entry_access_count = ttk.Entry(self.settings_frame)
        self.entry_access_count.grid(row=3, column=1, padx=5)

        self.run_button = ttk.Button(
            self.settings_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=4, columnspan=2, pady=10)

        self.results_frame = ttk.Frame(self.root)
        self.results_frame.grid(row=1, column=0, padx=10, pady=10)
        self.results_text = tk.Text(self.results_frame, height=10, width=50)
        self.results_text.pack()

    def run_simulation(self):
        cache_sizes = [int(size)
                       for size in self.entry_cache_size.get().split(',')]
        policies = [policy.strip()
                    for policy in self.entry_replacement_policy.get().split(',')]
        pattern = self.entry_access_pattern.get().strip()
        count = int(self.entry_access_count.get().strip())

        # Update memory hierarchy based on user input
        self.memory_hierarchy[0].size = cache_sizes[0]
        self.memory_hierarchy[1].size = cache_sizes[1]
        self.memory_hierarchy[2].size = cache_sizes[2]

        policy_map = {
            "LRU": LRU,
            "FIFO": FIFO,
            "Random": Random,
            "MRU": MRU,
            "SecondChance": SecondChance,
            "LFU": LFU
        }

        self.memory_hierarchy[0].replacement_policy = policy_map[policies[0]](
            self.memory_hierarchy[0])
        self.memory_hierarchy[1].replacement_policy = policy_map[policies[1]](
            self.memory_hierarchy[1])
        self.memory_hierarchy[2].replacement_policy = policy_map[policies[2]](
            self.memory_hierarchy[2])

        addresses = self.simulator.generate_accesses(pattern, count)
        results = self.simulator.run_simulation(addresses)
        self.performance_analyzer.analyze(results)

        report = self.performance_analyzer.generate_report()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, report.to_string())
        self.performance_analyzer.visualize()


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryHierarchySimulatorUI(root)
    root.mainloop()

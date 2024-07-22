import tkinter as tk
from tkinter import ttk, messagebox
from memory_hierarchy import CacheMemory, MainMemory, ExternalMemory
from simulation import MemoryAccessSimulation
from performance_analysis import PerformanceAnalysis
from cache_policies import LRU, FIFO, Random, MRU, SecondChance, LFU, LFRU
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

L1_CACHE = "L1 Cache"
L2_CACHE = "L2 Cache"
L3_CACHE = "L3 Cache"
MAIN_MEMORY = "Main Memory"
EXTERNAL_MEMORY = "External Memory"


class MemoryHierarchySimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Hierarchy Simulator")

        self.create_widgets()
        self.default_memory_hierarchy()

    def default_memory_hierarchy(self):
        external_memory = ExternalMemory(EXTERNAL_MEMORY, 8192, 1000)
        main_memory = MainMemory(
            MAIN_MEMORY, 512, 100, lower_level=external_memory)
        l3_cache = CacheMemory(L3_CACHE, 16, 10, 1,
                               Random, lower_level=main_memory)
        l2_cache = CacheMemory(L2_CACHE, 8, 5, 1, FIFO, lower_level=l3_cache)
        l1_cache = CacheMemory(L1_CACHE, 4, 1, 1, LRU, lower_level=l2_cache)

        self.memory_hierarchy = [l1_cache, l2_cache,
                                 l3_cache, main_memory, external_memory]
        self.simulator = MemoryAccessSimulation(self.memory_hierarchy)
        self.performance_analyzer = PerformanceAnalysis(self.simulator)

    def create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(input_frame, text="Number of Cache Levels:").grid(
            row=0, column=0, sticky=tk.W)
        self.combo_cache_levels = ttk.Combobox(
            input_frame, values=["1", "2", "3"], state="readonly")
        self.combo_cache_levels.grid(row=0, column=1, sticky=tk.W)
        self.combo_cache_levels.current(1)
        self.combo_cache_levels.bind(
            "<<ComboboxSelected>>", self.update_cache_size_fields)

        ttk.Label(input_frame, text="Cache Sizes (L1, L2, L3):").grid(
            row=1, column=0, sticky=tk.W)
        self.entry_cache_size_l1 = ttk.Entry(input_frame)
        self.entry_cache_size_l1.grid(row=1, column=2, sticky=tk.W)
        self.entry_cache_size_l1.insert(0, "4")

        self.entry_cache_size_l2 = ttk.Entry(input_frame)
        self.entry_cache_size_l2.grid(row=1, column=1, sticky=tk.W)
        self.entry_cache_size_l2.insert(0, "8")

        self.entry_cache_size_l3 = ttk.Entry(input_frame)
        self.entry_cache_size_l3.grid(row=1, column=3, sticky=tk.W)
        self.entry_cache_size_l3.insert(0, "16")
        self.entry_cache_size_l3.grid_remove()

        ttk.Label(input_frame, text="Block Size:").grid(
            row=2, column=0, sticky=tk.W)
        self.entry_block_size = ttk.Entry(input_frame, width=5)
        self.entry_block_size.grid(row=2, column=1, sticky=tk.W)
        self.entry_block_size.insert(0, "1")

        ttk.Label(input_frame, text="Replacement Policy:").grid(
            row=3, column=0, sticky=tk.W)
        self.combo_replacement_policy = ttk.Combobox(input_frame, values=[
                                                     "LRU", "FIFO", "Random", "MRU", "SecondChance", "LFU", "LFRU"], state="readonly")
        self.combo_replacement_policy.grid(row=3, column=1, sticky=tk.W)
        self.combo_replacement_policy.current(0)

        ttk.Label(input_frame, text="Access Pattern:").grid(
            row=4, column=0, sticky=tk.W)
        self.combo_access_pattern = ttk.Combobox(
            input_frame, values=["Sequential", "Random"], state="readonly")
        self.combo_access_pattern.grid(row=4, column=1, sticky=tk.W)
        self.combo_access_pattern.current(0)

        ttk.Label(input_frame, text="Number of Accesses:").grid(
            row=5, column=0, sticky=tk.W)
        self.entry_access_count = ttk.Entry(input_frame, width=10)
        self.entry_access_count.grid(row=5, column=1, sticky=tk.W)
        self.entry_access_count.insert(0, "100")

        self.run_button = ttk.Button(
            input_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=6, column=0, columnspan=2, pady=10)

        result_frame = ttk.Frame(self.root, padding="10")
        result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

    def update_cache_size_fields(self, event):
        num_cache_levels = int(self.combo_cache_levels.get())
        if num_cache_levels == 1:
            self.entry_cache_size_l2.grid_remove()
            self.entry_cache_size_l3.grid_remove()
        elif num_cache_levels == 2:
            self.entry_cache_size_l2.grid()
            self.entry_cache_size_l3.grid_remove()
        elif num_cache_levels == 3:
            self.entry_cache_size_l2.grid()
            self.entry_cache_size_l3.grid()

    def show_results_window(self):
        self.simulator.hits = 0
        self.simulator.misses = 0
        self.simulator.access_time = 0
        self.simulator.total_access_time = 0
        self.simulator.accesses = 0
        result_window = tk.Toplevel(self.root)
        result_window.title("Simulation Results")

        result_frame = ttk.Frame(result_window, padding="10")
        result_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.result_text = tk.Text(
            result_frame, wrap=tk.NONE, height=20, width=80)
        self.result_text.grid(row=0, column=0, columnspan=2)

        result_scrollbar_y = ttk.Scrollbar(
            result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        result_scrollbar_y.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.result_text['yscrollcommand'] = result_scrollbar_y.set

        result_scrollbar_x = ttk.Scrollbar(
            result_frame, orient=tk.HORIZONTAL, command=self.result_text.xview)
        result_scrollbar_x.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self.result_text['xscrollcommand'] = result_scrollbar_x.set

        # Combo box for access mode selection
        ttk.Label(result_frame, text="Access Mode:").grid(
            row=2, column=0, sticky=tk.W)
        self.access_mode = ttk.Combobox(
            result_frame, values=["Manual", "Sequential", "Random"], state="readonly")
        self.access_mode.grid(row=2, column=1, sticky=tk.W)
        self.access_mode.bind("<<ComboboxSelected>>",
                              self.update_access_fields)

        # Frame for dynamic access fields
        self.dynamic_frame = ttk.Frame(result_window, padding="10")
        self.dynamic_frame.grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Button to access addresses
        self.access_button = ttk.Button(
            result_window, text="Access", command=self.access_address)
        self.access_button.grid(row=4, column=0, columnspan=3, pady=10)

        self.stats_label = ttk.Label(
            result_window, text=self.generate_stats_text())
        self.stats_label.grid(row=5, column=0, columnspan=3)

        self.cache_contents_text = tk.Text(
            result_window, wrap=tk.NONE, height=10, width=80)
        self.cache_contents_text.grid(row=6, column=0, columnspan=2)
        self.cache_contents_scroll_y = ttk.Scrollbar(
            result_window, orient=tk.VERTICAL, command=self.cache_contents_text.yview)
        self.cache_contents_scroll_y.grid(row=6, column=2, sticky=(tk.N, tk.S))
        self.cache_contents_text['yscrollcommand'] = self.cache_contents_scroll_y.set

    def update_access_fields(self, event):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        mode = self.access_mode.get()
        if mode == "Manual":
            ttk.Label(self.dynamic_frame, text="Access Addresses:").grid(
                row=0, column=0, sticky=tk.W)
            self.entry_address = ttk.Entry(self.dynamic_frame, width=40)
            self.entry_address.grid(row=0, column=1, sticky=tk.W)
        elif mode == "Sequential":
            ttk.Label(self.dynamic_frame, text="Min of Addresses:").grid(
                row=0, column=0, sticky=tk.W)
            self.entry_min_address = ttk.Entry(self.dynamic_frame, width=20)
            self.entry_min_address.grid(row=0, column=1, sticky=tk.W)
            ttk.Label(self.dynamic_frame, text="Max of Addresses:").grid(
                row=1, column=0, sticky=tk.W)
            self.entry_max_address = ttk.Entry(self.dynamic_frame, width=20)
            self.entry_max_address.grid(row=1, column=1, sticky=tk.W)
        elif mode == "Random":
            ttk.Label(self.dynamic_frame, text="Min of Addresses:").grid(
                row=0, column=0, sticky=tk.W)
            self.entry_min_address = ttk.Entry(self.dynamic_frame, width=20)
            self.entry_min_address.grid(row=0, column=1, sticky=tk.W)
            ttk.Label(self.dynamic_frame, text="Max of Addresses:").grid(
                row=1, column=0, sticky=tk.W)
            self.entry_max_address = ttk.Entry(self.dynamic_frame, width=20)
            self.entry_max_address.grid(row=1, column=1, sticky=tk.W)
            ttk.Label(self.dynamic_frame, text="Size of Addresses:").grid(
                row=2, column=0, sticky=tk.W)
            self.entry_size_address = ttk.Entry(self.dynamic_frame, width=20)
            self.entry_size_address.grid(row=2, column=1, sticky=tk.W)

    def validate_non_negetive_integer(self, value_if_allowed):
        if value_if_allowed.isdigit() and int(value_if_allowed) >= 0:
            return True
        else:
            return False

    def run_simulation(self):
        num_cache_levels = int(self.combo_cache_levels.get())
        cache_sizes = [
            int(self.entry_cache_size_l1.get().strip()),
            int(self.entry_cache_size_l2.get().strip()
                ) if num_cache_levels > 1 else 0,
            int(self.entry_cache_size_l3.get().strip()
                ) if num_cache_levels > 2 else 0
        ]
        cache_sizes = cache_sizes[:num_cache_levels]

        block_size = int(self.entry_block_size.get().strip())
        policy = self.combo_replacement_policy.get().strip()
        pattern = self.combo_access_pattern.get().strip()
        count = self.entry_access_count.get().strip()

        if not count.isdigit() or int(count) < 0:
            messagebox.showerror(
                "Invalid Input", "Number of Accesses must be a nonnegative integer.")
            return

        count = int(count)

        policy_map = {
            "LRU": LRU,
            "FIFO": FIFO,
            "Random": Random,
            "MRU": MRU,
            "SecondChance": SecondChance,
            "LFU": LFU,
            "LFRU": LFRU
        }

        external_memory = ExternalMemory(EXTERNAL_MEMORY, 8192, 1000)
        main_memory = MainMemory(MAIN_MEMORY, 512, 100,
                                 lower_level=external_memory)

        memory_hierarchy = []
        lower_level = main_memory
        for i in reversed(range(num_cache_levels)):
            policy_class = policy_map.get(policy, Random)
            cache = CacheMemory(
                f"L{i + 1} Cache", cache_sizes[i], 10, block_size, policy_class, lower_level)
            memory_hierarchy.insert(0, cache)
            lower_level = cache
        memory_hierarchy.append(main_memory)
        memory_hierarchy.append(external_memory)
        self.simulator = MemoryAccessSimulation(memory_hierarchy)

        if pattern == "Sequential":
            addresses = range(count)
        elif pattern == "Random":
            rng = np.random.default_rng(int(random.random() * 10 ** 16))
            addresses = rng.integers(0, 100, count).tolist()
        else:
            raise ValueError("Unknown access pattern")

        for address in addresses:
            self.simulator.access_address(address)

        self.performance_analyzer.update_metrics(
            self.simulator.hits, self.simulator.misses, self.simulator.accesses)

        self.show_results_window()
        self.update_cache_contents_text()

    def access_address(self):
        mode = self.access_mode.get()
        rng = np.random.default_rng(int(random.random() * 10 ** 16))
        if mode == "Manual":
            addresses = [int(addr.strip())
                         for addr in self.entry_address.get().split(',')]
        elif mode == "Sequential":
            min_addr = int(self.entry_min_address.get().strip())
            max_addr = int(self.entry_max_address.get().strip())
            addresses = range(min_addr, max_addr + 1)
        elif mode == "Random":
            min_addr = int(self.entry_min_address.get().strip())
            max_addr = int(self.entry_max_address.get().strip())
            size_addr = int(self.entry_size_address.get().strip())
            addresses = rng.integers(
                min_addr, max_addr + 1, size_addr).tolist()

        for address in addresses:
            hit, _, memory_name = self.simulator.access_address(address)
            result = "Hit" if hit else "Miss"
            self.result_text.insert(tk.END, f"Address {address}: "
                                    f"{result} in {memory_name}\n")
            self.update_cache_contents_text()

        self.stats_label.config(text=self.generate_stats_text())
        hit_rate = self.simulator.hits / \
            self.simulator.accesses if self.simulator.accesses else 0
        miss_rate = self.simulator.misses / \
            self.simulator.accesses if self.simulator.accesses else 0

        self.data = {
            'hit_rate': [],
            'miss_rate': []
        }

        self.data['hit_rate'].append(hit_rate)
        self.data['miss_rate'].append(miss_rate)

        self.performance_analyzer.visualize(self.data)

    def update_cache_contents_text(self):
        cache_contents = self.simulator.get_cache_contents()
        contents_text = "\n".join(
            [f"{cache}: {addresses}" for cache, addresses in cache_contents.items()])
        self.cache_contents_text.delete(1.0, tk.END)
        self.cache_contents_text.insert(tk.END, contents_text)

    def generate_stats_text(self):
        hit_rate = self.simulator.hits / \
            self.simulator.accesses if self.simulator.accesses else 0
        miss_rate = self.simulator.misses / \
            self.simulator.accesses if self.simulator.accesses else 0
        return (f"Total Accesses: {self.simulator.accesses}\n"
                f"Total Access Time: {self.simulator.total_access_time}\n"
                f"Access Time: {self.simulator.access_time}\n"
                f"Hits: {self.simulator.hits}\n"
                f"Misses: {self.simulator.misses}\n"
                f"Hit Rate: {hit_rate:.2f}\n"
                f"Miss Rate: {miss_rate:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryHierarchySimulatorUI(root)
    root.mainloop()

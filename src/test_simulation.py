import tkinter as tk
from ui import MemoryHierarchySimulatorUI

def test_simulation():
    root = tk.Tk()
    app = MemoryHierarchySimulatorUI(root)

    # Define test parameters
    test_cases = [
        # Small cache sizes, varying policies, sequential access
        {
            "cache_sizes": "2, 4, 8",
            "replacement_policies": "LRU, FIFO, Random",
            "access_pattern": "sequential",
            "access_count": 50
        },
        # Small cache sizes, varying policies, random access
        {
            "cache_sizes": "2, 4, 8",
            "replacement_policies": "FIFO, LRU, Random",
            "access_pattern": "random",
            "access_count": 50
        },
        # Medium cache sizes, varying policies, sequential access
        {
            "cache_sizes": "4, 8, 16",
            "replacement_policies": "Random, FIFO, LRU",
            "access_pattern": "sequential",
            "access_count": 100
        },
        # Medium cache sizes, varying policies, random access
        {
            "cache_sizes": "4, 8, 16",
            "replacement_policies": "Random, LRU, FIFO",
            "access_pattern": "random",
            "access_count": 100
        },
        # Larger cache sizes, varying policies, sequential access
        {
            "cache_sizes": "8, 16, 32",
            "replacement_policies": "Random, LRU, FIFO",
            "access_pattern": "sequential",
            "access_count": 200
        },
        # Larger cache sizes, varying policies, random access
        {
            "cache_sizes": "8, 16, 32",
            "replacement_policies": "Random, LRU, FIFO",
            "access_pattern": "random",
            "access_count": 200
        },
        # Large cache sizes, MRU policy, sequential access
        {
            "cache_sizes": "16, 32, 64",
            "replacement_policies": "MRU, MRU, MRU",
            "access_pattern": "sequential",
            "access_count": 300
        },
        # Large cache sizes, SecondChance policy, random access
        {
            "cache_sizes": "16, 32, 64",
            "replacement_policies": "SecondChance, SecondChance, SecondChance",
            "access_pattern": "random",
            "access_count": 300
        },
        # Large cache sizes, LFU policy, mixed access pattern
        {
            "cache_sizes": "16, 32, 64",
            "replacement_policies": "LFU, LFU, LFU",
            "access_pattern": "sequential",
            "access_count": 300
        },
        {
            "cache_sizes": "16, 32, 64",
            "replacement_policies": "LFU, LFU, LFU",
            "access_pattern": "random",
            "access_count": 300
        }
    ]

    for i, case in enumerate(test_cases):
        print(f"Running Test Case {i + 1}:")
        print(f"Cache Sizes: {case['cache_sizes']}")
        print(f"Replacement Policies: {case['replacement_policies']}")
        print(f"Access Pattern: {case['access_pattern']}")
        print(f"Access Count: {case['access_count']}")
        print("--------------------------------------------------")

        app.entry_cache_size.delete(0, tk.END)
        app.entry_cache_size.insert(0, case['cache_sizes'])

        app.entry_replacement_policy.delete(0, tk.END)
        app.entry_replacement_policy.insert(0, case['replacement_policies'])

        app.entry_access_pattern.delete(0, tk.END)
        app.entry_access_pattern.insert(0, case['access_pattern'])

        app.entry_access_count.delete(0, tk.END)
        app.entry_access_count.insert(0, case['access_count'])

        app.run_simulation()

        print(app.results_text.get("1.0", tk.END))
        print("--------------------------------------------------")

    root.destroy()

if __name__ == "__main__":
    test_simulation()

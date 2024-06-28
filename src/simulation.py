# src/simulation.py
import random
import logging

logging.basicConfig(level=logging.DEBUG)


class MemoryAccessSimulation:
    def __init__(self, memory_hierarchy):
        self.memory_hierarchy = memory_hierarchy

    def generate_accesses(self, pattern, count):
        addresses = []
        if pattern == "sequential":
            addresses = list(range(count))
        elif pattern == "random":
            addresses = [random.randint(
                0, self.memory_hierarchy[-1].size) for _ in range(count)]
        logging.debug(f"Generated Accesses: {addresses}")
        return addresses

    def run_simulation(self, addresses):
        results = {"hits": 0, "misses": 0, "access_times": []}
        for address in addresses:
            for level in self.memory_hierarchy:
                _, hit, access_time = level.access(address)
                results["access_times"].append(access_time)
                if hit:
                    results["hits"] += 1
                    logging.debug(f"Address {address} Hit in {level.name}")
                    break
            else:
                results["misses"] += 1
                logging.debug(f"Address {address} Missed in All Levels")
        return results

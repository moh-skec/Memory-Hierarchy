# src/simulation.py
from memory_hierarchy import CacheMemory


class MemoryAccessSimulation:
    def __init__(self, memory_hierarchy):
        self.memory_hierarchy = memory_hierarchy
        self.first_cache = memory_hierarchy[0]
        self.hits = 0
        self.misses = 0
        self.access_time = 0
        self.total_access_time = 0
        self.accesses = 0

    def access_address(self, address):
        self.accesses += 1
        _, _, access_time, name = self.first_cache.access(address)
        self.access_time = access_time
        self.total_access_time += access_time
        if name in ["L1 Cache", "L2 Cache", "L3 Cache"]:
            self.hits += 1
            return True, _, name
        self.misses += 1
        return False, -1, "all cache levels"

    def get_cache_contents(self):
        cache_contents = {}
        for memory in self.memory_hierarchy:
            if isinstance(memory, CacheMemory):
                cache_contents[memory.name] = list(memory.cache.keys())
        return cache_contents

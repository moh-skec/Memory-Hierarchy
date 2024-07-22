# src/memory_hierarchy.py
from collections import OrderedDict


class MemoryLevel:
    def __init__(self, name, size, access_time):
        self.name = name
        self.size = size
        self.access_time = access_time
        self.data = {}
        self.access_count = 0

    def access(self, address):
        raise NotImplementedError(
            "This method should be implemented by subclasses")


class CacheMemory(MemoryLevel):
    def __init__(self, name, size, access_time, block_size, replacement_policy, lower_level=None):
        super().__init__(name, size, access_time)
        self.block_size = block_size
        self.replacement_policy = replacement_policy(self)
        self.cache = OrderedDict()
        self.lower_level = lower_level

    def access(self, address):
        self.access_count += 1
        block_address = address // self.block_size
        if block_address in self.cache:
            self.replacement_policy.hit(block_address)
            return self.cache[block_address], True, self.access_time, self.name
        else:
            evicted_block = block_address
            if len(self.cache) >= self.size // self.block_size:
                evicted_block = self.replacement_policy.evict()
            data, _, lower_access_time, name = self.lower_level.access(address)
            self.replacement_policy.order = OrderedDict([(block_address, data) if k == evicted_block else (
                k, v) for k, v in self.replacement_policy.order.items()])
            self.replacement_policy.miss(block_address, data)
            return data, False, self.access_time + lower_access_time, name


class MainMemory(MemoryLevel):
    def __init__(self, name, size, access_time, lower_level=None):
        super().__init__(name, size, access_time)
        self.lower_level = lower_level

    def access(self, address):
        self.access_count += 1
        if address in self.data:
            return self.data[address], True, self.access_time, self.name
        else:
            if self.lower_level:
                data, _, lower_access_time, name = self.lower_level.access(
                    address)
            else:
                data, lower_access_time = f"Data at {address}", 0
            self.data[address] = data
            return data, False, self.access_time + lower_access_time, name


class ExternalMemory(MemoryLevel):
    def __init__(self, name, size, access_time):
        super().__init__(name, size, access_time)

    def access(self, address):
        self.access_count += 1
        if address in self.data:
            return self.data[address], True, self.access_time, self.name
        else:
            data = f"Data at {address}"
            self.data[address] = data
            return data, False, self.access_time, "None"

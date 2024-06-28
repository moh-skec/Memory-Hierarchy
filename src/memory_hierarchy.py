# src/memory_hierarchy.py
import logging

logging.basicConfig(level=logging.DEBUG)


class MemoryLevel:
    def __init__(self, name, size, access_speed):
        self.name = name
        self.size = size
        self.access_speed = access_speed
        self.data = {}
        self.access_count = 0

    def access(self, address):
        raise NotImplementedError(
            "This method should be implemented by subclasses")


class CacheMemory(MemoryLevel):
    def __init__(self, name, size, access_speed, replacement_policy, lower_level=None):
        super().__init__(name, size, access_speed)
        self.replacement_policy = replacement_policy(self)
        self.cache = {}
        self.lower_level = lower_level

    def access(self, address):
        self.access_count += 1
        if address in self.cache:
            self.replacement_policy.hit(address)
            logging.debug(f"Cache Hit: {address} in {self.name}")
            return self.cache[address], True, self.access_speed
        else:
            if len(self.cache) >= self.size:
                self.replacement_policy.evict()
            _, _, lower_access_speed = self.lower_level.access(address)
            self.cache[address] = f"Data at {address}"
            self.replacement_policy.miss(address)
            logging.debug(f"Cache Miss: {address} in {self.name}")
            return self.cache[address], False, self.access_speed + lower_access_speed


class MainMemory(MemoryLevel):
    def __init__(self, name, size, access_speed, lower_level=None):
        super().__init__(name, size, access_speed)
        self.lower_level = lower_level

    def access(self, address):
        self.access_count += 1
        if address in self.data:
            logging.debug(f"MainMemory Hit: {address}")
            return self.data[address], True, self.access_speed
        else:
            if self.lower_level:
                _, _, lower_access_speed = self.lower_level.access(address)
            else:
                lower_access_speed = 0
            self.data[address] = f"Data at {address}"
            logging.debug(f"MainMemory Miss: {address}")
            return self.data[address], False, self.access_speed + lower_access_speed


class ExternalMemory(MemoryLevel):
    def access(self, address):
        self.access_count += 1
        if address in self.data:
            logging.debug(f"ExternalMemory Hit: {address}")
            return self.data[address], True, self.access_speed
        else:
            self.data[address] = f"Data at {address}"
            logging.debug(f"ExternalMemory Miss: {address}")
            return self.data[address], False, self.access_speed

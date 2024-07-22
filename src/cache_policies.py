# src/cache_policies.py
from collections import OrderedDict
import random
from math import floor, ceil


class ReplacementPolicy:
    def __init__(self, cache):
        self.cache = cache
        self.order = OrderedDict()
        self.hit_address = None
        self.miss_address = None
        self.data = None

    def hit(self, address):
        self.hit_address = address

    def miss(self, address, data):
        self.data = data
        self.miss_address = address
        raise NotImplementedError

    def evict(self):
        raise NotImplementedError


class LRU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.use = OrderedDict()

    def hit(self, address):
        self.use[address] += 1

    def miss(self, address, data):
        self.order[address] = data
        self.use[address] = 0
        self.cache.cache = self.order

    def evict(self):
        oldest = sorted(self.use.items(), key=lambda x: x[1])[0][0]
        del self.use[oldest]
        return oldest


class FIFO(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)

    def hit(self, address):
        return super().hit(address)

    def miss(self, address, data):
        self.order[address] = data
        self.cache.cache = self.order

    def evict(self):
        oldest = self.order.popitem(last=False)[0]
        return oldest


class Random(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)

    def hit(self, address):
        return super().hit(address)

    def miss(self, address, data):
        self.order[address] = data
        self.cache.cache = self.order

    def evict(self):
        to_evict = random.choice(list(self.order.keys()))
        return to_evict


class MRU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.use = OrderedDict()

    def hit(self, address):
        self.use[address] += 1

    def miss(self, address, data):
        self.order[address] = data
        self.use[address] = 0
        self.cache.cache = self.order

    def evict(self):
        oldest = sorted(self.use.items(), key=lambda x: x[1])[-1][0]
        del self.use[oldest]
        return oldest


class SecondChance(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.frequency = {}
        self.how_long = OrderedDict()

    def hit(self, address):
        self.frequency[address] = 1
        for addr in self.how_long:
            self.how_long[addr] += 1

    def miss(self, address, data):
        self.order[address] = data
        self.frequency[address] = 0
        for addr in self.how_long:
            self.how_long[addr] += 1
        self.how_long[address] = 0
        self.cache.cache = self.order

    def evict(self):
        while True:
            for oldest in OrderedDict(sorted(self.how_long.items(), key=lambda x: x[1], reverse=True)).keys():
                if self.frequency[oldest]:
                    self.frequency[oldest] = 0
                else:
                    del self.frequency[oldest]
                    del self.how_long[oldest]
                    return oldest


class LFU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.frequency = {}  # Keeps track of access frequency

    def hit(self, address):
        self.frequency[address] += 1

    def miss(self, address, data):
        self.order[address] = data
        self.frequency[address] = 1
        self.cache.cache = self.order

    def evict(self):
        # Find the item with the lowest frequency
        min_freq = min(self.frequency.values())
        for address, freq in self.frequency.items():
            if freq == min_freq:
                # Remove the item from frequency
                del self.frequency[address]
                return address


class LFRU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.privileged_size = floor(
            self.cache.size / self.cache.block_size / 2)
        self.unprivileged_size = ceil(
            self.cache.size / self.cache.block_size / 2)
        self.privileged_cache = OrderedDict()
        self.privileged_use = OrderedDict()
        self.unprivileged_cache = OrderedDict()
        self.unprivileged_frequency = {}

    def hit(self, address):
        if address in self.privileged_cache:
            self.privileged_use[address] += 1
        elif address in self.unprivileged_cache:
            oldest = sorted(self.privileged_use.items(),
                            key=lambda x: x[1])[-1][0]
            privilege_data = self.privileged_cache[oldest]
            unprivilege_data = self.unprivileged_cache[address]

            self.privileged_cache = OrderedDict([(address, unprivilege_data) if k == oldest else (
                k, v) for k, v in self.privileged_cache.items()])
            del self.privileged_use[oldest]
            self.privileged_use[address] = 0
            self.unprivileged_cache = OrderedDict([(oldest, privilege_data) if k == address else (
                k, v) for k, v in self.unprivileged_cache.items()])
            del self.unprivileged_frequency[address]
            self.unprivileged_frequency[oldest] = 0
            self.order = self.privileged_cache | self.unprivileged_cache
            self.cache.cache = self.order

    def miss(self, address, data):
        items = list(self.order.items())
        self.privileged_cache = OrderedDict(items[:self.privileged_size])
        self.unprivileged_cache = OrderedDict(
            items[self.privileged_size:self.privileged_size+self.unprivileged_size])
        if len(self.privileged_cache) < self.privileged_size:
            self.privileged_cache[address] = data
            self.privileged_use[address] = 0
        else:
            self.unprivileged_cache[address] = data
            self.unprivileged_frequency[address] = 0
        self.order = self.privileged_cache | self.unprivileged_cache
        self.cache.cache = self.order

    def evict(self):
        items = list(self.order.items())
        self.privileged_cache = OrderedDict(items[:self.privileged_size])
        self.unprivileged_cache = OrderedDict(
            items[self.privileged_size:self.privileged_size+self.unprivileged_size])

        # Find the item with the lowest frequency
        min_freq = min(self.unprivileged_frequency.values())
        for address, freq in self.unprivileged_frequency.items():
            if freq == min_freq:
                # Remove the item from both unprivileged frequency and cache
                del self.unprivileged_frequency[address]
                del self.unprivileged_cache[address]
                return address

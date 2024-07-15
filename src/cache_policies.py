# src/cache_policies.py
from collections import defaultdict, OrderedDict

class ReplacementPolicy:
    def __init__(self, cache):
        self.cache = cache

    def hit(self, address):
        raise NotImplementedError

    def miss(self, address):
        raise NotImplementedError

    def evict(self):
        raise NotImplementedError


class LRU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.order = OrderedDict()

    def hit(self, address):
        if address in self.order:
            self.order.move_to_end(address)
            self.cache.cache = self.order

    def miss(self, address):
        self.order[address] = None

    def evict(self):
        if self.order:
            oldest = self.order.popitem(last=False)
            return oldest[0]


class FIFO(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.order = OrderedDict()

    def hit(self, address):
        pass  # No action needed for FIFO on hit

    def miss(self, address):
        self.order[address] = None

    def evict(self):
        if self.order:
            oldest = self.order.popitem(last=False)
            return oldest[0]


class Random(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)

    def hit(self, address):
        pass  # No action needed for Random on hit

    def miss(self, address):
        pass  # No action needed for Random on miss

    def evict(self):
        import random
        if self.cache.cache:
            to_evict = random.choice(list(self.cache.cache.keys()))
            return to_evict


class MRU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.order = OrderedDict()

    def hit(self, address):
        if address in self.order:
            self.order.move_to_end(address)
            self.cache.cache = self.order

    def miss(self, address):
        self.order[address] = None

    def evict(self):
        if self.order:
            newest = self.order.popitem(last=True)
            return newest[0]


class SecondChance(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.order = OrderedDict()
        self.frequency = {}

    def hit(self, address):
        self.frequency[address] = True

    def miss(self, address):
        self.order[address] = None
        self.frequency[address] = False
        self.cache.cache = self.order

    def evict(self):
        while self.order:
            oldest = next(iter(self.order))
            if self.frequency[oldest]:
                self.order.move_to_end(oldest)
                self.frequency[oldest] = False
            else:
                del self.order[oldest]
                del self.frequency[oldest]
                return oldest


class LFU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.frequency = {}  # Keeps track of access frequency
        self.order = OrderedDict()

    def hit(self, address):
        if address in self.frequency:
            self.frequency[address] += 1
        else:
            self.frequency[address] = 1
        self.order[address] = self.frequency[address]

    def miss(self, address):
        self.frequency[address] = 1
        self.order[address] = 1
        self.cache.cache = self.order

    def evict(self):
        if self.order:
            # Find the item with the lowest frequency
            min_freq = min(self.order.values())
            for address, freq in self.order.items():
                if freq == min_freq:
                    # Remove the item from both frequency and order
                    del self.order[address]
                    del self.frequency[address]
                    return address


class LFRU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.frequency = {}
        self.order = OrderedDict()

    def hit(self, address):
        if address in self.frequency:
            self.frequency[address] += 1
        else:
            self.frequency[address] = 1
        self.order[address] = self.frequency[address]

    def miss(self, address):
        self.frequency[address] = 1
        self.order[address] = 1
        self.cache.cache = self.order

    def evict(self):
        if self.order:
            min_freq = min(self.order.values())
            for address, freq in self.order.items():
                if freq == min_freq:
                    # Remove the item from both frequency and order
                    del self.order[address]
                    del self.frequency[address]
                    return address

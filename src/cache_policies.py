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
        self.order = []

    def hit(self, address):
        if address in self.order:
            self.order.remove(address)
        self.order.append(address)

    def miss(self, address):
        if address not in self.order:
            self.order.append(address)

    def evict(self):
        if self.order:
            oldest = self.order.pop(0)
            del self.cache.cache[oldest]

class FIFO(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.order = []

    def hit(self, address):
        pass  # No action needed for FIFO on hit

    def miss(self, address):
        if address not in self.order:
            self.order.append(address)

    def evict(self):
        if self.order:
            oldest = self.order.pop(0)
            del self.cache.cache[oldest]

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
            del self.cache.cache[to_evict]

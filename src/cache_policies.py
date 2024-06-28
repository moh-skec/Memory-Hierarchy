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

class MRU(ReplacementPolicy):
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
            newest = self.order.pop()
            del self.cache.cache[newest]

class SecondChance(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.order = []
        self.reference_bits = {}

    def hit(self, address):
        if address in self.reference_bits:
            self.reference_bits[address] = True

    def miss(self, address):
        if address not in self.reference_bits:
            self.order.append(address)
            self.reference_bits[address] = True

    def evict(self):
        while self.order:
            address = self.order.pop(0)
            if self.reference_bits[address]:
                self.reference_bits[address] = False
                self.order.append(address)
            else:
                del self.cache.cache[address]
                del self.reference_bits[address]
                break

class LFU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.frequency = {}

    def hit(self, address):
        if address in self.frequency:
            self.frequency[address] += 1

    def miss(self, address):
        if address not in self.frequency:
            self.frequency[address] = 1

    def evict(self):
        if self.frequency:
            least_used = min(self.frequency, key=self.frequency.get)
            del self.cache.cache[least_used]
            del self.frequency[least_used]
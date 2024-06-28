# src/cache_policies.py
from collections import OrderedDict, deque
import heapq
import logging

logging.basicConfig(level=logging.DEBUG)


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
            logging.debug(f"LRU Hit: {address}")

    def miss(self, address):
        self.order[address] = None
        logging.debug(f"LRU Miss: {address}")

    def evict(self):
        if self.order:
            oldest = self.order.popitem(last=False)
            del self.cache.cache[oldest[0]]
            logging.debug(f"LRU Evict: {oldest[0]}")


class FIFO(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.order = deque()

    def hit(self, address):
        pass  # No action needed for FIFO on hit

    def miss(self, address):
        self.order.append(address)
        logging.debug(f"FIFO Miss: {address}")

    def evict(self):
        if self.order:
            oldest = self.order.popleft()
            del self.cache.cache[oldest]
            logging.debug(f"FIFO Evict: {oldest}")


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
            logging.debug(f"Random Evict: {to_evict}")


class MRU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.order = []

    def hit(self, address):
        if address in self.order:
            self.order.remove(address)
        self.order.append(address)
        logging.debug(f"MRU Hit: {address}")

    def miss(self, address):
        if address not in self.order:
            self.order.append(address)
        logging.debug(f"MRU Miss: {address}")

    def evict(self):
        if self.order:
            newest = self.order.pop()
            del self.cache.cache[newest]
            logging.debug(f"MRU Evict: {newest}")


class SecondChance(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.order = deque()
        self.reference_bits = {}

    def hit(self, address):
        self.reference_bits[address] = True
        logging.debug(f"SecondChance Hit: {address}")

    def miss(self, address):
        self.order.append(address)
        self.reference_bits[address] = True
        logging.debug(f"SecondChance Miss: {address}")

    def evict(self):
        while self.order:
            address = self.order.popleft()
            if self.reference_bits[address]:
                self.reference_bits[address] = False
                self.order.append(address)
            else:
                del self.cache.cache[address]
                del self.reference_bits[address]
                logging.debug(f"SecondChance Evict: {address}")
                break


class LFU(ReplacementPolicy):
    def __init__(self, cache):
        super().__init__(cache)
        self.frequency = {}
        self.heap = []

    def hit(self, address):
        if address in self.frequency:
            self.frequency[address] += 1
            logging.debug(f"LFU Hit: {address}")

    def miss(self, address):
        self.frequency[address] = 1
        heapq.heappush(self.heap, (self.frequency[address], address))
        logging.debug(f"LFU Miss: {address}")

    def evict(self):
        while self.heap:
            freq, address = heapq.heappop(self.heap)
            if self.frequency.get(address) == freq:
                del self.cache.cache[address]
                del self.frequency[address]
                logging.debug(f"LFU Evict: {address}")
                break

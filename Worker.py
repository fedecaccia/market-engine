import logging
from threading import Thread

from PriceQueue import PriceQueue
from PricePoint import PricePoint


class CoinbaseWorker(Thread):

    def __init__(self, queue, mutex, pair, precision):

        Thread.__init__(self)
        self.queue = queue
        self.mutex = mutex
        self.last_sequence = None
        self.prices = PriceQueue(200, pair, precision)

    def setLastSequence(self, sequence):
        self.last_sequence = sequence

    def checkLastSequence(self, sequence):
        
        if self.last_sequence != None and sequence != self.last_sequence + 1:
            logging.warning("WARNING, last sequence: %d and new sequence: %d" % (self.last_sequence, sequence))

        self.setLastSequence(sequence)

    def run(self):

        item = self.queue.get()

        while item != None:

            product = item["product_id"]
            # side = item["side"]
            size = item["size"]
            price = item["price"]
            sequence = item["sequence"]
            
            self.checkLastSequence(sequence)
            price = PricePoint(price, size)

            self.mutex.acquire()

            self.prices.update(price)

            self.mutex.release()
            
            item = self.queue.get()
from queue import Queue
from threading import Lock
import json

from Client import CoinbaseClient
from Worker import CoinbaseWorker


class MarketEngine:

    def __init__(self):

        self.pairs = []
        self.precisions = []
        self.queues = {}
        self.mutex = Lock()
        self.source = None
        self.client_workers = []
        self.pair_workers = []

    def loadConfig(self, config_file):
        
        config = json.load(open(config_file))
        self.source = config["source"]
        pairs = config["pairs"]
        self.pairs = []
        self.precisions = []
        for p in pairs:
            self.pairs.append(p["name"])
            self.precisions.append(p["precision"])
            self.queues[p["name"]] = Queue()

    def run(self):

        if self.source == "coinbase":
            worker = CoinbaseClient(self.queues, self.pairs)
            worker.start()
            self.client_workers.append(worker)

            for (pair, precision) in zip(self.pairs, self.precisions):
                worker = CoinbaseWorker(self.queues[pair], self.mutex, pair, precision)
                worker.start()
                self.pair_workers.append(worker)

            for w in self.client_workers:
                w.join()
            for w in self.pair_workers:
                w.join()
            
        else:
            raise Exception("Unrecognized source")
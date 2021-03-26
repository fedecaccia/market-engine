import numpy as np
import logging


class PriceQueue:
    
    def __init__(self, max_elem, name, precision):

        self.max = max_elem
        self.total_elems = 0
        self.average = None
        self.total_vol = None
        self.first = None
        self.last = None
        self.name = name
        self.precision = precision

    def update(self, node):

        if self.first is None:

            self.first = node
            self.last = node
            self.average = node.price
            self.total_vol = node.size
            self.total_elems = 1

        else:
        
            node.next = self.first
            self.first.prev = node
            self.first = node
            self.total_elems += 1            

            cap = self.average * self.total_vol
            new_cap = cap + node.size * node.price
            self.total_vol += node.size

            if self.total_elems > self.max:
                removing = self.last
                self.last = self.last.prev
                self.total_elems -= 1
                new_cap -= removing.size * removing.price
                self.total_vol -= removing.size

            self.average = new_cap / self.total_vol

        logging.info("Updated %s average: " %(self.name) + str(np.around(self.average, decimals = self.precision)))
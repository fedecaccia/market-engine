import websocket
import time
import json
from threading import Thread

from PricePoint import PricePoint
from PriceQueue import PriceQueue


class CoinbaseClient(Thread):

    def __init__(self, queues, pairs):

        Thread.__init__(self)
        self.queues = queues
        self.pairs = pairs

    def on_message(self, ws, message):

        msg = json.loads(message)
        
        if (msg["type"] == "error"):
            logging.error("ERROR found, original message: %s" % msg["message"])
        
        if (msg["type"] == "match"):
            self.queues[msg["product_id"]].put(msg)

    def on_open(self, ws):
        payload = {
            "type":"subscribe", 
            "product_ids":[], 
            "channels":["matches"]
        }
        for p in self.pairs:
            payload["product_ids"].append(p)
            
        ws.send(json.dumps(payload))

    def on_error(self, ws, error):
        logging.error(error)

    def on_close(self, ws):
        logging.info("### ws closed ###")

    def run(self):
        ws = websocket.WebSocketApp(
            "wss://ws-feed.pro.coinbase.com/",
            on_open = self.on_open,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close)
        ws.run_forever()
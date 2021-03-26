# Market Engine

Welcome to the source code of the crypto market engine to compute (VWAP)[https://en.wikipedia.org/wiki/Volume-weighted_average_price]. The `MarketEngine` class is exchange agnostic and it runs mutiple threads to stream/process data from the selected source. Right now, it only accepts `coinbase` as the market source.

## Quickstart

The program runs on Python3. To use the MarketEngine class we recommend you to prepare a virtual environment, install dependencies and imoprt the class in your main file. It just needs to load configuration from a `config.json` file and then its ready to run. 

The configuration file only expects two fields: `pairs` and `source`. `pairs` contains an array of the different markets which will be post-processed, containing the `name` and the `precision` to output the computation in each pair. `source` details the exchange source used to stream data.

Use the following snippet to run the engine (you can just run `example.py` which implements it):

```
from MarketEngine import MarketEngine


if __name__ == "__main__":

    m = MarketEngine()
    m.loadConfig("config.json")
    m.run()
```

## How it Works

The main class, MarketEngine, shoots one thread that keeps the websocket connection with the market source, which puts each product message on a differet queue. At the same time, the engine shoots one thread per queue to post-process the jobs scheduled. Each of those threads compute the VWAP on a different pair and just log to standard output.

VWAP is computed using last 200 match points. Due to the high frequency of the updates, and the small amount of points considered, we don't lose time connecting to a database and, instead, all points are loaded on memory in a linked list. A database that supports fast I/O operations like redis or an "in memory" table in a SQL server could be the solution to scale the engine, if we need to process big data.
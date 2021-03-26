import logging

from MarketEngine import MarketEngine


if __name__ == "__main__":
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    m = MarketEngine()
    logging.info("Loading config")
    m.loadConfig("config.json")
    logging.info("Running market engine")
    m.run()
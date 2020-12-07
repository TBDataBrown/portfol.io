import time
import sched
import logging
import requests
from io import StringIO

import utils
from database import upsert_bpa

import logging
import pymongo
import expiringdict

import pandas as pd
import yfinance as yf
import numpy as np


# parameter for testing
portfolio = ['TSLA', 'AMD', 'ZM', 'MRNA', 'PTON', 'AAPL', 'TGT', 'WMT', 'SBUX', 'ABBV', 'NIO', 'SPY', '^DJI']
p = '5d'
i = '1m'


# database info
MAX_DOWNLOAD_ATTEMPT = 5
DOWNLOAD_PERIOD = 10         # second
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'data.log')
client = pymongo.MongoClient()


# Download data for one stock
def download_one(t, p, i):
    data = yf.download(
            tickers = t,
            period = p,
            interval = i,
            group_by = 'ticker',
            auto_adjust = True,
            prepost = False,
            threads = True,
            proxy = None,
            # no progress bar
            progress=False)
    data.reset_index(inplace=True,drop=False)
    data.rename(columns = {'Close':t}, inplace = True) 
    data = data.drop(['Open', 'High','Low','Volume'], axis=1)
    return data


# Download data for a portfolio
def make_portfolio(port, p ,i):
    rst = download_one(port[0],p,i)
    for t in port[1:]:
        one = download_one(t,p,i)
        rst = pd.merge(rst, one, on = 'Datetime', how = 'outer', sort = True)
    return rst


# Update once
def update_once(port, p ,i):
    df = make_portfolio(port, p, i)
    upsert_stock(df)


# Keep updating
def main_loop(timeout=DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
        try:
            print("Updating")
            update_once(portfolio, p ,i)
        except Exception as e:
            logger.warning("main loop worker ignores exception and continues: {}".format(e))
        scheduler.enter(timeout, 1, _worker)    # schedule the next event

    scheduler.enter(0, 1, _worker)              # start the first event
    scheduler.run(blocking=True)


# Call main loop
if __name__ == '__main__':
    main_loop()


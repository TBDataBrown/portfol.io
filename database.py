#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import yfinance as yf
import numpy as np
from sklearn.preprocessing import StandardScaler


# In[7]:


import logging
import pymongo
import pandas as pds
import expiringdict

import utils

client = pymongo.MongoClient(host=['127.0.0.1:27017'])
logger = logging.Logger(__name__)
RESULT_CACHE_EXPIRATION = 10        


def upsert_stock(df):
    """
    Update MongoDB database `stock` and collection `stock` with the given `DataFrame`.
    """
    db = client.get_database("stock")
    collection = db.get_collection("stock3")
    update_count = 0
    for record in df.to_dict('records'):
        result = collection.replace_one(
            filter={'Datetime': record['Datetime']},    
            replacement=record,                         
            upsert=True)                                
        if result.matched_count > 0:
            update_count += 1
    logger.info("rows={}, update={}, ".format(df.shape[0], update_count) +
                "insert={}".format(df.shape[0]-update_count))


def fetch_all_stock():
    db = client.get_database("stock")
    
    # drop for now
    db.stock3.drop()
    
    collection = db.get_collection("stock3")
    ret = list(collection.find())
    logger.info(str(len(ret)) + ' documents read from the db')
    return ret


_fetch_all_stock_as_df_cache = expiringdict.ExpiringDict(max_len=1,
                                                       max_age_seconds=RESULT_CACHE_EXPIRATION)


def fetch_all_stock_as_df(allow_cached=False):
    """Converts list of dicts returned by `fetch_all_stock` to DataFrame with ID removed
    Actual job is done in `_worker`. When `allow_cached`, attempt to retrieve timed cached from
    `_fetch_all_stock_as_df_cache`; ignore cache and call `_work` if cache expires or `allow_cached`
    is False.
    """
    def _work():
        data = fetch_all_stock()
        if len(data) == 0:
            return None
        df = pds.DataFrame.from_records(data)
        df.drop('_id', axis=1, inplace=True)
        return df

    if allow_cached:
        try:
            return _fetch_all_stock_as_df_cache['cache']
        except KeyError:
            pass
    ret = _work()
    _fetch_all_stock_as_df_cache['cache'] = ret
    return ret


if __name__ == '__main__':
    print(fetch_all_stock_as_df())


# In[ ]:





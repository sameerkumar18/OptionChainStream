"""
@author: rakeshr
"""
"""
Dump all exchange instruments/contract data to Redis
Retrive strike and instrument token detail from redis for each symbol search
"""

import redis
import json
import os


REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
REDIS_DB = os.environ.get('REDIS_DB', 0)


class InstrumentDumpFetch():
    
    def __init__(self):
        # Default redis port connection
        # Port no and host be edited by user or will make both as acceptable argument in later release 
        self.conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)

    def data_dump(self, symbol, instrument_data):
        """
        Dump specific exchange complete instrument data
        Param symbol:(string) - Option contract symbol
        Param instrument_data:(dictionary) - List of dict for specific option contract containing all strike, etc 
        """
        self.conn.set(symbol, json.dumps(instrument_data))

    def symbol_data(self, symbol):    
        """
        Return instrument detail for required symbol
        Param symbol:(string) - Option contract symbol to be searched
        """
        try:
            contract_detail = json.loads(self.conn.get(symbol))
        except TypeError:
            raise Exception('Key not found - {}'.format(symbol))
        return contract_detail

    def fetch_token(self, token):
        """
        Fetch contract name for requested instrument token
        Param token:(integer) - Instrument token 
        """
        try:
            token_instrument = json.loads(self.conn.get(token))
        except Exception as e:
            raise Exception('Error {}'.format(e))
        return token_instrument

    def store_optiondata(self, tradingsymbol, token, optionData):
        """
        Store option chain data for requested symbol
        Param symbol:(string) - Option contract symbol
        Param token:(integer) - Instrument token
        Param optionData:(dict) - Complete data dump for specific option symbol
        """
        optionChainKey = '{}:{}'.format(tradingsymbol, token)
        try:
            self.conn.set(optionChainKey, json.dumps(optionData))
        except Exception as e:
            raise Exception('Error - {}'.format(e))

    def fetch_option_data(self, tradingsymbol, token):
        """
        Fetch stored option data
        Param symbol:(string) - Option contract symbol
        Param token:(integer) - Instrument token
        """
        optionContractKey = '{}:{}'.format(tradingsymbol, token)
        try:
            token_data = json.loads(self.conn.get(optionContractKey))
        except Exception as e:
            raise Exception('Error - {}'.format(e))
        return token_data

# LIVE
import logging
import requests, urllib3
import time
import typing
from urllib.parse import urlencode
import hmac
import hashlib
# import pprint
from tools import setup_logger_v2
import json


logger = logging.getLogger()

class BinanceClient_v2:
    def __init__(self, db, _proxy, _source_addr, public_key: str, secret_key: str, testnet: bool, futures: bool, bot_id: int, bot_name: str): 
        """
        https://binance-docs.github.io/apidocs/futures/en
        :param public_key:
        :param secret_key:
        :param testnet:
        :param futures: if False, the Client will be a Spot API Client
        """

        self.futures = futures

        if self.futures:
            self.platform = "binance_futures"
            if testnet:
                self._base_url = "https://testnet.binancefuture.com"
                self._wss_url = "wss://stream.binancefuture.com/ws"
            else:
                self._base_url = "https://fapi.binance.com"
                self._wss_url = "wss://fstream.binance.com/ws"
        else:
            self.platform = "binance_spot"
            if testnet:
                self._base_url = "https://testnet.binance.vision"
                self._wss_url = "wss://testnet.binance.vision/ws"
            else:
                self._base_url = "https://api.binance.com"
                self._wss_url = "wss://stream.binance.com:9443/ws"
        

        self.bot_id = bot_id
        self.bot_name = bot_name
        # self.bot_note = bot_note
        # self.bot_k_type = bot_k_type
        # self.bot_type = bot_type
        # self.bot_symbol = bot_symbol
        # self.bot_qty = bot_qty
        # self.bot_tp_per = bot_tp_per
        # self.bot_sl_per = bot_sl_per
        # self.bot_time_sleep = bot_time_sleep
        # self.bot_play_same_time = bot_play_same_time
           
        self._public_key = public_key
        self._secret_key = secret_key

        self._headers = {'X-MBX-APIKEY': self._public_key}


        self.bot_logger = setup_logger_v2(bot_name+".log")
        # self.bot_logger.info("Binance Futures Client successfully initialized --connectors.binance")

        self.db = db
        self._proxy = _proxy
        self._source_addr = _source_addr
        # self.cur_open_order = []
        self.bot_level = 20 # Don bay x20

    def _generate_signature(self, data: typing.Dict) -> str:

        """
        Generate a signature with the HMAC-256 algorithm.
        :param data: Dictionary of parameters to be converted to a query string
        :return:
        """

        return hmac.new(self._secret_key.encode(), urlencode(data).encode(), hashlib.sha256).hexdigest()

    def _make_request_old_by_request(self, method: str, endpoint: str, data: typing.Dict):

        """
        This can use with proxy
        Wrapper that normalizes the requests to the REST API and error handling.
        :_proxy: none or sample: '10.100.20.30:8080'
        :param method: GET, POST, DELETE
        :param endpoint: Includes the /api/v1 part
        :param data: Parameters of the request
        :return:
        """
        if self._proxy:
            proxy_use = {
                "http": "http://" + self._proxy,
                "https": "http://" + self._proxy
                }
        else:
            proxy_use = None

        if method == "GET":
            try:
                response = requests.get(self._base_url + endpoint, params=data, headers=self._headers, proxies=proxy_use)
            except Exception as e:  # Takes into account any possible error, most likely network errors
                self.bot_logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "POST":
            try:
                response = requests.post(self._base_url + endpoint, params=data, headers=self._headers, proxies=proxy_use)
            except Exception as e:
                self.bot_logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "DELETE":
            try:
                response = requests.delete(self._base_url + endpoint, params=data, headers=self._headers, proxies=proxy_use)
            except Exception as e:
                self.bot_logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None
        else:
            raise ValueError()

        if response.status_code == 200:  # 200 is the response code of successful requests
            # self.bot_logger.info("X-MBX-USED-WEIGHT-1M: %s"%response.headers['X-MBX-USED-WEIGHT-1M'])
            # self.bot_logger.info(response.headers)
            return response.json()
        else:
            self.bot_logger.error("Error while making %s request to %s: %s (error code %s)",
                         method, endpoint, response.json(), response.status_code)
            # return None # Original
            return response.json()

    def _make_request(self, method: str, endpoint: str, data: typing.Dict):

        """
        This use with multi network interface
        Wrapper that normalizes the requests to the REST API and error handling.
        :_proxy: none or sample: '10.100.20.30:8080'
        :param method: GET, POST, DELETE
        :param endpoint: Includes the /api/v1 part
        :param data: Parameters of the request
        :return:
        """
        if self._proxy:
            proxy_use = {
                "http": "http://" + self._proxy,
                "https": "http://" + self._proxy
                }
        else:
            proxy_use = None        

        if self._source_addr:
            http = urllib3.PoolManager(source_address=self._source_addr)
        else:
            http = urllib3.PoolManager(source_address=self._source_addr)


        if method == "GET":
            try:
                response = http.request('GET', self._base_url + endpoint, fields=data, headers=self._headers)
            except Exception as e:  # Takes into account any possible error, most likely network errors
                self.bot_logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "POST":
            try:
                response = http.request("POST", self._base_url + endpoint, fields=data, headers=self._headers)
            except Exception as e:
                self.bot_logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "DELETE":
            try:
                response = http.request("DELETE", self._base_url + endpoint, fields=data, headers=self._headers)
            except Exception as e:
                self.bot_logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None
        else:
            raise ValueError()

        if response.status == 200:  # 200 is the response code of successful requests
            # self.bot_logger.info("X-MBX-USED-WEIGHT-1M: %s"%response.headers['X-MBX-USED-WEIGHT-1M'])
            # self.bot_logger.info(response.headers)
            json_data = json.loads(response.data.decode('utf-8'))
            return json_data
        else:
            self.bot_logger.error("Error while making %s request to %s: %s (error code %s)",
                         method, endpoint, json.loads(response.data.decode('utf-8')), response.status_code)
            # return None # Original
            return json.loads(response.data.decode('utf-8'))
        
    def get_historical_candles(self, _symbol, _ktype, _limit:int):
        data = dict()
        data['symbol'] = _symbol
        data['interval'] = _ktype
        data['limit'] = _limit

        # print ("binance2 - starting get_historical_candles %s %s %s..."%(_symbol, _ktype, _limit))
        raw_candles = self._make_request("GET", "/fapi/v1/klines", data)   # /api/v3/klines  #/fapi/v1/klines

        candles = []
        try:
            if raw_candles is not None:
                for c in raw_candles:
                    candles.append([c[0], float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])])
            return candles  
        except Exception as e:
            return ("Error: %s"%e)
        
  
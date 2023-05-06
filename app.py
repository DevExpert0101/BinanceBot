from flask import Flask
from config import config_flask_dev, coin_list
from datetime import datetime
from flask_crontab import Crontab
from concurrent.futures import ThreadPoolExecutor
from connectors.binance2 import BinanceClient_v2
from tools import setup_logger
from flask_sqlalchemy import SQLAlchemy
from main import get_klines_limit, worker_crawl_data

app = Flask(__name__, template_folder='templates') 
app.config.from_object(config_flask_dev)
db = SQLAlchemy(app)
# db = SQLAlchemy()
# db.init_app(app)
crontab = Crontab(app)

logger_general = setup_logger('general_logger', './logs/crawler_data.log')


@crontab.job(minute="*/2")
def scheduled_crawler_data_v1():
    start_job=datetime.now()
    # db = None
    _interface_list = [('10.140.0.4',0), ('10.1.0.2',0), ('10.1.2.2',0), ('10.1.3.2',0)] # CHECKPOINT --> Replace this with other interface
    num_of_interface = len(_interface_list)
    next_interface_index = 0

    public_key = "000000000000"
    secret_key = "000000000000"
    testnet = False
    futures = True
    bot_id = 1
    # bot_name ="crawler_"

    _type_list = ['3m', '5m', '15m', '30m', '1h', '4h', '1d']
    _i_num = 1
    # num_coin_process_same_time = 15
    # num_max_thread_same_time = num_coin_process_same_time * len(_type_list)

    kline_limit_dict = dict()

    for coin in coin_list:
        coin_limit_by_type = dict()
        for ktype in _type_list:
            coin_limit_by_type[ktype] = get_klines_limit(coin, ktype)
        kline_limit_dict[coin] = coin_limit_by_type

    i_need_data = len(coin_list)

    with ThreadPoolExecutor(max_workers=30) as executor:
        while i_need_data > 0:
            for _coin in coin_list:
                bot_name = "crawler_" + str(_i_num) + "_" + _coin
                _interface = _interface_list[next_interface_index]
                crawler = BinanceClient_v2(None, None, _interface, public_key, secret_key, testnet, futures, bot_id, bot_name)
                for i in range(7):
                    k_type = _type_list[i]
                    # limit = get_klines_limit(_coin, k_type)

                    # print ("app--Submiting worker for: %s %s %s"%(_coin, k_type, limit))
                    executor.submit(worker_crawl_data, crawler, _coin, k_type, kline_limit_dict[_coin][k_type])
                    
                    
                    # executor.submit(worker_crawl_data, crawler, _coin, k_type, 2)
                next_interface_index = (next_interface_index + 1) % num_of_interface
                _i_num += 1
                i_need_data -= 1
                # print("app--number of need_data: %s"%i_need_data)
        

    logger_general.info("Run time: %s"%(datetime.now()-start_job))
    print("Run time: %s"%(datetime.now()-start_job))


scheduled_crawler_data_v1()
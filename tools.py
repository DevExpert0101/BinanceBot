# LIVE
# #02--Use for log system.
import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
# logger_indicator = setup_logger('general_logger', './logs/_indicator.log')

def setup_logger_v2(name, level=logging.INFO):
    log_file = './logs/' + name
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


import time 
time_sub = time.ctime()
def name_now_time():
    name_now_time=str(time.ctime()).replace(":","-").replace(" ","-")
    return (name_now_time)

 # 02--Use to handle datetime and timestamp from Binance.   
import time
from datetime import datetime,timedelta
from pytz import timezone


def get_timestamp_now():
    now_= datetime.now()
    ts_now = round(datetime.timestamp(now_)*1000,0)
    return int(ts_now)# Timestamp base Binance

def get_diff_time_misec(timestamp):
    ts_now = get_timestamp_now()
    diff_mili_sec = ts_now - timestamp
    return(diff_mili_sec)

def get_datetime_before_days(day): 
    datetime_ = datetime.now() - timedelta(days=day)
    return datetime_

def _get_hour_of_this_time():
    import datetime
    hour_ = datetime.datetime.now().hour
    return(hour_)

def get_timestamp_of_this_hour():
    hour_ = _get_hour_of_this_time()
    datetime_= datetime.now()
    start_hour = datetime_.replace(hour=hour_, minute=0, second=0, microsecond=0)
    ts_start_hour = round(datetime.timestamp(start_hour)*1000,0)
    return int(ts_start_hour) # Timestamp base Binance

def get_datetime_from_timestamp(ts): #work with Binance data   
    # import datetime
    return datetime.fromtimestamp(ts/1000)

def get_timestamp_from_datetime(dt):
    ts_ = round(datetime.timestamp(dt)*1000,0)
    return int(ts_) # Timestamp base Binance

def get_datetime_utc7(datetime_,diff_day=-7/24): 
    datetime_ = datetime_ - timedelta(days=diff_day)
    return datetime_
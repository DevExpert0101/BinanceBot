import time
from tools import get_datetime_before_days, get_timestamp_from_datetime, get_datetime_from_timestamp

from sqlalchemy import update



def get_timestamp_of_last_klines_from_db(_symbol, _ktype):
    from app import app, db

    with app.app_context():
        sql = '''SELECT k_timestamp FROM auto_trading_pro.at_klines where k_type = "@ktype@" and k_symbol = "@ksymbol@" order by id desc limit 1'''
        sql = sql.replace("@ktype@",_ktype)
        sql = sql.replace("@ksymbol@",_symbol)

        # print("main--get lastest ts: %s"%sql)
        try:
            last_timestamp_db = db.engine.execute(sql).fetchone()
        except:
            print("main--error when check last ts of %s %s!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"%(_symbol, _ktype))
            last_timestamp = get_timestamp_from_datetime(get_datetime_before_days(5/24))
        db.session.remove()
        # print("main--get lastest ts: %s --remove"%sql)

        # THIS FIX ERROR FOR FIRST TIME PROCESS NEW KLINES TYPE
        try:
            last_timestamp = last_timestamp_db.k_timestamp 
        except:
            last_timestamp = get_timestamp_from_datetime(get_datetime_before_days(10))
        return last_timestamp

def get_klines_limit(_symbol, _ktype):
    now_ts = int(time.time() * 1000)
    if _ktype == "4h":
        last_ts_of_k_4h = get_timestamp_of_last_klines_from_db(_symbol, "4h")
        kline_backdate_interval = int((now_ts - last_ts_of_k_4h)//14400000) # 4*3600*1000
        # kline_backdate_interval = 8
    elif _ktype == "1d":
        last_ts_of_k_1d = get_timestamp_of_last_klines_from_db(_symbol, "1d")
        kline_backdate_interval = int((now_ts - last_ts_of_k_1d)//86400000) # 3600s*1000milisec
    elif _ktype == "1h":
        last_ts_of_k_1h = get_timestamp_of_last_klines_from_db(_symbol, "1h")
        kline_backdate_interval = int((now_ts - last_ts_of_k_1h)//3600000) # 3600s*1000milisec
        # kline_backdate_interval = 24
    elif _ktype == "15m":
        last_ts_of_k_15m = get_timestamp_of_last_klines_from_db(_symbol, "15m")
        kline_backdate_interval = int((now_ts - last_ts_of_k_15m)//900000) # +1 for safe
        # kline_backdate_interval = 90
    elif _ktype == "3m":
        last_ts_of_k_15m = get_timestamp_of_last_klines_from_db(_symbol, "3m")
        kline_backdate_interval = int((now_ts - last_ts_of_k_15m)//180000) # +1 for safe
        # kline_backdate_interval = 90
    elif _ktype == "5m":
        last_ts_of_k_15m = get_timestamp_of_last_klines_from_db(_symbol, "5m")
        kline_backdate_interval = int((now_ts - last_ts_of_k_15m)//300000) # +1 for safe
    elif _ktype == "30m":
        last_ts_of_k_30m = get_timestamp_of_last_klines_from_db(_symbol, "30m")
        kline_backdate_interval = int((now_ts - last_ts_of_k_30m)//1800000) # +1 for safe
        # kline_backdate_interval = 90
    elif _ktype == "2h":
        last_ts_of_k_2h = get_timestamp_of_last_klines_from_db(_symbol, "2h")
        kline_backdate_interval = int((now_ts - last_ts_of_k_2h)//7200000) # +1 for safe
        # kline_backdate_interval = 90
    else:
        kline_backdate_interval = 2
    
    return (kline_backdate_interval + 1)
    # return (2)

def insert_kline_to_db(_symbol, _type, _data):
    from app import db
    from models.at_klines import at_klines
    _k_timestamp = _data[0]
    _date_time = get_datetime_from_timestamp(_k_timestamp)
    _open = _data[1]
    _high = _data[2]
    _low = _data[3]
    _close = _data[4]
    _volume = _data[5]

    with db.session.begin():
        # kline_valid = at_klines.query.filter_by(k_symbol=_symbol, k_type=_type, k_timestamp=_k_timestamp).first()

        kline_valid = at_klines.query.with_entities(at_klines.id).filter_by(k_symbol=_symbol, k_type=_type, k_timestamp=_k_timestamp).first()


        if not kline_valid:
            new_kline = at_klines(
                k_symbol=_symbol,
                k_type=_type,
                k_timestamp=_k_timestamp,
                k_datetime=_date_time,
                k_open=_open,
                k_high=_high,
                k_low=_low,
                k_close=_close,
                k_volume=_volume
            )
            db.session.add(new_kline)
        else:
            stmt = update(at_klines).where(at_klines.id == kline_valid.id).values(
                    k_high=_high,
                    k_low=_low,
                    k_close=_close,
                    k_volume=_volume
                )
            
            db.engine.execute(stmt)

        db.session.commit()
    db.session.remove()

def worker_crawl_data(crawler, _symbol, _type, _limit):
    from app import app
    # from models.at_klines import at_klines
    with app.app_context():
        kline_data = crawler.get_historical_candles(_symbol, _type, _limit)

        print("main--kline_data recieved data %s %s: return data: %s"%(_symbol, _type, len(kline_data)))
        for _data in kline_data:
            insert_kline_to_db(_symbol, _type, _data)
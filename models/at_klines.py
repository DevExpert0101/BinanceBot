# LIVE
create_table = False

if create_table:
    import sys
    sys.path.append('/mnt/auto_trading_pro/')

from app import db

    # from app import db, app

class at_klines(db.Model):
    __tablename__ = 'at_klines'
    # __tablename__ = 'klines_1h_indicator_7'

    id = db.Column(db.Integer, primary_key=True)
    k_symbol = db.Column(db.String(128))
    k_type = db.Column(db.String(32))
    k_timestamp = db.Column(db.BigInteger)
    k_datetime = db.Column(db.String(128))
    # k_datetime_utc7 = db.Column(db.String(128))
    k_open = db.Column(db.Float)
    k_high = db.Column(db.Float)
    k_low = db.Column(db.Float)
    k_close = db.Column(db.Float)
    k_volume = db.Column(db.Float)
    
    
if create_table:
    # with app.app_context():
    db.create_all()


class config_flask_dev(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://auto_trading_pro:tadatada!_-!#1@localhost/auto_trading_pro'
    SQLALCHEMY_POOL_SIZE = 70
    SQLALCHEMY_MAX_OVERFLOW = 70
    SQLALCHEMY_POOL_TIMEOUT = 300
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = ''
    CSRF_ENABLED = True


coin_list=[
'DOGEUSDT',
'XRPUSDT',
'BNBUSDT',
'LTCUSDT',
'SOLUSDT',
'MATICUSDT',
'APTUSDT',
'ADAUSDT',
'FILUSDT',
'DOTUSDT',
'AVAXUSDT',
'LINKUSDT',
'BCHUSDT',
'MASKUSDT',
'ATOMUSDT',
'SXPUSDT',
'1000SHIBUSDT',
'APEUSDT',
'ETCUSDT',
'EOSUSDT',
'CHZUSDT',
'FTMUSDT',
'LDOUSDT',
'SANDUSDT',
'CRVUSDT',
'TRXUSDT',
'NEARUSDT',
'AXSUSDT',
'GALAUSDT',
'ENJUSDT',
'MKRUSDT',
'LINAUSDT',
'GMTUSDT',
'UNIUSDT',
'FOOTBALLUSDT',
'MANAUSDT',
'ICXUSDT',
'SUSHIUSDT',
'ONTUSDT',
'PEOPLEUSDT',
'SNXUSDT',
'AAVEUSDT',
'OMGUSDT',
'XLMUSDT',
'WAVESUSDT',
'XMRUSDT',
'NEOUSDT',
'DOGEBUSD',
'GRTUSDT',
'ZECUSDT',
'EGLDUSDT',
'DASHUSDT',
'OCEANUSDT',
'C98USDT',
'ZRXUSDT',
'VETUSDT',
'ALGOUSDT',
'XTZUSDT',
'THETAUSDT',
'HBARUSDT',
'ADABUSD',
'IMXUSDT',
'YFIUSDT',
'COMPUSDT',
'RUNEUSDT',
'ANKRUSDT',
'STGUSDT',
'SOLBUSD',
'CELRUSDT',
'JASMYUSDT',
'LRCUSDT',
'1INCHUSDT',
'ROSEUSDT',
'LUNA2USDT',
'TOMOUSDT',
'KAVAUSDT',
'ZILUSDT',
'AUDIOUSDT',
'IOSTUSDT',
'STORJUSDT',
'RSRUSDT',
'KSMUSDT',
'SFPUSDT',
'XEMUSDT',
'RENUSDT',
'APTBUSD',
'BALUSDT',
'KNCUSDT',
'ATAUSDT',
'TRBUSDT',
'MATICBUSD',
'BANDUSDT',
'RVNUSDT',
'BATUSDT',
'IOTAUSDT',
'COTIUSDT',
'REEFUSDT',
'CHRUSDT',
'TRXBUSD',
'RLCUSDT',
'QTUMUSDT',
'GALUSDT',
'ONEUSDT',
'HOTUSDT',
'WOOUSDT',
'BAKEUSDT',
'NKNUSDT',
'OPUSDT',
'FTMBUSD',
'GALABUSD',
'BLZUSDT',
'ALPHAUSDT',
'OGNUSDT',
'FLMUSDT',
'IOTXUSDT',
'ARPAUSDT',
'SKLUSDT',
'DENTUSDT',
'BELUSDT',
'MTLUSDT',
'DUSKUSDT',
'CTKUSDT',
'STMXUSDT',
'CTSIUSDT',
'QNTUSDT',
'SPELLUSDT',
'DYDXUSDT',
'DGBUSDT',
'DODOBUSD',
'XRPBUSD',
'1000XECUSDT',
'CVXUSDT',
'INJUSDT',
'TLMUSDT',
'KLAYUSDT',
'BNXUSDT',
'PHBBUSD',
'ENSUSDT',
'ARUSDT',
'ANTUSDT',
'GTCUSDT',
'CELOUSDT',
'ALICEUSDT',
'FLOWUSDT',
'ZENUSDT',
'LITUSDT',
'UNFIUSDT',
'LPTUSDT',
'LINKBUSD',
'AVAXBUSD',
'LDOBUSD',
'APEBUSD',
'DARUSDT',
'NEARBUSD',
'API3USDT',
'ETCBUSD',
'BNBBUSD',
'DOTBUSD',
'FILBUSD',
'GMTBUSD',
'SANDBUSD',
'ICPUSDT',
'UNIBUSD',
'BLUEBIRDUSDT',
'LTCBUSD',
'CFXUSDT',
'ARBUSDT',
'ACHUSDT',
'STXUSDT',
'AGIXUSDT',
'LQTYUSDT',
'IDUSDT',
'MAGICUSDT',
'FETUSDT',
'SSVUSDT',
'COCOSUSDT',
'FXSUSDT',
'TRUUSDT',
'HOOKUSDT',
'CKBUSDT',
'MINAUSDT',
'RNDRUSDT',
'HIGHUSDT',
'GMXUSDT',
'ASTRUSDT',
'TUSDT',
'LEVERUSDT',
'AMBUSDT',
'AGIXBUSD',
'PHBUSDT',
'1000SHIBBUSD',
'PERPUSDT',
'USDCUSDT',
]
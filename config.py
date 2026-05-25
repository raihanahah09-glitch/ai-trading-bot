import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Config:
    """Base configuration"""
    
    # API Keys
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
    
    # Trading Parameters
    TRADING_PAIR = os.getenv('TRADING_PAIR', 'BTCUSDT')
    TRADING_AMOUNT = float(os.getenv('TRADING_AMOUNT', 100))
    RISK_PER_TRADE = float(os.getenv('RISK_PER_TRADE', 0.02))
    TAKE_PROFIT_RATIO = float(os.getenv('TAKE_PROFIT_RATIO', 2.0))
    STOP_LOSS_RATIO = float(os.getenv('STOP_LOSS_RATIO', 1.0))
    
    # Strategy Parameters
    RSI_PERIOD = int(os.getenv('RSI_PERIOD', 14))
    RSI_OVERBOUGHT = int(os.getenv('RSI_OVERBOUGHT', 70))
    RSI_OVERSOLD = int(os.getenv('RSI_OVERSOLD', 30))
    BB_PERIOD = int(os.getenv('BB_PERIOD', 20))
    BB_STD_DEV = float(os.getenv('BB_STD_DEV', 2))
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///trading_bot.db')
    
    # Server
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)
    PORT = int(os.getenv('PORT', 5000))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = f'logs/trading_bot_{datetime.now().strftime("%Y%m%d")}.log'
    
    # Model Parameters
    LSTM_LOOKBACK = 60
    LSTM_EPOCHS = 50
    LSTM_BATCH_SIZE = 32
    MODEL_PATH = 'models/lstm_model.h5'
    
    # Backtesting
    BACKTEST_START_DATE = '2023-01-01'
    BACKTEST_END_DATE = '2024-01-01'
    
    # Update intervals (seconds)
    MARKET_UPDATE_INTERVAL = 60
    MODEL_RETRAIN_INTERVAL = 86400  # 24 hours
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()

config = get_config()

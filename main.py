#!/usr/bin/env python
"""
AI Trading Bot - Main Entry Point
Strategies: RSI + Bollinger Bands + LSTM Neural Network
"""

import os
import sys
import logging
from datetime import datetime
from config import config
from src.bot.trader import AITradingBot
from src.api.app import create_app

# Setup Logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def initialize_bot():
    """
    Initialize and start the trading bot
    """
    try:
        logger.info("="*60)
        logger.info(f"AI Trading Bot Starting - {datetime.now()}")
        logger.info(f"Trading Pair: {config.TRADING_PAIR}")
        logger.info(f"Risk Per Trade: {config.RISK_PER_TRADE*100}%")
        logger.info("="*60)
        
        # Initialize bot
        bot = AITradingBot(config)
        
        # Start trading
        bot.start()
        
    except Exception as e:
        logger.error(f"Fatal error in bot initialization: {str(e)}", exc_info=True)
        sys.exit(1)

def run_api_server():
    """
    Run Flask API server for monitoring and control
    """
    try:
        logger.info(f"Starting API Server on port {config.PORT}")
        app = create_app(config)
        app.run(
            host='0.0.0.0',
            port=config.PORT,
            debug=config.FLASK_DEBUG
        )
    except Exception as e:
        logger.error(f"API Server error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Trading Bot')
    parser.add_argument(
        '--mode',
        choices=['bot', 'api', 'both'],
        default='both',
        help='Run mode: bot (trading), api (monitoring), or both'
    )
    parser.add_argument(
        '--backtest',
        action='store_true',
        help='Run backtest instead of live trading'
    )
    
    args = parser.parse_args()
    
    if args.backtest:
        logger.info("Running in BACKTEST mode")
        from src.backtester import Backtester
        backtester = Backtester(config)
        backtester.run()
    else:
        if args.mode in ['bot', 'both']:
            initialize_bot()
        elif args.mode in ['api', 'both']:
            run_api_server()

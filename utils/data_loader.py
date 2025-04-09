import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

class DataLoader:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('ALPHA_VANTAGE_KEY')  # Optional for premium data

    def fetch_ohlc(self, symbol, start_date, end_date, source='yahoo'):
        """Fetch OHLC data from specified source"""
        if source.lower() == 'yahoo':
            data = yf.download(
                symbol,
                start=start_date,
                end=end_date,
                progress=False
            )
            data.columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
            return data[['open', 'high', 'low', 'close', 'volume']]
        
        elif source.lower() == 'alpha_vantage':
            # Implement Alpha Vantage API fallback
            pass

    def preprocess_data(self, df):
        """Clean and format data for backtesting"""
        df = df.dropna()
        df['returns'] = df['close'].pct_change()
        df['volatility'] = df['returns'].rolling(20).std()
        return df

if __name__ == "__main__":
    loader = DataLoader()
    eurusd_data = loader.fetch_ohlc('EURUSD=X', '2020-01-01', '2023-12-31')
    processed_data = loader.preprocess_data(eurusd_data)
    print(processed_data.tail())
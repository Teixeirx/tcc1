import os
import ccxt
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_binance_client():
    api_key = os.getenv('BINANCE_API_KEY')
    secret_key = os.getenv('BINANCE_SECRET_KEY')
    
    # Se as chaves forem placeholder, instanciamos sem elas (permite ler dados públicos)
    if api_key == "sua_chave_binance_aqui":
        api_key = None
        secret_key = None
        
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': secret_key,
        'enableRateLimit': True,
    })
    return exchange

def fetch_historical_data(symbol='BTC/USDT', timeframe='1d', limit=100):
    """
    Busca dados históricos da Binance e retorna um DataFrame do Pandas.
    """
    exchange = get_binance_client()
    print(f"Buscando dados para {symbol} ({timeframe}) - {limit} candles...")
    
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    return df

if __name__ == "__main__":
    df = fetch_historical_data()
    print(df.tail())

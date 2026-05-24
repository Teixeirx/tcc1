import os
import mplfinance as mpf
import pandas as pd

def generate_candlestick_chart(df: pd.DataFrame, output_filename="chart.png"):
    """
    Gera um gráfico de candlestick a partir de um DataFrame (OHLCV)
    e salva em um arquivo de imagem.
    """
    print(f"Gerando gráfico: {output_filename}...")
    
    mc = mpf.make_marketcolors(up='g', down='r', edge='inherit', wick='inherit', volume='in')
    s  = mpf.make_mpf_style(marketcolors=mc, gridstyle='--', y_on_right=False)
    
    mpf.plot(
        df, 
        type='candle', 
        style=s, 
        volume=True, 
        title='Histórico de Preço',
        savefig=output_filename,
        figratio=(10, 6),
        figscale=1.2
    )
    return output_filename

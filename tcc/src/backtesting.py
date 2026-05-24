import os
import pandas as pd
from typing import List
from data_collection import fetch_historical_data
from charting import generate_candlestick_chart
from lmm_analyzer import analyze_chart_with_gemini

def run_backtest(symbol='BTC/USDT', timeframe='1d', total_days=40, window_size=30):
    """
    Executa um backtest simples usando o LMM.
    Pega os últimos 'total_days' dias. Para cada dia a partir do 'window_size',
    gera um gráfico com os dados anteriores, envia para o LMM e simula a operação.
    ATENÇÃO: Consome chamadas da API do Gemini.
    """
    print(f"Iniciando Backtest para {symbol}...")
    df = fetch_historical_data(symbol, timeframe, limit=total_days)
    
    if len(df) < window_size:
        print("Dados insuficientes para a janela solicitada.")
        return
    
    saldo_inicial = 1000.0 # USD
    saldo_usd = saldo_inicial
    saldo_cripto = 0.0
    
    # Iterar sobre os dias
    for i in range(window_size, len(df)):
        current_date = df.index[i]
        df_window = df.iloc[i-window_size:i]
        current_price = df['Close'].iloc[i] 
        
        chart_filename = f"temp_chart.png"
        generate_candlestick_chart(df_window, chart_filename)
        
        ia_response = analyze_chart_with_gemini(chart_filename)
        
        sinal = "MANTER"
        if "COMPRAR" in ia_response.upper():
            sinal = "COMPRAR"
        elif "VENDER" in ia_response.upper():
            sinal = "VENDER"
            
        print(f"[{current_date.date()}] Preço: {current_price:.2f} | IA sugeriu: {sinal}")
        
        if sinal == "COMPRAR" and saldo_usd > 0:
            comprado = saldo_usd / current_price
            saldo_cripto += comprado
            print(f"  => Comprou {comprado:.4f} crypto por {saldo_usd:.2f} USD")
            saldo_usd = 0.0
            
        elif sinal == "VENDER" and saldo_cripto > 0:
            vendido = saldo_cripto * current_price
            saldo_usd += vendido
            print(f"  => Vendeu {saldo_cripto:.4f} crypto por {vendido:.2f} USD")
            saldo_cripto = 0.0
            
        if os.path.exists(chart_filename):
            os.remove(chart_filename)
            
    # Saldo final
    valor_final = saldo_usd + (saldo_cripto * df['Close'].iloc[-1])
    roi = ((valor_final - saldo_inicial) / saldo_inicial) * 100
    
    print("\n" + "="*30)
    print("RESULTADO DO BACKTEST")
    print(f"Saldo Inicial: {saldo_inicial:.2f} USD")
    print(f"Valor Final:   {valor_final:.2f} USD")
    print(f"ROI:           {roi:.2f}%")
    print("="*30)

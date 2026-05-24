import argparse
from backtesting import run_backtest
from data_collection import fetch_historical_data
from charting import generate_candlestick_chart
from lmm_analyzer import analyze_chart_with_gemini
from web_generator import generate_html_report
from data_collection import get_binance_client
import os
from datetime import datetime

def run_live(symbol='BTC/USDT', timeframe='1d', limit=30):
    """
    Roda a análise para o momento atual.
    """
    print(f"Executando análise AO VIVO para {symbol}...")
    df = fetch_historical_data(symbol, timeframe, limit=limit)
    
    chart_file = "live_chart.png"
    generate_candlestick_chart(df, chart_file)
    
    print("Buscando preço exato do momento (via ticker)...")
    exchange = get_binance_client()
    ticker = exchange.fetch_ticker(symbol)
    exact_price = ticker['last']
    exact_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    print("Enviando para o modelo Gemini analisar...")
    resultado = analyze_chart_with_gemini(chart_file)
    
    print("\n" + "="*40)
    print("RESULTADO DA ANÁLISE (IA):")
    print("="*40)
    print(f"Ação: {resultado.get('acao')}")
    print(f"Justificativa: {resultado.get('justificativa')}")
    if resultado.get('previsao_venda'):
        print(f"Previsão de Venda: {resultado.get('previsao_venda')}")
    print("="*40)
    
    html_file = generate_html_report(
        symbol=symbol,
        current_price=exact_price,
        current_time=exact_time,
        action=resultado.get('acao', 'ERRO'),
        justification=resultado.get('justificativa', 'Sem dados'),
        previsao_venda=resultado.get('previsao_venda')
    )
    
    full_path = os.path.abspath(html_file).replace(os.sep, '/')
    print(f"\nDashboard gerado com sucesso! Abrindo automaticamente no seu navegador...")
    import webbrowser
    webbrowser.open(f"file:///{full_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crypto Bot com LMM")
    parser.add_argument('--mode', type=str, choices=['live', 'backtest'], default='live', help='Modo de execução')
    parser.add_argument('--symbol', type=str, default='BTC/USDT', help='Par de moedas')
    
    args = parser.parse_args()
    
    if args.mode == 'live':
        run_live(symbol=args.symbol)
    elif args.mode == 'backtest':
        run_backtest(symbol=args.symbol, total_days=40, window_size=30)

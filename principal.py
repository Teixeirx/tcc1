"""
principal.py -- Ponto de entrada do sistema CriptoIA.

Orquestra o fluxo completo de análise:
  1. Coleta dados históricos da Binance (OHLCV via API pública)
  2. Calcula indicadores técnicos (RSI, MACD, Médias Móveis, Bollinger)
  3. Gera gráfico de candlestick (PNG para o Gemini)
  4. Envia imagem + indicadores ao Google Gemini para análise
  5. Gera e abre o dashboard web interativo no navegador

Uso:
    python principal.py
    python principal.py --par ETH/USDT --intervalo 4h --quantidade 60
"""

import os
import sys
import argparse
import webbrowser
from datetime import datetime

# Garante saida UTF-8 no terminal do Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Adiciona a pasta raiz ao path para importar backend/ e frontend/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.coleta_dados import buscar_dados_historicos, buscar_preco_atual
from backend.analise_tecnica import enriquecer_dataframe, resumir_indicadores
from backend.gerador_grafico import gerar_grafico_candlestick
from backend.analisador_ia import analisar_mercado_com_gemini
from frontend.gerador_dashboard import gerar_dashboard


def executar_analise(par: str = "BTC/USDT", intervalo: str = "1d", quantidade: int = 90):
    """
    Executa o fluxo completo de análise de criptomoedas.

    Parâmetros:
        par        : Par de negociação (ex: 'BTC/USDT', 'ETH/USDT')
        intervalo  : Timeframe dos candles (ex: '1d', '4h', '1h')
        quantidade : Número de candles a buscar (padrão: 90 dias)
    """
    print("\n" + "=" * 55)
    print("  CriptoIA -- Sistema de Analise com Gemini")
    print("=" * 55)
    print(f"  Par:       {par}")
    print(f"  Intervalo: {intervalo}")
    print(f"  Candles:   {quantidade}")
    print("=" * 55 + "\n")

    horario_analise = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    # ── ETAPA 1: Coleta de Dados ─────────────────────────────────────────
    print("[1/5] Coletando dados históricos da Binance...")
    df_historico = buscar_dados_historicos(par, intervalo, quantidade)

    print("[1/5] Buscando preço em tempo real...")
    dados_ticker = buscar_preco_atual(par)

    # ── ETAPA 2: Análise Técnica ─────────────────────────────────────────
    print("\n[2/5] Calculando indicadores técnicos...")
    df_enriquecido = enriquecer_dataframe(df_historico)
    indicadores = resumir_indicadores(df_enriquecido)

    print(f"       RSI(14):  {indicadores.get('rsi14', 'N/A'):.2f}")
    print(f"       MACD:     {indicadores.get('macd', 'N/A'):.4f}")
    print(f"       MM20:     ${indicadores.get('mm20', 0):,.2f}")
    print(f"       MM50:     ${indicadores.get('mm50', 0):,.2f}")

    # ── ETAPA 3: Geração do Gráfico ──────────────────────────────────────
    print("\n[3/5] Gerando gráfico técnico para análise...")
    caminho_grafico = gerar_grafico_candlestick(
        df_enriquecido,
        nome_arquivo="grafico_bitcoin.png",
        titulo=f"{par} — Análise Técnica ({intervalo})"
    )

    # ── ETAPA 4: Análise com IA ──────────────────────────────────────────
    print("\n[4/5] Enviando para análise com Google Gemini...")
    analise_ia = analisar_mercado_com_gemini(caminho_grafico, indicadores)

    print("\n" + "-" * 55)
    print("  RESULTADO DA ANALISE (Gemini):")
    print("-" * 55)
    print(f"  Acao:            {analise_ia.get('acao', 'N/A')}")
    print(f"  Preco Alvo:      {analise_ia.get('preco_alvo', 'N/A')}")
    print(f"  Tempo p/ Lucro:  {analise_ia.get('tempo_estimado', 'N/A')}")
    justif = str(analise_ia.get('justificativa', '')).encode('ascii', 'replace').decode('ascii')
    print(f"  Justificativa:   {justif[:120]}...")
    print("-" * 55)

    # ── ETAPA 5: Geração do Dashboard ────────────────────────────────────
    print("\n[5/5] Gerando dashboard web interativo...")
    caminho_dashboard = gerar_dashboard(
        df=df_enriquecido,
        dados_ticker=dados_ticker,
        analise_ia=analise_ia,
        indicadores=indicadores,
        par=par,
        horario_analise=horario_analise,
    )

    caminho_absoluto = os.path.abspath(caminho_dashboard).replace(os.sep, "/")
    url_dashboard = f"file:///{caminho_absoluto}"

    print(f"\nDashboard gerado: {caminho_absoluto}")
    print("Abrindo no navegador...")
    webbrowser.open(url_dashboard)

    print("\n" + "=" * 55)
    print("  Analise concluida com sucesso!")
    print("=" * 55 + "\n")


def configurar_argumentos() -> argparse.Namespace:
    """Configura e retorna os argumentos da linha de comando."""
    analisador = argparse.ArgumentParser(
        description="CriptoIA — Análise de criptomoedas com Google Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python principal.py
  python principal.py --par BTC/USDT --intervalo 1d --quantidade 90
  python principal.py --par ETH/USDT --intervalo 4h --quantidade 60
        """
    )
    analisador.add_argument(
        "--par",
        type=str,
        default="BTC/USDT",
        help="Par de negociação (padrão: BTC/USDT)"
    )
    analisador.add_argument(
        "--intervalo",
        type=str,
        default="1d",
        choices=["1h", "4h", "1d", "1w"],
        help="Timeframe dos candles (padrão: 1d)"
    )
    analisador.add_argument(
        "--quantidade",
        type=int,
        default=90,
        help="Número de candles a buscar (padrão: 90)"
    )
    return analisador.parse_args()


if __name__ == "__main__":
    args = configurar_argumentos()
    executar_analise(
        par=args.par,
        intervalo=args.intervalo,
        quantidade=args.quantidade
    )

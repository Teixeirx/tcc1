"""
analisador_ia.py — Módulo de análise de mercado com Google Gemini.

Envia o gráfico de candlestick + indicadores técnicos numéricos ao modelo
Gemini e recebe uma recomendação estruturada em JSON:
  - acao           : 'COMPRAR', 'VENDER' ou 'MANTER'
  - justificativa  : Explicação detalhada da recomendação
  - preco_alvo     : Estimativa de preço-alvo da operação
  - tempo_estimado : Estimativa de tempo para geração de lucro
"""

import os
import json
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Modelo Gemini a ser utilizado
MODELO_GEMINI = "gemini-2.5-flash"


def _construir_prompt(indicadores: dict) -> str:
    """
    Constrói o prompt textual enviado ao Gemini com os dados numéricos
    dos indicadores técnicos.

    Parâmetros:
        indicadores : Dicionário retornado por analise_tecnica.resumir_indicadores()

    Retorna:
        String com o prompt completo
    """
    rsi = indicadores.get("rsi14")
    mm20 = indicadores.get("mm20")
    mm50 = indicadores.get("mm50")
    macd = indicadores.get("macd")
    sinal = indicadores.get("sinal_macd")
    boll_sup = indicadores.get("bollinger_superior")
    boll_inf = indicadores.get("bollinger_inferior")
    fechamento = indicadores.get("preco_fechamento")

    # Avaliações qualitativas dos indicadores
    situacao_rsi = (
        "sobrecomprado (possível reversão de baixa)" if rsi and rsi > 70
        else "sobrevendido (possível reversão de alta)" if rsi and rsi < 30
        else "neutro"
    )

    tendencia_macd = (
        "sinal de compra (MACD acima da linha de sinal)" if macd and sinal and macd > sinal
        else "sinal de venda (MACD abaixo da linha de sinal)" if macd and sinal and macd < sinal
        else "indefinida"
    )

    posicao_medias = (
        "tendência de alta (MM20 acima da MM50)" if mm20 and mm50 and mm20 > mm50
        else "tendência de baixa (MM20 abaixo da MM50)" if mm20 and mm50 and mm20 < mm50
        else "indefinida"
    )

    prompt = f"""Você é um trader especialista em análise técnica de criptomoedas.
Analise o gráfico de candlestick do Bitcoin (BTC/USDT) anexo junto com os dados numéricos abaixo:

=== INDICADORES TÉCNICOS (último candle) ===
- Preço de Fechamento: ${fechamento:,.2f} USDT
- RSI (14): {rsi:.2f} → {situacao_rsi}
- MACD: {macd:.4f} | Linha de Sinal: {sinal:.4f} → {tendencia_macd}
- Média Móvel 20: ${mm20:,.2f} | Média Móvel 50: ${mm50:,.2f} → {posicao_medias}
- Banda de Bollinger Superior: ${boll_sup:,.2f}
- Banda de Bollinger Inferior: ${boll_inf:,.2f}
============================================

Com base na imagem do gráfico E nos indicadores acima, determine:

1. A ação recomendada: COMPRAR, VENDER ou MANTER
2. Uma justificativa técnica clara e detalhada (mínimo 2 parágrafos)
3. Se a ação for COMPRAR ou VENDER: um preço-alvo estimado para encerrar a operação com lucro
4. Uma estimativa de tempo para que a operação gere lucro (ex: "3 a 7 dias", "2 a 4 semanas")

IMPORTANTE: Responda EXCLUSIVAMENTE em formato JSON válido, sem texto adicional antes ou depois.
Use exatamente este formato:

{{
  "acao": "COMPRAR",
  "justificativa": "Justificativa técnica detalhada aqui.",
  "preco_alvo": "$98.500,00",
  "tempo_estimado": "7 a 14 dias"
}}

Se a ação for MANTER, use null para preco_alvo e tempo_estimado.
A chave 'acao' deve conter APENAS uma das palavras: COMPRAR, VENDER ou MANTER.
"""
    return prompt


def _extrair_json_da_resposta(texto: str) -> dict:
    """
    Extrai e valida o JSON da resposta do Gemini.
    Lida com casos onde o modelo envolve o JSON em blocos de código Markdown.

    Parâmetros:
        texto : Texto bruto retornado pelo Gemini

    Retorna:
        Dicionário com os campos da análise
    """
    texto = texto.strip()

    # Remove marcações Markdown de código (```json ... ``` ou ``` ... ```)
    texto = re.sub(r"^```(?:json)?\s*", "", texto)
    texto = re.sub(r"\s*```$", "", texto)
    texto = texto.strip()

    dados = json.loads(texto)

    # Normaliza a ação para maiúsculas
    acao = dados.get("acao", "MANTER").upper().strip()
    if acao not in {"COMPRAR", "VENDER", "MANTER"}:
        acao = "MANTER"

    return {
        "acao": acao,
        "justificativa": dados.get("justificativa", "Sem justificativa disponível."),
        "preco_alvo": dados.get("preco_alvo"),
        "tempo_estimado": dados.get("tempo_estimado"),
    }


def analisar_mercado_com_gemini(
    caminho_grafico: str,
    indicadores: dict
) -> dict:
    """
    Envia o gráfico + indicadores ao Google Gemini e retorna a análise.

    Parâmetros:
        caminho_grafico : Caminho para o arquivo PNG do gráfico
        indicadores     : Dicionário de indicadores de analise_tecnica.resumir_indicadores()

    Retorna:
        Dicionário com: acao, justificativa, preco_alvo, tempo_estimado
    """
    chave_api = os.getenv("GEMINI_API_KEY", "")

    if not chave_api or chave_api == "sua_chave_gemini_aqui":
        return {
            "acao": "ERRO",
            "justificativa": "A variável GEMINI_API_KEY não está configurada no arquivo .env.",
            "preco_alvo": None,
            "tempo_estimado": None,
        }

    try:
        import PIL.Image
        cliente = genai.Client(api_key=chave_api)

        imagem = PIL.Image.open(caminho_grafico)
        prompt = _construir_prompt(indicadores)

        print(f"[Gemini] Enviando gráfico e indicadores para análise ({MODELO_GEMINI})...")

        resposta = cliente.models.generate_content(
            model=MODELO_GEMINI,
            contents=[prompt, imagem]
        )

        print("[Gemini] Análise recebida. Processando resultado...")
        resultado = _extrair_json_da_resposta(resposta.text)
        return resultado

    except json.JSONDecodeError as erro:
        print(f"[Gemini] Erro ao interpretar JSON: {erro}")
        print(f"[Gemini] Resposta bruta: {resposta.text[:500]}")
        return {
            "acao": "MANTER",
            "justificativa": f"Não foi possível interpretar a resposta da IA. Resposta: {resposta.text[:300]}",
            "preco_alvo": None,
            "tempo_estimado": None,
        }

    except Exception as erro:
        print(f"[Gemini] Erro na chamada à API: {erro}")
        return {
            "acao": "ERRO",
            "justificativa": f"Falha ao conectar com o Google Gemini: {str(erro)}",
            "preco_alvo": None,
            "tempo_estimado": None,
        }

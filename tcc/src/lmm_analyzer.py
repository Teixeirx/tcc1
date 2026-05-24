import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def analyze_chart_with_gemini(image_path: str) -> str:
    """
    Envia a imagem do gráfico para o Google Gemini e retorna a sugestão (COMPRAR, VENDER, MANTER).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "sua_chave_gemini_aqui":
        return {"acao": "ERRO", "justificativa": "GEMINI_API_KEY não configurada no arquivo .env."}
    
    try:
        client = genai.Client(api_key=api_key)
        
        import PIL.Image
        import json
        img = PIL.Image.open(image_path)
        
        prompt = (
            "Você é um trader especialista em análise técnica de criptomoedas. "
            "Analise este gráfico de candlestick. "
            "Com base apenas nos padrões gráficos visíveis (tendência, suportes, resistências, volume), "
            "qual seria a sua sugestão de operação para o momento atual (último candle)? "
            "Se a sua sugestão for COMPRAR, forneça obrigatoriamente uma estimativa aproximada (de preço ou tempo) de quando vender na chave 'previsao_venda'. Caso contrário, retorne null. "
            "Responda OBRIGATORIAMENTE em formato JSON válido contendo exatamente as seguintes chaves:\n"
            '{"acao": "COMPRAR", "justificativa": "Sua justificativa aqui.", "previsao_venda": "..."}\n'
            "A chave 'acao' deve conter apenas uma das palavras: COMPRAR, VENDER ou MANTER."
        )
        
        print(f"Enviando {image_path} para o modelo Gemini analisar...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img]
        )
        
        # Limpar o texto para garantir que seja apenas JSON, removendo marcações Markdown (```json ... ```) se existirem
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        try:
            result = json.loads(text.strip())
            return {
                "acao": result.get("acao", "MANTER").upper(), 
                "justificativa": result.get("justificativa", "Sem justificativa."),
                "previsao_venda": result.get("previsao_venda")
            }
        except json.JSONDecodeError:
            print("Erro ao parsear o JSON do Gemini. Resposta crua:", response.text)
            return {"acao": "MANTER", "justificativa": response.text, "previsao_venda": None}
            
    except Exception as e:
        return {"acao": "ERRO", "justificativa": f"Erro ao acessar Gemini: {e}", "previsao_venda": None}

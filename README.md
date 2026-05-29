# 🤖 CriptoIA — Análise de Criptomoedas com Google Gemini

> Trabalho de Conclusão de Curso 1 (TCC1) — Sistema de análise técnica de criptomoedas com suporte de Inteligência Artificial via Google Gemini.

---

## 📋 Sobre o Projeto

O **CriptoIA** é um sistema de análise de mercado de criptomoedas que combina **análise técnica tradicional** com **Inteligência Artificial generativa**. A aplicação coleta dados históricos diretamente da Binance, calcula indicadores técnicos clássicos, gera um gráfico de candlestick e o envia ao modelo **Google Gemini**, que retorna uma recomendação estruturada de compra, venda ou manutenção do ativo.

O resultado final é exibido em um **dashboard web interativo**, gerado e aberto automaticamente no navegador.

---

## ✨ Funcionalidades

- 📡 **Coleta de dados em tempo real e históricos** via API pública da Binance (ccxt)
- 📊 **Cálculo de indicadores técnicos**:
  - RSI (Relative Strength Index) — 14 períodos
  - MACD (Moving Average Convergence Divergence)
  - Médias Móveis Simples (MM20 e MM50)
  - Bandas de Bollinger (20 períodos, 2 desvios)
- 🖼️ **Geração de gráfico de candlestick** com todos os indicadores sobrepostos (PNG)
- 🤖 **Análise com Google Gemini** — recebe imagem + indicadores e retorna JSON estruturado:
  - Ação recomendada: `COMPRAR`, `VENDER` ou `MANTER`
  - Justificativa técnica detalhada
  - Preço-alvo estimado
  - Tempo estimado para lucro
- 🌐 **Dashboard web interativo** gerado automaticamente (HTML + Plotly.js) e aberto no navegador

---

## 🏗️ Arquitetura

```
CriptoIa/
├── principal.py              # Ponto de entrada — orquestra o fluxo completo
├── requisitos.txt            # Dependências Python
├── .env                      # Variáveis de ambiente (chaves de API)
├── backend/
│   ├── coleta_dados.py       # Coleta OHLCV + ticker em tempo real (Binance/ccxt)
│   ├── analise_tecnica.py    # Cálculo de RSI, MACD, MM, Bollinger
│   ├── gerador_grafico.py    # Geração do gráfico de candlestick (mplfinance)
│   └── analisador_ia.py      # Integração com Google Gemini (análise multimodal)
└── frontend/
    └── gerador_dashboard.py  # Geração do dashboard web interativo (Plotly.js)
```

### Fluxo de Execução

```
Binance API → coleta_dados → analise_tecnica → gerador_grafico
                                                      ↓
                                              analisador_ia (Gemini)
                                                      ↓
                                           gerador_dashboard → Navegador
```

---

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.10 ou superior
- Conta na [Binance](https://www.binance.com) (opcional — dados públicos funcionam sem autenticação)
- Chave de API do [Google Gemini](https://aistudio.google.com/api-keys) (obrigatória para análise com IA)

### 1. Clone o repositório

```bash
git clone https://github.com/Teixeirx/tcc1.git
cd tcc1/CriptoIa
```

### 2. Instale as dependências

```bash
pip install -r requisitos.txt
```

### 3. Configure as variáveis de ambiente

Edite o arquivo `.env` na pasta `CriptoIa/`:

```env
BINANCE_API_KEY=Adicione aqui a api da binance adquirida através do link: https://www.binance.com/en/my/settings/api-management
BINANCE_SECRET_KEY=Adicione aqui a api da binance adquirida através do link: https://www.binance.com/en/my/settings/api-management
GEMINI_API_KEY=Adicione aqui a api da gemini adquirida através do link: https://aistudio.google.com/api-keys
```


### 4. Execute o sistema

```bash
# Análise padrão (BTC/USDT, diário, 90 candles)
python principal.py

# Análise personalizada
python principal.py --par ETH/USDT --intervalo 4h --quantidade 60
```

### Parâmetros disponíveis

| Parâmetro      | Padrão    | Opções disponíveis          | Descrição                        |
|----------------|-----------|-----------------------------|----------------------------------|
| `--par`        | `BTC/USDT`| Qualquer par da Binance     | Par de negociação                |
| `--intervalo`  | `1d`      | `1h`, `4h`, `1d`, `1w`      | Timeframe dos candles            |
| `--quantidade` | `90`      | Qualquer inteiro positivo   | Número de candles históricos     |

---

## 📦 Dependências

| Biblioteca       | Uso                                              |
|------------------|--------------------------------------------------|
| `ccxt`           | Conexão com a API da Binance                     |
| `pandas`         | Manipulação de dados e séries temporais          |
| `matplotlib`     | Geração de gráficos base                         |
| `mplfinance`     | Gráfico de candlestick com indicadores           |
| `plotly`         | Dashboard web interativo                         |
| `python-dotenv`  | Carregamento de variáveis de ambiente            |
| `google-genai`   | Integração com a API do Google Gemini            |
| `Pillow`         | Leitura da imagem do gráfico para envio ao Gemini|
| `ta`             | Biblioteca auxiliar de análise técnica           |

---

## 📄 Artigo

Este projeto é acompanhado de um artigo científico (`Artigo Tcc1.pdf`) que documenta a metodologia, fundamentação teórica e resultados experimentais do sistema.

---

## 🎓 Contexto Acadêmico

Desenvolvido como Trabalho de Conclusão de Curso 1 (TCC1), este projeto investiga a aplicação de modelos de linguagem de grande escala (LLMs) com capacidade multimodal — especificamente o Google Gemini — como ferramenta de suporte à decisão em mercados financeiros de criptomoedas.

---

## 📜 Licença

Este projeto é de caráter acadêmico. Todos os direitos reservados ao autor.

---

> ⚠️ **Aviso:** Este sistema tem fins exclusivamente educacionais e acadêmicos. Não constitui recomendação financeira. Invista com responsabilidade.

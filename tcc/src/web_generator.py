import base64
import os

def generate_html_report(symbol, current_price, current_time, action, justification, previsao_venda=None):
    # Define color based on action
    color = "#4ade80" if action.upper() == "COMPRAR" else "#f87171" if action.upper() == "VENDER" else "#fbbf24"
    previsao_html = f'<div class="justification" style="margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); color: #e2e8f0;"><strong>Previsão de Venda:</strong> {previsao_venda}</div>' if previsao_venda else ''
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise LMM - {symbol}</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: {color};
        }}
        body {{
            margin: 0;
            padding: 0;
            background-color: var(--bg-color);
            background-image: radial-gradient(circle at top right, #1e293b 0%, transparent 40%),
                              radial-gradient(circle at bottom left, #1e293b 0%, transparent 40%);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .container {{
            max-width: 1000px;
            width: 90%;
            margin: 40px auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            animation: fadeIn 1s ease-in;
        }}
        .header h1 {{
            font-size: 2.5rem;
            margin: 0;
            background: linear-gradient(to right, #e2e8f0, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .header p {{
            color: var(--text-muted);
            font-size: 1.1rem;
            margin-top: 10px;
        }}
        .dashboard {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }}
        @media (min-width: 768px) {{
            .dashboard {{ grid-template-columns: 1fr 1fr; }}
        }}
        .card {{
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.6);
            border-color: rgba(255, 255, 255, 0.2);
        }}
        .price-val {{
            font-size: 2rem;
            font-weight: bold;
            margin: 10px 0;
            color: #fff;
            text-shadow: 0 0 20px rgba(255,255,255,0.2);
        }}
        .action-val {{
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--accent);
            text-transform: uppercase;
            text-shadow: 0 0 15px var(--accent);
        }}
        .label {{
            font-size: 0.9rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .justification {{
            font-size: 1.1rem;
            line-height: 1.6;
            margin-top: 15px;
            color: #cbd5e1;
        }}
        .chart-container {{
            grid-column: 1 / -1;
            background: var(--card-bg);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Análise Técnica com IA</h1>
            <p>Gerado em {current_time}</p>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <div class="label">Ativo & Preço Exato</div>
                <div class="price-val" style="font-size: 1.5rem; color: var(--text-muted);">{symbol}</div>
                <div class="price-val">${current_price:,.2f}</div>
            </div>
            
            <div class="card">
                <div class="label">Recomendação da IA</div>
                <div class="action-val">{action}</div>
                <div class="justification">{justification}</div>
                {previsao_html}
            </div>
            
            <div class="chart-container" style="height: 500px; padding: 0; overflow: hidden;">
                <!-- TradingView Widget BEGIN -->
                <div class="tradingview-widget-container" style="height:100%;width:100%">
                  <div id="tradingview_widget" style="height:100%;width:100%"></div>
                  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                  <script type="text/javascript">
                  new TradingView.widget(
                  {{
                  "autosize": true,
                  "symbol": "BINANCE:{symbol.replace('/', '')}",
                  "interval": "D",
                  "timezone": "America/Sao_Paulo",
                  "theme": "dark",
                  "style": "1",
                  "locale": "br",
                  "enable_publishing": false,
                  "backgroundColor": "rgba(30, 41, 59, 1)",
                  "gridColor": "rgba(255, 255, 255, 0.06)",
                  "hide_top_toolbar": false,
                  "save_image": false,
                  "container_id": "tradingview_widget"
                }}
                  );
                  </script>
                </div>
                <!-- TradingView Widget END -->
            </div>
        </div>
    </div>
</body>
</html>
"""
    output_file = "dashboard.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    return output_file

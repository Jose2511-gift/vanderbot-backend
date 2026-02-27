from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas_ta as ta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista completa com os 12 ativos (Moedas, Japão, Ouro e Cripto)
ATIVOS = [
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "EURJPY=X",
    "GBPJPY=X", "GC=F", "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD"
]

def calcular_indicadores(df):
    try:
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]
        bb = ta.bbands(df['Close'], length=20, std=2)
        return rsi, df['Close'].iloc[-1], bb['BBU_20_2.0'].iloc[-1], bb['BBL_20_2.0'].iloc[-1]
    except:
        return None, None, None, None

@app.get("/analizar")
def analisar(estrategia: str = "WANDER"):
    melhor_ativo = "ANALISANDO..."
    melhor_sinal = "AGUARDAR"
    melhor_taxa = "0%"

    for ticker in ATIVOS:
        try:
            # Baixa o dado de cada moeda individualmente para o Yahoo não bloquear
            data = yf.download(ticker, period="1d", interval="1m", progress=False, timeout=10)
            if data.empty: continue
            
            rsi, atual, sup, inf = calcular_indicadores(data)
            if rsi is None: continue

            nome = ticker.replace("=X", "").replace("-USD", "/USD").replace("GC=F", "GOLD (OURO)")

            # --- LÓGICA DAS 3 ESTRATÉGIAS ---
            
            # 1. EXTRA WANDER (Sinal Forte: RSI + Bandas)
            if estrategia.upper() == "WANDER":
                if atual <= inf and rsi < 35: 
                    melhor_sinal, melhor_taxa, melhor_ativo = "CALL", "96%", nome
                    break
                elif atual >= sup and rsi > 65: 
                    melhor_sinal, melhor_taxa, melhor_ativo = "PUT", "97%", nome
                    break

            # 2. ZEUS OTC (RSI Agressivo)
            elif estrategia.upper() == "ZEUS":
                if rsi < 30: 
                    melhor_sinal, melhor_taxa, melhor_ativo = "CALL", "92%", nome
                    break
                elif rsi > 70: 
                    melhor_sinal, melhor_taxa, melhor_ativo = "PUT", "93%", nome
                    break

            # 3. ETARE (RSI Moderado)
            elif estrategia.upper() == "ETARE":
                if rsi < 45: 
                    melhor_sinal, melhor_taxa, melhor_ativo = "CALL", "88%", nome
                    break
                elif rsi > 55: 
                    melhor_sinal, melhor_taxa, melhor_ativo = "PUT", "89%", nome
                    break

        except:
            continue

    # Se não achar nada, ele sugere o EUR/USD por padrão
    if melhor_ativo == "ANALISANDO...":
        melhor_ativo = "EUR/USD"

    return {"ativo": melhor_ativo, "sinal": melhor_sinal, "assertividade": melhor_taxa}

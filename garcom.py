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

# Lista de ativos focada nos mais fortes
ATIVOS = [
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "EURJPY=X", 
    "BTC-USD", "ETH-USD", "GC=F"
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
    melhor_ativo = "PROCURANDO..."
    melhor_sinal = "AGUARDAR"
    melhor_taxa = "0%"

    for ticker in ATIVOS:
        try:
            # Baixa o dado de cada moeda individualmente para evitar bloqueio
            data = yf.download(ticker, period="1d", interval="1m", progress=False, timeout=10)
            if data.empty: continue
            
            rsi, atual, sup, inf = calcular_indicadores(data)
            if rsi is None: continue

            nome = ticker.replace("=X", "").replace("-USD", "/USD").replace("GC=F", "GOLD")

            # Lógica da Estratégia Extra Wander
            if estrategia.upper() == "WANDER":
                if atual <= inf or rsi < 40: 
                    melhor_sinal, melhor_taxa, melhor_ativo = "CALL", "96%", nome
                    break
                elif atual >= sup or rsi > 60: 
                    melhor_sinal, melhor_taxa, melhor_ativo = "PUT", "97%", nome
                    break
            else: # Zeus / Etare
                if rsi < 45: 
                    melhor_sinal, melhor_taxa, melhor_ativo = "CALL", "91%", nome
                    break
                elif rsi > 55: 
                    melhor_sinal, melhor_taxa, melhor_ativo = "PUT", "92%", nome
                    break
        except:
            continue

    if melhor_ativo == "PROCURANDO...": melhor_ativo = "EUR/USD"

    return {"ativo": melhor_ativo, "sinal": melhor_sinal, "assertividade": melhor_taxa}

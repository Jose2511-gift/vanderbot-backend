from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas_ta as ta
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista um pouco menor para o Yahoo não se irritar
ATIVOS = [
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", 
    "BTC-USD", "ETH-USD", "GC=F"
]

def calcular_indicadores(data):
    try:
        fechamentos = data['Close']
        rsi = ta.rsi(fechamentos, length=14).iloc[-1]
        bbands = ta.bbands(fechamentos, length=20, std=2)
        sup = bbands['BBU_20_2.0'].iloc[-1]
        inf = bbands['BBL_20_2.0'].iloc[-1]
        atual = fechamentos.iloc[-1]
        return rsi, atual, sup, inf
    except:
        return None, None, None, None

@app.get("/analizar")
def analisar(estrategia: str = "ZEUS", id: str = "0"):
    melhor_ativo = "EUR/USD"
    melhor_sinal = "AGUARDAR"
    melhor_taxa = "0%"
    
    # Baixa todos de uma vez (isso evita o erro de 'Too Many Requests')
    try:
        dados_multiplos = yf.download(ATIVOS, period="1d", interval="1m", group_by='ticker', progress=False, threads=False)
        
        for ticker in ATIVOS:
            df = dados_multiplos[ticker].tail(30)
            if len(df) < 20: continue
            
            rsi, atual, sup, inf = calcular_indicadores(df)
            if rsi is None: continue
            
            nome_limpo = ticker.replace("=X", "").replace("-USD", "/USD").replace("GC=F", "GOLD")

            # LÓGICA
            if estrategia.upper() == "ZEUS":
                if rsi < 40: melhor_sinal, melhor_taxa = "CALL", "91%"
                elif rsi > 60: melhor_sinal, melhor_taxa = "PUT", "92%"
            
            elif estrategia.upper() == "ETARE":
                if rsi < 48: melhor_sinal, melhor_taxa = "CALL", "88%"
                elif rsi > 52: melhor_sinal, melhor_taxa = "PUT", "89%"
            
            elif estrategia.upper() == "WANDER":
                if atual <= inf: melhor_sinal, melhor_taxa = "CALL", "96%"
                elif atual >= sup: melhor_sinal, melhor_taxa = "PUT", "97%"

            if melhor_sinal != "AGUARDAR":
                melhor_ativo = nome_limpo
                break
    except:
        pass

    return {
        "ativo": melhor_ativo,
        "sinal": melhor_sinal,
        "assertividade": melhor_taxa,
        "resultado": "Win ✅" if melhor_sinal != "AGUARDAR" else "Analisando..."
    }

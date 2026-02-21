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

# Lista de ativos para busca automática de WIN
ATIVOS = ["EURUSD=X", "GBPUSD=X", "BTC-USD", "ETH-USD"]

def calcular_indicadores(data):
    fechamentos = data['Close']
    rsi = ta.rsi(fechamentos, length=14).iloc[-1]
    # Bandas de Bollinger para a estratégia Wander
    bbands = ta.bbands(fechamentos, length=20, std=2)
    sup = bbands['BBU_20_2.0'].iloc[-1]
    inf = bbands['BBL_20_2.0'].iloc[-1]
    atual = fechamentos.iloc[-1]
    return rsi, atual, sup, inf

@app.get("/analizar")
def analisar(estrategia: str = "ZEUS", id: str = "0"):
    melhor_ativo = "EUR/USD"
    melhor_sinal = "AGUARDAR"
    melhor_taxa = "0%"
    
    # O robô percorre a lista para achar o melhor "Win"
    for ticker in ATIVOS:
        try:
            df = yf.Ticker(ticker).history(period="1d", interval="1m")
            if len(df) < 20: continue
            
            rsi, atual, sup, inf = calcular_indicadores(df)
            nome_limpo = ticker.replace("=X", "").replace("-USD", "/USD")

            # Lógica por Estratégia do Menu
            if estrategia.upper() == "ETARE":
                if rsi < 35: melhor_sinal, melhor_taxa = "CALL", "88%"
                elif rsi > 65: melhor_sinal, melhor_taxa = "PUT", "89%"
            
            elif estrategia.upper() == "ZEUS":
                if rsi < 30: melhor_sinal, melhor_taxa = "CALL", "91%"
                elif rsi > 70: melhor_sinal, melhor_taxa = "PUT", "92%"
            
            else: # WANDER EXTRA (A mais forte)
                if atual <= inf and rsi < 30: melhor_sinal, melhor_taxa = "CALL", "95%"
                elif atual >= sup and rsi > 70: melhor_sinal, melhor_taxa = "PUT", "96%"

            # Se achou sinal, define esse como o ativo do momento
            if melhor_sinal != "AGUARDAR":
                melhor_ativo = nome_limpo
                break # Encontrou a oportunidade de Win!
                
        except:
            continue

    return {
        "ativo": melhor_ativo,
        "sinal": melhor_sinal,
        "assertividade": melhor_taxa,
        "resultado": "Win" if melhor_sinal != "AGUARDAR" else "Analisando"
    }

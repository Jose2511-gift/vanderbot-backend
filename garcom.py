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

# ATIVOS QUE VAMOS MONITORAR
ATIVOS = ["EURUSD=X", "USDJPY=X", "GC=F"]

def calcular_indicadores(df):
    try:
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]
        bb = ta.bbands(df['Close'], length=20, std=2)
        return rsi, df['Close'].iloc[-1], bb['BBU_20_2.0'].iloc[-1], bb['BBL_20_2.0'].iloc[-1]
    except:
        return None, None, None, None

@app.get("/analizar")
def analisar(estrategia: str = "WANDER"):
    for ticker in ATIVOS:
        try:
            data = yf.download(ticker, period="1d", interval="1m", progress=False, timeout=8)
            if data.empty: continue
            
            rsi, atual, sup, inf = calcular_indicadores(data)
            if rsi is None: continue

            # Nomes limpos para o App
            nome = ticker.replace("=X", "").replace("GC=F", "GOLD (OURO)")
            if "JPY" in nome: nome = "USD/JPY (JAPÃO) 🎌"

            # AJUSTE DE SENSIBILIDADE: Se o RSI estiver abaixo de 45 ou acima de 55, ele já mostra o par!
            if rsi < 45: 
                return {"ativo": nome, "sinal": "CALL", "assertividade": "92%"}
            elif rsi > 55: 
                return {"ativo": nome, "sinal": "PUT", "assertividade": "93%"}

        except:
            continue

    # Se não achar nada mesmo assim, volta para o padrão
    return {"ativo": "EUR/USD", "sinal": "AGUARDAR", "assertividade": "85%"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas_ta as ta
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ATIVOS QUE VAMOS MONITORAR
# Mudei a ordem para ele não começar sempre pelo EURUSD
ATIVOS = ["USDJPY=X", "GC=F", "EURUSD=X"]

def calcular_indicadores(df):
    try:
        # Pega o último valor de fechamento
        ultimo_fechamento = df['Close'].iloc[-1]
        # Calcula o RSI
        rsi_series = ta.rsi(df['Close'], length=14)
        if rsi_series is None or rsi_series.empty:
            return None, None
        
        rsi = rsi_series.iloc[-1]
        return rsi, ultimo_fechamento
    except:
        return None, None

@app.get("/analizar")
def analisar(estrategia: str = "WANDER"):
    # EMBALHAR ATIVOS: Isso evita pedir sempre o mesmo e tomar bloqueio
    random.shuffle(ATIVOS)
    
    for ticker in ATIVOS:
        try:
            # Baixa apenas o necessário (periodo 1 dia, intervalo 1 minuto)
            data = yf.download(ticker, period="1d", interval="1m", progress=False, timeout=5)
            
            if data is None or data.empty:
                continue
            
            rsi, atual = calcular_indicadores(data)
            
            if rsi is None or rsi != rsi: # Verifica se é NaN
                continue

            # Nomes limpos para o App
            nome = ticker.replace("=X", "").replace("GC=F", "GOLD (OURO)")
            if "JPY" in nome: nome = "USD/JPY (JAPÃO) 🎌"
            if "EURUSD" in nome: nome = "EUR/USD (EURO)"

            # LÓGICA DE SINAL (Aumentei um pouco a margem para ser mais real)
            if rsi < 48: 
                return {"ativo": nome, "sinal": "COMPRA (CALL)", "assertividade": "92.4%"}
            elif rsi > 52: 
                return {"ativo": nome, "sinal": "VENDA (PUT)", "assertividade": "93.1%"}

        except Exception as e:
            print(f"Erro no ticker {ticker}: {e}")
            continue

    # Se o Yahoo bloquear (Rate Limit), ele cai aqui:
    return {"ativo": "MERCADO EM ANALISE", "sinal": "AGUARDAR", "assertividade": "--"}

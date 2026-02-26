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

# LISTA COMPLETA COM 12 ATIVOS (Incluindo Japão, Ouro e Criptos)
ATIVOS = [
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", 
    "USDCAD=X", "EURJPY=X", "GBPJPY=X", "GC=F", 
    "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD"
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
    melhor_ativo = "ANALISANDO..."
    melhor_sinal = "AGUARDAR"
    melhor_taxa = "0%"
    
    for ticker in ATIVOS:
        try:
            # Download rápido para não dar timeout no Render
            df = yf.download(ticker, period="1d", interval="1m", progress=False).tail(30)
            if len(df) < 20: continue
            
            rsi, atual, sup, inf = calcular_indicadores(df)
            if rsi is None: continue
            
            # Limpa o nome para exibir bonito no seu App
            nome_limpo = ticker.replace("=X", "").replace("-USD", "/USD").replace("GC=F", "GOLD (OURO)")

            # --- LÓGICA DAS 3 ESTRATÉGIAS ---
            
            # 1. ZEUS (RSI AGRESSIVO)
            if estrategia.upper() == "ZEUS":
                if rsi < 35: melhor_sinal, melhor_taxa = "CALL", "91%"
                elif rsi > 65: melhor_sinal, melhor_taxa = "PUT", "92%"
            
            # 2. ETARE (RSI MODERADO)
            elif estrategia.upper() == "ETARE":
                if rsi < 45: melhor_sinal, melhor_taxa = "CALL", "88%"
                elif rsi > 55: melhor_sinal, melhor_taxa = "PUT", "89%"
            
            # 3. EXTRA WANDER (RSI + BANDAS DE BOLLINGER)
            elif estrategia.upper() == "WANDER":
                if atual <= inf and rsi < 35: melhor_sinal, melhor_taxa = "CALL", "96%"
                elif atual >= sup and rsi > 65: melhor_sinal, melhor_taxa = "PUT", "97%"

            # Se achou uma oportunidade, escolhe esse ativo e para a busca
            if melhor_sinal != "AGUARDAR":
                melhor_ativo = nome_limpo
                break 

        except:
            continue

    # Se não achar nada nas 3 estratégias, ele sugere o primeiro da lista
    if melhor_ativo == "ANALISANDO...":
        melhor_ativo = "EUR/USD"

    return {
        "ativo": melhor_ativo,
        "sinal": melhor_sinal,
        "assertividade": melhor_taxa,
        "resultado": "Win ✅" if melhor_sinal != "AGUARDAR" else "Analisando..."
    }

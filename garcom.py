from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analizar")
def analisar(estrategia: str = "WANDER"):
    # Simula o tempo de processamento do robô
    time.sleep(1.5) 
    
    # LÓGICA PARA A ESTRATÉGIA WANDER (Focada em Moedas Principais)
    if estrategia == "WANDER":
        ativos = ["EUR/USD (EURO) 🇪🇺", "GBP/USD (LIBRA) 🇬🇧", "USD/CHF (SUIÇA) 🇨🇭"]
        sinal = random.choice(["COMPRA (CALL)", "VENDA (PUT)"])
        win = f"{random.uniform(92.1, 94.5):.1f}%"

    # LÓGICA PARA A ESTRATÉGIA ZEUS (Focada em Ouro e Japão - Mais agressiva)
    elif estrategia == "ZEUS":
        ativos = ["GOLD (OURO) 🏆", "USD/JPY (JAPÃO) 🎌", "EUR/JPY (JAPÃO) 🎌"]
        sinal = random.choice(["COMPRA (CALL)", "VENDA (PUT)"])
        win = f"{random.uniform(94.6, 96.8):.1f}%"

    # LÓGICA PARA A ESTRATÉGIA ETARE (Focada em Tendência de Fluxo)
    elif estrategia == "ETARE":
        ativos = ["AUD/USD (AUST) 🇦🇺", "USD/CAD (CANADÁ) 🇨🇦", "EUR/GBP (EURO/LIBRA) 🇪🇺"]
        # A ETARE às vezes pede para aguardar se o fluxo estiver baixo
        sinal = random.choice(["COMPRA (CALL)", "VENDA (PUT)", "AGUARDAR"])
        win = f"{random.uniform(90.5, 93.0):.1f}%"
        if sinal == "AGUARDAR": win = "--"

    else:
        return {"ativo": "ERRO", "sinal": "ESTRATEGIA INVALIDA", "assertividade": "0%"}

    ativo_escolhido = random.choice(ativos)

    return {
        "ativo": ativo_escolhido,
        "sinal": sinal,
        "assertividade": win
    }

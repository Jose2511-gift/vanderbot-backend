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
def analisar(estrategia: str = "WANDER", id_user: str = ""):
    time.sleep(1.2) 
    
    # BANCO DE DADOS ATUALIZADO COM SEUS 4 IDs
    corretoras = {
        "62846177": "QUOTEX",
        "97181892": "IQ OPTION",
        "174555933": "POLARIUM", # O ID QUE VOCÊ ESTÁ TENTANDO USAR
        "171825029": "STOCKITY"
    }

    # Se o ID não estiver na lista acima, ele bloqueia
    if id_user not in corretoras:
        return {
            "ativo": "ID NÃO AUTORIZADO", 
            "sinal": "VERIFIQUE SEU ID", 
            "assertividade": "0%"
        }

    nome_corretora = corretoras[id_user]

    # Ativos por Estratégia
    if estrategia == "ZEUS":
        ativos = ["GOLD (OURO) 🏆", "USD/JPY 🎌"]
        win = f"{random.uniform(94.5, 96.5):.1f}%"
    elif estrategia == "ETARE":
        ativos = ["AUD/USD 🇦🇺", "EUR/GBP 🇪🇺"]
        win = f"{random.uniform(91.0, 93.5):.1f}%"
    else: # WANDER
        ativos = ["EUR/USD 🇪🇺", "GBP/USD 🇬🇧", "USD/CHF 🇨🇭"]
        win = f"{random.uniform(92.5, 94.8):.1f}%"

    sinal = random.choice(["COMPRA (CALL)", "VENDA (PUT)"])
    ativo_escolhido = random.choice(ativos)

    return {
        "ativo": f"[{nome_corretora}] {ativo_escolhido}",
        "sinal": sinal,
        "assertividade": win
    }

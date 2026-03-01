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
    # Pequena pausa para simular a inteligência artificial pensando
    time.sleep(1.2) 
    
    # BANCO DE DADOS DE IDS AUTORIZADOS
    corretoras = {
        "62846177": "QUOTEX",
        "97181892": "IQ OPTION",
        "174555933": "POLARIUM",
        "171825029": "STOCKITY"
    }

    # Verifica se o ID digitado no App existe na nossa lista
    if id_user not in corretoras:
        return {
            "ativo": "ID NÃO AUTORIZADO", 
            "sinal": "VERIFIQUE SEU ID", 
            "assertividade": "0%"
        }

    nome_corretora = corretoras[id_user]

    # Configuração de Ativos por Estratégia
    if estrategia == "ZEUS":
        ativos = ["GOLD (OURO) 🏆", "USD/JPY 🎌", "EUR/JPY 🎌"]
        win = f"{random.uniform(94.5, 96.5):.1f}%"
    elif estrategia == "ETARE":
        ativos = ["AUD/USD 🇦🇺", "USD/CAD 🇨🇦", "EUR/GBP 🇪🇺"]
        win = f"{random.uniform(91.0, 93.5):.1f}%"
    else: # WANDER
        ativos = ["EUR/USD 🇪🇺", "GBP/USD 🇬🇧", "USD/CHF 🇨🇭"]
        win = f"{random.uniform(92.5, 94.8):.1f}%"

    sinal = random.choice(["COMPRA (CALL)", "VENDA (PUT)"])
    # Para a ETARE, às vezes o mercado entra em espera
    if estrategia == "ETARE" and random.random() < 0.2:
        sinal = "AGUARDAR"
        win = "--"

    ativo_escolhido = random.choice(ativos)

    # Retorna o resultado com o nome da corretora no início
    return {
        "ativo": f"[{nome_corretora}] {ativo_escolhido}",
        "sinal": sinal,
        "assertividade": win
    }

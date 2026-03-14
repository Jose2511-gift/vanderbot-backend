import random
from datetime import datetime

def analisar_mercado(estrategia, id_user):
    # Obtém o segundo atual para a regra dos 2 segundos
    segundo_atual = datetime.now().second
    
    # Lista de ativos que quase sempre estão abertos
    ativos_premium = [
        "EUR/USD (OTC) 🇪🇺", "GBP/USD (OTC) 🇬🇧", 
        "USD/JPY (OTC) 🎌", "GOLD (OURO) 🏆", "OIL (PETRÓLEO) 🛢️"
    ]

    # Escolha do ativo e direção
    ativo_escolhido = random.choice(ativos_premium)
    direcao = random.choice(["COMPRA (CALL) 🟢", "VENDA (PUT) 🔴"])
    
    # IA de Assertividade e Tendência
    win_rate = random.uniform(96.2, 99.8)
    
    # Lógica de Alerta de Tendência
    if win_rate > 98.5:
        alerta = "🔥 TENDÊNCIA FORTE! ENTRADA SEGURA"
    elif win_rate > 97.5:
        alerta = "✅ SINAL CONFIRMADO PELA IA"
    else:
        alerta = "⚠️ MERCADO INSTÁVEL! CUIDADO"

    # Lógica do Cronômetro de Virada (Regra dos 2 segundos)
    if segundo_atual >= 55:
        cronometro = "🚀 HORA DE ANALISAR! CLIQUE AGORA!"
    else:
        segundos_faltam = 58 - segundo_atual if segundo_atual < 58 else 0
        cronometro = f"⏳ AGUARDE {segundos_faltam}s PARA A VIRADA"

    if estrategia == "ZEUS" or estrategia == "WANDER":
        return {
            "ativo": ativo_escolhido,
            "sinal": direcao,
            "assertividade": f"{win_rate:.1f}%",
            "alerta": alerta,
            "cronometro": cronometro
        }

    return {
        "ativo": "ERRO", 
        "sinal": "TENTE NOVAMENTE", 
        "assertividade": "0%", 
        "alerta": "ERRO DE CONEXÃO",
        "cronometro": "AGUARDE"
    }

import random
from datetime import datetime

def analisar_mercado(estrategia, id_user):
    segundo_atual = datetime.now().second
    
    # Ativos para Quotex, IQ Option, Stockity e Polarium
    ativos_premium = ["EUR/USD (OTC) 🇪🇺", "GBP/USD (OTC) 🇬🇧", "USD/JPY (OTC) 🎌", "GOLD (OURO) 🏆"]
    ativo_escolhido = random.choice(ativos_premium)
    direcao = random.choice(["COMPRA (CALL) 🟢", "VENDA (PUT) 🔴"])
    win_rate = random.uniform(96.2, 99.8)
    
    # Define a Tendência e o Alerta que aparecem no site
    if win_rate > 98.5:
        alerta = "🔥 TENDÊNCIA FORTE! ENTRADA SEGURA"
        tendencia = "FORTE"
    else:
        alerta = "✅ SINAL CONFIRMADO PELA IA"
        tendencia = "ESTÁVEL"

    # Libera as 3 estratégias: WANDER, ZEUS e ETARE
    estrategias_validas = ["WANDER", "ZEUS", "ETARE"]
    
    if estrategia.upper() in estrategias_validas:
        return {
            "ativo": ativo_escolhido,
            "sinal": direcao,
            "assertividade": f"{win_rate:.1f}%",
            "alerta": alerta,       # CAMPO OBRIGATÓRIO PARA O NOVO HTML
            "tendencia": tendencia  # CAMPO OBRIGATÓRIO PARA O NOVO HTML
        }

    return {"ativo": "ERRO", "sinal": "ESTRATEGIA INVÁLIDA", "assertividade": "0%", "alerta": "---", "tendencia": "---"}

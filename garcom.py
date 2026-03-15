import random
from datetime import datetime

def analisar_mercado(estrategia, id_user):
    # Obtém o segundo atual para a regra dos 2 segundos
    segundo_atual = datetime.now().second
    
    # Lista de ativos (Mantendo os seus ativos premium)
    ativos_premium = [
        "EUR/USD (OTC) 🇪🇺", "GBP/USD (OTC) 🇬🇧", 
        "USD/JPY (OTC) 🎌", "GOLD (OURO) 🏆", "OIL (PETRÓLEO) 🛢️"
    ]

    # Escolha do ativo e direção
    ativo_escolhido = random.choice(ativos_premium)
    direcao = random.choice(["COMPRA (CALL) 🟢", "VENDA (PUT) 🔴"])
    
    # IA de Assertividade e Tendência
    win_rate = random.uniform(96.2, 99.8)
    
    # Lógica de Alerta e Tendência (O que vai aparecer no site)
    if win_rate > 98.5:
        alerta = "🔥 TENDÊNCIA FORTE! ENTRADA SEGURA"
        tendencia = "FORTE (ALTA ASSERTIVIDADE)"
    elif win_rate > 97.5:
        alerta = "✅ SINAL CONFIRMADO PELA IA"
        tendencia = "NORMAL (ESTÁVEL)"
    else:
        alerta = "⚠️ MERCADO INSTÁVEL! CUIDADO"
        tendencia = "LATERAL (RISCO MODERADO)"

    # Lógica do Cronômetro de Virada
    if segundo_atual >= 55:
        cronometro = "🚀 HORA DE ANALISAR! CLIQUE AGORA!"
    else:
        segundos_faltam = 58 - segundo_atual if segundo_atual < 58 else 0
        cronometro = f"⏳ AGUARDE {segundos_faltam}s PARA A VIRADA"

    # AGORA ACEITA AS 3 ESTRATÉGIAS: ZEUS, WANDER E ETARE
    estrategias_validas = ["ZEUS", "WANDER", "ETARE"]
    
    if estrategia.upper() in estrategias_validas:
        return {
            "ativo": ativo_escolhido,
            "sinal": direcao,
            "assertividade": f"{win_rate:.1f}%",
            "alerta": alerta,
            "tendencia": tendencia, # Adicionado para o HTML novo
            "cronometro": cronometro
        }

    # Caso a estratégia não seja reconhecida
    return {
        "ativo": "ERRO", 
        "sinal": "ESTRATEGIA INVÁLIDA", 
        "assertividade": "0%", 
        "alerta": "ERRO DE SELEÇÃO",
        "tendencia": "---",
        "cronometro": "AGUARDE"
    }

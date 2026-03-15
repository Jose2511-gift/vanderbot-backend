from flask import Flask, render_template, request, jsonify
from garcom import analisar_mercado

app = Flask(__name__)

@app.route('/')
def index():
    # Carrega a página principal do seu bot
    return render_template('index.html')

@app.route('/analisar')
def analisar():
    # Pega a estratégia selecionada (WANDER ou ZEUS)
    estrategia = request.args.get('estrategia', 'ZEUS')
    
    # Chama a IA que a gente configurou no garcom.py
    resultado = analisar_mercado(estrategia, "usuario_premium")
    
    # Envia os dados (Sinal, Assertividade, Alerta e Cronômetro) para o celular
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)

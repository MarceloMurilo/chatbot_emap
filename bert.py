# Importe as bibliotecas necessárias
from flask import Flask, request, jsonify
import json
import pandas as pd
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch
import threading

app = Flask(__name__)

# Carregue o modelo BERT pré-treinado e o tokenizador
model_name = "piEsposito/braquad-bert-qna"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Carregue o arquivo CSV com perguntas e respostas
df = pd.read_csv("ia2 - ia.csv")

# Converter os dados para um formato adequado para JSON
data = []
for index, row in df.iterrows():
    pergunta = row['PERGUNTA']
    resposta = row['RESPOSTA']
    data.append({'pergunta': pergunta, 'resposta': resposta})

# Variável global para controlar o estado do bot
bot_ativado = 0  # Inicialmente desativado

@app.route('/whatsapp', methods=['POST'])
def receive_whatsapp():
    global bot_ativado
    data = request.json
    user_input = data['question']

    if bot_ativado == 0:
        if user_input == "iniciar":
            iniciar()
            return jsonify({"answer": "O bot foi iniciado."})
        else:
            return jsonify({"answer": "O bot ainda não foi iniciado. Use o comando 'iniciar' para iniciar o bot."})

    # Chame a função para responder à pergunta do usuário
    resposta = chatbot(user_input)
    return jsonify({"answer": resposta})

# Função para vetorizar texto usando BERT
def vetorizar_texto(texto):
    inputs = tokenizer(texto, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = torch.mean(outputs.last_hidden_state, dim=1)  # Média das embeddings das palavras
    return embeddings

# Vetorizar perguntas usando BERT
perguntas_embeddings = torch.cat([vetorizar_texto(d['pergunta']) for d in data])

# Função para encontrar a melhor resposta com base na pergunta do usuário
def chatbot(user_input):
    global bot_ativado

    if user_input == "sair":
        bot_ativado = 0
        return "Bot encerrado. Digite 'iniciar' para iniciar novamente."

    user_input_embedding = vetorizar_texto(user_input)
    similarity_scores = cosine_similarity(user_input_embedding, perguntas_embeddings)
    best_match_index = similarity_scores.argmax()
    resposta = data[best_match_index]['resposta']
    return resposta

# Função para iniciar o bot
def iniciar():
    global bot_ativado
    bot_ativado = 1
    return "O bot foi iniciado."

# Rota para iniciar o bot
@app.route('/iniciar', methods=['POST'])
def iniciar_bot():
    iniciar()
    return {"status": "ok"}

if __name__ == '__main__':
    # Inicie uma thread para executar o Flask
    thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    thread.start()

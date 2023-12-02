# chatbot_emap

# **Funcionamento do Chatbot**

Este chatbot, desenvolvido para operar no WhatsApp, envolve a integração de código JavaScript (Node.js) e Python. Abaixo, detalhamos como cada parte do código contribui para o funcionamento do chatbot.

## **Parte JavaScript (Node.js)**

### **Inicialização do Cliente WhatsApp**

O código começa inicializando o cliente WhatsApp usando a biblioteca **`@wppconnect-team/wppconnect`**. A instância do cliente é criada utilizando o método **`create()`**, e a execução do restante do código é condicionada à resolução da promise resultante.

### **Manipulação de Mensagens Recebidas**

O chatbot reage a mensagens recebidas, mas ignora mensagens provenientes de grupos. A pergunta do usuário é extraída da mensagem recebida e enviada para o servidor Python através de uma requisição HTTP usando a biblioteca **`axios`**.

A resposta do modelo Python é então enviada de volta ao WhatsApp utilizando a função **`sendText`** do cliente.

## **Parte Python (Flask + BERT)**

### **Inicialização do Servidor Flask**

O servidor Flask é inicializado para lidar com as requisições provenientes do código JavaScript. Ele escuta na porta 5000 e expõe a rota **`/whatsapp`** para receber as perguntas do usuário.

### **Vetorização de Texto usando BERT**

O modelo BERT pré-treinado é carregado usando a biblioteca **`transformers`**. A função **`vetorizar_texto`** converte o texto em embeddings usando BERT. As perguntas do conjunto de dados CSV são pré-vetorizadas e armazenadas.

### **Função de Resposta do Chatbot**

A função **`chatbot`** recebe a pergunta do usuário, vetoriza-a e calcula a similaridade com as perguntas pré-vetorizadas. A resposta mais apropriada é escolhida com base na similaridade.

### **Inicialização e Controle do Bot**

O bot é inicialmente desativado e pode ser ativado com o comando "iniciar". Isso é feito utilizando uma variável global **`bot_ativado`**.

## **Conjunto de Dados (CSV)**

O conjunto de dados em formato CSV contém perguntas e respostas. Cada pergunta está associada à sua respectiva resposta, e esses dados são utilizados para treinar e operar o chatbot.

Para iniciar o bot, um comando "iniciar" deve ser enviado.

---

## **Para Executar o Chatbot:**

1. **Instale as Dependências:**
    - Certifique-se de ter as bibliotecas e pacotes necessários instalados para ambas as partes (Node.js e Python).
2. **Inicie o Servidor Flask:**
    - Execute o código Python para iniciar o servidor Flask que escuta em **`http://127.0.0.1:5000`**.
3. **Execute o Cliente WhatsApp:**
    - Inicie o cliente WhatsApp usando o código JavaScript. O bot responderá às mensagens recebidas com base nas respostas do modelo BERT.

Lembre-se de configurar corretamente os caminhos dos arquivos CSV e do modelo BERT no código Python antes de iniciar.



## **Agradecimentos**

Gostaria de agradecer ao querido professor Josenildo, por me ajudar nesse projeto, me orientando a compreender e pesquisar os principais conteúdos pra criação desse chatbot.
Ao IFMA e à SOFTEX pela oportunidade de participar deste Hackaton e pelo aprendizado conquistado ao decorrer desse período.
Foi maravilhoso aprender técnicas de NLP, e entender como funciona as nuances de uma Inteligência Artificial de Linguagem Natural 🤖🤖🤖

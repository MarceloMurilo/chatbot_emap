const axios = require('axios');
const { create, Client } = require('@wppconnect-team/wppconnect');
const app = require('./app'); // Adicione esta linha para importar 'app.js'
create().then((client) => {
  // Resto do código para inicializar o cliente WhatsApp

  // Lidar com mensagens recebidas
  client.onMessage(async (message) => {
    if (message.isGroupMsg) {
      console.log('Ignorando mensagem de grupo');
      return;
    }

    const userQuestion = message.body;

    // Enviar a pergunta para o servidor Python
    try {
      const response = await axios.post('http://127.0.0.1:5000/whatsapp', {
        question: userQuestion,
      });

      const modelResponse = response.data.answer;

      // Enviar a resposta do modelo de volta ao WhatsApp
      await client.sendText(message.from, modelResponse);
    } catch (error) {
      console.error('Erro ao se comunicar com o servidor Python: ', error);
    }
  });
});

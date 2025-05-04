# bot_integration.py
from flask import Flask, request, jsonify
import openai  # или другая библиотека для работы с вашим ботом
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Конфигурация (лучше вынести в отдельный config.py)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
API_KEY = os.getenv('BOT_API_KEY')


class ChatBot:
    def __init__(self):
        # Инициализация бота
        self.setup_bot()

    def setup_bot(self):
        """Настройка подключения к API бота"""
        openai.api_key = API_KEY  # Пример для OpenAI

    def get_response(self, message, context=None):
        """Получение ответа от бота"""
        try:
            # Пример для OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            return f"Ошибка при обработке запроса: {str(e)}"


# Инициализация бота
bot = ChatBot()


@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint для общения с ботом"""
    # Проверка авторизации
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401

    # Получение данных запроса
    data = request.get_json()
    message = data.get('message', '')
    context = data.get('context', None)

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Получение ответа от бота
    response = bot.get_response(message, context)

    return jsonify({
        "response": response,
        "status": "success"
    })


@app.route('/chat-widget')
def chat_widget():
    """HTML виджет чата для встраивания на сайт"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Widget</title>
        <style>
            #chat-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 350px;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                background: white;
                z-index: 1000;
            }
            #chat-header {
                background: #4CAF50;
                color: white;
                padding: 10px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                cursor: pointer;
            }
            #chat-body {
                height: 300px;
                overflow-y: auto;
                padding: 10px;
            }
            #chat-input {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            #send-btn {
                background: #4CAF50;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 5px;
            }
            .message {
                margin: 5px 0;
                padding: 8px 12px;
                border-radius: 5px;
                max-width: 80%;
            }
            .user-message {
                background: #e3f2fd;
                margin-left: auto;
            }
            .bots-message {
                background: #f1f1f1;
                margin-right: auto;
            }
        </style>
    </head>
    <body>
        <div id="chat-container">
            <div id="chat-header">Чат с ботом</div>
            <div id="chat-body"></div>
            <div style="padding: 10px;">
                <input type="text" id="chat-input" placeholder="Введите сообщение...">
                <button id="send-btn">Отправить</button>
            </div>
        </div>

        <script>
            const chatBody = document.getElementById('chat-body');
            const chatInput = document.getElementById('chat-input');
            const sendBtn = document.getElementById('send-btn');

            function addMessage(text, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'bots-message'}`;
                messageDiv.textContent = text;
                chatBody.appendChild(messageDiv);
                chatBody.scrollTop = chatBody.scrollHeight;
            }

            async function sendMessage() {
                const message = chatInput.value.trim();
                if (!message) return;

                addMessage(message, true);
                chatInput.value = '';

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer YOUR_API_KEY'
                        },
                        body: JSON.stringify({ message })
                    });

                    const data = await response.json();
                    if (data.response) {
                        addMessage(data.response, false);
                    } else {
                        addMessage("Ошибка при получении ответа", false);
                    }
                } catch (error) {
                    addMessage("Ошибка соединения с сервером", false);
                }
            }

            sendBtn.addEventListener('click', sendMessage);
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    """


if __name__ == '__main__':
    app.run(debug=True)
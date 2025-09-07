from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Ваш API-ключ от DeepSeek мы будем получать из переменной окружения
# Важно: мы используем os.environ.get(...), чтобы получить значение из настроек Railway
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
# Уточните точный URL API в документации DeepSeek! Этот примерный.
DEEPSEEK_API_URL = "https://api.deepseek.com"

@app.route('/v1/chat/completions', methods=['POST'])
def proxy_to_deepseek():
    try:
        # Получаем данные, которые пришли от нашего скрипта
        data = request.get_json()

        # Заголовки для запроса к DeepSeek API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }

        # Отправляем запрос к настоящему API DeepSeek
        response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers)
        # Возвращаем ответ от DeepSeek обратно нашему скрипту
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

from flask import Flask, request, Response
import requests

app = Flask(__name__)

SITE1_URL = 'http://site1.ru'
SITE2_URL = 'http://site2.ru'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f'{SITE1_URL}/{path}'
    
    try:
        response = requests.get(url, headers=request.headers)
        if response.status_code == 200:
            # Перенаправляем на site1.ru/ указав location если ошибка == коду
            return Response(status=302, headers={'Location': f'{SITE1_URL}/'})
        else:
            return Response(status=302, headers={'Location': SITE2_URL})
    except (requests.exceptions.RequestException, ConnectionError) as e:
        # Обработка ошибок сети и ошибок подключения
        # Перенаправляем на site2.ru в случае ошибок
        return Response(status=302, headers={'Location': SITE2_URL})

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80)

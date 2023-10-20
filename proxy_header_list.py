from flask import Flask, Response, request
import requests

app = Flask(__name__)

SITE1_URL = 'http://site1.com'
SITE2_URL = 'http://site2.com'
SITE3_URL = 'http://site3.com'

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    if path == '1':
        url = f'{SITE1_URL}/api/v1/ntlm'
    elif path == '2':
        url = f'{SITE2_URL}/api/v1/ntlm'
    else:
        # Если значение параметра пути не '1' и не '2', перенаправляем на SITE3_URL
        url = SITE3_URL

    try:
        # Используем метод запроса текущего запроса (GET, POST, PUT, DELETE)
        # и передаем все заголовки, включая заголовки авторизации и другие заголовки запроса
        response = requests.request(request.method, url, headers=request.headers, data=request.data)
        if response.status_code == 404:
            # Возвращаем перенаправление на SITE3_URL, если получен статус 404
            return Response(status=302, headers={'Location': SITE3_URL})
        else:
            # В противном случае возвращаем ответ, полученный от удаленного сервера
            return response
    except (requests.exceptions.RequestException, ConnectionError) as e:
        # В случае ошибки также перенаправляем на SITE3_URL
        return Response(status=302, headers={'Location': SITE3_URL})

if __name__ == '__main__':
    app.run()

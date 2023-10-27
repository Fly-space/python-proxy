from flask import Flask, Response, request
import requests
import logging

app = Flask(__name__)

log_file = "./app/app.log"

app.debug = True

handler = logging.FileHandler(log_file)

handler.setLevel(logging.DEBUG)

app.logger.addHandler(handler)

SITE1_URL = 'http://miass.ru'
SITE2_URL = 'http://74.ru'
SITE3_URL = 'http://google.ru'

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    if path == '1':
        url = f'{SITE1_URL}/actual.html'
    elif path == '2':
        url = f'{SITE2_URL}/text/world/2023/10/27/72855869'
    else:
        # Если значение параметра пути не '1' и не '2', перенаправляем на SITE3_URL
        url = SITE3_URL

    try:
        response = requests.get(url, headers=request.headers)
        if response.status_code == 404:
            return Response(status=302, headers={'Location': SITE3_URL})
        else:
            return response
    except (requests.exceptions.RequestException, ConnectionError) as e:
        return Response(status=302, headers={'Location': SITE3_URL})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

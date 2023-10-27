from flask import Flask, Response, request
import requests

app = Flask(__name__)

SITE1_URL = 'http://a1'
SITE2_URL = 'http://a2'
SITE3_URL = 'http://a3'

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
        response = requests.get(url, headers=request.headers)
        if response.status_code == 404:
            return Response(status=302, headers={'Location': SITE3_URL})
        else:
            return response
    except (requests.exceptions.RequestException, ConnectionError) as e:
        return Response(status=302, headers={'Location': SITE3_URL})

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80)

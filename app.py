from flask import Flask, request
import logging
import json
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {'session': request.json['session'],
                'version': request.json['version'],
                'response': {'end_session': False}}
    handleDialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handleDialog(res, req):
    if req['session']['new']:
        res['response']['text'] = 'Привет! Я могу перевести любую фразу! Просто скажи "Переведи ..."!'
        return
    phrase = req['request']['original_utterance'].lower()
    if phrase.startswith('переведи'):
        res['response']['text'] = getTranslation(phrase[9:])
    else:
        res['response']['text'] = 'Неверный формат запроса!'


def getTranslation(phrase):
    try:
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        params = {
            'key': 'trnsl.1.1.20200425T163049Z.df8faea63f55d3a5.63e0685f564e78f2f1731927d759911df3ea9eb8',
            'text': phrase,
            'lang': 'en'
        }
        data = requests.get(url, params).json()
        return data['text'][0]
    except Exception as e:
        return e


if __name__ == '__main__':
    app.run()

import logging
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from matcher import match_rules
from displacy_highlighter import highlight

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

app = Flask(__name__)
app.logger.handlers = logging.getLogger().handlers


@app.route('/api/match', methods=['POST'])
@cross_origin(origin='*')
def match():
    data = request.json
    highlights_count, doc = match_rules(data['text'], data['rules'])
    highlighted_text = highlight(doc)
    return jsonify({'highlights_count': highlights_count, 'highlighted_text': highlighted_text})


@app.before_request
def log_request_info():
    app.logger.debug('Body: %s', request.get_data())


@app.after_request
def after(response):
    app.logger.debug('Response: %s', response.get_data())
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

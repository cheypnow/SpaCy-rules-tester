import logging
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from matcher import match_rules
from highlighter import highlight_text

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

app = Flask(__name__)
app.logger.handlers = logging.getLogger().handlers


#  Rules example:
# [
#     {
#         "label": "EXPERIENCE",
#         "pattern": [
#             [{"IS_DIGIT": true}, {"LEMMA": "год"}],
#             [{"IS_DIGIT": true}, {"LEMMA": "year"}],
#             [{"IS_DIGIT": true}, {"LENGTH":  1}, {"LEMMA": "year"}],
#             [{"LEMMA": "experience"}, {"IS_PUNCT": true}]
#         ]
#     },
#     {
#         "label": "REMOTE",
#         "pattern": [
#             [{"LOWER": "Remote work"}]
#         ]
#     },
#     {
#         "label": "RELOCATION",
#         "pattern": [
#             [{"LOWER": "relocation"}]
#         ]
#     }
# ]
@app.route('/api/match', methods=['POST'])
@cross_origin(origin='*')
def match():
    data = request.json
    text = data['text']
    result = match_rules(text, data['rules'])
    highlighted_text = highlight_text(text, result['highlights'])
    return jsonify({'highlights_count': len(result['highlights']), 'highlighted_text': highlighted_text})


@app.before_request
def log_request_info():
    app.logger.debug('Body: %s', request.get_data())


@app.after_request
def after(response):
    app.logger.debug('Response: %s', response.get_data())
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

import logging
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from matcher import match_rules

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
    rules = json.loads(request.json['rules'])
    text = request.json['text']

    matched_terms = match_rules(rules, text)

    return jsonify(matched_terms)


@app.before_request
def log_request_info():
    app.logger.debug('Body: %s', request.get_data())


@app.after_request
def after(response):
    app.logger.debug('Response: %s', response.get_data())
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

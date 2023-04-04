from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/match', methods=['POST'])
def match():
    rules = request.json['rules']
    text = request.json['text']

    matched_terms = match_rules(rules, text)

    return jsonify(matched_terms)

if __name__ == '__main__':
    app.run()
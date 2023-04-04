import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

def match_rules(rules, text):

    matcher = Matcher(nlp.vocab)
    for rule in rules:
        matcher.add(rule["label"], None, rule["pattern"])

    # Tokenize the input text using the Spacy nlp object
    doc = nlp(text)

    # Use the matcher to match the rules against the tokenized text
    matches = matcher(doc)

    # Collect the matched terms and return them as a list
    matched_terms = []
    for match_id, start, end in matches:
        matched_terms.append(doc[start:end].text)

    return matched_terms
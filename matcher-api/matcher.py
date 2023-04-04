import spacy
import logging
import json

from spacy.matcher import Matcher

logger = logging.getLogger(__name__)

nlp = spacy.load("en_core_web_trf")


def match_rules(rules, text):
    matcher = Matcher(nlp.vocab)

    logger.info(f"Rules: {rules}")

    for rule in rules:
        if isinstance(rule, dict) and "label" in rule and "pattern" in rule:
            label = rule["label"]
            pattern = rule["pattern"]
            logger.info(f"Add rule {label} with patterns {pattern}")
            matcher.add(label, pattern)
        else:
            logger.info(f"Invalid rule: {rule}")

    # Tokenize the input text using the Spacy nlp object
    doc = nlp(text)

    # Use the matcher to match the rules against the tokenized text
    matches = matcher(doc)

    # Collect the matched terms and return them as a list
    matched_terms = []
    for match_id, start, end in matches:
        logger.info(f"Match: {matches}")
        matched_terms.append(doc[start:end].text)

    return matched_terms

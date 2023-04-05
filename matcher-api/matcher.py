import spacy
import logging
import json

from spacy.matcher import Matcher

logger = logging.getLogger(__name__)

nlp = spacy.load("en_core_web_trf")


def match_rules(text, rules):
    matcher = Matcher(nlp.vocab)

    logger.info(f"Rules: {rules}")

    for rule in rules:
        if isinstance(rule, dict) and "label" in rule and "patterns" in rule:
            label = rule["label"]
            patterns = json.loads(rule["patterns"])
            logger.info(f"Add rule {label} with patterns {patterns}")
            matcher.add(label, patterns)
        else:
            logger.info(f"Invalid rule: {rule}")

    doc = nlp(text)

    highlights = []
    for match_id, start, end in matcher(doc):
        label = doc.vocab.strings[match_id]

        logger.info(f"Match {match_id}. Label: {label}. Start: {start}. End: {end}")

        highlights.append({
            "start": start,
            "end": end,
            "label": doc.vocab.strings[label]
        })
    return {"text": text, "highlights": highlights}

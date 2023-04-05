import spacy
import logging
import json

from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy.util import filter_spans

logger = logging.getLogger(__name__)

nlp = spacy.load("en_core_web_trf")


def match_rules(text, rules):
    matcher = create_matcher(rules)

    doc = nlp(text)

    spans = []
    for match_id, start, end in matcher(doc):
        label = doc.vocab.strings[match_id]

        logger.info(f"Match {match_id}. Label: {label}. Start: {start}. End: {end}")

        span = Span(doc, start, end, label=match_id)

        spans = spans + [span]

    all_matches = doc.ents + tuple(spans)
    filtered_spans = filter_spans(all_matches)

    doc.ents = tuple(filtered_spans)

    return len(doc.ents), doc


def create_matcher(rules):
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

    return matcher

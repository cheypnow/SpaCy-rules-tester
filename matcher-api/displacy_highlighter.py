from spacy import displacy


def highlight(doc):
    return displacy.render(doc, style="ent", page=False)

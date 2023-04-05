css_class_highlight = 'highlight'


def highlight_text(text, highlights):
    html = ""
    current_pos = 0
    for highlight in highlights:
        start = highlight['start']
        end = highlight['end']
        label = highlight['label']
        html += text[current_pos:start]
        html += f'<span class="{css_class_highlight}">{text[start:end]}</span>'
        current_pos = end
    html += text[current_pos:]
    return html

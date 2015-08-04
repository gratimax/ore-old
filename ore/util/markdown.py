from markdown2 import markdown
from bleach import clean

# Our own custom ruleset for sanitized markdown

ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'div',
    'em',
    'i',
    'li',
    'ol',
    'p',
    'pre',
    'span',
    'strong',
    'table',
    'ul',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'hr'
]

ALLOWED_ATTRIBUTES = {
    '*': ['style', 'class', 'id'],
    'a': ['href', 'title', 'rel'],
    'abbr': ['title'],
    'acronym': ['title'],
    # NOTE: While bleach does a good job at cleaning out <img src="javascript:alert('XSS')"> hacks,
    # perhaps some greater care should be taken
    'img': ['src', 'alt']
}

ALLOWED_STYLES = [
    'color',
    'background-color',
    'font-size',
    'font-weight',
    'font-family',
    'float',
    'width',
    'height',
    'border'
]

MARKDOWN_EXTRAS = [
    'fenced-code-blocks',
    'header-ids',
    'markdown-in-html',
    'spoilers',
    'tables'
]


def compile(text):
    md = markdown(text, extras=MARKDOWN_EXTRAS)
    sanitized = clean(
        md, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)
    return sanitized

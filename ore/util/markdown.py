from markdown2 import markdown
from bleach import clean
from bs4 import BeautifulSoup
from ore.core.regexs import EXTENDED_URL_REGEX
import re
from django.core.urlresolvers import reverse

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
    'img',
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
    '*': ['style', 'id'],
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

PAGE_REGEX = re.compile('^(?:page!)?(?P<page>' + EXTENDED_URL_REGEX + ')$')
PROJECT_REGEX = re.compile(
    '^(?:project!)?(?P<namespace>' + EXTENDED_URL_REGEX + ')/(?P<project>' + EXTENDED_URL_REGEX + ')$')
NAMESPACE_REGEX = re.compile(
    '^(?:namespace!|user!|organization!|org!)(?P<namespace>' + EXTENDED_URL_REGEX + ')$')
OTHER_PROJECT_PAGE_REGEX = re.compile(
    '^(?:projectpage!)?(?P<namespace>' + EXTENDED_URL_REGEX + ')/(?P<project>' + EXTENDED_URL_REGEX + ')/(?P<page>' + EXTENDED_URL_REGEX + ')$')


def compile(text, context={}):
    md = markdown(text, extras=MARKDOWN_EXTRAS)
    sanitized = clean(
        md, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)

    bs = BeautifulSoup(sanitized, "html5lib")
    # if we have links of the form "x" or "x/y" or "x/y/z", then we link to:
    # page: x
    # project: x/y
    # page-in-project: x/y:z
    for link in bs.find_all('a'):
        href = link.get('href', '')
        if href == '':
            continue
        rem = PAGE_REGEX.match(href)
        prem = PROJECT_REGEX.match(href)
        nem = NAMESPACE_REGEX.match(href)
        oprem = OTHER_PROJECT_PAGE_REGEX.match(href)
        if rem:
            ctx = dict(context)
            ctx.update(rem.groupdict())
            if ctx['page'] == 'home':
                ctx = {
                    x: y for x, y in ctx.items() if x in ('namespace', 'project')
                }
                link['href'] = reverse('projects-detail', kwargs=ctx)
            else:
                ctx = {
                    x: y for x, y in ctx.items() if x in ('namespace', 'project', 'page')
                }
                link['href'] = reverse('projects-pages-detail', kwargs=ctx)
        elif prem:
            ctx = dict(context)
            ctx.update(prem.groupdict())
            ctx = {
                x: y for x, y in ctx.items() if x in ('namespace', 'project')
            }
            link['href'] = reverse('projects-detail', kwargs=ctx)
        elif nem:
            ctx = dict(context)
            ctx.update(nem.groupdict())
            ctx = {
                x: y for x, y in ctx.items() if x in ('namespace',)
            }
            link['href'] = reverse('core-namespace', kwargs=ctx)
        elif oprem:
            ctx = dict(context)
            ctx.update(oprem.groupdict())
            if ctx['page'] == 'home':
                ctx = {
                    x: y for x, y in ctx.items() if x in ('namespace', 'project')
                }
                link['href'] = reverse('projects-detail', kwargs=ctx)
            else:
                ctx = {
                    x: y for x, y in ctx.items() if x in ('namespace', 'project', 'page')
                }
                link['href'] = reverse('projects-pages-detail', kwargs=ctx)

    return str(bs)

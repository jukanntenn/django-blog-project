import re

import markdown
from bs4 import BeautifulSoup
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def generate_rich_content(value, *, toc_depth=2, toc_url=''):
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.admonition',
        'markdown.extensions.nl2br',
        TocExtension(slugify=slugify, toc_depth=toc_depth),
        'pymdownx.magiclink',
        'pymdownx.tasklist',
        'pymdownx.tilde',
        'pymdownx.caret',
    ])
    content = md.convert(value)
    toc = md.toc

    soup = BeautifulSoup(toc, 'html.parser')
    # must use contents, not children
    # if soup.ul.contents:
    toc = ''.join(map(str, soup.ul.contents)).strip()

    if toc_url:
        def absolutify(matchobj):
            return 'href="{toc_url}{frag}"'.format(toc_url=toc_url, frag=matchobj.group(1))

        toc = re.sub('href="(.+)"', absolutify, toc)
    return {
        'content': content,
        'toc': toc
    }

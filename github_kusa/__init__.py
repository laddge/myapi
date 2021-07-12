from urllib import request
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import os
import re


def main(user=''):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__), encoding='utf8'))
    try:
        res = request.urlopen('https://github.com/' + user)
    except Exception:
        return env.get_template('template.html').render(content='')
    soup = BeautifulSoup(res, 'html.parser')
    res.close()
    head = str(soup.select_one('head'))
    if not head:
        head = ''
    graph = str(soup.select_one('.js-calendar-graph'))
    if not graph:
        graph = ''
    content = head + graph
    content = content.replace('head>', 'contentHead>')
    content = re.sub('^.*og:.*\n', '', content, flags=re.MULTILINE)
    content = re.sub('^.*twitter:.*\n', '', content, flags=re.MULTILINE)
    return env.get_template('template.html').render(content=content)


if __name__ == '__main__':
    print(main('laddge'))

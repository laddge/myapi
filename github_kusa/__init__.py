from urllib import request
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import os


def main(user=''):
    res = request.urlopen('https://github.com/' + user)
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
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__), encoding='utf8'))
    return env.get_template('template.html').render(content=content)


if __name__ == '__main__':
    print(main('laddge'))

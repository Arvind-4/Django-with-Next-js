import argparse
import glob
import os
from fnmatch import fnmatch
from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--dir',
        type=str,
        required=True)
    args = parser.parse_args()
    return args
def search_and_parse(soup, tag):
    for x in soup.find_all(tag):
        if x.get('src') and x['src'].startswith('/_next/'):
            x['src'] = "{% static \"" + x['src'] + "\" %}"
        if x.get('href') and x['href'].startswith('/_next/'):
            x['href'] = "{% static \"" + x['href'] + "\" %}"

def main():
    args = parse_args()
    root = args.dir
    pattern = "*.html"
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                html_file = os.path.join(path, name)
                soup = BeautifulSoup(open(html_file), 'html.parser')
                soup.insert(0, '{% load static %}')
                is_authenticated = "window.is_authenticated = '{{request.user.is_authenticated}}'"
                django_script = BeautifulSoup(f'<script>{is_authenticated}</script>;', 'html.parser')
                head = soup.find('head')
                head.append(django_script)
                search_and_parse(soup, 'link')
                search_and_parse(soup, 'script')
                fout = open(html_file, 'wb')
                fout.write(soup.encode('utf-8'))
                fout.close()
main()
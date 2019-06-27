from flask import Flask, request, jsonify
from urllib import urlopen
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route("/")
def root():
    return "ok"

@app.route("/news_google_com")
def news_google_com():
  news = []
  soup = BeautifulSoup(urlopen('https://news.google.com'), 'html.parser')
  for article in soup.find_all('article'):
    header = article.find('h3')
    if (header):
      news.append(header.get_text())
    for childHeader in article.find_all('h4'):
      news.append(childHeader.get_text())
  return jsonify(
    items=news
  )

@app.route("/wikipedia_com")
def wikipedia_com():
  content = {}
  url = 'https://en.wikipedia.org/wiki/' + request.args.get('q')
  soup = BeautifulSoup(urlopen(url), 'html.parser')
  content['title'] = soup.find(id='firstHeading').get_text()
  content['items'] = []
  mwContentText = soup.find(id='mw-content-text').find('div')
  for child in mwContentText:
    text = None
    if child.name == 'h2':
      text = child.get_text()
    if child.name == 'p':
      text = child.get_text()
    if text:
      content['items'].append(re.sub(r'[^\x00-\x7f]',r'', text).strip())
  return jsonify(content)

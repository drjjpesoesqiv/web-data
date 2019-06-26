from flask import Flask
from flask import jsonify

from urllib import urlopen
from bs4 import BeautifulSoup

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

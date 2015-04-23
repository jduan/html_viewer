from collections import defaultdict
from HTMLParser import HTMLParser
import operator

from flask import Flask
from flask import render_template
from flask import request
import requests

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/fetch_url')
def fetch_url():
  request_url = request.args.get('url')
  response = requests.get(request_url)
  content = response.content.decode('utf-8')
  parser = MyHTMLParser()
  parser.feed(content)
  sorted_tags = sorted(parser.tags.items(), key=operator.itemgetter(1),
                       reverse=True)
  return render_template('viewer.html',
                         content=content,
                         sorted_tags=sorted_tags)


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
  def __init__(self):
    self._tags = defaultdict(int)
    HTMLParser.__init__(self)

  def handle_starttag(self, tag, attrs):
    self._tags[tag] += 1

  @property
  def tags(self):
    return self._tags


if __name__ == '__main__':
  app.run(debug=True)

from flask import Flask, request
from flask.templating import render_template
from script_scrapper2 import crawler, crawl_links
from nltk import sent_tokenize
import nltk

app = Flask(__name__)
nltk.download('punkt')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        link = request.form['link']
        if link == 'link':
            link = request.form['choose']
        pa_out, en_out = crawler(link)
        en_out = sent_tokenize(en_out)
        web_links = crawl_links(link)
        return render_template('input.html', link='link', web_links=web_links, pa_out=pa_out, en_out=en_out)
    return render_template('input.html', link='none', pa_out='', en_out='', web_links=['none'])

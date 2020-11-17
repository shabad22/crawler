from flask import Flask, request
from flask.templating import render_template
from script_scrapper2 import crawler, crawl_links
from nltk import sent_tokenize
import nltk
import numpy
from langdetect import detect

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
        en_out, pa_out = clean_en_pa(en_out, pa_out.split('\n'))
        web_links = crawl_links(link)
        # return render_template('input.html', link='link', web_links=web_links, pa_out=pa_out.split('\n'), en_out=en_out)
        return render_template('input.html', link='link', web_links=web_links, pa_out=pa_out, en_out=en_out)
    return render_template('input.html', link='none', pa_out='', en_out='', web_links=['none'])


def clean_en_pa(en_data, pa_data):
    en_data = numpy.array(en_data)
    pa_data = numpy.array(pa_data)
    temp_en_data = []
    temp_pa_data = []
    for i in en_data:
        temp_count = []
        for j in i.split():
            try:
                if detect(j) == 'pa':
                    temp_count.append('pa')
                else:
                    temp_count.append('en')
            except:
                pass
        if temp_count.count('pa') < 1:
            temp_en_data.append(i)
    for i in pa_data:
        temp_count = []
        for j in i.split():
            try:
                if detect(j) == 'pa':
                    temp_count.append('pa')
                else:
                    temp_count.append('en')
            except:
                print(j)
        if temp_count.count('en') < 1:
            temp_pa_data.append(i)

    return temp_en_data, temp_pa_data

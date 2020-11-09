from flask import Flask, request
from flask.templating import render_template
from script_scrapper2 import crawler
from nltk import sent_tokenize

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        link = request.form['link']
        print(link)
        pa_out, en_out = crawler(link)
        en_out = sent_tokenize(en_out)
        return render_template('input.html', pa_out=pa_out, en_out=en_out)
    return render_template('input.html', pa_out='', en_out='')


app.run(debug=True)

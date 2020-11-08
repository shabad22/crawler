# import packages
from bs4 import BeautifulSoup
from dotenv import find_dotenv, load_dotenv
import requests
import os
from cleaner import tokenizer
from langdetect import detect

# finding provided user defined environment as .env file and load it
load_dotenv(find_dotenv())
Encd = os.environ['ENCODING_TYPE']
Text_Area = os.environ['CONTENT_TAG']


def crawler(link, user_choice='n'):
    pa_out = ''
    en_out = ''
    # sending get request to link
    data = requests.get(link)
    # Getting content and parse html data
    soup = BeautifulSoup(data.content, 'html.parser')
    data_list = []
    # user_choice = input(f'Want to explore all links in link {link}?("y/n") : ')
    if user_choice == 'y':
        data_links = [link for link in soup.find_all('a', href=True)]
        data_links.append(link)
        i = 0
        for link in data_links:
            try:
                data = requests.get(link['href'])
                soup = BeautifulSoup(data.content, 'html.parser')
                tags = [tag.name for tag in soup.find_all()]
                print('Crawling ', link['href'])
                tags = list(set(tags))
                i += 1
                if i == 15:
                    break
                for tag in tags:
                    for info in soup.find_all(tag):
                        text_data = info.text
                        data_list.append(text_data)

            except:
                print(f'Unable to connect with ', link['href'])
                continue
    else:
        data = requests.get(link)
        soup = BeautifulSoup(data.content, 'html.parser')
        tags = [tag.name for tag in soup.find_all()]
        for tag in tags:
            for inf in soup.find_all('p'):
                text_data = inf.text
                data_list.append(text_data)
    str_data = tokenizer(' '.join([i for i in data_list]))
    data_list = list(set(str_data.split('\n')))
    for line in data_list:
        try:
            if detect(line) == 'pa':
                pa_out = pa_out+line+'\n'
            if detect(line) == 'en':
                en_out = en_out+line+'\n'
        except:
            print(line)
    return pa_out, en_out
    # if detect(line) == 'pa':
    #     pa_out.write(line+'\n')
    # else:
    #     en_out.write(line+'\n')
    # pa_out.write('\n'.join([i for i in data_list]))


if __name__ == "__main__":
    link = 'http://www.punjabiuniversity.ac.in/Pages/Page.aspx?dsenc=AboutUnv'
    crawler(link)

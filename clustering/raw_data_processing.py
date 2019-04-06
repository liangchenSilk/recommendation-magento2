# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 18:14:53 2019

@author: Silk
"""

import csv
import re
import unicodedata
from bs4 import BeautifulSoup

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
#from nltk.stem.snowball import SnowballStemmer
#from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer

stop = stopwords.words('english')
sno = nltk.stem.SnowballStemmer('english')

def clean_html(sentence):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', sentence)
    return cleantext

def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text

def clean_punc(word):
    cleaned = re.sub(r'[?|!|\'|#]', r'', word)
    cleaned = re.sub(r'[.|,|)|(|\|/]', r' ', cleaned)
    return cleaned

def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


data = {}

with open ('test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    lineNo = 0
    for line in csv_reader:
        if lineNo == 0:
            lineNo += 1
            print("start reading data...")
        else:
            print("read line" + str(lineNo))
            lineNo += 1
            sku = line[0]
            text = []
            for i in range(1, len(line)):
                sentence = clean_html(line[i])
                for word in sentence.split():
                    for clean_word in clean_punc(word).split():
                        if(clean_word not in stop and len(clean_word) > 2):
                            tmp = (sno.stem(clean_word.lower())).encode('utf8')
                            text.append(tmp)
            data[sku] = b' '.join(text)
            print(data[sku])
                




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
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

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

with open ('raw_data.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    lineNo = 0
    for line in csv_reader:
        if lineNo == 0:
            lineNo += 1
            print("start reading data...")
        else:
            #print("read line" + str(lineNo))
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
            if sku not in data:
                data[sku] = b' '.join(text)
            else:
                data[sku] = data[sku] + (b' '.join(text))



#vectorization
corpus = []
mapping = []

for sku in data:
    #print(sku)
    #print(data[sku])
    #print("================")
    corpus.append(str(data[sku]))
    mapping.append(sku)

vectorizer = TfidfVectorizer()
vector = vectorizer.fit_transform(corpus)
print(vector.shape)
#print(vectorizer.get_feature_names())

kmeans = KMeans(n_clusters = 100, random_state = 0).fit(vector)
labels = kmeans.labels_
for i in range(0,len(labels)):
    if labels[i] == 30:
        print(mapping[i])
        print(str(labels[i]))
    

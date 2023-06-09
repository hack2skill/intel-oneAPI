from flask import Flask, render_template, redirect
from flask_ngrok import run_with_ngrok
import pandas as pd
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
import re

from daal4py.sklearn import patch_sklearn
patch_sklearn()

from daal4py import daalinit

daalinit()

df = pd.read_csv('prog_book.csv')
nltk.download('stopwords')
stop = stopwords.words('english')

stop = set(stop)
from string import punctuation

def clean_text(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('','', punctuation))
    text = " ".join([word for word in str(text).split() if word not in stop])
    text = re.sub(r'\d+', '', text)
    return text

df['clean_Book_title']=df['title'].apply(clean_text)
df['clean_Description']=df['description'].apply(clean_text)

vectorizer = TfidfVectorizer(analyzer='word', lowercase=False)
title_vectors = vectorizer.fit_transform(df['clean_Book_title']).toarray()

desc_vectorizer = TfidfVectorizer(analyzer='word', lowercase=False)
desc_vectors = desc_vectorizer.fit_transform(df['clean_Description']).toarray()

def get_recommendations(value_of_element, feature_locate, df, vectors_array, feature_show):
    index_of_element = df[df[feature_locate]==value_of_element].index.values[0]
    show_value_of_element = df.iloc[index_of_element][feature_show]
    df_without = df.drop(index_of_element).reset_index().drop(['index'], axis=1)
    vectors_array = list(vectors_array)
    target = vectors_array.pop(index_of_element).reshape(1,-1)
    vectors_array = np.array(vectors_array)
    most_similar_sklearn = cosine_similarity(target, vectors_array)[0]
    idx = (-most_similar_sklearn).argsort()
    all_values = df_without[[feature_show]]
    for index in idx:
      simular = all_values.values[idx]
    recommendations_df = {"original": show_value_of_element,"rec_1": simular[0][0],"rec_2": simular[1][0],"rec_3": simular[2][0],"rec_4": simular[3][0]}
    return recommendations_df

def nestedRecDict(title):
    titleDict = get_recommendations(title, 'title', df, desc_vectors, 'title')
    authorDict = get_recommendations(title, 'title', df, desc_vectors, 'authors')
    genreDict = get_recommendations(title, 'title', df, desc_vectors, 'categories')
    picURLDict = get_recommendations(title, 'title', df, desc_vectors, 'thumbnail')
    descDict = get_recommendations(title, 'title', df, desc_vectors, 'description')
    ratingDict = get_recommendations(title, 'title', df, desc_vectors, 'average_rating')
    titleDict.update({"original": [titleDict["original"], authorDict["original"], genreDict["original"], picURLDict["original"], descDict["original"], ratingDict["original"]]})
    titleDict.update({"rec_1": [titleDict["rec_1"], authorDict["rec_1"], genreDict["rec_1"], picURLDict["rec_1"], descDict["rec_1"], ratingDict["rec_1"]]})
    titleDict.update({"rec_2": [titleDict["rec_2"], authorDict["rec_2"], genreDict["rec_2"], picURLDict["rec_2"], descDict["rec_2"], ratingDict["rec_2"]]})
    titleDict.update({"rec_3": [titleDict["rec_3"], authorDict["rec_3"], genreDict["rec_3"], picURLDict["rec_3"], descDict["rec_3"], ratingDict["rec_3"]]})
    titleDict.update({"rec_4": [titleDict["rec_4"], authorDict["rec_4"], genreDict["rec_4"], picURLDict["rec_4"], descDict["rec_4"], ratingDict["rec_4"]]})
    return titleDict

app = Flask(__name__)
run_with_ngrok(app)

df = pd.read_csv('prog_book.csv')
d = df.to_dict('records')
i=0
new_list=[]
while i<len(d):
    new_list.append(d[i:i+84])
    i+=84

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/library')
def library():
    return render_template('library.html', listofdicts = new_list)

@app.route('/loadrecs/<title>')
def loading_model(title):
    return render_template ("loading.html", title=title)

@app.route('/rec/<title>')
def rec(title):
    recs = nestedRecDict(title)
    print(recs['original'])
    return render_template('rec.html', recDict = recs)

if __name__ == '__main__':
    app.run()
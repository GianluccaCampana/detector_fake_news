
import pandas as pd
import numpy as np
import re #expressão regular
import pickle
from setuptools import find_packages
#importe para retirar a acentuação das palavras
# usar antes pip install unidecode
import unidecode 
#import para tratamento de dados
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


#download stopwords
nltk.download("stopwords")


stopwords = set(stopwords.words('portuguese'))


# Load model and vectorizer
regressaoLogistica = pickle.load(open('./pkl/regressaoLog.pkl', 'rb'))
svm = pickle.load(open('./pkl/SVM.pkl', 'rb'))
mlp =  pickle.load(open('./pkl/MLP.pkl', 'rb'))
tfidfvect = pickle.load(open('./pkl/tfidfvect.pkl', 'rb'))


ps = PorterStemmer()


#preprpocessamento e predição do texto

def predicaoRegressãoLogistica(text):
    portugues = nltk.corpus.stopwords.words('portuguese')
    preprocessando = unidecode.unidecode(text) # retirando potuações
    preprocessando = re.sub('[^a-zA-Z]', ' ', preprocessando) # Se tiver algo diferente de palavras, ele ira preencher com espaco em branco
    preprocessando = preprocessando.lower() # deixando tudo em minúcuslo
    preprocessando = preprocessando.split() # Separa a frase em uma lista de sentencas. 
    preprocessando = [ps.stem(word) for word in preprocessando if not word in portugues ] # Aplica o porter stemmer nessas palavras
    preprocessando = [item for item in preprocessando if item not in portugues]
    preprocessando = ' '.join(preprocessando) # deixando novamente em frases
    preprocessando_vect = tfidfvect.transform([preprocessando]).toarray()
    predicao = 'FAKE' if regressaoLogistica.predict(preprocessando_vect) == 'fake' else 'TRUE' 
    return predicao  

def predicaoSVM(text):
    portugues = nltk.corpus.stopwords.words('portuguese')
    preprocessando = unidecode.unidecode(text) # retirando potuações
    preprocessando = re.sub('[^a-zA-Z]', ' ', preprocessando) # Se tiver algo diferente de palavras, ele ira preencher com espaco em branco
    preprocessando = preprocessando.lower() # deixando tudo em minúcuslo
    preprocessando = preprocessando.split() # Separa a frase em uma lista de sentencas. 
    preprocessando = [ps.stem(word) for word in preprocessando if not word in portugues ] # retirando stopwords
    preprocessando = [item for item in preprocessando if item not in portugues]
    preprocessando = ' '.join(preprocessando) # deixando novamente em frases
    preprocessando_vect = tfidfvect.transform([preprocessando]).toarray()
    predicao = 'FAKE' if svm.predict(preprocessando_vect) == 'fake' else 'TRUE' 
    return predicao  

def predicaoMLP(text):
    portugues = nltk.corpus.stopwords.words('portuguese')
    preprocessando = unidecode.unidecode(text) # retirando potuações
    preprocessando = re.sub('[^a-zA-Z]', ' ', preprocessando) # Se tiver algo diferente de palavras, ele ira preencher com espaco em branco
    preprocessando = preprocessando.lower() # deixando tudo em minúcuslo
    preprocessando = preprocessando.split() # Separa a frase em uma lista de sentencas. 
    preprocessando = [ps.stem(word) for word in preprocessando if not word in portugues ] # retirando stopwords
    preprocessando = [item for item in preprocessando if item not in portugues]
    preprocessando = ' '.join(preprocessando) # deixando novamente em frases
    preprocessando_vect = tfidfvect.transform([preprocessando]).toarray()
    predicao = 'FAKE' if mlp.predict(preprocessando_vect) == 'fake' else 'TRUE' 
    return predicao  


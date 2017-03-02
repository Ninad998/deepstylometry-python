#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline 
import pandas as pd
import numpy as np
np.random.seed(123)

databaseConnectionServer = 'srn02.cs.cityu.edu.hk'
documentTable = 'document'

def loadAuthData(authorList, doc_id, chunk_size = 1000, samples = 300):
    texts = []  # list of text samples
    labels_index = {}  # dictionary mapping label name to numeric id
    labels = []  # list of label ids
    import DatabaseQuery
    from sshtunnel import SSHTunnelForwarder
    PORT=5432
    with SSHTunnelForwarder((databaseConnectionServer, 22),
                            ssh_username='stylometry',
                            ssh_password='stylometry',
                            remote_bind_address=('localhost', 5432),
                            local_bind_address=('localhost', 5400)):
        textToUse = DatabaseQuery.getWordAuthData(5400, authorList, doc_id,
                                                  documentTable = documentTable, chunk_size = chunk_size)
    labels = []
    texts = []
    size = []
    authorList = textToUse.author_id.unique()
    for auth in authorList:
        current = textToUse.loc[textToUse['author_id'] == auth]
        size.append(current.shape[0])
        print("Author: %5s  Size: %5s" % (auth, current.shape[0]))
    print("Min: %s" % (min(size)))
    print("Max: %s" % (max(size)))

    authorList = authorList.tolist()

    for auth in authorList:
        current = textToUse.loc[textToUse['author_id'] == auth]
        if (samples > min(size)):
            samples = min(size)
        current = current.sample(n = samples)
        textlist = current.doc_content.tolist()
        texts = texts + textlist
        labels = labels + [authorList.index(author_id) for author_id in current.author_id.tolist()]
    labels_index = {}
    labels_index[0] = 0
    for i, auth in enumerate(authorList):
        labels_index[i] = auth

    del textToUse

    print('Authors %s.' % (str(authorList)))
    print('Found %s texts.' % len(texts))
    print('Found %s labels.' % len(labels))

    return (texts, labels, labels_index, samples)

def loadDocData(authorList, doc_id, chunk_size = 1000):
    texts = []  # list of text samples
    labels = []  # list of label ids
    import DatabaseQuery
    from sshtunnel import SSHTunnelForwarder
    PORT=5432
    with SSHTunnelForwarder((databaseConnectionServer, 22),
                            ssh_username='stylometry',
                            ssh_password='stylometry',
                            remote_bind_address=('localhost', 5432),
                            local_bind_address=('localhost', 5400)):
        textToUse = DatabaseQuery.getWordDocData(5400, doc_id, documentTable = documentTable,
                                                 chunk_size = chunk_size)
    labels = []
    texts = []
    for index, row in textToUse.iterrows():
        labels.append(authorList.index(row.author_id))
        texts.append(row.doc_content)

    del textToUse

    print('Found %s texts.' % len(texts))
    return (texts, labels)

def preProcessTrainVal(texts, labels, chunk_size = 1000, VALIDATION_SPLIT = 0.2):

    # split the data into a training set and a validation set
    from sklearn.model_selection import train_test_split
    trainX, valX, trainY, valY = train_test_split(texts, labels, test_size=VALIDATION_SPLIT)

    del texts, labels

    return (trainX, trainY, valX, valY)

def compileModel(algo):
    
    ct_multi_nb = Pipeline([
        ("tfidf_vectorizer", CountVectorizer(ngram_range = (1, 4), stop_words = None, lowercase = False,
                                             max_features = 40000)), 
        ("linear svc", MultinomialNB())
    ])


    tfidf_multi_nb = Pipeline([
        ("tfidf_vectorizer", TfidfVectorizer(ngram_range = (1, 4), stop_words = None, lowercase = False,
                                             max_features = 40000, use_idf = True, smooth_idf = True,
                                             sublinear_tf = True)), 
        ("linear svc", MultinomialNB())
    ])


    ct_svc = Pipeline([
        ("tfidf_vectorizer", CountVectorizer(ngram_range = (1, 4), stop_words = None, lowercase = False,
                                             max_features = 40000)), 
        ("linear svc", SVC(kernel="linear"))
    ])

    tfidf_svc = Pipeline([
        ("tfidf_vectorizer", TfidfVectorizer(ngram_range = (1, 4), stop_words = None, lowercase = False,
                                             max_features = 40000, use_idf = True, smooth_idf = True,
                                             sublinear_tf = True)), 
        ("linear svc", SVC(kernel="linear"))
    ])

    if algo == 'ct_multi_nb':
        return ct_multi_nb

    elif algo == 'tfidf_multi_nb':
        return tfidf_multi_nb
    
    elif algo == 'ct_svc':
        return ct_svc
    
    elif algo == 'tfidf_svc':
        return tfidf_svc
    
    else:
        print("Model not found")
        return None

def fitModel(model, trainX, trainY, valX, valY):
    
    model.fit(trainX, trainY)
    
    train_acc = model.score(trainX, trainY)
    
    val_acc = model.score(valX, valY)
    
    print("\n\nFinal Train Accuracy: %.2f" % (train_acc * 100))
    
    print("\nFinal Test Accuracy: %.2f" % (val_acc * 100))

    return (model, train_acc, val_acc)

def predictModel(model, testX):
    # Function to take input of data and return prediction model
    predY = np.array(model.predict(testX))
    predYList = predY[:]
    entro = []
    flag = False
    import math
    for row in predY:
        entroval = 0
        for i in row:
            if(i <= 0):
                flag = True
                pass
            else:
                entroval += (i * (math.log(i , 2)))
        entroval = -1 * entroval
        entro.append(entroval)
    if(flag == False):
        yx = zip(entro, predY)
        yx = sorted(yx, key = lambda t: t[0])
        newPredY = [x for y, x in yx]
        predYEntroList = newPredY[:int(len(newPredY)*0.5)]
        predY = np.mean(predYEntroList, axis=0)
    else:
        predY = np.mean(predYList, axis=0)
    return (predYList, predY)

#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(authorList = None, doc_id = None, chunk_size = 1000):
    if (authorList is None) or (doc_id is None) or (doc_id == 0):
        return None
    else:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.svm import SVC
        from sklearn.pipeline import Pipeline 
        import pandas as pd
        import numpy as np
        np.random.seed(123)
        
        svc_tfidf = Pipeline([
            ("tfidf_vectorizer", TfidfVectorizer(analyzer=lambda x: x)), 
            ("linear svc", SVC(kernel="linear"))
        ])
        texts = []  # list of text samples
        labels_index = {}  # dictionary mapping label name to numeric id
        labels = []  # list of label ids
        import DatabaseQuery
        # textToUse = pd.read_csv("suffle_4_6000.csv", names=["author_id", "doc_content"], dtype={'author_id': int})
        from sshtunnel import SSHTunnelForwarder
        PORT=5432
        with SSHTunnelForwarder(('srn02.cs.cityu.edu.hk', 22),
                                ssh_username='stylometry',
                                ssh_password='stylometry',
                                remote_bind_address=('localhost', 5432),
                                local_bind_address=('localhost', 5400)):
            textToUse = DatabaseQuery.getWordAuthData(5400, authors = authorList, doc = doc_id,
                                                      chunk_size = chunk_size)
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
        
        # split the data into a training set and a validation set
        # from sklearn.model_selection import KFold
        # kfold = KFold(n_splits=6, shuffle=True, random_state=123)
        from sklearn.model_selection import train_test_split
        x_train, x_val, y_train, y_val = train_test_split(texts, labels, test_size=0.2)
        
        svc_tfidf.fit(x_train, y_train)

        print('Train Accuracy %s.' % (str(svc_tfidf.score(x_train, y_train))))
        print('Test Accuracy %s.' % (str(svc_tfidf.score(x_val, y_val))))
        
        texts = []  # list of text samples
        labels = []  # list of label ids
        import DatabaseQuery
        # textToUse = pd.read_csv("suffle_4_6000.csv", names=["author_id", "doc_content"], dtype={'author_id': int})
        from sshtunnel import SSHTunnelForwarder
        PORT=5432
        with SSHTunnelForwarder(('srn02.cs.cityu.edu.hk', 22),
                                ssh_username='stylometry',
                                ssh_password='stylometry',
                                remote_bind_address=('localhost', 5432),
                                local_bind_address=('localhost', 5400)):
            textToUse = DatabaseQuery.getWordDocData(5400, doc_id, chunk_size = chunk_size)
        labels = []
        texts = []
        for index, row in textToUse.iterrows():
            labels.append(authorList.index(row.author_id))
            texts.append(row.doc_content)

        print('Found %s texts.' % len(texts))

        del textToUse
        
        predYList = svc_tfidf.predict(texts)
        
        predY = []
        for i, val in enumerate(authorList):
            pred = (float)(list(predYList).count(i)) / len(predYList)
            predY.append(pred)
            
        return (labels_index, predYList, predY, samples)

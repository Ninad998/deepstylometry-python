#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(authorList = None, doc_id = None, samples = 3200, chunk_size = 1000):
    if (authorList is None) or (doc_id is None) or (doc_id == 0):
        return None
    else:
        from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.svm import SVC
        from sklearn.pipeline import Pipeline 
        import pandas as pd
        import numpy as np
        np.random.seed(123)
        
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
        
        all_models = [
            ("ct_multi_nb", ct_multi_nb),
            ("tfidf_multi_nb", tfidf_multi_nb),
            ("ct_svc", ct_svc),
            ("tfidf_svc", tfidf_svc)
        ]
        
        from sklearn.model_selection import train_test_split
        x_train, x_val, y_train, y_val = train_test_split(texts, labels, test_size=0.2)
        
        clf = {}
        
        for name, model in all_models:
            model.fit(x_train, y_train)
            train_acc = model.score(x_train, y_train)
            val_acc = model.score(x_val, y_val)
            clf[name] = [train_acc, val_acc]
            del model
            print("Completed %s" % (name))
            
        for name, vals in clf.iteritems():
            print("Classifier: %s " % (name))
            print("Train Acc: %1.4f  Test Acc: %1.4f" % (vals[0], vals[1]))
            
        return (labels_index, clf, samples)

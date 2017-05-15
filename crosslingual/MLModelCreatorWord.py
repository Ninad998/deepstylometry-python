#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from sklearn.ensemble import RandomForestClassifier 
import pandas as pd
import numpy as np
np.random.seed(123)

databaseConnectionServer = 'srn01.cs.cityu.edu.hk'
documentTable = 'document'

def loadData(documentTable, samples = 30000):
    texts = []  # list of text samples
    labels_index = {}  # dictionary mapping label name to numeric id
    labels = []  # list of label ids
    import DatabaseQuery
    from sshtunnel import SSHTunnelForwarder
    with SSHTunnelForwarder((databaseConnectionServer, 22),
                            ssh_username='stylometry',
                            ssh_password='stylometry',
                            remote_bind_address=('localhost', 5432),
                            local_bind_address=('localhost', 5400)):
        textToUse = DatabaseQuery.getDocData(5400, documentTable = documentTable)
        
    labels = []
    groups = []
    features = []
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
            
        # current = current.sample(n = samples)
        feat = current[["feature1", "feature2", "feature3", "feature4", 
                        "feature5", "feature6", "feature7", "feature8"]].values.tolist()
        features = features + feat
        author = current["author_id"].tolist()
        labels = labels + author
        doc = current["doc_id"].tolist()
        groups = groups + doc
        
    del textToUse

    print('Authors %s.' % (str(authorList)))
    print('Found %s texts.' % len(features))
    print('Found %s features.' % len(labels))
    print('Found %s groups.' % len(groups))

    return (np.array(features), np.array(labels), np.array(groups), samples)

def preProcessTrainVal(features, labels, groups, K_FOLD = 2):

    # split the data into a training set and a validation set
    from sklearn.model_selection import LeaveOneGroupOut
    logo = LeaveOneGroupOut()
    
    print(logo.get_n_splits(features, labels, groups))
    
    return logo

def compileModel():
    
    rf = RandomForestClassifier() 
    
    return rf

def recompileModel():
    
    import cPickle as pickle
    
    algoloadname = str("RandomForestClassifier" + '.pickle')
    
    with open(algoloadname, 'rb') as handle:
        model = pickle.load(handle)
    
    return model

def fitModel(model, trainX, trainY, valX, valY):
    
    model.fit(trainX, trainY)
    
    train_acc = model.score(trainX, trainY)
    
    val_acc = model.score(valX, valY)
    
    print("\n\nFinal Train Accuracy: %.2f" % (train_acc * 100))
    
    print("\nFinal Validation Accuracy: %.2f" % (val_acc * 100))
    
    return (model, train_acc, val_acc)

def predictModel(model, testX, authorList):
    # Function to take input of data and return prediction model
    predY = np.array(model.predict_proba(testX))

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

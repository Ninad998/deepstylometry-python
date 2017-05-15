#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(doc_table = "author_study_six", samples = 3200, chunk_size = 1000):
    
    import MLModelCreatorWord as md

    (features, labels, groups, samples) = md.loadData(doc_table)

    logo = md.preProcessTrainVal(features, labels, groups)

    model = md.compileModel()

    for train_index, test_index in logo.split(features, labels, groups):
        print("TRAIN:", train_index, "TEST:", test_index)
        trainX, valX = X[train_index], X[test_index]
        trainY, valY = y[train_index], y[test_index]
        (model, train_acc, val_acc) = md.fitModel(model, algo, trainX, trainY, valX, valY)

    del model

    return (labels_index, train_acc, val_acc, samples)

def getTestResults(algo, authorList = None, doc_id = None, labels_index = None, samples = 3200, chunk_size = 1000):
    if (authorList is None) or (doc_id is None) or (doc_id == 0):
        return None
    else:
        import MLModelCreatorWord as md
        
        print("Algo: %s" % (str(algo)))
    
        (testX, testY) = md.loadDocData(authorList, doc_id, chunk_size = chunk_size)
        
        import numpy as np
        testY = np.mean(testY, axis=0, dtype=int)
            
        model = md.recompileModel(algo)
        
        (predYList, predY) = md.predictModel(model, testX, authorList)
        
        del model

        return (predYList, predY, testY)

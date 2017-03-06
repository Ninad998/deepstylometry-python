#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(algo, samples = 3200, chunk_size = 1000):
    global model
    if (algo is None):
        return None
    else:
        import MLModelCreatorGender as md
        
        print("Algo: %s" % (str(algo)))
    
        (texts, labels, labels_index, samples) = md.loadGenderData(chunk_size = chunk_size)
        
        (trainX, trainY, valX, valY) = md.preProcessTrainVal(texts, labels, chunk_size = chunk_size)
            
        model = md.compileModel(algo)
        
        (model, train_acc, val_acc) = md.fitModel(model, trainX, trainY, valX, valY)
        
        return (labels_index, train_acc, val_acc, samples)

def getTestResults(doc_id = 0, chunk_size = 1000):
    if (authorList is None) or (doc_id is None) or (doc_id == 0):
        return None
    else:
        import MLModelCreatorGender as md
        
        print("Algo: %s" % (str(algo)))
        
        labels_index = {
            0: 'M',
            1: 'F'
        }
        
        genderList = ['M', 'F']
        
        (testX, testY) = md.loadDocData(doc_id, genderList, chunk_size = chunk_size)
        
        import numpy as np
        testY = np.mean(testY, axis=0, dtype=int)
        
        (predYList, predY) = md.predictModel(model, testX, batch_size = batch_size)
        
        return (predY, testY)
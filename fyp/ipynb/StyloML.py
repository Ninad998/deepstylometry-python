#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(algo, authorList = None, doc_id = None, samples = 3200, chunk_size = 1000):
    if (authorList is None) or (doc_id is None) or (doc_id == 0):
        return None
    else:
        import MLModelCreatorWord as md
        
        print("Algo: %s" % (str(algo)))
    
        (texts, labels, labels_index, samples) = md.loadAuthData(authorList, doc_id, 
                                                                 chunk_size = chunk_size, samples = samples)
        
        (trainX, trainY, valX, valY) = md.preProcessTrainVal(texts, labels, chunk_size = chunk_size)
            
        model = md.compileModel(algo)
        
        (model, train_acc, val_acc) = md.fitModel(model, algo, trainX, trainY, valX, valY)
        
        del model

        return (labels_index, train_acc, val_acc, samples)

def getTestResults(algo, authorList = None, doc_id = None, labels_index = None, samples = 3200, chunk_size = 1000):
    if (authorList is None) or (doc_id is None) or (doc_id == 0):
        return None
    else:
        import MLModelCreatorWord as md
        
        print("Algo: %s" % (str(algo)))
    
        (testX, textY) = md.loadDocData(authorList, doc_id, chunk_size = chunk_size)\
            
        model = md.recompileModel(algo)
        
        (predY) = md.predictModel(model, testX, authorList)
        
        del model

        return (labels_index, textY, predY, samples)

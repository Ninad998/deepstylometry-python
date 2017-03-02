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
        
        (model, train_acc, val_acc) = md.fitModel(model, trainX, trainY, valX, valY)
        
        # (testX, textY) = md.loadDocData(authorList, doc_id, chunk_size = chunk_size)
        # 
        # (testX, textY) = md.preProcessTest(testX, labels_index, textY, chunk_size = chunk_size)
        # 
        # textY = np.mean(textY, axis=0)
        # (predYList, predY) = md.predictModel(model, testX, batch_size = batch_size)
        
        del model
        
        # return (labels_index, predYList, predY, history, samples)

        return (labels_index, train_acc, val_acc, samples)

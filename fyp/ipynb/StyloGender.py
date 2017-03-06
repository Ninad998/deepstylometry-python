#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(glove = '../glove/', dimensions = 200, dropout = 0.5, chunk_size = 1000, batch_size = 10, nb_epoch = 30):
    
    import ANNModelCreatorWordGender as md
    
    embedfile = 'glove.6B.' + str(dimensions) + 'd.txt'

    embeddings_index = md.readVectorData(embedfile, GLOVE_DIR=glove)

    (texts, labels, labels_index, samples) = md.loadGenderData(chunk_size = chunk_size)

    (trainX, trainY, valX, valY) = md.preProcessTrainVal(texts, labels, chunk_size = chunk_size)

    embedding_matrix = None
    
    embedding_matrix = md.prepareEmbeddingMatrix(embeddings_index, EMBEDDING_DIM = dimensions)

    model = md.compileModel(len(labels_index), embedding_matrix, chunk_size = chunk_size,
                            DROP_OUT = dropout, EMBEDDING_DIM = dimensions)

    (model, history, train_acc, val_acc) = md.fitModel(model, trainX, trainY, valX, valY, 
                                                       nb_epoch = nb_epoch, batch_size = batch_size)

    # (testX, testY) = md.loadDocData(doc_id, chunk_size = chunk_size)
    
    # (testX, testY) = md.preProcessTest(testX, labels_index, testY, chunk_size = chunk_size)
    # 
    # textY = np.mean(textY, axis=0)
    # (predYList, predY) = md.predictModel(model, testX, batch_size = batch_size)

    del model
    
    # return (labels_index, history, train_acc, val_acc, predYList, predY, samples)
    
    return (labels_index, history, train_acc, val_acc, samples)

def getTestResults(doc_id = 0, glove = '../glove/', dimensions = 200, dropout = 0.5, chunk_size = 1000, batch_size = 10):
    
    import ANNModelCreatorWordGender as md
    
    embedfile = 'glove.6B.' + str(dimensions) + 'd.txt'

    embeddings_index = md.readVectorData(embedfile, GLOVE_DIR=glove)
    
    md.makeTokenizer()
    
    labels_index = {
        0: 'M',
        1: 'F'
    }
    
    genderList = ['M', 'F']

    (testX, testY) = md.loadDocData(doc_id, genderList, chunk_size = chunk_size)
    
    (testX, testY) = md.preProcessTest(testX, labels_index, testY, chunk_size = chunk_size)

    embedding_matrix = None
    
    embedding_matrix = md.prepareEmbeddingMatrix(embeddings_index, EMBEDDING_DIM = dimensions)

    model = md.recompileModel(len(labels_index), embedding_matrix, chunk_size = chunk_size,
                              DROP_OUT = dropout, EMBEDDING_DIM = dimensions)
    
    import numpy as np
    testY = np.mean(testY, axis=0)
    
    (predYList, predY) = md.predictModel(model, testX, batch_size = batch_size)

    del model
    
    # return (labels_index, history, train_acc, val_acc, predYList, predY, samples)
    
    return (predY, testY)
        
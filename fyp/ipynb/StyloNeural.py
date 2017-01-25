#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(authorList = None, doc_id = None, chunk_size = 1000, nb_epoch = 30, level = 'word', 
               glove = '../glove/', samples = 300):
    if (authorList is None) or (doc_id is None) or (doc_id == 0):
        return None
    else:
        if level == 'char':
            import ModelCreatorChar as md
        else:
            import ModelCreatorWord as md
        embedfile = 'glove.6B.100d.txt'
        embed = 100
        embeddings_index = md.readVectorData(embedfile, GLOVE_DIR=glove)
        (texts, labels, labels_index) = md.loadAuthData(authorList, doc_id, chunk_size = chunk_size, samples = samples)
        (trainX, trainY, valX, valY) = md.preProcessTrainVal(texts, labels, chunk_size = chunk_size)
        embedding_matrix = None
        if level != 'char':
            embedding_matrix = md.prepareEmbeddingMatrix(embeddings_index, EMBEDDING_DIM = embed)
        model = md.compileModel(len(labels_index), embedding_matrix, chunk_size = chunk_size, EMBEDDING_DIM = embed)
        (model, history) = md.fitModel(model, trainX, trainY, valX, valY, nb_epoch = nb_epoch)
        (testX, textY) = md.loadDocData(authorList, doc_id, chunk_size = chunk_size)
        (testX, textY) = md.preProcessTest(testX, labels_index, textY, chunk_size = chunk_size)
        # textY = np.mean(textY, axis=0)
        (predYList, predY) = md.predictModel(model, testX)
        return (labels_index, predYList, predY, history)

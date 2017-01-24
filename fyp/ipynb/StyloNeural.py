#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(authorList = None, doc_id = None, chunk_size = 1000, nb_epoch = 30):
    if (authorList is None) or (doc_id is None) or (doc_id == 0):
        return None
    else:
        import ModelCreator
        embedfile = 'glove.6B.100d.txt'
        embed = 100
        embeddings_index = ModelCreator.readVectorData(embedfile, GLOVE_DIR='../glove/')
        # embeddings_index = ModelCreator.readVectorData(embedfile, GLOVE_DIR='/var/tmp/')
        (texts, labels, labels_index) = ModelCreator.loadAuthData(authorList, doc_id, chunk_size = chunk_size)
        (trainX, trainY, valX, valY) = ModelCreator.preProcessTrainVal(texts, labels, chunk_size = chunk_size)
        embedding_matrix = ModelCreator.prepareEmbeddingMatrix(embeddings_index, EMBEDDING_DIM = embed)
        model = ModelCreator.compileModel(len(labels_index), embedding_matrix, chunk_size = chunk_size, EMBEDDING_DIM = embed)
        model = ModelCreator.fitModel(model, trainX, trainY, valX, valY, nb_epoch = nb_epoch)
        (testX, textY) = ModelCreator.loadDocData(authorList, doc_id, chunk_size = chunk_size)
        (testX, textY) = ModelCreator.preProcessTest(testX, labels_index, textY, chunk_size = chunk_size)
        # textY = np.mean(textY, axis=0)
        (predYList, predY) = ModelCreator.predictModel(model, testX)
        return (labels_index, predYList, predY)

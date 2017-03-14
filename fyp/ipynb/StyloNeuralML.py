#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(authorList = None, doc_id = None, algo = None, chunk_size = 1000, level = 'word',
               glove = '../glove/', samples = 300, dimensions = 200, dropout = 0.5):
    
    if (authorList is None) or (doc_id is None) or (algo is None) or (doc_id == 0):
        return None

    else:
        import CNNModelCreatorWordEdit as md

        embedfile = 'glove.6B.' + str(dimensions) + 'd.txt'

        embeddings_index = md.readVectorData(embedfile, GLOVE_DIR=glove)

        (texts, labels, labels_index, samples) = md.loadAuthData(authorList, doc_id, chunk_size = chunk_size, samples = samples)

        (trainX, trainY, valX, valY) = md.preProcessTrainVal(texts, labels, chunk_size = chunk_size)

        embedding_matrix = None

        if level == 'word':
            embedding_matrix = md.prepareEmbeddingMatrix(embeddings_index, EMBEDDING_DIM = dimensions)
            
        feature_model = md.recompileModelCNN(len(labels_index), embedding_matrix, chunk_size = chunk_size,
                                             DROP_OUT = dropout, EMBEDDING_DIM = dimensions)
        
        mlmodel = md.compileModelML(algo, new = True)
        
        (trainX, trainY, valX, valY) = md.preProcessTrainVal(texts, labels, ml = True, chunk_size = chunk_size)

        del texts, labels

        (train_acc, val_acc) = md.fitModelML(feature_model, mlmodel, algo, trainX, trainY, valX, valY)
        
        del feature_model
        
        return (labels_index, train_acc, val_acc, samples)


def getTestResults(authorList = None, doc_id = None, labels_index = None, algo = None, chunk_size = 1000, level = 'word',
               glove = '../glove/', dimensions = 200, dropout = 0.5, predYList_cnn = None):

    if (authorList is None) or (labels_index is None) or (doc_id is None) or (doc_id == 0):
        return None

    else:
        if level == 'char':
            import CNNModelCreatorChar as md
        else:
            import CNNModelCreatorWordEdit as md

        embedfile = 'glove.6B.' + str(dimensions) + 'd.txt'

        embeddings_index = md.readVectorData(embedfile, GLOVE_DIR=glove)

        md.makeTokenizer()

        (testX, testY) = md.loadDocData(authorList, doc_id, chunk_size = chunk_size)

        (testX, testY) = md.preProcessTest(testX, labels_index, testY, chunk_size = chunk_size)

        embedding_matrix = None

        embedding_matrix = md.prepareEmbeddingMatrix(embeddings_index, EMBEDDING_DIM = dimensions)

        feature_model = md.recompileModelCNN(len(labels_index), embedding_matrix, chunk_size = chunk_size,
                                             DROP_OUT = dropout, EMBEDDING_DIM = dimensions)

        mlmodel = md.compileModelML(algo, new = False)

        import numpy as np
        testY = np.mean(testY, axis=0, dtype=int)

        (predYList, predY) = md.predictModel(feature_model, mlmodel, testX, authorList)

        del feature_model
        
        newPredList = []
        
        newPredList = np.concatenate((predYList_cnn, predYList))
        
        (predList, predEntro) = entropy(newPredList, cutoff = 0.5)

        return (predYList, predY, testY, predEntro)
    
def entropy(predList, cutoff = 0.5):
    
    import numpy as np
    
    predYList = predList[:]
    entro = []
    
    flag = False
    import math
    for row in predList:
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
        yx = zip(entro, predList)
        yx = sorted(yx, key = lambda t: t[0])
        newPredY = [x for y, x in yx]
        predYEntroList = newPredY[:int(len(newPredY)*cutoff)]
        predY = np.mean(predYEntroList, axis=0)
    else:
        predY = np.mean(predYList, axis=0)
        
    return (predYList, predY)

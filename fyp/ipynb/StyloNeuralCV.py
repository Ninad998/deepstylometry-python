#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(authorList = None, doc_id = None, chunk_size = 1000, nb_epoch = 180, level = 'word',
               glove = '../glove/', samples = 3200, dimensions = 200, dropout = 0.4, batch_size = 10, 
               fold = 5):
    if (authorList is None) or (doc_id is None) or (doc_id == 0):
        return None
    
    else:
        if level == 'char':
            import CNNModelCreatorChar as md
        else:
            import CNNModelCreatorWordEditCV as md
            
        embedfile = 'glove.6B.' + str(dimensions) + 'd.txt'
        
        embeddings_index = md.readVectorData(embedfile, GLOVE_DIR=glove)
        
        (texts, labels, labels_index, samples) = md.loadAuthData(authorList, doc_id, chunk_size = chunk_size, samples = samples)
        
        (data, labels, train, test) = md.preProcessTrainVal(texts, labels, chunk_size = chunk_size)
        
        embedding_matrix = None
        
        if level == 'word':
            embedding_matrix = md.prepareEmbeddingMatrix(embeddings_index, EMBEDDING_DIM = dimensions)
        
        train_acc_list = []
        
        val_acc_list = []
        
        pos = 0
        
        for train_index, test_index in zip(train, test):
            
            if (pos > fold):
                break
            
            print("K-Fold: Fold no. %s" % (str(pos)))
            
            model = md.compileModel(len(labels_index), embedding_matrix, chunk_size = chunk_size,
                                    DROP_OUT = dropout, EMBEDDING_DIM = dimensions)
            
            (model, history, train_acc, val_acc) = md.fitModel(model, data[train_index], labels[train_index], 
                                                               data[test_index], labels[test_index], 
                                                               nb_epoch = nb_epoch, batch_size = batch_size)
            
            del model
            
            train_acc_list.append(train_acc)
            
            val_acc_list.append(val_acc)
            
            print("Values Appended")
            
            pos = pos + 1
            
            from keras import backend as K
            K.clear_session()
            
        # (testX, textY) = md.loadDocData(authorList, doc_id, chunk_size = chunk_size)
        # 
        # (testX, textY) = md.preProcessTest(testX, labels_index, textY, chunk_size = chunk_size)
        # 
        # textY = np.mean(textY, axis=0)
        # (predYList, predY) = md.predictModel(model, testX, batch_size = batch_size)
        
        # del model
        
        # return (labels_index, predYList, predY, history, samples)

        return (labels_index, train_acc_list, val_acc_list, samples)

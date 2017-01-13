#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os

import numpy as np

# np.random.seed(1337)

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.layers import Dense, Flatten
from keras.layers import Convolution1D, MaxPooling1D, Embedding
from keras.layers import Dropout
from keras.optimizers import SGD
from keras.models import Sequential
from keras.callbacks import LearningRateScheduler
from keras.regularizers import WeightRegularizer

databaseConnectionServer = 'srn01.cs.cityu.edu.hk'
documentTable = 'document'

def readVectorData(fileName, GLOVE_DIR = 'glove/'):
    embeddings_index = {}
    f = open(os.path.join(GLOVE_DIR, fileName))
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    
    print('Found %s word vectors.' % len(embeddings_index))
    return embeddings_index

def loadAuthData(authorList, doc_id, chunk_size = 1000):
    texts = []  # list of text samples
    labels_index = {}  # dictionary mapping label name to numeric id
    labels = []  # list of label ids
    import DatabaseQuery
    # textToUse = pd.read_csv("suffle_4_6000.csv", names=["author_id", "doc_content"], dtype={'author_id': int})
    from sshtunnel import SSHTunnelForwarder
    PORT=5432
    with SSHTunnelForwarder((databaseConnectionServer, 22),
                            ssh_username='stylometry',
                            ssh_password='stylometry',
                            remote_bind_address=('localhost', 5432),
                            local_bind_address=('localhost', 5400)):
        textToUse = DatabaseQuery.getAuthData(5400, authorList, doc_id, 
                                              documentTable = documentTable, chunk_size = chunk_size)
    labels = []
    texts = []
    for index, row in textToUse.iterrows():
        labels.append(authorList.index(row.author_id))
        texts.append(row.doc_content)
    labels_index = {}
    for i, auth in enumerate(authorList):
        labels_index[auth] = i
        
    print('Authors %s.' % (str(authorList)))
    print('Found %s texts.' % len(texts))
    return (texts, labels, labels_index)

def loadDocData(authorList, doc_id, chunk_size = 1000):
    texts = []  # list of text samples
    labels = []  # list of label ids
    import DatabaseQuery
    # textToUse = pd.read_csv("suffle_4_6000.csv", names=["author_id", "doc_content"], dtype={'author_id': int})
    from sshtunnel import SSHTunnelForwarder
    PORT=5432
    with SSHTunnelForwarder((databaseConnectionServer, 22),
                            ssh_username='stylometry',
                            ssh_password='stylometry',
                            remote_bind_address=('localhost', 5432),
                            local_bind_address=('localhost', 5400)):
        textToUse = DatabaseQuery.getDocData(5400, doc_id, 
                                             documentTable = documentTable, chunk_size = chunk_size)
    labels = []
    texts = []
    for index, row in textToUse.iterrows():
        labels.append(authorList.index(row.author_id))
        texts.append(row.doc_content)
        
    print('Found %s texts.' % len(texts))
    return (texts, labels)

def preProcessTrainVal(texts, labels, chunk_size = 1000, MAX_NB_WORDS = 20000, VALIDATION_SPLIT = 0.2):
    global tokenizer, word_index
    # finally, vectorize the text samples into a 2D integer tensor
    tokenizer = Tokenizer(nb_words=MAX_NB_WORDS)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)

    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

    X = pad_sequences(sequences, maxlen = chunk_size)

    y = to_categorical(np.asarray(labels))
    print('Shape of data tensor:', X.shape)
    print('Shape of label tensor:', y.shape)
    
    # split the data into a training set and a validation set
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    data = X[indices]
    labels = y[indices]
    nb_validation_samples = int(VALIDATION_SPLIT * X.shape[0])

    trainX = X[:-nb_validation_samples]
    trainY = y[:-nb_validation_samples]
    valX = X[-nb_validation_samples:]
    valY = y[-nb_validation_samples:]
    
    return (trainX, trainY, valX, valY)

def preProcessTest(texts, labels_index, labels = None, chunk_size = 1000, MAX_NB_WORDS = 20000):
    # finally, vectorize the text samples into a 2D integer tensor
    sequences = tokenizer.texts_to_sequences(texts)

    print('Found %s unique tokens.' % len(word_index))

    X = pad_sequences(sequences, maxlen = chunk_size)
    
    print('Shape of data tensor:', X.shape)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    data = X[indices]
    testX = X[:]
    
    if labels is not None:
        y = np.zeros((len(labels), len(labels_index)))
        for i, val in enumerate(labels):
            y[i][val] = 1
        print('Shape of label tensor:', y.shape)
        labels = y[indices]
        testY = y[:]
        return (testX, testY)
        
    return (testX)

def prepareEmbeddingMatrix(embeddings_index, MAX_NB_WORDS = 20000, EMBEDDING_DIM = 100):
    global nb_words, embedding_matrix
    nb_words = min(MAX_NB_WORDS, len(word_index))
    embedding_matrix = np.zeros((nb_words + 1, EMBEDDING_DIM))
    for word, i in word_index.items():
        if i > MAX_NB_WORDS:
            continue
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector
    return embedding_matrix

def compileModel(classes, embedding_matrix, EMBEDDING_DIM = 100, chunk_size = 1000, CONVOLUTION_FEATURE = 256, 
                 DENSE_FEATURE = 1024, DROP_OUT = 0.5, LEARNING_RATE=0.01, MOMENTUM=0.9):
    weightR = WeightRegularizer(l1=0.01, l2=0.01)
    
    model = Sequential()
    
    model.add(Embedding(                              # Layer 0, Start
            input_dim=nb_words + 1,                   # Size to dictionary, has to be input + 1
            output_dim=EMBEDDING_DIM,                 # Dimensions to generate
            weights=[embedding_matrix],               # Initialize word weights
            input_length=chunk_size))                 # Define length to input sequences in the first layer
    
    model.add(Convolution1D(                          # Layer 1,   Features: 256, Kernel Size: 7
            nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
            filter_length=7,                          # Size of kernels
            border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
            activation='relu'))                       # Activation function to use
    
    model.add(MaxPooling1D(                           # Layer 1a,  Max Pooling: 3
            pool_length=3))                           # Size of kernels
    
    model.add(Convolution1D(                          # Layer 2,   Features: 256, Kernel Size: 7
            nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
            filter_length=7,                          # Size of kernels
            border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
            activation='relu'))                       # Activation function to use
    
    model.add(MaxPooling1D(                           # Layer 2a,  Max Pooling: 3
            pool_length=3))                           # Size of kernels
    
    model.add(Convolution1D(                          # Layer 3,   Features: 256, Kernel Size: 3
            nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
            filter_length=3,                          # Size of kernels
            border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
            activation='relu'))                       # Activation function to use
    
    model.add(Convolution1D(                          # Layer 4,   Features: 256, Kernel Size: 3
            nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
            filter_length=3,                          # Size of kernels
            border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
            activation='relu'))                       # Activation function to use
    
    model.add(Convolution1D(                          # Layer 5,   Features: 256, Kernel Size: 3
            nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
            filter_length=3,                          # Size of kernels
            border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
            activation='relu'))                       # Activation function to use
    
    model.add(Convolution1D(                          # Layer 6,   Features: 256, Kernel Size: 3
            nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
            filter_length=3,                          # Size of kernels
            border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
            activation='relu'))                       # Activation function to use
    
    model.add(MaxPooling1D(                           # Layer 6a,  Max Pooling: 3
            pool_length=3))                           # Size of kernels
    
    model.add(Flatten())                              # Layer 7
    
    model.add(Dense(                                  # Layer 7a,  Output Size: 1024
            output_dim=DENSE_FEATURE,                 # Output dimension
            activation='relu'))                       # Activation function to use
    
    model.add(Dropout(DROP_OUT))
    
    model.add(Dense(                                  # Layer 8,   Output Size: 1024
            output_dim=DENSE_FEATURE,                 # Output dimension
            activation='relu'))                       # Activation function to use
    
    model.add(Dropout(DROP_OUT))
    
    model.add(Dense(                                  # Layer 9,  Output Size: Size Unique Labels, Final
            output_dim=classes,                       # Output dimension
            activation='softmax'))                    # Activation function to use
    
    sgd = SGD(lr=LEARNING_RATE, momentum=MOMENTUM, nesterov=True)

    # adadelta = Adadelta(lr=1.0, rho=0.95, epsilon=1e-08)

    model.compile(loss='categorical_crossentropy', optimizer=sgd,
                  metrics=['accuracy'])
    
    return model

def step_decay(epoch):
    initial_lrate = 0.01
    drop = 0.2
    epochs_drop = 5.0
    import math
    lrate = initial_lrate * math.pow(drop, math.floor((1+epoch)/epochs_drop))
    print("Learning rate: %s" % (str(lrate)))
    return lrate

def fitModel(model, trainX, trainY, valX, valY, nb_epoch=30, batch_size=100):
    # Function to take input of data and return fitted model
    callbacks = [
        # EarlyStopping(monitor='val_loss', patience=6, verbose=1, mode='auto'),
        LearningRateScheduler(step_decay)
    ]
    model.fit(trainX, trainY, validation_data=(valX, valY),
              nb_epoch=nb_epoch, batch_size=batch_size)
    #          nb_epoch=nb_epoch, batch_size=batch_size, callbacks=callbacks)
    
    return model
    
def predictModel(model, testX, batch_size=128):
    # Function to take input of data and return prediction model
    predY = np.array(model.predict(testX, batch_size=batch_size))
    predYList = predY[:]
    entro = []
    import math
    for row in predY:
        entroval = 0
        for i in row:
            entroval += (i * (math.log(i , 2)))
        entroval = -1 * entroval
        entro.append(entroval)
    yx = zip(entro, predY)
    yx = sorted(yx, key = lambda t: t[0])
    newPredY = [x for y, x in yx]
    predYEntroList = newPredY[:int(len(newPredY)*0.9)]
    predY = np.mean(predYEntroList, axis=0)
    return (predYList, predY)

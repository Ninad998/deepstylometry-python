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

databaseConnectionServer = 'srn02.cs.cityu.edu.hk'
documentTable = 'document'

def readVectorData(fileName, GLOVE_DIR = 'glove/'):
    global alphabet, vocab_size, check, vocab, reverse_vocab
    # first, build index mapping words in the embeddings set
    # to their embedding vector

    #This alphabet is 69 chars vs. 70 reported in the paper since they include two
    # '-' characters. See https://github.com/zhangxiangxiao/Crepe#issues.
    
    print('Level = Char')
    
    print('Indexing char vectors.')

    import string
    
    alphabet = (list(string.ascii_lowercase) + list(string.digits) + 
                list(string.punctuation) + ['\n'])
    vocab_size = len(alphabet)
    check = set(alphabet)

    vocab = {}
    reverse_vocab = {}
    for ix, t in enumerate(alphabet):
        vocab[t] = ix
        reverse_vocab[ix] = t

    MAX_NB_WORDS = vocab_size

    print('Found %s char vectors.' % str(MAX_NB_WORDS))

    # second, prepare text samples and their labels
    print('Processing text dataset')

def loadAuthData(authorList, doc_id, chunk_size = 1000, samples = 300):
    texts = []  # list of text samples
    labels_index = {}  # dictionary mapping label name to numeric id
    labels = []  # list of label ids
    import DatabaseQuery
    from sshtunnel import SSHTunnelForwarder
    PORT=5432
    with SSHTunnelForwarder((databaseConnectionServer, 22),
                            ssh_username='stylometry',
                            ssh_password='stylometry',
                            remote_bind_address=('localhost', 5432),
                            local_bind_address=('localhost', 5400)):
        textToUse = DatabaseQuery.getCharAuthData(5400, authorList, doc_id, 
                                                  documentTable = documentTable, chunk_size = chunk_size)
    labels = []
    texts = []
    size = []
    authorList = textToUse.author_id.unique()
    for auth in authorList:
        current = textToUse.loc[textToUse['author_id'] == auth]
        size.append(current.shape[0])
    print("Mean: %s" % (sum(size) / len(size)))
    print("Min: %s" % (min(size)))
    print("Max: %s" % (max(size)))

    authorList = authorList.tolist()
    
    for auth in authorList:
        current = textToUse.loc[textToUse['author_id'] == auth]
        current = current.sample(n = samples)
        textlist = current.doc_content.tolist()
        texts = texts + textlist
        labels = labels + [authorList.index(author_id) for author_id in current.author_id.tolist()]
    labels_index = {}
    labels_index[0] = 0
    for i, auth in enumerate(authorList):
        labels_index[i] = auth

    del textToUse
    
    print('Authors %s.' % (str(authorList)))
    print('Found %s texts.' % len(texts))
    print('Found %s labels.' % len(labels))
    
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
        textToUse = DatabaseQuery.getCharDocData(5400, doc_id, 
                                             documentTable = documentTable, chunk_size = chunk_size)
    labels = []
    texts = []
    for index, row in textToUse.iterrows():
        labels.append(authorList.index(row.author_id))
        texts.append(row.doc_content)
    
    del textToUse
                 
    print('Found %s texts.' % len(texts))
    return (texts, labels)

def preProcessTrainVal(texts, labels, chunk_size = 1000, vocab_size = 69, VALIDATION_SPLIT = 0.2):
    global MAX_SEQUENCE_LENGTH
    
    MAX_SEQUENCE_LENGTH = (int) ((100 * chunk_size) / vocab_size)

    data = np.zeros((len(texts), MAX_SEQUENCE_LENGTH, vocab_size))
    for dix, sent in enumerate(texts):
        counter = 0
        sent_array = np.zeros((MAX_SEQUENCE_LENGTH, vocab_size))
        chars = list(sent.lower().replace(' ', ''))
        for c in chars:
            if counter >= MAX_SEQUENCE_LENGTH:
                pass
            else:
                char_array = np.zeros(vocab_size, dtype=np.int)
                if c in check:
                    ix = vocab[c]
                    char_array[ix] = 1
                sent_array[counter, :] = char_array
                counter += 1
        data[dix, :, :] = sent_array

    labels = to_categorical(np.asarray(labels))
    print('Shape of data tensor:', data.shape)
    print('Shape of label tensor:', labels.shape)
    
    # split the data into a training set and a validation set
    from sklearn.model_selection import train_test_split
    trainX, valX, trainY, valY = train_test_split(data, labels, test_size=VALIDATION_SPLIT)
    
    del data, labels
    
    return (trainX, trainY, valX, valY)

def preProcessTest(texts, labels_index, labels = None, chunk_size = 1000, vocab_size = 69):

    data = np.zeros((len(texts), MAX_SEQUENCE_LENGTH, vocab_size))
    for dix, sent in enumerate(texts):
        counter = 0
        sent_array = np.zeros((MAX_SEQUENCE_LENGTH, vocab_size))
        chars = list(sent.lower().replace(' ', ''))
        for c in chars:
            if counter >= MAX_SEQUENCE_LENGTH:
                pass
            else:
                char_array = np.zeros(vocab_size, dtype=np.int)
                if c in check:
                    ix = vocab[c]
                    char_array[ix] = 1
                sent_array[counter, :] = char_array
                counter += 1
        data[dix, :, :] = sent_array

    print('Shape of data tensor:', data.shape)

    testX = data[:]

    print('Shape of label tensor:', testX.shape)
    
    if labels is not None:
        testY = labels[:]
        return (testX, testY)
        
    return (testX)

def compileModel(classes, embedding_matrix, EMBEDDING_DIM = 100, chunk_size = 1000, CONVOLUTION_FEATURE = 256, 
                 BORDER_MODE = 'valid', DENSE_FEATURE = 1024, DROP_OUT = 0.4, LEARNING_RATE=0.001, MOMENTUM=0.9):

    model = Sequential()

    model.add(Convolution1D(                                  # Layer 1,   Features: 256, Kernel Size: 7
        nb_filter=CONVOLUTION_FEATURE,                        # Number of kernels or number of filters to generate
        filter_length=7,                                      # Size of kernels
        border_mode=BORDER_MODE,                              # Border = 'valid', cause kernel to reduce dimensions
        activation='relu',                                    # Activation function to use
        input_shape=(MAX_SEQUENCE_LENGTH, vocab_size)))       # Input = (((100 * chunk_size) / vocab_size), 69)

    model.add(MaxPooling1D(                                   # Layer 1a,  Max Pooling: 3
        pool_length=3))                                       # Size of kernels

    model.add(Convolution1D(                                  # Layer 2,   Features: 256, Kernel Size: 7
        nb_filter=CONVOLUTION_FEATURE,                        # Number of kernels or number of filters to generate
        filter_length=7,                                      # Size of kernels
        border_mode=BORDER_MODE,                              # Border = 'valid', cause kernel to reduce dimensions
        activation='relu'))                                   # Activation function to use

    model.add(MaxPooling1D(                                   # Layer 2a,  Max Pooling: 3
        pool_length=3))                                       # Size of kernels

    model.add(Convolution1D(                                  # Layer 3,   Features: 256, Kernel Size: 3
        nb_filter=CONVOLUTION_FEATURE,                        # Number of kernels or number of filters to generate
        filter_length=3,                                      # Size of kernels
        border_mode=BORDER_MODE,                              # Border = 'valid', cause kernel to reduce dimensions
        activation='relu'))                                   # Activation function to use

    model.add(Convolution1D(                                  # Layer 4,   Features: 256, Kernel Size: 3
        nb_filter=CONVOLUTION_FEATURE,                        # Number of kernels or number of filters to generate
        filter_length=3,                                      # Size of kernels
        border_mode=BORDER_MODE,                              # Border = 'valid', cause kernel to reduce dimensions
        activation='relu'))                                   # Activation function to use

    model.add(Convolution1D(                                  # Layer 5,   Features: 256, Kernel Size: 3
        nb_filter=CONVOLUTION_FEATURE,                        # Number of kernels or number of filters to generate
        filter_length=3,                                      # Size of kernels
        border_mode=BORDER_MODE,                              # Border = 'valid', cause kernel to reduce dimensions
        activation='relu'))                                   # Activation function to use

    model.add(Convolution1D(                                  # Layer 6,   Features: 256, Kernel Size: 3
        nb_filter=CONVOLUTION_FEATURE,                        # Number of kernels or number of filters to generate
        filter_length=5,                                      # Size of kernels
        border_mode=BORDER_MODE,                              # Border = 'valid', cause kernel to reduce dimensions
        activation='relu'))                                   # Activation function to use

    model.add(MaxPooling1D(                                   # Layer 6a,  Max Pooling: 3
        pool_length=3))                                       # Size of kernels

    model.add(Flatten())                                      # Layer 7

    model.add(Dense(                                          # Layer 7a,  Output Size: 1024
        output_dim=DENSE_FEATURE,                             # Output dimension
        activation='relu'))                                   # Activation function to use

    model.add(Dropout(DROP_OUT))

    model.add(Dense(                                          # Layer 8,   Output Size: 1024
        output_dim=DENSE_FEATURE,                             # Output dimension
        activation='relu'))                                   # Activation function to use

    model.add(Dropout(DROP_OUT))

    model.add(Dense(                                          # Layer 9,  Output Size: Size Unique Labels, Final
        output_dim=classes,                                   # Output dimension
        activation='softmax'))                                # Activation function to use
    
    
    # model = Model(start, end)

    sgd = SGD(lr=LEARNING_RATE, momentum=MOMENTUM, nesterov=True)

    model.compile(loss='categorical_crossentropy', optimizer=sgd,
                  metrics=['accuracy'])

    print("Done compiling.")
    return model

def fitModel(model, trainX, trainY, valX, valY, nb_epoch=30, batch_size=100):
    # Function to take input of data and return fitted model
    history = model.fit(trainX, trainY, validation_data=(valX, valY),
                        nb_epoch=nb_epoch, batch_size=batch_size)
    
    return (model, history)
    
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

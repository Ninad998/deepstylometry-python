#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os

import numpy as np

np.random.seed(123)

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.models import Sequential, Model
from keras.layers import Embedding, Convolution1D, MaxPooling1D, Flatten
from keras.layers import Input, Merge, Dense
from keras.layers import Dropout
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier

databaseConnectionServer = 'srn02.cs.cityu.edu.hk'
documentTable = 'document'

def readVectorData(fileName, GLOVE_DIR = 'glove/'):
    print('Level = Word')
    embeddings_index = {}
    f = open(os.path.join(GLOVE_DIR, fileName))
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()

    print('File used: %s' % (fileName))
    print('Found %s word vectors.' % (len(embeddings_index)))
    return embeddings_index

def loadAuthData(authorList, doc_id, chunk_size = 1000, samples = 300):
    texts = []  # list of text samples
    labels_index = {}  # dictionary mapping label name to numeric id
    labels = []  # list of label ids
    import DatabaseQuery
    from sshtunnel import SSHTunnelForwarder
    with SSHTunnelForwarder((databaseConnectionServer, 22),
                            ssh_username='stylometry',
                            ssh_password='stylometry',
                            remote_bind_address=('localhost', 5432),
                            local_bind_address=('localhost', 5400)):
        textToUse = DatabaseQuery.getWordAuthData(5400, authorList, doc_id,
                                                  documentTable = documentTable, chunk_size = chunk_size)
    labels = []
    texts = []
    size = []
    authorList = textToUse.author_id.unique()
    for auth in authorList:
        current = textToUse.loc[textToUse['author_id'] == auth]
        size.append(current.shape[0])
        print("Author: %5s  Size: %5s" % (auth, current.shape[0]))
    print("Min: %s" % (min(size)))
    print("Max: %s" % (max(size)))

    authorList = authorList.tolist()

    for auth in authorList:
        current = textToUse.loc[textToUse['author_id'] == auth]
        if (samples > min(size)):
            samples = min(size)
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

    return (texts, labels, labels_index, samples)

def loadDocData(authorList, doc_id, chunk_size = 1000):
    texts = []  # list of text samples
    labels = []  # list of label ids
    import DatabaseQuery
    from sshtunnel import SSHTunnelForwarder
    with SSHTunnelForwarder((databaseConnectionServer, 22),
                            ssh_username='stylometry',
                            ssh_password='stylometry',
                            remote_bind_address=('localhost', 5432),
                            local_bind_address=('localhost', 5400)):
        textToUse = DatabaseQuery.getWordDocData(5400, doc_id, documentTable = documentTable,
                                                 chunk_size = chunk_size)
    labels = []
    texts = []
    for index, row in textToUse.iterrows():
        labels.append(authorList.index(row.author_id))
        texts.append(row.doc_content)

    del textToUse

    print('Found %s texts.' % len(texts))
    return (texts, labels)

def preProcessTrainVal(texts, labels, ml = False, chunk_size = 1000, MAX_NB_WORDS = 40000, VALIDATION_SPLIT = 0.2):
    global tokenizer, word_index

    # finally, vectorize the text samples into a 2D integer tensor
    tokenizer = Tokenizer(nb_words=MAX_NB_WORDS)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)

    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

    data = pad_sequences(sequences, maxlen=chunk_size)

    if not ml:
        labels = to_categorical(np.asarray(labels))

    labels = np.asarray(labels)

    print('Shape of data tensor:', data.shape)
    print('Shape of label tensor:', labels.shape)

    # split the data into a training set and a validation set
    from sklearn.model_selection import train_test_split
    trainX, valX, trainY, valY = train_test_split(data, labels, test_size=VALIDATION_SPLIT, random_state = 123)

    del data, labels

    return (trainX, trainY, valX, valY)

def makeTokenizer():
    global tokenizer, word_index

    import cPickle as pickle

    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

def preProcessTest(texts, labels_index, labels = None, chunk_size = 1000, MAX_NB_WORDS = 40000):
    # finally, vectorize the text samples into a 2D integer tensor
    sequences = tokenizer.texts_to_sequences(texts)

    print('Found %s unique tokens.' % len(word_index))

    X = pad_sequences(sequences, maxlen = chunk_size)

    print('Shape of data tensor:', X.shape)

    testX = X[:]

    if labels is not None:
        testY = labels[:]
        return (testX, testY)

    return (testX)

def prepareEmbeddingMatrix(embeddings_index, MAX_NB_WORDS = 40000, EMBEDDING_DIM = 100):
    global nb_words, embedding_matrix
    
    nb_words = MAX_NB_WORDS
    
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
                 BORDER_MODE = 'valid', DENSE_FEATURE = 512, DROP_OUT = 0.5, LEARNING_RATE=0.01, MOMENTUM=0.9):
    global sgd

    ngram_filters = [3, 4]                                  # Define ngrams list, 3-gram, 4-gram, 5-gram
    convs = []

    graph_in = Input(shape=(chunk_size, EMBEDDING_DIM))

    for n_gram in ngram_filters:
        conv = Convolution1D(                                  # Layer X,   Features: 256, Kernel Size: ngram
            nb_filter=CONVOLUTION_FEATURE,                     # Number of kernels or number of filters to generate
            filter_length=n_gram,                              # Size of kernels, ngram
            activation='relu')(graph_in)                       # Activation function to use

        pool = MaxPooling1D(                                   # Layer X a,  Max Pooling: 3
            pool_length=3)(conv)                               # Size of kernels

        flat = Flatten()(pool)

        convs.append(flat)

    model = Sequential()

    model.add(Embedding(                                       # Layer 0, Start
        input_dim=nb_words + 1,                                # Size to dictionary, has to be input + 1
        output_dim=EMBEDDING_DIM,                              # Dimensions to generate
        weights=[embedding_matrix],                            # Initialize word weights
        input_length=chunk_size,                               # Define length to input sequences in the first layer
        trainable=False))                                      # Disable weight changes during training

    model.add(Dropout(0.25))                                   # Dropout 25%

    out = Merge(mode='concat')(convs)                          # Layer 1,  Output Size: Concatted ngrams feature maps

    graph = Model(input=graph_in, output=out)                  # Concat the ngram convolutions

    model.add(graph)                                           # Concat the ngram convolutions

    model.add(Dropout(DROP_OUT))                               # Dropout 50%

    model.add(Dense(                                           # Layer 3,  Output Size: 256
        output_dim=DENSE_FEATURE,                              # Output dimension
        activation='sigmoid'))                                    # Activation function to use

    model.add(Dense(                                           # Layer 4,  Output Size: Size Unique Labels, Final
        output_dim=classes,                                    # Output dimension
        activation='softmax'))                                 # Activation function to use

    sgd = SGD(lr=LEARNING_RATE, momentum=MOMENTUM, nesterov=True)

    model.compile(loss='categorical_crossentropy', optimizer=sgd,
                  metrics=['accuracy'])

    print("Done compiling.")
    return model

def recompileModelCNN(classes, embedding_matrix, EMBEDDING_DIM = 100, chunk_size = 1000, CONVOLUTION_FEATURE = 256,
                      BORDER_MODE = 'valid', DENSE_FEATURE = 512, DROP_OUT = 0.5, LEARNING_RATE=0.01, MOMENTUM=0.9):
    global sgd

    ngram_filters = [3, 4]                                  # Define ngrams list, 3-gram, 4-gram, 5-gram
    convs = []

    graph_in = Input(shape=(chunk_size, EMBEDDING_DIM))

    for n_gram in ngram_filters:
        conv = Convolution1D(                                  # Layer X,   Features: 256, Kernel Size: ngram
            nb_filter=CONVOLUTION_FEATURE,                     # Number of kernels or number of filters to generate
            filter_length=n_gram,                              # Size of kernels, ngram
            activation='relu')(graph_in)                       # Activation function to use

        pool = MaxPooling1D(                                   # Layer X a,  Max Pooling: 3
            pool_length=3)(conv)                               # Size of kernels

        flat = Flatten()(pool)

        convs.append(flat)

    model = Sequential()

    model.add(Embedding(                                       # Layer 0, Start
        input_dim=nb_words + 1,                                # Size to dictionary, has to be input + 1
        output_dim=EMBEDDING_DIM,                              # Dimensions to generate
        weights=[embedding_matrix],                            # Initialize word weights
        input_length=chunk_size,                               # Define length to input sequences in the first layer
        trainable=False))                                      # Disable weight changes during training

    model.add(Dropout(0.25))                                   # Dropout 25%

    out = Merge(mode='concat')(convs)                          # Layer 1,  Output Size: Concatted ngrams feature maps

    graph = Model(input=graph_in, output=out)                  # Concat the ngram convolutions

    model.add(graph)                                           # Concat the ngram convolutions

    model.add(Dropout(DROP_OUT))                               # Dropout 50%

    model.add(Dense(                                           # Layer 3,  Output Size: 256
        output_dim=DENSE_FEATURE,                              # Output dimension
        activation='sigmoid'))                                    # Activation function to use

    model.add(Dense(                                           # Layer 4,  Output Size: Size Unique Labels, Final
        output_dim=classes,                                    # Output dimension
        activation='softmax'))                                 # Activation function to use

    sgd = SGD(lr=LEARNING_RATE, momentum=MOMENTUM, nesterov=True)

    filepath="author-cnn-ngrams-word.hdf5"

    model.load_weights(filepath)

    model.compile(loss='categorical_crossentropy', optimizer=sgd,
                  metrics=['accuracy'])

    print("Done compiling.")
    return model

def getMLModel(algo):

    multi_nb = MultinomialNB()

    svc = SVC(kernel="linear", probability=True)
    
    oneVsSVC =  OneVsRestClassifier(SVC(kernel='linear', probability=True), n_jobs = 4)

    if algo == 'multi_nb':
        return multi_nb

    elif algo == 'svc':
        return svc
    
    elif algo == 'oneVsSVC':
        return oneVsSVC

    else:
        print("Model not found")
        return None


def recompileModelML(model, embedding_matrix, algo, new = True, EMBEDDING_DIM = 100, chunk_size = 1000,
                     CONVOLUTION_FEATURE = 256, BORDER_MODE = 'valid', DENSE_FEATURE = 512, DROP_OUT = 0.5,
                     LEARNING_RATE=0.01, MOMENTUM=0.9):
    global sgd

    ngram_filters = [3, 4]                                  # Define ngrams list, 3-gram, 4-gram, 5-gram
    convs = []

    graph_in = Input(shape=(chunk_size, EMBEDDING_DIM))

    for n_gram in ngram_filters:
        conv = Convolution1D(                                  # Layer X,   Features: 256, Kernel Size: ngram
            nb_filter=CONVOLUTION_FEATURE,                     # Number of kernels or number of filters to generate
            filter_length=n_gram,                              # Size of kernels, ngram
            activation='relu',                                 # Activation function to use
            trainable=False)(graph_in)                         # Disable weight changes during training

        pool = MaxPooling1D(                                   # Layer X a,  Max Pooling: 3
            pool_length=3,                                     # Size of kernels
            trainable=False)(conv)                             # Disable weight changes during training

        flat = Flatten()(pool)

        convs.append(flat)

    feature_model = Sequential()

    feature_model.add(Embedding(                               # Layer 0, Start
        input_dim=nb_words + 1,                                # Size to dictionary, has to be input + 1
        output_dim=EMBEDDING_DIM,                              # Dimensions to generate
        weights=[embedding_matrix],                            # Initialize word weights
        input_length=chunk_size,                               # Define length to input sequences in the first layer
        trainable=False))                                      # Disable weight changes during training

    feature_model.add(Dropout(0.25))                           # Dropout 25%

    out = Merge(mode='concat')(convs)                          # Layer 1,  Output Size: Concatted ngrams feature maps

    graph = Model(input=graph_in, output=out)                  # Concat the ngram convolutions

    feature_model.add(graph)                                   # Concat the ngram convolutions

    feature_model.add(Dropout(DROP_OUT))                       # Dropout 50%

    feature_model.add(Dense(                                   # Layer 3,  Output Size: 256
                      output_dim=DENSE_FEATURE,                # Output dimension
                      activation='sigmoid'))                      # Activation function to use

    feature_model.layers[1].set_weights(model.layers[1].get_weights())
    feature_model.layers[2].set_weights(model.layers[2].get_weights())
    feature_model.layers[3].set_weights(model.layers[3].get_weights())

    sgd = SGD(lr=LEARNING_RATE, momentum=MOMENTUM, nesterov=True)

    feature_model.compile(loss='categorical_crossentropy', optimizer=sgd,
                          metrics=['accuracy'])

    mlmodel = getMLModel(algo)

    if not new:
        import cPickle as pickle

        algoloadname = str(algo + '.pickle')

        with open(algoloadname, 'rb') as handle:
            mlmodel = pickle.load(handle)

    print("Done compiling.")

    return (feature_model, mlmodel)

def fitModelCNN(model, trainX, trainY, valX, valY, nb_epoch=30, batch_size=100):
    filepath="author-cnn-ngrams-word.hdf5"

    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')

    callbacks_list = [checkpoint]

    # Function to take input of data and return fitted model
    history = model.fit(trainX, trainY, validation_data=(valX, valY),
                        nb_epoch=nb_epoch, batch_size=batch_size,
                        callbacks=callbacks_list)

    # load weights from the best checkpoint
    model.load_weights(filepath)

    # Compile model again (required to make predictions)
    model.compile(loss='categorical_crossentropy', optimizer=sgd,
                  metrics=['accuracy'])

    train_acc = (model.evaluate(trainX, trainY))[1]
    print("\n\nFinal Train Accuracy: %.2f" % (train_acc * 100))

    val_acc = (model.evaluate(valX, valY))[1]
    print("\nFinal Validation Accuracy: %.2f" % (val_acc * 100))

    import cPickle as pickle

    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return (model, history, train_acc, val_acc)

def fitModelML(feature_model, mlmodel, algo, trainX, trainY, valX, valY):

    trainX = feature_model.predict(trainX)

    mlmodel.fit(trainX, trainY)

    train_acc = mlmodel.score(trainX, trainY)

    valX = feature_model.predict(valX)

    val_acc = mlmodel.score(valX, valY)

    print("\n\nFinal Train Accuracy: %.2f" % (train_acc * 100))

    print("\nFinal Validation Accuracy: %.2f" % (val_acc * 100))

    import cPickle as pickle

    algosavename = str(algo + '.pickle')

    with open(algosavename, 'wb') as handle:
        pickle.dump(mlmodel, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return (train_acc, val_acc)

def predictModel(feature_model, mlmodel, testX, authorList):
    # Function to take input of data and return prediction model

    testX = feature_model.predict(testX)

    predY = np.array(mlmodel.predict_proba(testX))

    unique, counts = np.unique(predY, return_counts=True)

    tot = len(predY)

    predYprob = [0.0] * len(authorList)

    for pred, predcount in zip(unique, counts):
        predval = 0.0
        predval = predcount/tot
        predYprob.insert(pred, predval)

    predYprob = np.array(predYprob)

    return (predYprob)

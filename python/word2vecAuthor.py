
# coding: utf-8
from __future__ import print_function
import os
import numpy as np
np.random.seed(1337)

import pandas as pd
import theano
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.layers import Dense, Flatten
from keras.layers import Convolution1D, MaxPooling1D, Embedding
from keras.models import Model
from keras.layers import Input, Dropout
from keras.optimizers import SGD, Adadelta
from keras.models import Sequential
import sys

BASE_DIR = ''
GLOVE_DIR = BASE_DIR + 'glove/'

MAX_SEQUENCE_LENGTH = 1000
MAX_NB_WORDS = 20000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.2
CONVOLUTION_FEATURE = 256
DENSE_FEATURE = 1024
DROP_OUT = 0.5
LEARNING_RATE=0.01
MOMENTUM=0.9
EPOCH=25
BATCH_SIZE=128

# first, build index mapping words in the embeddings set
# to their embedding vector

print('Indexing word vectors.')

print('Embedding Dimesions: %s' % (str(EMBEDDING_DIM)))

embeddings_index = {}
f = open(os.path.join(GLOVE_DIR, 'glove.6B.' + str(EMBEDDING_DIM) + 'd.txt'))
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

print('Found %s word vectors.' % len(embeddings_index))

# second, prepare text samples and their labels
print('Processing text dataset')

texts = []  # list of text samples
labels_index = {}  # dictionary mapping label name to numeric id
labels = []  # list of label ids
textToUse = pd.read_csv("suffle_4_6000.csv", names=["author_id", "text"], dtype={'author_id': int})
labels = []
texts = []
for index, row in textToUse.iterrows():
    labels.append(row.author_id)
    texts.append(row.text)
labels_index = {
    "Nobody": 0,
    "R M Ballantyne": 1, 
    "Anthony Trollope": 2, 
    "George Alfred Henty": 3, 
    "Charlotte Mary Yonge": 4
}

print('Found %s texts.' % len(texts))

# finally, vectorize the text samples into a 2D integer tensor
tokenizer = Tokenizer(nb_words=MAX_NB_WORDS)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

labels = to_categorical(np.asarray(labels))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)

# split the data into a training set and a validation set
indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]
nb_validation_samples = int(VALIDATION_SPLIT * data.shape[0])

x_train = data[:-nb_validation_samples]
y_train = labels[:-nb_validation_samples]
x_val = data[-nb_validation_samples:]
y_val = labels[-nb_validation_samples:]

print('Preparing embedding matrix.')

# prepare embedding matrix
nb_words = min(MAX_NB_WORDS, len(word_index))
embedding_matrix = np.zeros((nb_words + 1, EMBEDDING_DIM))
for word, i in word_index.items():
    if i > MAX_NB_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

print('Training model.')

model = Sequential()

model.add(Embedding(                          # Layer 0, Start
    input_dim=nb_words + 1,                   # Size to dictionary, has to be input + 1
    output_dim=EMBEDDING_DIM,                 # Dimensions to generate
    weights=[embedding_matrix],               # Initialize word weights
    input_length=MAX_SEQUENCE_LENGTH))        # Define length to input sequences in the first layer

model.add(Convolution1D(                      # Layer 1,   Features: 256, Kernel Size: 7
    nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
    filter_length=7,                          # Size of kernels
    border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
    activation='relu'))                       # Activation function to use

model.add(MaxPooling1D(                       # Layer 1a,  Max Pooling: 3
    pool_length=3))                           # Size of kernels

model.add(Convolution1D(                      # Layer 2,   Features: 256, Kernel Size: 7
    nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
    filter_length=7,                          # Size of kernels
    border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
    activation='relu'))                       # Activation function to use

model.add(MaxPooling1D(                       # Layer 2a,  Max Pooling: 3
    pool_length=3))                           # Size of kernels

model.add(Convolution1D(                      # Layer 3,   Features: 256, Kernel Size: 3
    nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
    filter_length=3,                          # Size of kernels
    border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
    activation='relu'))                       # Activation function to use

model.add(Convolution1D(                      # Layer 4,   Features: 256, Kernel Size: 3
    nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
    filter_length=3,                          # Size of kernels
    border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
    activation='relu'))                       # Activation function to use

model.add(Convolution1D(                      # Layer 5,   Features: 256, Kernel Size: 3
    nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
    filter_length=3,                          # Size of kernels
    border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
    activation='relu'))                       # Activation function to use

model.add(Convolution1D(                      # Layer 6,   Features: 256, Kernel Size: 3
    nb_filter=CONVOLUTION_FEATURE,            # Number of kernels or number of filters to generate
    filter_length=5,                          # Size of kernels
    border_mode='valid',                      # Border = 'valid', cause kernel to reduce dimensions
    activation='relu'))                       # Activation function to use

model.add(MaxPooling1D(                       # Layer 6a,  Max Pooling: 3
    pool_length=3))                           # Size of kernels

model.add(Flatten())                          # Layer 7

model.add(Dense(                              # Layer 7a,  Output Size: 1024
    output_dim=DENSE_FEATURE,                 # Output dimension
    activation='relu'))                       # Activation function to use

model.add(Dropout(DROP_OUT))

model.add(Dense(                              # Layer 8,   Output Size: 1024
    output_dim=DENSE_FEATURE,                 # Output dimension
    activation='relu'))                       # Activation function to use

model.add(Dropout(DROP_OUT))

model.add(Dense(                              # Layer 9,  Output Size: Size Unique Labels, Final
    output_dim=len(labels_index),             # Output dimension
    activation='softmax'))                    # Activation function to use

# model = Model(start, end)

sgd = SGD(lr=LEARNING_RATE, momentum=MOMENTUM, nesterov=True)

adadelta = Adadelta(lr=1.0, rho=0.95, epsilon=1e-08)

model.compile(loss='categorical_crossentropy', optimizer=sgd,
              metrics=['accuracy'])

print("Done compiling.")

model.fit(x_train, y_train, validation_data=(x_val, y_val),
          nb_epoch=EPOCH, batch_size=BATCH_SIZE)


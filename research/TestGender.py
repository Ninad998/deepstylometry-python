authorList = [11, 18, 80, 88, 64]
doc_id = 495

candidate = len(authorList)

test = "batch10" # change before run

level = "word"

iterations = 30

dropout = 0.5

samples = 3200

dimensions = 50

printstate = (("doc_id = %s, candidate = %s, ") % (str(doc_id), str(candidate)))
printstate += (("dimensions = %s, samples = %s, ") % (str(dimensions), str(samples)))
printstate += (("\niterations = %s, dropout = %s, test = %s") % (str(iterations), str(dropout), str(test)))

print("Current test: %s" % (str(printstate)))

print("Running: %12s" % (str(printstate)))

import StyloNeuralGender as Stylo
(labels_index, history, train_acc, val_acc, samples) = Stylo.getResults(
    glove = '../../glove/', dimensions = dimensions, nb_epoch = iterations, dropout = dropout, batch_size = 10 )

del Stylo

from keras import backend as K
K.clear_session()

import time
time.sleep(10)

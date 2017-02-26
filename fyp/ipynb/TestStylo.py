
authorList = [11, 18, 80, 88, 64]
doc_id = 1

candidate = len(authorList)

test = "batch10" # change before run

level = "word"

iterations = 30

dropout = 0.5

samples = 3200

dimensions = 200

printstate = (("doc_id = %s, candidate = %s, ") % (str(doc_id), str(candidate)))
printstate += (("dimensions = %s, samples = %s, ") % (str(dimensions), str(samples)))
printstate += (("\niterations = %s, dropout = %s, test = %s") % (str(iterations), str(dropout), str(test)))

print("Current test: %s" % (str(printstate)))

print("Running: %12s" % (str(printstate)))

import StyloNeural as Stylo
(labels_index, history, train_acc, val_acc, samples) = Stylo.getResults(
    doc_id = doc_id, authorList = authorList[:], 
    level = level, glove = '../../glove/', dimensions = dimensions, 
    samples = samples, nb_epoch = iterations, dropout = dropout, batch_size = 10 )

del Stylo

output = [
    [doc_id, candidates, dimensions, samples, 
     iterations, dropout, train_acc, val_acc, 
     test], 
    [doc_id, candidates, dimensions, samples, 
     iterations, dropout, train_acc, val_acc, 
     test]]

import pandas as pd
df = pd.DataFrame(output, columns=["doc_id", "candidates", "dimensions", "samples",
                                   "iterations", "dropout", "train_acc", "val_acc", 
                                   "test"])

# df.loc[i] = [randint(-1,1) for n in range(3)]

df.to_csv('out.csv', encoding='utf-8')

from keras import backend as K
K.clear_session()

import time
time.sleep(10)

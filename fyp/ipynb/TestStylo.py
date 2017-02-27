
authorList = [11, 18, 80, 88, 64, 44, 91, 19, 97]

doc_id = 1

parameters = {
    'candidate': [2, 3, 4, 5, 6, 7, 8, 9],
    'samples': [320, 1600, 3200],
    'dropout': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
    'dimensions': [50, 100, 200],
    'iterations': [10, 20, 40, 80, 120, 240],
    'cv': [320, 1600]#, 3200],
}

level = 'word'

output = []

for idxp, paralist in parameters.iteritems():
    if idxp == 'candidate':
        for idxl, val in enumerate(paralist):
            
            authorList = [11, 18, 80, 88, 64, 44, 91, 19, 97]
            
            doc_id = 1

            candidate = val

            test = idxp # change before run

            level = "word"

            iterations = 30

            dropout = 0.5

            samples = 3200

            dimensions = 200

            # loc = authorList.index(author_id)

            printstate = (("doc_id = %s, candidate = %s, ") % (str(doc_id), str(candidate)))
            printstate += (("dimensions = %s, samples = %s, ") % (str(dimensions), str(samples)))
            printstate += (("\niterations = %s, dropout = %s, test = %s") % (str(iterations), str(dropout), str(test)))

            print("Current test: %s" % (str(printstate)))
            
            print("Running: %12s" % (str(printstate)))
            
            import StyloNeural as Stylo
            (labels_index, train_acc_list, val_acc_list, samples) = Stylo.getResults(
                doc_id = doc_id, authorList = authorList[:candidate + 1], 
                level = level, glove = '../../glove/', dimensions = dimensions, 
                samples = samples, nb_epoch = iterations, dropout = dropout, batch_size = 10 )
            
            output.append([doc_id, candidate, dimensions, samples, 
                           iterations, dropout, train_acc, val_acc, 
                           test])
            
            del Stylo

            from keras import backend as K
            K.clear_session()

            import time
            time.sleep(10)

            from IPython.display import clear_output
            clear_output()

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

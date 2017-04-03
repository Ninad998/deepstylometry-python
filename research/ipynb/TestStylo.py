import pandas as pd
df = pd.read_csv('queryset_CNN.csv')
print(df.shape)
print(df.dtypes)


for index, row in df.iterrows():
    doc_id = row.doc_id

    author_id = row.author_id

    import ast
    authorList = ast.literal_eval(row.authorList)
    
    candidate = len(authorList)

    test = "dense_256" # change before run

    level = "word"

    iterations = 30

    dropout = 0.5

    samples = 3200

    dimensions = 200

    loc = authorList.index(author_id)

    printstate = (("doc_id = %s, candidate = %s, ") % (str(doc_id), str(candidate)))
    printstate += (("dimensions = %s, samples = %s, ") % (str(dimensions), str(samples)))
    printstate += (("\niterations = %s, dropout = %s, test = %s") % (str(iterations), str(dropout), str(test)))

    print("Current test: %s" % (str(printstate)))
    
    from sshtunnel import SSHTunnelForwarder
    with SSHTunnelForwarder(('144.214.121.15', 22),
                            ssh_username='ninadt',
                            ssh_password='Ninad123',
                            remote_bind_address=('localhost', 3306),
                            local_bind_address=('localhost', 3300)):
        import UpdateDB as db
        case = db.checkCNN(doc_id = doc_id, candidate = candidate, dimensions = dimensions,
                           samples = samples, iterations = iterations, dropout = dropout,
                           test = test, port = 3300)

    if case == False:

        print("Running: %12s" % (str(printstate)))

        import StyloNeural as Stylo
        (labels_index, history, train_acc, val_acc, samples) = Stylo.getResults(
            doc_id = doc_id, authorList = authorList[:], 
            level = level, glove = '../../glove/', dimensions = dimensions, 
            samples = samples, nb_epoch = iterations, dropout = dropout, batch_size = 10 )

        (predYList, predY, testY) = Stylo.getTestResults(
            doc_id = doc_id, authorList = authorList[:], labels_index = labels_index,
            level = level, glove = '../../glove/', dimensions = dimensions, 
            samples = samples, nb_epoch = iterations, dropout = dropout, batch_size = 10 )

        loc = testY
        
        test_acc = predY[loc]

        test_bin = 0

        if(predY.tolist().index(max(predY)) == testY):
            test_bin = 1
        
        from sshtunnel import SSHTunnelForwarder
        with SSHTunnelForwarder(('144.214.121.15', 22),
                                ssh_username='ninadt',
                                ssh_password='Ninad123',
                                remote_bind_address=('localhost', 3306),
                                local_bind_address=('localhost', 3300)):
            import UpdateDB as db
            case = db.updateresultCNN(doc_id = doc_id, candidate = candidate, dimensions = dimensions,
                                      samples = samples, iterations = iterations, dropout = dropout,
                                      train_acc = train_acc, val_acc = val_acc,
                                      test_acc = test_acc, test_bin = test_bin,
                                      test = test, port = 3300)
                                     
        del Stylo

        from keras import backend as K
        K.clear_session()

        import time
        time.sleep(10)
        
        from IPython.display import clear_output

        clear_output()

    else:
        print("Skipped: %12s" % (str(printstate)))


# import pandas as pd
# df = pd.DataFrame(output)
# df.to_csv("styloout.csv", index = False, encoding='utf-8')

import time
time.sleep(10)

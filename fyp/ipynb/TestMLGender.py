import pandas as pd
df = pd.read_csv('queryset_CNN.csv')
print(df.shape)
print(df.dtypes)

algo = 'tfidf_svc'

test = str("initial" + "-" + algo)

samples = 3200

import StyloMLGender as Stylo
(labels_index, train_acc, val_acc, samples) = Stylo.getResults(algo, samples = samples)
output = []
# from sshtunnel import SSHTunnelForwarder
for index, row in df.iterrows():
    doc_id = row.doc_id

    printstate = (("doc_id = %s") % (str(doc_id)))

    print("Current test: %s" % (str(printstate)))
    """
    with SSHTunnelForwarder(('144.214.121.15', 22),
                             ssh_username='ninadt',
                             ssh_password='Ninad123',
                             remote_bind_address=('localhost', 3306),
                             local_bind_address=('localhost', 3300)):
        import UpdateDB as db
        case = db.checkOldML(port = 3300, doc_id = doc_id, candidate = candidate, samples = samples,
                             test = test)

    if case == False:
    """
    print("Running: %12s" % (str(printstate)))

    (predY, testY) = Stylo.getTestResults(doc_id = doc_id, chunk_size = 1000)

    loc = testY

    test_acc = predY[loc]

    test_bin = 0

    if(predY.tolist().index(max(predY)) == testY):
        test_bin = 1
    """
    with SSHTunnelForwarder(('144.214.121.15', 22),
                             ssh_username='ninadt',
                             ssh_password='Ninad123',
                             remote_bind_address=('localhost', 3306),
                             local_bind_address=('localhost', 3300)):
        import UpdateDB as db
        case = db.updateresultOldML(port = 3300, doc_id = doc_id, candidate = candidate,
                                    samples = samples, train_acc = train_acc,
                                    val_acc = val_acc, test_acc = test_acc,
                                    test_bin = test_bin, test = str(test))
    """
    output.append([doc_id, candidate, samples,
                   train_acc, val_acc, test_acc,
                   test_bin])
    import time
    time.sleep(10)

else:
    print("Skipped: %12s" % (str(printstate)))

del Stylo

import pandas as pd
df = pd.DataFrame(output)
df.to_csv("mlout.csv", index = False, encoding='utf-8')

import time
time.sleep(10)

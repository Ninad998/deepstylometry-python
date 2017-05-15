#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import nltk.tokenize
import psycopg2
import pandas as pd
import sys

def getDocData(PORT, documentTable = 'document'):
    df = pd.DataFrame()
    conn = None
    output = []
    # nltk.download('punkt')
    try:
        conn = psycopg2.connect(user="stylometry", password="stylometry",
                                database="crosslingual", host="localhost", port=PORT)
        cur = conn.cursor()
        query = "SELECT doc_id, author_id, feature1, feature2, feature3,"
        query += " feature4, feature5, feature6, feature7, feature8 FROM"
        query += " comparative WHERE doc_id IN (select doc_id from " + str(documentTable) + ");"
        
        cur.execute(query)
        
        print("Execution completed")
        
        rows = cur.fetchall()
        
        print("Read completed")
        
        print("Number of rows: %s" % (len(rows)))
        
        print(type(rows))
        
        for row in rows:
            output.append([row[0], row[1], float(row[2]), float(row[3]), 
                           float(row[4]), float(row[5]), float(row[6]), float(row[7]), 
                           float(row[8]), float(row[9])])

        df = pd.DataFrame(output, columns=["doc_id", "author_id", "feature1", "feature2", 
                                           "feature3", "feature4", "feature5", "feature6", 
                                           "feature7", "feature8"])
        
        print(df.dtypes)
        
        print("Data Frame created: Shape: %s" % (str(df.shape)))

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn is not None:
            conn.close()

    return df

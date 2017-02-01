#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import nltk.tokenize
import MySQLdb
import pandas as pd
import sys

def updateresult(doc_id = 0, candidate = 4, dimensions = 200, samples = 300, 
                  iterations = 180, dropout = 0.2, accuracy = 0, test = 'Error'):
    
    conn = None
    
    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests")
        
        cursor = conn.cursor()
        
        cursor.execute("""SELECT * FROM readings WHERE doc_id = %s AND candidates = %s AND
        dimensions = %s AND samples = %s AND iterations = %s AND dropout = %s AND test = %s ;""", 
                        (str(doc_id), str(candidate), str(dimensions), str(samples), 
                         str(iterations), str(dropout), str(accuracy), str(test)))
        
        print("Execution completed")
        rows = cursor.fetchall()
        
        if (len(rows) > 0)
            print("Data exists")
        else:
            cursor.execute("""INSERT INTO readings 
            (doc_id, candidates, dimensions, samples, iterations, dropout, accuracy, test)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s); """, 
                           (str(doc_id), str(candidate), str(dimensions), str(samples), 
                            str(iterations), str(dropout), str(accuracy), str(test)))
            conn.commit()
        
    except MySQLdb.Error as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn is not None:
            conn.close()

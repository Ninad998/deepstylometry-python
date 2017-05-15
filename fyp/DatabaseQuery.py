#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import nltk.tokenize
import psycopg2
import pandas as pd
import sys, re

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets
    Every dataset is lower cased
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)     
    string = re.sub(r"\'s", " \'s", string) 
    string = re.sub(r"\'ve", " \'ve", string) 
    string = re.sub(r"n\'t", " n\'t", string) 
    string = re.sub(r"\'re", " \'re", string) 
    string = re.sub(r"\'d", " \'d", string) 
    string = re.sub(r"\'ll", " \'ll", string) 
    string = re.sub(r",", " , ", string) 
    string = re.sub(r"!", " ! ", string) 
    string = re.sub(r"\(", " \( ", string) 
    string = re.sub(r"\)", " \) ", string) 
    string = re.sub(r"\?", " \? ", string) 
    string = re.sub(r"\s{2,}", " ", string)    
    return string.strip().lower()

def getWordAuthData(PORT, authors, doc, documentTable = 'document', chunk_size = 1000):
    df = pd.DataFrame()
    conn = None
    output = []
    i = 1
    # nltk.download('punkt')
    try:
        conn = psycopg2.connect(user="stylometry", password="stylometry",
                                database="stylometry_v2", host="localhost", port=PORT)
        cur = conn.cursor()
        query = "SELECT author_id, doc_content FROM " + str(documentTable) + " WHERE author_id IN ("
        flag = False
        for auth in authors:
            if not flag:
                query = query + str(auth)
                flag = True
            else:
                query = query + ", " + str(auth)
        query = query + ") AND doc_id <> '" + str(doc) + "' ;"
        cur.execute(query)
        print("Execution completed")
        rows = cur.fetchall()
        print("Read completed")
        print("Number of rows: %s" % (len(rows)))
        for row in rows:
            clean_row = clean_str(row[1].decode("utf8"))
            tokens = nltk.word_tokenize(clean_row)
            chunk1 = []
            for x in tokens:
                if (i < chunk_size):
                    chunk1.append(x.encode("utf8"))
                    i += 1
                else:
                    chunk1.append(x.encode("utf8"))
                    xx = ' '.join(chunk1)
                    xx = str(xx)
                    chunk1 = []
                    output.append([row[0], xx])
                    i = 1
            if len(chunk1) > 0:
                xx = ' '.join(chunk1)
                xx = str(xx)
                chunk1 = []
                output.append([row[0], xx])
                i = 1

        df = pd.DataFrame(output, columns=["author_id", "doc_content"])
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

def getWordDocData(PORT, doc, documentTable = 'document', chunk_size = 1000):
    df = pd.DataFrame()
    conn = None
    output = []
    i = 1
    try:
        conn = psycopg2.connect(user="stylometry", password="stylometry",
                                database="stylometry_v2", host="localhost", port=PORT)
        cur = conn.cursor()
        query = "SELECT author_id, doc_content FROM " + str(documentTable) + " WHERE doc_id = '" + str(doc) + "' ;"
        cur.execute(query)
        print("Execution completed")
        rows = cur.fetchall()
        print("Read completed")
        print("Number of rows: %s" % (len(rows)))
        for row in rows:
            clean_row = clean_str(row[1].decode("utf8"))
            tokens = nltk.word_tokenize(clean_row)
            chunk1 = []
            for x in tokens:
                if (i < chunk_size):
                    chunk1.append(x.encode("utf8"))
                    i += 1
                else:
                    chunk1.append(x.encode("utf8"))
                    xx = ' '.join(chunk1)
                    xx = str(xx)
                    chunk1 = []
                    output.append([row[0], xx])
                    i = 1
            if len(chunk1) > 0:
                xx = ' '.join(chunk1)
                xx = str(xx)
                chunk1 = []
                output.append([row[0], xx])
                i = 1

        df = pd.DataFrame(output, columns=["author_id", "doc_content"])
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


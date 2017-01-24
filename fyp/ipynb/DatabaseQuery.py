#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import nltk.tokenize
import psycopg2
import pandas as pd
import sys

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
            tokens = nltk.word_tokenize(row[1].decode("utf8"))
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
            tokens = nltk.word_tokenize(row[1].decode("utf8"))
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

def getCharAuthData(PORT, authors, doc, documentTable = 'document', vocab_size = 69, chunk_size = 1000):
    df = pd.DataFrame()
    conn = None
    output = []
    i = 1
    chunk_size = (int) ((100 * chunk_size) / vocab_size)
    # nltk.download('punkt')
    print("chunk_size %s." % str(chunk_size))
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
            tokens = list(row[1])
            chunk1 = []
            for x in tokens:
                if (i < chunk_size):
                    chunk1.append(x)
                    i += 1
                else:
                    chunk1.append(x)
                    xx = ''.join(chunk1)
                    xx = str(xx)
                    chunk1 = []
                    output.append([row[0], xx])
                    i = 1
            if len(chunk1) > 0:
                xx = ''.join(chunk1)
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

def getCharDocData(PORT, doc, documentTable = 'document', vocab_size = 69, chunk_size = 1000):
    df = pd.DataFrame()
    conn = None
    output = []
    i = 1
    chunk_size = (int) ((100 * chunk_size) / vocab_size)
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
            tokens = list(row[1])
            chunk1 = []
            for x in tokens:
                if (i < chunk_size):
                    chunk1.append(x)
                    i += 1
                else:
                    chunk1.append(x)
                    xx = ''.join(chunk1)
                    xx = str(xx)
                    chunk1 = []
                    output.append([row[0], xx])
                    i = 1
            if len(chunk1) > 0:
                xx = ''.join(chunk1)
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

def getAllWordAuthData(PORT, doc, documentTable = 'document_cnn', chunk_size = 1000):
    df = pd.DataFrame()
    conn = None
    output = []
    i = 1
    # nltk.download('punkt')
    try:
        conn = psycopg2.connect(user="stylometry", password="stylometry",
                                database="stylometry_v2", host="localhost", port=PORT)
        cur = conn.cursor()
        query = "SELECT author_id, doc_content FROM " + str(documentTable) + " WHERE doc_id <> '" + str(doc) + "' ;"
        cur.execute(query)
        print("Execution completed")
        rows = cur.fetchall()
        print("Read completed")
        print("Number of rows: %s" % (len(rows)))
        for row in rows:
            tokens = nltk.word_tokenize(row[1].decode("utf8"))
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


def getAllCharAuthData(PORT, authors, doc, documentTable = 'document_cnn', vocab_size = 69, chunk_size = 1000):
    df = pd.DataFrame()
    conn = None
    output = []
    i = 1
    chunk_size = (int) ((100 * chunk_size) / vocab_size)
    # nltk.download('punkt')
    print("chunk_size %s." % str(chunk_size))
    try:
        conn = psycopg2.connect(user="stylometry", password="stylometry",
                                database="stylometry_v2", host="localhost", port=PORT)
        cur = conn.cursor()
        query = "SELECT author_id, doc_content FROM " + str(documentTable) + " WHERE doc_id <> '" + str(doc) + "' ;"
        cur.execute(query)
        print("Execution completed")
        rows = cur.fetchall()
        print("Read completed")
        print("Number of rows: %s" % (len(rows)))
        for row in rows:
            tokens = list(row[1])
            chunk1 = []
            for x in tokens:
                if (i < chunk_size):
                    chunk1.append(x)
                    i += 1
                else:
                    chunk1.append(x)
                    xx = ''.join(chunk1)
                    xx = str(xx)
                    chunk1 = []
                    output.append([row[0], xx])
                    i = 1
            if len(chunk1) > 0:
                xx = ''.join(chunk1)
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

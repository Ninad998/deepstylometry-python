#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import nltk.tokenize
import psycopg2
import pandas as pd
import sys

def getDocBigData(PORT, documentTable = 'document'):
    df = pd.DataFrame()
    conn = None
    output = []
    # nltk.download('punkt')
    try:
        conn = psycopg2.connect(user="stylometry", password="stylometry",
                                database="stylometry", host="localhost", port=PORT)
        cur = conn.cursor()
        query = "SELECT doc_id, doc_title, year_of_pub FROM " + str(documentTable) + ";"
        
        cur.execute(query)
        
        print("Execution completed")
        
        rows = cur.fetchall()
        
        print("Read completed")
        
        print("Number of rows: %s" % (len(rows)))
        
        print(type(rows))
        
        for row in rows:
            output.append([row[0], row[1], row[2]])

        df = pd.DataFrame(output, columns=["doc_id" , "doc_title" , "year_of_pub"])
        
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


def getDocSmallData(PORT, documentTable = 'document'):
    df = pd.DataFrame()
    conn = None
    output = []
    # nltk.download('punkt')
    try:
        conn = psycopg2.connect(user="stylometry", password="stylometry",
                                database="stylometry_v2", host="localhost", port=PORT)
        cur = conn.cursor()
        query = "SELECT doc_id, doc_title, year_of_pub FROM " + str(documentTable) + ";"
        
        cur.execute(query)
        
        print("Execution completed")
        
        rows = cur.fetchall()
        
        print("Read completed")
        
        print("Number of rows: %s" % (len(rows)))
        
        print(type(rows))
        
        for row in rows:
            output.append([row[0], row[1], row[2]])

        df = pd.DataFrame(output, columns=["doc_id" , "doc_title" , "year_of_pub"])
        
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


def updateDocSmallData(PORT, doc_id, doc_title, year_of_pub, documentTable = 'document'):
    df = pd.DataFrame()
    conn = None
    output = []
    # nltk.download('punkt')
    try:
        conn = psycopg2.connect(user="stylometry", password="stylometry",
                                database="stylometry_v2", host="localhost", port=PORT)
        cur = conn.cursor()
        query = "UPDATE " + str(documentTable) + " SET"
        query += " doc_id = " + str(doc_id) + ","
        query += " year_of_pub = " + str(year_of_pub)
        query += " WHERE doc_title LIKE '%" + str(doc_title) + "%' ;"
        
        cur.execute(query)
        
        print("Execution completed")
        
        rows = cur.fetchall()
        
        print("Read completed")
        
        print("Number of rows: %s" % (len(rows)))
        
        print(type(rows))
        
        for row in rows:
            output.append([row[0], row[1], row[2]])

        df = pd.DataFrame(output, columns=["doc_id" , "doc_title" , "year_of_pub"])
        
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

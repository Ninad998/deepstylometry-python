#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import nltk.tokenize
import MySQLdb
import pandas as pd
import sys

def checkOldCNN(doc_id = 0, candidate = 4, dimensions = 200,
                samples = 300, iterations = 180, dropout = 0.2,
                test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsOldCNN WHERE doc_id = " + str(doc_id) + " AND candidates = " + str(candidate)
        query += " AND dimensions = " + str(dimensions) + " AND samples = " + str(samples)
        query += " AND iterations = " + str(iterations) + " AND dropout = " + str(dropout)
        query += " AND test LIKE '%" + str(test) + "%' ;"

        cursor.execute(query)

        print("Execution completed")
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return True
        else:
            return False

    except MySQLdb.Error as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn is not None:
            conn.close()

def updateresultOldCNN(doc_id = 0, candidate = 4, dimensions = 200,
                       samples = 300, iterations = 180, dropout = 0.2,
                       train_acc = 0.0, val_acc = 0.0,
                       test_acc = 0.0, test_bin = 0.0, 
                       test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsOldCNN WHERE doc_id = " + str(doc_id) + " AND candidates = " + str(candidate)
        query += " AND dimensions = " + str(dimensions) + " AND samples = " + str(samples)
        query += " AND iterations = " + str(iterations) + " AND dropout = " + str(dropout)
        query += " AND test LIKE '%" + str(test) + "%' ;"

        cursor.execute(query)

        print("Execution completed")
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return False
        else:
            cursor.execute("""INSERT INTO readingsOldCNN
            (doc_id, candidates, dimensions, samples, iterations, dropout, train_acc, val_acc, test_acc, test_bin, test)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """,
                           (str(doc_id), str(candidate), str(dimensions),
                            str(samples), str(iterations), str(dropout),
                            str(train_acc), str(val_acc),
                            str(test_acc), str(test_bin),
                            str(test)))
            conn.commit()

            return True

    except MySQLdb.Error as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn is not None:
            conn.close()
            
def checkOldCNNDiff(doc_id = 0, candidate = 4, dimensions = 200,
                    samples = 300, iterations = 180, dropout = 0.2,
                    test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsOldCNNDiff WHERE doc_id = " + str(doc_id) + " AND candidates = " + str(candidate)
        query += " AND dimensions = " + str(dimensions) + " AND samples = " + str(samples)
        query += " AND iterations = " + str(iterations) + " AND dropout = " + str(dropout)
        query += " AND test LIKE '%" + str(test) + "%' ;"

        cursor.execute(query)

        print("Execution completed")
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return True
        else:
            return False

    except MySQLdb.Error as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn is not None:
            conn.close()

def updateresultOldCNNDiff(doc_id = 0, candidate = 4, dimensions = 200,
                           samples = 300, iterations = 180, dropout = 0.2,
                           train_acc = 0.0, val_acc = 0.0,
                           test_acc = 0.0, test_bin = 0.0, 
                           test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsOldCNNDiff WHERE doc_id = " + str(doc_id) + " AND candidates = " + str(candidate)
        query += " AND dimensions = " + str(dimensions) + " AND samples = " + str(samples)
        query += " AND iterations = " + str(iterations) + " AND dropout = " + str(dropout)
        query += " AND test LIKE '%" + str(test) + "%' ;"

        cursor.execute(query)

        print("Execution completed")
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return False
        else:
            cursor.execute("""INSERT INTO readingsOldCNNDiff
            (doc_id, candidates, dimensions, samples, iterations, dropout,
             train_acc, val_acc, test_acc, test_bin, test)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """,
                           (str(doc_id), str(candidate), str(dimensions),
                            str(samples), str(iterations), str(dropout),
                            str(train_acc), str(val_acc),
                            str(test_acc), str(test_bin),
                            str(test)))
            conn.commit()

            return True

    except MySQLdb.Error as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn is not None:
            conn.close()
            
def checkOldML(doc_id = 0, candidate = 4, samples = 300,
               test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsOldML WHERE doc_id = " + str(doc_id)
        query += " AND candidates = " + str(candidate)
        query += " AND samples = " + str(samples)
        query += " AND test LIKE '%" + str(test) + "%' ;"

        cursor.execute(query)

        print("Execution completed")
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return True
        else:
            return False

    except MySQLdb.Error as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn is not None:
            conn.close()

def updateresultOldML(doc_id = 0, candidate = 4, samples = 300,
                      train_acc = 0.0, val_acc = 0.0,
                      test_acc = 0.0, test_bin = 0.0, 
                      test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsOldML WHERE doc_id = " + str(doc_id)
        query += " AND candidates = " + str(candidate)
        query += " AND samples = " + str(samples)
        query += " AND test LIKE '%" + str(test) + "%' ;"

        cursor.execute(query)

        print("Execution completed")
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return False
        else:
            cursor.execute("""INSERT INTO readingsOldML
            (doc_id, candidates, samples, train_acc, val_acc, test_acc, test_bin, test)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s); """,
                           (str(doc_id), str(candidate), str(samples), 
                            str(train_acc), str(val_acc),
                            str(test_acc), str(test_bin),
                            str(test)))
            conn.commit()

            return True

    except MySQLdb.Error as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn is not None:
            conn.close()
            
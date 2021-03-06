#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import nltk.tokenize
import MySQLdb
import pandas as pd
import sys


def checkCNN(doc_id = 0, candidate = 4, dimensions = 200,
                samples = 300, iterations = 180, dropout = 0.2,
                test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsCNN WHERE doc_id = " + str(doc_id) + " AND candidates = " + str(candidate)
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

def updateresultCNN(doc_id = 0, candidate = 4, dimensions = 200,
                       samples = 300, iterations = 180, dropout = 0.2,
                       train_acc = 0.0, val_acc = 0.0,
                       test_acc = 0.0, test_bin = 0.0, 
                       test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsCNN WHERE doc_id = " + str(doc_id) + " AND candidates = " + str(candidate)
        query += " AND dimensions = " + str(dimensions) + " AND samples = " + str(samples)
        query += " AND iterations = " + str(iterations) + " AND dropout = " + str(dropout)
        query += " AND test LIKE '%" + str(test) + "%' ;"

        cursor.execute(query)

        print("Execution completed")
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return False
        else:
            cursor.execute("""INSERT INTO readingsCNN
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
            (doc_id, candidates, dimensions, samples, iterations, dropout, train_acc, val_acc, test)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); """,
                           (str(doc_id), str(candidate), str(dimensions),
                            str(samples), str(iterations), str(dropout),
                            str(train_acc), str(val_acc),
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

        query = "SELECT * FROM readingsOldML WHERE doc_id = " + str(doc_id) + " AND candidates = " + str(candidate)
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

def updateresultOldML(doc_id = 0, candidate = 4, dimensions = 200,
                       samples = 300, iterations = 180, dropout = 0.2,
                       train_acc = 0.0, val_acc = 0.0,
                       test_acc = 0.0, test_bin = 0.0, 
                       test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsOldML WHERE doc_id = " + str(doc_id) + " AND candidates = " + str(candidate)
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
                           (str(doc_id), str(candidate), 
                            str(samples),
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

def checkOldCNNDiffBoth(doc_id = 0, candidate = 4, dimensions = 200,
                        samples = 300, iterations = 180, dropout = 0.2,
                        test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsOldCNNDiffBoth WHERE doc_id = " + str(doc_id) + " AND candidates = " + str(candidate)
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

def updateresultOldCNNDiffBoth(doc_id = 0, candidate = 4, dimensions = 200,
                               samples = 300, iterations = 180, dropout = 0.2,
                               train_acc_cnn = 0.0, val_acc_cnn = 0.0,
                               test_acc_cnn = 0.0, test_bin_cnn = 0.0, 
                               train_acc_ml = 0.0, val_acc_ml = 0.0,
                               test_acc_ml = 0.0, test_bin_ml = 0.0, 
                               test = 'Error', port = 3306):

    conn = None

    try:
        conn = MySQLdb.connect(host="127.0.0.1", user="ninadt", passwd="ninadt", db="tests", port = port)

        cursor = conn.cursor()

        query = "SELECT * FROM readingsOldCNNDiffBoth WHERE doc_id = " + str(doc_id) + " AND candidates = " + str(candidate)
        query += " AND dimensions = " + str(dimensions) + " AND samples = " + str(samples)
        query += " AND iterations = " + str(iterations) + " AND dropout = " + str(dropout)
        query += " AND test LIKE '%" + str(test) + "%' ;"

        cursor.execute(query)

        print("Execution completed")
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return False
        else:
            cursor.execute("""INSERT INTO readingsOldCNNDiffBoth
            (doc_id, candidates, dimensions, samples, iterations, dropout,
             train_acc_cnn, val_acc_cnn, test_acc_cnn, test_bin_cnn,
             train_acc_ml, val_acc_ml, test_acc_ml, test_bin_ml,
             test)
            VALUES (%s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s); """,
                           (str(doc_id), str(candidate), str(dimensions),
                            str(samples), str(iterations), str(dropout),
                            str(train_acc_cnn), str(val_acc_cnn),
                            str(test_acc_cnn), str(test_bin_cnn),
                            str(train_acc_ml), str(val_acc_ml),
                            str(test_acc_ml), str(test_bin_ml),
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
       

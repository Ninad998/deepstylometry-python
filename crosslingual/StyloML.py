#!/usr/bin/python
# -*- coding: utf-8 -*-

def getResults(doc_table = "author_study_six", samples = 3200):
    
    import MLModelCreatorWord as md

    (features, labels, groups, samples) = md.loadData(doc_table)

    logo = md.preProcessTrainVal(features, labels, groups)
    
    for train_index, test_index in logo.split(features, labels, groups):
        
        model = md.compileModel()
        
        trainX = features[train_index]
        valX = features[test_index]
        
        trainY, valY = labels[train_index], labels[test_index]
        
        (model, train_acc, val_acc) = md.fitModel(model, trainX, trainY, valX, valY)
        
        del model

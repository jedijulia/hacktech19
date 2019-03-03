#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 19:47:37 2019

@author: vivekmishra
"""

from sklearn.externals import joblib
from operator import itemgetter

class Ranker():
    def rankThem(self,ranked_list):
        classifier = joblib.load('lr_model.joblib')
        count_vect = joblib.load('count_vect.joblib')
        ranking = []
        for item in ranked_list:
            title = str(item['title'])
            material = str(item['material'])
            docs_new = [title+material]
            new_counts = count_vect.transform(docs_new)
            predicted = classifier.predict_proba(new_counts)
            
            temp = {}
            temp['title'] = title
            temp['material'] = material
            temp['emission'] = item['emission']
            temp['price'] = item['price']
            temp['gallleryURL'] = item['gallleryURL']
            temp['eco'] = 1 - predicted[0][0]
            
            ranking.append(temp)
            
        newlist = sorted(ranking, key=itemgetter('eco'), reverse=True)
        
        return newlist
            
            
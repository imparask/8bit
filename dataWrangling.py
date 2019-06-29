import numpy as np 
import pandas as pd 
"""
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold   #For K-fold cross validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as mlt
import seaborn as sns
from warnings import simplefilter
"""
import pymysql

#Taking data from database and storing in csv file
conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore",use_unicode=True,charset="utf8")
cursor = conn.cursor()
query = "Select * from apps"
results = pd.read_sql_query(query,conn)
results.to_csv('F:\\Python Class\\Project\\apps1.csv',index=False)
conn.commit()
conn.close()

#Data wrangling of apps
apps=pd.read_csv('F:\\Python Class\\Project\\apps.csv',encoding = "ISO-8859-1")
#print(apps.head())


apps['App'] = apps['App'].str.replace('?','')
apps['App'] = apps['App'].str.replace('(','')
apps['App'] = apps['App'].str.replace(')','')
apps=apps.drop([3750,6333,9306],axis=0)
#apps.replace(['?'],[''])
#print(apps)
#print(apps.iloc[313])

#length=len(apps)
#for i in range(1,length):
#    if apps.iloc[i]['Rating']== "NaN":
#        apps=apps.drop([i],inplace=True)
#        
#
#print(apps.iloc[23])   

apps=apps[apps.Rating.notnull()]
#print(apps.iloc[120])
#print(apps)

#Taking data from database and storing in csv file
conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore",use_unicode=True,charset="utf8")
cursor = conn.cursor()
query = "Select * from reviews"
results = pd.read_sql_query(query,conn)
results.to_csv('F:\\Python Class\\Project\\review1.csv',index=False)
conn.commit()
conn.close()

#Data wrangling of reviews
review=pd.read_csv('F:\\Python Class\\Project\\review.csv',encoding = "ISO-8859-1")
#print(review)


#print(review)



for i in range(200,240):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)

#print(review.iloc[330])
for i in range(1020,1098):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)
    
for i in range(33545,33585):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)
    
'''for i in range(51024,51064):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)'''
    
for i in range(51024,51064):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)

#review['App'] = review['App'].str.replace('â€“','')'''
#print(review.iloc[50906])
review=review[review.Translated_Review.notnull()]
#print(review)
        
    


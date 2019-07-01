from tkinter import *
from tkinter import messagebox
import re, pymysql
import numpy as np 
import pandas as pd 
from datetime import date
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

#Choose theme of window
color1 ='#CD3333'#TITLE COLOR
bgcolor_middle = '#5F9EA0'#BODY COLOR
color3 = '#00C957'#Button Color
text_color ='white'


#DATA WRANGLING
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

apps['App'] = apps['App'].str.replace('?','')
apps['App'] = apps['App'].str.replace('(','')
apps['App'] = apps['App'].str.replace(')','')
apps=apps.drop([3750,6333,9306,10472],axis=0)

apps=apps[apps.Rating.notnull()]

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

for i in range(200,240):
    review=review.drop([i],axis=0)

for i in range(1020,1098):
    review=review.drop([i],axis=0)
    
for i in range(33545,33585):
    review=review.drop([i],axis=0)
       
for i in range(51024,51064):
    review=review.drop([i],axis=0)

review=review[review.Translated_Review.notnull()]
apps['Installs'] = apps['Installs'].str.replace(',','')
apps['Installs'] = apps['Installs'].str.replace('+','')


def categoryDownloads():
    global cat_inst,category,installs_sum
    cat_inst={}
    cat = apps.drop_duplicates(subset='Category', keep='first')
    category=[]
    for i in cat['Category']:
        category.append(i)
    
    installs_sum=[]
    for i in category:
        sum=0
        for index,row in apps.iterrows():
            if i==row['Category']:
                sum=sum+int(row['Installs'])
        installs_sum.append(sum)
    total_sum=0
    for i in  installs_sum:
        total_sum=total_sum+i
    
    i=0
    while(i<len(category)):
        cat_inst[category[i]]=installs_sum[i]
        i=i+1 

def fetch_installs(cat,x1,y1):
    cat = str(cat.get())
    if(cat=="--Select a Category--"):
        messagebox.showerror("Error", "Please select proper category", parent=screen4)
    else:
        for i in cat_inst:
            if(i==cat):
                Label(screen3, text=i,font=("Open Sans", 15, 'bold'), fg=text_color,anchor=W,width=20, bg=bgcolor_middle).place(x=x1+60,y=y1+220)
                Label(screen3, text=cat_inst[i],font=("Open Sans", 15, 'bold'), fg=text_color,anchor=W,width=20, bg=bgcolor_middle).place(x=x1+310,y=y1+220)
                
def fetch_downloads(ran,x2,y2):
    global range1,range2,range3,range4,range5
    ran = str(ran.get())
    range1=0
    range2=0
    range3=0
    range4=0
    range5=0
    for index,rows in apps.iterrows():
        if int(rows['Installs']) >= 10000 and int(rows['Installs']) <50000:
            range1+=1
        elif int(rows['Installs']) >= 50000 and int(rows['Installs']) <150000:
            range2+=1
        elif int(rows['Installs']) >= 150000 and int(rows['Installs']) <500000:
            range3+=1
        elif int(rows['Installs']) >= 500000 and int(rows['Installs']) <5000000:
            range4+=1
        elif int(rows['Installs']) >= 5000000:
            range5+=1
            
    if(ran=="10000-50000"):
        installs=range1
    elif(ran=="50000-150000"):
        installs=range2
    elif(ran=="150000-500000"):
        installs=range3
    elif(ran=="500000-5000000"):
        installs=range4
    elif(ran==">5000000"):
        installs=range5
        
    Label(screen3, text=ran,font=("Open Sans", 15, 'bold'), fg=text_color,anchor=W,width=20, bg=bgcolor_middle).place(x=x2+60,y=y2+220)
    Label(screen3, text=installs,font=("Open Sans", 15, 'bold'), fg=text_color,width=20, bg=bgcolor_middle).place(x=x2+310,y=y2+220)
        
def max_min_avg_downloads():
    global max_cat_download,min_cat_download,avg_cat_download
        
    max_cat_download=category[installs_sum.index(max(installs_sum))]
    min_cat_download=category[installs_sum.index(min(installs_sum))]
    
    avg_number_of_installs = float(sum(installs_sum)/len(installs_sum))
    num_in_installs_sum_list = min(installs_sum,key=lambda x:abs(x-avg_number_of_installs))#gives me the closest number to avg in the installs_sum list
    avg_cat_download=category[installs_sum.index(num_in_installs_sum_list)]
      
def highest_rating():  
    rating_sum=[]
    for i in category:
        sum=0
        counter=0
        avg=0
        for index,row in apps.iterrows():
            if i==row['Category']:
                counter+=1
                sum=sum+int(row['Rating'])
        avg=sum/counter
        rating_sum.append(round(avg,2))  
        
    highest_value = max(rating_sum)
    index = rating_sum.index(highest_value)
    return category[index] 
                       
def adjustWindow(window):
    ws = window.winfo_screenwidth() # width of the screen
    hs = window.winfo_screenheight() # height of the screen
    w = ws # width for the window size
    h = hs# height for the window size
    x = (ws/2) - (w/2) # calculate x and y coordinates for the Tk window
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w-15, h-40, x, y)) # set the dimensions of the screen and where it is placed
    window.resizable(False, False) # disabling the resize option for the window
    window.configure(background='white')

def stats():
    global screen3,cat,ran
    screen3 = Tk()
    cat=StringVar()
    ran=StringVar()
    #screen3 = Toplevel(screen2)
    screen3.title("STATISTICS")
    adjustWindow(screen3)
    categoryDownloads()
    
    Label(screen3, text="", width='500', height="20", bg=color1).pack() 
    Label(screen3, text="8-BIT ANALYSIS",font=("Calibri", 70, 'bold'), fg=text_color, bg=color1).place(x=475,y=10)
    Button(screen3, text='BACK', width=8, font=("Open Sans", 13, 'bold'), bg=color3, fg=text_color, command=screen3.destroy).place(x=1380, y=55)
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\stats.png") # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(screen3,borderwidth=0, image=photo1) # attaching image to the label
    label.place(x=0, y=152)
    
    #Section 1
    x1=60# Change these parameters 
    y1=200# to shift the whole below section
    Label(screen3, text="", width=95, height=18, bg=bgcolor_middle).place(x=x1,y=y1)
    Label(screen3, text="Category Downloads",font=("Open Sans", 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+175,y=y1+10)
    droplist = OptionMenu(screen3, cat, *category,command=lambda x : fetch_installs(cat,x1,y1))
    droplist.config(font=('Open Sans',13),width=30)
    cat.set('--Select a Category--')
    droplist.place(x=x1+160, y=y1+90) 
    Label(screen3, text="Category",font=("Open Sans", 18, 'bold'), fg=text_color,width=20,anchor=W, bg=bgcolor_middle).place(x=x1+60,y=y1+170)
    Label(screen3, text="Downloads",font=("Open Sans", 18, 'bold'), fg=text_color,width=18,anchor=W, bg=bgcolor_middle).place(x=x1+310,y=y1+170)
    
    #Section2
    x2=800# Change these parameters 
    y2=200# to shift the whole below section
    rangelist=["10000-50000","50000-150000","150000-500000","500000-5000000",">5000000"]
    Label(screen3, text="", width=95, height=18, bg=bgcolor_middle).place(x=x2,y=y2)
    Label(screen3, text="Number of Downloads",font=("Open Sans", 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+175,y=y2+10)
    droplist = OptionMenu(screen3, ran, *rangelist,command=lambda x : fetch_downloads(ran,x2,y2))
    droplist.config(font=('Open Sans',13),width=30)
    ran.set('--Select a Range--')
    droplist.place(x=x2+160, y=y2+90)
    Label(screen3, text="Range",font=("Open Sans", 18, 'bold'), fg=text_color,width=20,anchor=W, bg=bgcolor_middle).place(x=x2+60,y=y2+170)
    Label(screen3, text="No. of Apps",font=("Open Sans", 18, 'bold'), fg=text_color,width=18,anchor=W, bg=bgcolor_middle).place(x=x2+310,y=y2+170)
    
    """ 
    TABLULAR FORMAT
    Label(screen3, text="", width=80, height=15, bg=bgcolor_middle).place(x=620,y=200)
    Label(screen3, text="Number Of Downloads",font=("Open Sans", 20, 'bold'), fg='white', bg=bgcolor_middle).place(x=630,y=210)
    Label(screen3, text="Range",font=("Open Sans", 18, 'bold'), fg='white',width=20,anchor=W, bg=bgcolor_middle).place(x=640,y=250)
    Label(screen3, text="Downloads",font=("Open Sans", 18, 'bold'), fg='white',width=18,anchor=W, bg=bgcolor_middle).place(x=900,y=250)
    rangelist=[[10000,50000],[50000,150000],[150000,500000],[500000,5000000]]
    
    y1=310
    for i in range(4): # this loop will generate all input field for taking input from the user
        x1=640
        for j in range(2):
            e = Label(screen3,text=rangelist[i][j],font=("Open Sans", 12, 'bold'), fg='white',bg=bgcolor_middle)
            e.place(x=x1,y=y1)
            x1=x1+100
        y1=y1+30
    
    """ 
    #Section 3
    max_min_avg_downloads()
    x3=60# Change these parameters 
    y3=500# to shift the whole below section
    today = str(date.today())
    Label(screen3, text="", width=95, height=18, bg=bgcolor_middle).place(x=x3,y=y3)
    Label(screen3, text=max_cat_download+" Category has the MOST number of downloads\n as on "+today,font=("Open Sans", 15, 'bold'), fg='green', bg=bgcolor_middle,anchor=W).place(x=x3+20,y=y3+20)
    Label(screen3, text=avg_cat_download+" Category has AVERAGE number of downloads\n as on "+today,font=("Open Sans", 15, 'bold'), fg='yellow', bg=bgcolor_middle,anchor=W).place(x=x3+20,y=y3+100)
    Label(screen3, text=min_cat_download+" Category has the LEAST number of downloads\n as on "+today,font=("Open Sans", 15, 'bold'), fg='red', bg=bgcolor_middle,anchor=W).place(x=x3+20,y=y3+180)
    
    #Section 4
    high_rating = highest_rating()
    x4=800# Change these parameters 
    y4=500# to shift the whole below section
    Label(screen3, text="", width=95, height=18, bg=bgcolor_middle).place(x=x4,y=y4)
    Label(screen3, text="Highest Rating",font=("Open Sans", 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x4+240,y=y4+10)
    Label(screen3, text="Category with highest rating as on "+today+" is\n"+high_rating,font=("Open Sans", 18, 'bold'), fg=text_color, bg=bgcolor_middle,anchor=W).place(x=x4+20,y=y4+100)
    screen3.mainloop()    
stats()
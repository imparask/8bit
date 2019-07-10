from tkinter import *
from tkinter import messagebox
import re, pymysql
import statsmodels.api as sm
import pandas as pd 
import time
from datetime import date
from pylab import rcParams
from textblob import TextBlob
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression


matplotlib.rcParams['axes.labelsize']=14
matplotlib.rcParams['xtick.labelsize']=12
matplotlib.rcParams['ytick.labelsize']=12
matplotlib.rcParams['text.color']='k'

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


#Choose theme of window
color1 ='#CD3333'#TITLE COLOR
bgcolor_middle = '#5F9EA0'#BODY COLOR
color3 = '#00C957'#Button Color
text_color ='white'

#Fonts
title_font="Calibri"
body_font="Open Sans"

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
    
def data_wrangling():
    global apps,review
    #DATA WRANGLING
    #Taking data from database and storing in csv file
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore",use_unicode=True,charset="utf8")
    cursor = conn.cursor()
    query = "Select * from apps"
    results = pd.read_sql_query(query,conn)
    results.to_csv('F:\\Python Class\\Project\\apps.csv',index=False)
    conn.commit()
    conn.close()

    #Data wrangling of apps
    apps=pd.read_csv('F:\\Python Class\\Project\\apps.csv',encoding = "ISO-8859-1")
    
    apps['Last Updated'] = apps['Last Updated'].str.replace(',','')
    apps['Last Updated'] = apps['Last Updated'].str.replace('January','Jan')
    apps['Last Updated'] = apps['Last Updated'].str.replace('February','Feb')
    apps['Last Updated'] = apps['Last Updated'].str.replace('March','Mar')
    apps['Last Updated'] = apps['Last Updated'].str.replace('April','Apr')
    apps['Last Updated'] = apps['Last Updated'].str.replace('May','May')
    apps['Last Updated'] = apps['Last Updated'].str.replace('June','Jun')
    apps['Last Updated'] = apps['Last Updated'].str.replace('July','Jul')
    apps['Last Updated'] = apps['Last Updated'].str.replace('August','Aug')
    apps['Last Updated'] = apps['Last Updated'].str.replace('September','Sep')
    apps['Last Updated'] = apps['Last Updated'].str.replace('October','Oct')
    apps['Last Updated'] = apps['Last Updated'].str.replace('November','Nov')
    apps['Last Updated'] = apps['Last Updated'].str.replace('December','Dec')
    
    
 
    apps['App'] = apps['App'].str.replace('?','')
    apps['App'] = apps['App'].str.replace('(','')
    apps['App'] = apps['App'].str.replace(')','')
    apps=apps.drop([3750,6333,9306,10472],axis=0)

    apps=apps[apps.Rating.notnull()]
    
    apps['Installs'] = apps['Installs'].str.replace(',','')
    apps['Installs'] = apps['Installs'].str.replace('+','')
    
    date=apps['Last Updated']
    d=date.values.tolist()  #temp variable
    
    x=[]     #temp variable
    for i in d:
        conv=time.strptime(i,"%b %d %Y")
        x.append(time.strftime("%Y-%m-%d",conv))

    apps['Last Updated']=x
    
    apps['Last Updated'] = pd.to_datetime(apps['Last Updated'])
    apps['year'] = apps['Last Updated'].dt.year
    apps['month'] = apps['Last Updated'].dt.month
    
    #Taking data from database and storing in csv file
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore",use_unicode=True,charset="utf8")
    cursor = conn.cursor()
    query = "Select * from reviews"
    results = pd.read_sql_query(query,conn)
    results.to_csv('F:\\Python Class\\Project\\review.csv',index=False)
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
    review['App'] = review['App'].str.replace('?','')
    
        
def initialise():
    global cat_inst,category,installs_sum,installs,types,genres,contentrating
    cat_inst={}
    cat = apps.drop_duplicates(subset='Category', keep='first')
    category=[]
    for i in cat['Category']:
        category.append(i)
    category.sort()
    
    inst = apps.drop_duplicates(subset='Installs', keep='first')
    installs=[]
    for i in inst['Installs']:
        installs.append(int(i))
    installs.sort()
    for i in range(0,len(installs)):
        installs[i]=str(installs[i])
    
    typ = apps.drop_duplicates(subset='Type', keep='first')
    types=[]
    for i in typ['Type']:
        types.append(i)
        
    genr = apps.drop_duplicates(subset='Genres', keep='first')
    genres=[]
    for i in genr['Genres']:
        genres.append(i)
    genres.sort()
        
    contrat = apps.drop_duplicates(subset='Content Rating', keep='first')
    contentrating=[]
    for i in contrat['Content Rating']:
        contentrating.append(i)
        
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

#INSIGHTS1 SECTION STARTS HERE---------------------------------------------------

#INSIGHTS1b starts here--------------------------------------------------------
def display_review(rev,sen_reviews,x2,y2):
    rev=int(rev.get())
    
    Label(screen5b, text="Review : ",font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+20,y=y2+200)
    Label(screen5b,width=90,height=15, bg=bgcolor_middle).place(x=x2+20,y=y2+240)

    Label(screen5b, text=sen_reviews[rev-1],font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,wraplength=600,anchor=W).place(x=x2+20,y=y2+250)
    return
        
    
def get_num_reviews_of_app(app_name,sentiment_selected,x2,y2):
    
    rev=StringVar()
    app_name=str(app_name.get())
    sentiment_selected = str(sentiment_selected.get())
    
    if(app_name=="--Select Application--"):
        Label(screen5b, text="Please Select an Application",font=(body_font, 12, 'bold'), fg='red', bg=bgcolor_middle,width=25,anchor=W).place(x=x2+210,y=y2+80)
        return
    if(sentiment_selected=="--Select Sentiment--"):
        Label(screen5b, text="Please Select a Sentiment",font=(body_font, 12, 'bold'), fg='red', bg=bgcolor_middle,width=25,anchor=W).place(x=x2+210,y=y2+80)
        return
    
    x=review.loc[review['App'] == app_name]
    revi=x['Translated_Review'].tolist() 
    senti = x['Sentiment'].tolist()

    
    sen_reviews =[]
    for i in range(len(senti)):
        if senti[i] ==sentiment_selected:
            sen_reviews.append(revi[i])
            
    count=len(sen_reviews)
    number=[]
    for i in range(count):
        number.append(i+1) 
        

    droplist = OptionMenu(screen5b, rev, *number,command=lambda x : display_review(rev,sen_reviews,x2,y2))
    droplist.config(font=(body_font,11),width=35)
    rev.set('--Select Review Number--')
    droplist.place(x=x2+200, y=y2+80)    
          
def yearly_avg_download_month(x1,y1):
    
    all_years=[2010,2011,2012,2013,2014,2015,2016,2017,2018]
    all_month=['January','February','March','April','May','June','July','August','September','October','November','December']


    yearly_installs=[0,0,0,0,0,0,0,0,0,0,0,0]
    yearly_counter=[0,0,0,0,0,0,0,0,0,0,0,0]

    year_no=all_years[0]
    yy=40
    for i in range(9):
        yearly_installs=[0,0,0,0,0,0,0,0,0,0,0,0]
        yearly_counter=[0,0,0,0,0,0,0,0,0,0,0,0]
        for index,row in apps.iterrows():
            if row['year']==year_no:
                counter=1
                for j in range(12):
                    if row['month']==counter:
                        yearly_installs[j]+=int(row['Installs'])
                        yearly_counter[j]+=1
                    counter+=1
            
        for i in range(12):
            if yearly_counter[i]==0:
                continue
            else:
                yearly_installs[i]=round(yearly_installs[i]/yearly_counter[i],2)

        max_value = max(yearly_installs)
        max_index = yearly_installs.index(max_value)
        Label(screen5b, text=year_no,font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+40,y=y1+yy)
        Label(screen5b, text=all_month[max_index],font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+200,y=y1+yy)
        Label(screen5b, text=max_value,font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+420,y=y1+yy)
        yy+=60
        year_no+=1

def insight1b():
    global screen5b
    
    screen5b = Toplevel(screen5)
    ap=StringVar()
    se=StringVar()
    
    
    screen5b.title("INSIGHT 1")
    adjustWindow(screen5b)
    
    Label(screen5b, text="", width='500', height="20", bg=color1).pack() 
    Label(screen5b, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg=text_color, bg=color1).place(x=455,y=10)
    Button(screen5b, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen5b.destroy).place(x=1380, y=55)
    Label(screen5b, text="PAGE 3",font=(body_font, 14, 'bold'), fg=text_color, bg='#e79700').place(x=1435,y=100)
    Button(screen5b, text='PAGE 1', width=6, font=(body_font, 12, 'bold'), bg='#e79700', fg=text_color,command=insight1).place(x=1270, y=100)#, command=trends1
    Button(screen5b, text='PAGE 2', width=6, font=(body_font, 12, 'bold'), bg='#e79700', fg=text_color,command=insight1a).place(x=1350, y=100)#, command=trends1
           
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\review.png")
    label = Label(screen5b,borderwidth=0, image=photo1)
    label.place(x=0, y=152)
    
    
    #Section 1
    x1=40
    y1=170
    Label(screen5b, width=100, height=38, bg=bgcolor_middle).place(x=x1,y=y1)
    Label(screen5b, text="YEAR",font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+40,y=y1+10)
    Label(screen5b, text="MONTH",font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+210,y=y1+10)
    Label(screen5b, text="AVERAGE DOWNLOADS",font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+410,y=y1+10)
    yearly_avg_download_month(x1,y1)
    
    #Section 2
    x2=780# Change these parameters 
    y2=170# to shift the whole below section
    Label(screen5b, width=98, height=38, bg=bgcolor_middle).place(x=x2,y=y2)
    
    cat = review.drop_duplicates(subset='App', keep='first')
    app=[]
    app=cat['App'].tolist()
    droplist = OptionMenu(screen5b, ap, *app)
    droplist.config(font=(body_font,11),width=32)
    ap.set('--Select Application--')
    droplist.place(x=x2+20, y=y2+20)
    
    sentiments=['Positive','Negative','Neutral']
    droplist = OptionMenu(screen5b, se, *sentiments,command= lambda x : get_num_reviews_of_app(ap,se,x2,y2))
    droplist.config(font=(body_font,11),width=32)
    se.set('--Select Sentiment--')
    droplist.place(x=x2+350, y=y2+20)
  
    screen5b.mainloop()
#INSIGHT1b ends here-----------------------------------------------------------
    
#INSIGHT1a starts here--------------------------------------------------------    
def sentiment_ratio(req,x2,y2):
    
    cat = review.drop_duplicates(subset='App', keep='first')
    app=[]
    app=cat['App'].tolist()
     
    positive=[]
    negative=[]
    pos_perc=[]
    neg_perc=[]
    
    req = str(req.get())
    print(req)
    for i in app:
             
        pos=0
        neg=0
        x=review.loc[review['App'] == i]
   
        counter=x['Sentiment'].tolist()
   
   
        pos=counter.count("Positive")
        neg=counter.count("Negative")
       
        positive.append(pos)
        negative.append(neg)
    
    for i in range(len(app)):
        if positive[i]==0 and negative[i]==0:
            pos_perc.append(0)
            neg_perc.append(0)
        else:
            pos_perc.append(round((positive[i]/(positive[i]+negative[i]))*100,2))
            neg_perc.append(round((negative[i]/(positive[i]+negative[i]))*100,2))
    yy=45
    xx=20 
    
    
    Label(screen5a, width=66, height=35, bg=bgcolor_middle).place(x=30,y=210)
    Label(screen5a, width=66, height=38, bg=bgcolor_middle).place(x=525,y=170)
    Label(screen5a, width=68, height=38, bg=bgcolor_middle).place(x=1015,y=170)
  
              
    if(req=="APPS WITH APPROX SAME RATIO"):
        k=1
        for i in range(len(app)):
            if positive[i]!=0 and negative[i]!=0 and positive[i]/negative[i]>=0.95 and positive[i]/negative[i]<=1.05:
                Label(screen5a, text="{0}. {1}".format(k,app[i]),font=(body_font, 13, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+xx,y=y2+yy)
                yy+=20
                k+=1
                if(k==27 or k==55 ):
                    xx+=490
                    yy=10
                
        return
       
    elif(req=="APPS WITH MOST POSITIVE SENTIMENT"):
        k=1
        max_value_pos = max(pos_perc)
        for i in range(len(app)):
            if pos_perc[i]==max_value_pos:
                Label(screen5a, text="{0}. {1}".format(k,app[i]),font=(body_font, 13, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+xx,y=y2+yy)
                yy+=20
                k+=1
                if(k==27 or k==55 ):
                    xx+=490
                    yy=10
                
        return
    
    elif(req=="APPS WITH MOST NEGATIVE SENTIMENT"):
        
        max_value_neg = max(neg_perc)
        k=1
        for i in range(len(app)):
            if neg_perc[i]==max_value_neg:
                Label(screen5a, text="{0}. {1}".format(k,app[i]),font=(body_font, 13, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+xx,y=y2+yy)
                yy+=20
                k+=1
                if(k==27 or k==55 ):
                    xx+=490
                    yy=10
        
        return

def insight1a():
    global screen5a
    
    screen5a = Toplevel(screen5)
    req=StringVar()
    
    screen5a.title("INSIGHT 1")
    adjustWindow(screen5a)
    
    Label(screen5a, text="", width='500', height="20", bg=color1).pack() 
    Label(screen5a, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg=text_color, bg=color1).place(x=455,y=10)
    Button(screen5a, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen5a.destroy).place(x=1380, y=55)
    Label(screen5a, text="PAGE 2",font=(body_font, 14, 'bold'), fg=text_color, bg='#e79700').place(x=1350,y=100)
    Button(screen5a, text='PAGE 1', width=6, font=(body_font, 12, 'bold'), bg='#e79700', fg=text_color,command=insight1).place(x=1270, y=100)#, command=trends1
    Button(screen5a, text='PAGE 3', width=6, font=(body_font, 12, 'bold'), bg='#e79700', fg=text_color,command=insight1b).place(x=1435, y=100)#, command=trends1
           
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\review.png")
    label = Label(screen5a,borderwidth=0, image=photo1)
    label.place(x=0, y=152)
    
    
    #Section 1
    x1=30
    y1=170
    Label(screen5a, width=66, height=38, bg=bgcolor_middle).place(x=x1,y=y1)
    require=["APPS WITH APPROX SAME RATIO","APPS WITH MOST POSITIVE SENTIMENT","APPS WITH MOST NEGATIVE SENTIMENT"]

    droplist = OptionMenu(screen5a, req, *require,command = lambda x:  sentiment_ratio(req,x1,y1))
    droplist.config(font=(body_font,11),width=35)
    req.set('--Select Requirement--')
    droplist.place(x=x1+65, y=y1+10)
   
    
    #Section 2
    x2=525# Change these parameters 
    y2=170# to shift the whole below section
    Label(screen5a, width=66, height=38, bg=bgcolor_middle).place(x=x2,y=y2)
    
    #Section 3
    x3=1015# Change these parameters 
    y3=170# to shift the whole below section
    Label(screen5a, width=68, height=38, bg=bgcolor_middle).place(x=x3,y=y3)
  
    
    screen5a.mainloop()

#INSIGHT1a ends here-----------------------------------------------------------
    
def rel_polarity_subjectivity(x1,y1):
    x=review['Sentiment_Polarity'].values.reshape(-1,1)
    y=review['Sentiment_Subjectivity'].values.reshape(-1,1)
    reg=LinearRegression()
    reg.fit(x,y)
    
    
    m=round(reg.coef_[0][0],5)
    c=round(reg.intercept_[0],5)
    result="Y = "+str(m)+"X + "+str(c)  
    
    predictions=reg.predict(x)
    
    f=plt.figure(figsize=(8,7),dpi=70)
    ax3 = f.add_subplot(111)
    

    ax3.scatter(review['Sentiment_Polarity'],review['Sentiment_Subjectivity'],c='blue',alpha=0.1)
    ax3.plot(review['Sentiment_Polarity'],predictions,c='red',linewidth=2)
    ax3.set_ylabel("Sentiment Subjectivity")
    ax3.set_xlabel("Sentiment Polarity")
    
    Label(screen5, text=result,font=(body_font, 14, 'bold'), fg=text_color, bg=bgcolor_middle,width=40,anchor=W).place(x=x1+20,y=y1+50)

    canvas = FigureCanvasTkAgg(f, master=screen5)
    canvas.get_tk_widget().place(x=x1+70,y=y1+90)
    canvas.draw()



def size_installs(x2,y2):
    temp = review.drop_duplicates(subset='App', keep='first')
    app=temp['App'].tolist()

    indexNames = apps[ apps['Size'] == "Varies with device" ].index
     
    # Delete these row indexes from dataFrame
    apps.drop(indexNames , inplace=True)
    
    
    temp=apps['Size'].tolist()
    
    size=[]
    for i in temp:
        if 'M' in i:
            x=i.replace("M","")
            size.append(float(x)*1024)
        elif 'k' in i:
            x=i.replace("k","")
            size.append(float(x))
            
    apps['Size']=size
    
    sum1=0
    sum2=0
    sum3=0
    sum4=0
    sum5=0
    sum6=0
    
    for index,row in apps.iterrows():
        if row['Size']>=0 and row['Size']<20000:
            sum1+=int(row['Installs'])
        elif row['Size']>=20000 and row['Size']<40000:
            sum2+=int(row['Installs'])
        elif row['Size']>=40000 and row['Size']<60000:
            sum3+=int(row['Installs'])
        elif row['Size']>=60000 and row['Size']<80000:
            sum4+=int(row['Installs'])
        elif row['Size']>=80000 and row['Size']<100000:
            sum5+=int(row['Installs'])
        elif row['Size']>=100000 and row['Size']<120000:
            sum6+=int(row['Installs'])
    
    sum1/=1000000
    sum2/=1000000
    sum3/=1000000
    sum4/=1000000
    sum5/=1000000
    sum6/=1000000
    
    list_installs=[]
    list_installs.append(sum1)
    list_installs.append(sum2)
    list_installs.append(sum3)
    list_installs.append(sum4)
    list_installs.append(sum5)
    list_installs.append(sum6)
    
    activities = ['0-20 Mb', '20-40 Mb', '40-60 Mb', '60-80 Mb','80-100 Mb','100-120 Mb']
    colors = ['red', 'yellow', 'green', 'blue','orange','pink'] 
      
    
    f=plt.figure(figsize=(8,7),dpi=70)
    ax4 = f.add_subplot(111)
    
    # plotting the pie chart 
    ax4.pie(list_installs, labels = activities, colors=colors,  
            startangle=0, shadow = True,  
            radius = 1.0, autopct = '%1.1f%%') 
    
    canvas = FigureCanvasTkAgg(f, master=screen5)
    canvas.get_tk_widget().place(x=x2+80,y=y2+90)
    canvas.draw()

def insight1():
    global screen5
    
    screen5 = Toplevel(screen)
    
    screen5.title("INSIGHT 1")
    adjustWindow(screen5)
    
    Label(screen5, text="", width='500', height="20", bg=color1).pack() 
    Label(screen5, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg=text_color, bg=color1).place(x=455,y=10)
    Button(screen5, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen5.destroy).place(x=1380, y=55)
    Label(screen5, text="PAGE 1",font=(body_font, 14, 'bold'), fg=text_color, bg='#e79700').place(x=1270,y=100)
    Button(screen5, text='PAGE 2', width=6, font=(body_font, 12, 'bold'), bg='#e79700', fg=text_color,command=insight1a).place(x=1350, y=100)#, command=trends1
    Button(screen5, text='PAGE 3', width=6, font=(body_font, 12, 'bold'), bg='#e79700', fg=text_color,command=insight1b).place(x=1435, y=100)#, command=trends1
      
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\review.png")
    label = Label(screen5,borderwidth=0, image=photo1)
    label.place(x=0, y=152)
    
    
    #Section 1
    x1=30# Change these parameters 
    y1=170# to shift the whole below section
    Label(screen5, text="", width=100, height=40, bg=bgcolor_middle).place(x=x1,y=y1)
    Label(screen5, text="Relation between Sentiment Polarity and Sentiment Subjectivity",font=(body_font, 16, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+20,y=y1+5)
    rel_polarity_subjectivity(x1,y1)
    
    #Section 2
    x2=780# Change these parameters 
    y2=170# to shift the whole below section
    Label(screen5, text="", width=100, height=40, bg=bgcolor_middle).place(x=x2,y=y2)
    Label(screen5, text="Pie Chart of size of the app and no. of downloads",font=(body_font, 16, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+20,y=y2+5)
    size_installs(x2,y2) 
  
    screen5.mainloop()
        
#INSIGHTS1 SECTION ENDS HERE-----------------------------------------------------
    
#INSIGHTS2 SECTION STARTS HERE----------------------------------------------------

#INSIGHTS2a SECTION STARTS HERE----------------------------------------------------

def quarter_report():
    x1=40
    y1=180
    all_years=[2010,2011,2012,2013,2014,2015,2016,2017,2018]
    all_month=['January-February-March','April-May-June','July-August-September','October-November-December']

    years, months = (len(all_years),len(all_month)) 
    quarterly_downloads = [[0 for i in range(months)] for j in range(years)] 
    
    for index,row in apps.iterrows(): 
        year_no=all_years[0]
        for i in range(years): 
            if row['year']==year_no:
                if row['month']==1 or row['month']==2 or row['month']==3:
                    quarterly_downloads[i][0]+=int(row['Installs'])
                elif row['month']==4 or row['month']==5 or row['month']==6:
                    quarterly_downloads[i][1]+=int(row['Installs'])
                elif row['month']==7 or row['month']==8 or row['month']==9:
                    quarterly_downloads[i][2]+=int(row['Installs'])
                elif row['month']==10 or row['month']==11 or row['month']==12:
                    quarterly_downloads[i][3]+=int(row['Installs'])
            year_no+=1

    
    max_month_downloads=list(map(max, quarterly_downloads))
    yy=50
    year_var=all_years[0]
    for i in range(years):
        Label(screen4a, text=year_var,font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+50,y=y1+yy)
        year_var+=1
        for j in range(months):
            if max_month_downloads[i]==quarterly_downloads[i][j]:
                Label(screen4a, text=all_month[j],font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+150,y=y1+yy)
                Label(screen4a, text=max_month_downloads[i],font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+460,y=y1+yy)
                yy+=60


def downloads_n_ratings(noi,rt,x2,y2):
 
    lessdownloadsmoreratings=0
    moredownloadslessratings=0
    moredownloadsmoreratings=0
    lessdownloadslessratings=0
    
    rt = str(rt.get())
    noi = str(noi.get())
    
    if(noi=="" or rt==""):
         Label(screen4a, text="Please fill all details",font=(body_font, 11, 'bold'), fg='red', bg=bgcolor_middle,width=24,anchor=W,).place(x=x2+550,y=y2+70)
         return
    if(re.match("^\d+(\.\d{0,1})?$",rt) and int(rt)>=0 and int(rt)<=5):
        if(re.match("^[0-9]*$",noi)):
            rt = float(rt)
            for index,row in apps.iterrows():
                if row['Installs'] >= noi:
                    if row['Rating']>=rt:
                        moredownloadsmoreratings+=1
                    else:
                        moredownloadslessratings+=1
                elif row['Installs'] < noi:
                    if row['Rating']>=rt:
                        lessdownloadsmoreratings+=1 
                    else:
                        lessdownloadslessratings+=1 

            Label(screen4a, text="More than {0} downloads and rating above {1} : {2}".format(noi,rt,moredownloadsmoreratings),font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+30,y=y2+120)
            Label(screen4a, text="More than {0} downloads and rating below {1} : {2}".format(noi,rt,moredownloadslessratings),font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+30,y=y2+160)
            Label(screen4a, text="Less than {0} downloads and rating above {1} : {2}".format(noi,rt,lessdownloadsmoreratings),font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+30,y=y2+200)
            Label(screen4a, text="Less than {0} downloads and rating below {1} : {2}".format(noi,rt,lessdownloadslessratings),font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+30,y=y2+240)
            Label(screen4a, text="",width=29,font=(body_font, 11, 'bold'), bg=bgcolor_middle).place(x=x2+500,y=y2+95)
            return  
        else:
            Label(screen4a, text="Enter Valid Number of installs",font=(body_font, 11, 'bold'), fg='red', bg=bgcolor_middle,width=24,anchor=W,).place(x=x2+550,y=y2+95)
            return  
    else:
        Label(screen4a, text="Enter Valid Rating",font=(body_font, 11, 'bold'), fg='red', bg=bgcolor_middle,width=24,anchor=W).place(x=x2+550,y=y2+95)
        return

def compare_prediction(category1,cat,x3,y3):
    
    cat = str(cat.get())
    
    year2017_total=[]
    year2018_total=[]
    perc_incre=[]
    
    for i in category1:
        total17=0
        total18=0 
        for index,row in apps.iterrows():
            if i==row['Category']:
                if row['year']==2017:
                    total17+=int(row['Installs'])
                elif row['year']==2018:
                    total18+=int(row['Installs'])
        year2017_total.append(total17)
        year2018_total.append(total18)
    

    for i in range(len(category1)):
        perc_incre.append(round(((year2018_total[i]-year2017_total[i])/year2017_total[i])*100,2))
    
    ind = category1.index(cat)
    percent = perc_incre[ind]
    Label(screen4a, text="Percentage increase in downloads of {0} \nfrom 2017 to 2018 : {1}%".format(cat,str(percent)), font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=50, anchor=W).place(x=x3+20, y=y3+200)


def predict_category(category1,x3,y3):
    
    year2017_total=[]
    year2018_total=[]
    perc_incre=[]
    
    for i in category1:
        total17=0
        total18=0 
        for index,row in apps.iterrows():
            if i==row['Category']:
                if row['year']==2017:
                    total17+=int(row['Installs'])
                elif row['year']==2018:
                    total18+=int(row['Installs'])
        year2017_total.append(total17)
        year2018_total.append(total18)

    for i in range(len(category1)):
        perc_incre.append(round(((year2018_total[i]-year2017_total[i])/year2017_total[i])*100,2))
    
    
    max_value = max(perc_incre)
    Label(screen4a, text="Percentage increase in downloads from 2017 to 2018 : "+str(max_value), font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x3+20, y=y3+80)

    max_index = perc_incre.index(max_value)
    Label(screen4a, text="CATEGORY OF APP MOST LIKELY TO BE DOWNLOADED is\n "+str(category1[max_index]), font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x3+20, y=y3+20)

    
def insight2a():
    global screen4a
    
    screen4a=Toplevel(screen4)
    rt=StringVar()
    noi=StringVar()
    cat = StringVar()
    
    adjustWindow(screen4a)
    screen4a.title("INSIGHT 2")
    
    Label(screen4a, text="", width='500', height="20", bg=color1).pack() 
    Label(screen4a, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg=text_color, bg=color1).place(x=475,y=10)
    Button(screen4a, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen4a.destroy).place(x=1380, y=55)
    Label(screen4a, text="PAGE 2",font=(body_font, 14, 'bold'), fg=text_color, bg='#e79700').place(x=1430,y=100)
    Button(screen4a, text='PAGE 1', width=6, font=(body_font, 12, 'bold'), bg='#e79700', fg=text_color,command=insight2).place(x=1350, y=100)#, command=trends1
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\trend.png") # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(screen4a,borderwidth=0, image=photo1) # attaching image to the label
    label.place(x=0, y=152)
    
    #Section 1
    x1=40
    y1=180
    Label(screen4a, width=89, height=38, bg=bgcolor_middle).place(x=x1,y=y1)
    Label(screen4a, text="YEAR",font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+50,y=y1+10)
    Label(screen4a, text="QUATER SPAN",font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+205,y=y1+10)
    Label(screen4a, text="DOWNLOADS",font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+440,y=y1+10)

    Button(screen4a, text="LOAD DATA", bg="#e79700", width=10, font=(body_font, 10, 'bold'), fg=text_color, command=quarter_report).place(x=x1+260,y=y1+290)

    #Section 2
    x2=710
    y2=180
    Label(screen4a, width=110, height=18, bg=bgcolor_middle).place(x=x2,y=y2)
    Label(screen4a, text="Number of Apps having :", font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x2+20, y=y2+10)

    Label(screen4a, text="Rating - ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x2+20, y=y2+50)
    Entry(screen4a,textvar=rt,font=('Open Sans',12),width=18).place(x=x2+110, y=y2+50)
    Label(screen4a, text="Eg : 4.1(out of 5)", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x2+110, y=y2+75)
    
    Label(screen4a, text="No. of Installs - ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x2+330, y=y2+50)
    Entry(screen4a,textvar=noi,font=('Open Sans',12),width=18).place(x=x2+490, y=y2+50)
    Label(screen4a, text="Eg : 100000", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x2+490, y=y2+75)
    
    Button(screen4a, text="OK", bg="#e79700", width=6, font=(body_font, 10, 'bold'), fg=text_color, command=lambda: downloads_n_ratings(noi,rt,x2,y2)).place(x=x2+700,y=y2+50)

    #Section 3
    x3=710
    y3=480
    Label(screen4a, width=110, height=18, bg=bgcolor_middle).place(x=x3,y=y3)
    category1=['SPORTS','ENTERTAINMENT','SOCIAL','NEWS_AND_MAGAZINES','EVENTS','TRAVEL_AND_LOCAL','GAME']
    category1.sort()
    
    predict_category(category1,x3,y3)
    Label(screen4a, text="Compare with other categories - ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x3+20, y=y3+140)

    droplist = OptionMenu(screen4a, cat, *category1,command = lambda x: compare_prediction(category1,cat,x3,y3))
    droplist.config(font=(body_font,10),width=24)
    cat.set('--Select Category--')
    droplist.place(x=x3+350, y=y3+140)

    
    screen4a.mainloop()
#INSIGHT2a SECTION ENDS HERE-----------------------------------------------------
       
def download_trend(cat,x1,y1):
    
    cat=str(cat.get()) 
    category_name=apps.loc[apps['Category']==cat]
    cols=['App','Category','Rating','Reviews','Size','Type','Price','Content Rating','Genres','Current Ver','Android Ver','year','month']
    category_name.drop(cols,axis=1,inplace=True)
    category_name=category_name.sort_values('Last Updated')
    x=[]
    for i in category_name['Installs']:
        x.append(int(i))
    
    category_name['Installs']=x   
   
    
    category_name['Last Updated']=pd.to_datetime(category_name['Last Updated'])
    category_name=category_name.set_index('Last Updated')
    decomposition=sm.tsa.seasonal_decompose(category_name,model="additive",freq=30)
    fig=decomposition.plot()
    
    rcParams['figure.figsize']=6,6
    canvas = FigureCanvasTkAgg(fig, master=screen4)
    canvas.get_tk_widget().place(x=x1+50,y=y1+120)
    canvas.draw()

def year_wise_downloads_percentage(x4,y4):
    
    year=[2016,2017,2018]
    list_sum_year=[]
    sum_per_category=[]
    total_installs=[]
    for i in year:
        total_installs.append(0)
        list_sum_year.append([])#Double list as per number of years
        sum_per_category.append(0)
 
    for i in category:
        for index,row in apps.iterrows():
            if i==row['Category']:
                for j in year:
                    if row['year']==j:
                        ind=year.index(j)
                        sum_per_category[ind]=sum_per_category[ind]+int(row['Installs'])
        for j in range(len(year)):
            list_sum_year[j].append(sum_per_category[j])
            sum_per_category[j]=0
               
    high_low=[]
    for i in range(len(year)):
        high_low.append([])
        high_low[i].append(min(list_sum_year[i]))
        high_low[i].append(max(list_sum_year[i]))

    highest_lowest=['LOWEST','HIGHEST']

    yy=20
    for i in year:
        ind = year.index(i)
        for j in highest_lowest:
            indx = highest_lowest.index(j)
            value=high_low[ind][indx]
            Label(screen4, text="Category with {0} downloads in {1}: {2} ({3})".format(j,i,category[list_sum_year[ind].index(value)],value),font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=70,anchor=W).place(x=x4+20,y=y4+yy)
            yy=yy+40
            
    for i in range(len(total_installs)):
        total_installs[i]=sum(list_sum_year[i])
 
    yy=yy+20
    for i in range(len(total_installs)-1):
        diff = total_installs[i+1]-total_installs[i]
        inc_dec='INCREASE'
        if(diff < 0):
            inc_dec = 'DECREASE'
        percentage = (diff/total_installs[i])*100
        Label(screen4, text="Percentage {0} from {1} to {2} : {3}%".format(inc_dec,year[i],year[i+1],round(percentage,2)),font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=70,anchor=W).place(x=x4+20,y=y4+yy)
        yy=yy+40
        
    for i in apps:
        android_spec=0
        android_varies=0
        for index,row in apps.iterrows():
            if row['Android Ver']=='Varies with device':
                android_spec=android_spec+int(row['Installs'])
            else:
                android_varies=android_varies+int(row['Installs'])   
    
    yy=yy+20
    inc_dec='INCREASE'
    diff = android_varies-android_spec
    if(diff < 0):
        inc_dec='DECREASE'
    percent = (diff/android_spec)*100
    Label(screen4, text="Percentage {0} of apps whose Android Version 'Varies With Device' is : {1}% ".format(inc_dec,round(percent,2)),font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=70,anchor=W).place(x=x4+20,y=y4+yy)
    
def ratio_content_rating(one,two,x3,y3):
    
    one = str(one.get())
    two = str(two.get())
   
    if(one=='--Select 1st Content Rating--' or two=='--Select 2nd Content Rating--'):
        Label(screen4, text="Please select both content ratings..!!".format(one,two,ratio),font=(body_font, 12, 'bold'), fg=text_color, bg=bgcolor_middle,width=25,anchor=W).place(x=x3+20,y=y3+40)
        return
    one_downloads=0
    two_downloads=0
    try:
        for i in apps:
            for index,row in apps.iterrows():
                if row['Content Rating'] == one:
                    one_downloads+=int(row['Installs'])
                if row['Content Rating'] == two:
                    two_downloads+=int(row['Installs'])
        
        ratio = round(one_downloads/two_downloads,2)
        print(ratio)
        Label(screen4, text="Ratio of downloads is {2}".format(one,two,ratio),font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle,width=25,anchor=W).place(x=x3+60,y=y3+70)

    except ZeroDivisionError:
        return


def category_best_month(cat,x2,y2):
    
    all_years=[2010,2011,2012,2013,2014,2015,2016,2017,2018]
    all_month=['January','February','March','April','May','June','July','August','September','October','November','December']

    years, months = (len(all_years), len(all_month)) 
    monthly_downloads = [[0 for i in range(months)] for j in range(years)] 
   
    i=str(cat.get())
    Label(screen4, text=i,font=(body_font, 12, 'bold'), fg=text_color, bg=bgcolor_middle,width=25,anchor=W).place(x=x2+20,y=y2+80)

    monthly_downloads = [[0 for i in range(months)] for j in range(years)] 
    for index,row in apps.iterrows():
        if i==row['Category']:
            if row['year']==2010:
                j=0
            elif row['year']==2011:
                j=1
            elif row['year']==2012:
                j=2
            elif row['year']==2013:
                j=3
            elif row['year']==2014:
                j=4
            elif row['year']==2015:
                j=5
            elif row['year']==2016:
                j=6
            elif row['year']==2017:
                j=7
            elif row['year']==2018:
                j=8    
            if row['month']==1:
                monthly_downloads[j][0]+=int(row['Installs'])
            elif row['month']==2:
                monthly_downloads[j][1]+=int(row['Installs'])
            elif row['month']==3:
                monthly_downloads[j][2]+=int(row['Installs'])
            elif row['month']==4:
                monthly_downloads[j][3]+=int(row['Installs'])
            elif row['month']==5:
                monthly_downloads[j][4]+=int(row['Installs'])
            elif row['month']==6:
                monthly_downloads[j][5]+=int(row['Installs'])
            elif row['month']==7:
                monthly_downloads[j][6]+=int(row['Installs'])
            elif row['month']==8:
                monthly_downloads[j][7]+=int(row['Installs'])
            elif row['month']==9:
                monthly_downloads[j][8]+=int(row['Installs'])
            elif row['month']==10:
                monthly_downloads[j][9]+=int(row['Installs'])
            elif row['month']==11:
                monthly_downloads[j][10]+=int(row['Installs'])
            elif row['month']==12:
                monthly_downloads[j][11]+=int(row['Installs'])        

    max_month_category=max(map(max, monthly_downloads))
    
    max_element_category=[(ix,iy) for ix, row in enumerate(monthly_downloads) for iy, i in enumerate(row) if i == max_month_category]
    for i in range(9):
        if max_element_category[0][0]==i:
            y = all_years[i]
            for j in range(12):
                if max_element_category[0][1]==j:
                    Label(screen4, text=str(all_month[j])+" ("+str(y)+")\n"+str(max_month_category),font=(body_font, 12, 'bold'), fg=text_color, bg=bgcolor_middle,width=15,anchor=W).place(x=x2+260,y=y2+80)

                    
def insight2():
    global screen4,cat
    
    screen4=Toplevel(screen)
    cat=StringVar()
    cat1=StringVar()
    cr1=StringVar()
    cr2=StringVar()
    adjustWindow(screen4)
    screen4.title("INSIGHT 2")
    
    Label(screen4, text="", width='500', height="20", bg=color1).pack() 
    Label(screen4, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg=text_color, bg=color1).place(x=475,y=10)
    Button(screen4, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen4.destroy).place(x=1380, y=55)
    Label(screen4, text="PAGE 1",font=(body_font, 14, 'bold'), fg=text_color, bg='#e79700').place(x=1350,y=100)
    Button(screen4, text='PAGE 2', width=6, font=(body_font, 12, 'bold'), bg='#e79700', fg=text_color,command=insight2a).place(x=1430, y=100)#, command=trends1
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\trend.png") # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(screen4,borderwidth=0, image=photo1) # attaching image to the label
    label.place(x=0, y=152)
    
    #Section 1
    x1=30# Change these parameters 
    y1=170# to shift the whole below section
    Label(screen4, text="", width=76, height=40, bg=bgcolor_middle).place(x=x1,y=y1)
    Label(screen4, text="Download Trends",font=(body_font, 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+145,y=y1+5)
    droplist = OptionMenu(screen4, cat, *category,command=lambda x : download_trend(cat,x1,y1))
    droplist.config(font=(body_font,10),width=30)
    cat.set('--Select a Category--')
    droplist.place(x=x1+140, y=y1+45) 
    
    #Section 2
    x2=590
    y2=170
    Label(screen4, text="", width=62, height=8, bg=bgcolor_middle).place(x=x2,y=y2)
    droplist = OptionMenu(screen4, cat1, *category,command=lambda x : category_best_month(cat1,x2,y2))
    droplist.config(font=(body_font,10),width=30)
    cat1.set('--Select a Category--')
    droplist.place(x=x2+100, y=y2+10) 
    Label(screen4, text="Category",font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+30,y=y2+50)
    Label(screen4, text="BEST MONTH",font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+260,y=y2+50)
    
    #Section 3
    x3=1050
    y3=170
    Label(screen4, text="", width=62, height=8, bg=bgcolor_middle).place(x=x3,y=y3)
    droplist = OptionMenu(screen4, cr1, *contentrating)
    droplist.config(font=(body_font,10),width=22)
    cr1.set('--Select 1st Content Rating--')
    droplist.place(x=x3+10, y=y3+10)
    
    Label(screen4, text="/",font=(body_font, 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x3+215,y=y3+10)

    droplist = OptionMenu(screen4, cr2, *contentrating,command=lambda x : ratio_content_rating(cr1,cr2,x3,y3))
    droplist.config(font=(body_font,10),width=22)
    cr2.set('--Select 2nd Content Rating--')
    droplist.place(x=x3+230, y=y3+10)
    
    
    #Section 4
    x4=590# Change these parameters 
    y4=320# to shift the whole below section
    Label(screen4, text="", width=128, height=30, bg=bgcolor_middle).place(x=x4,y=y4)
    Button(screen4, text="LOAD DATA", bg="#e79700", width=10, font=(body_font, 10, 'bold'), fg=text_color, command=lambda : year_wise_downloads_percentage(x4,y4)).place(x=x4+20,y=y4+20)

    
    screen4.mainloop()

#INSIGHT 2 SECTION ENDS HERE----------------------------------------------
    
#STATS SECTION STARTS HERE----------------------------------------------

def fetch_installs(cat,x1,y1):
    cat = str(cat.get())
    if(cat=="--Select a Category--"):
        messagebox.showerror("Error", "Please select proper category", parent=screen4)
    else:
        for i in cat_inst:
            if(i==cat):
                Label(screen3, text=i,font=(body_font, 15, 'bold'), fg=text_color,anchor=W,width=20, bg=bgcolor_middle).place(x=x1+60,y=y1+220)
                Label(screen3, text=cat_inst[i],font=(body_font, 15, 'bold'), fg=text_color,anchor=W,width=20, bg=bgcolor_middle).place(x=x1+310,y=y1+220)
                
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
        
    Label(screen3, text=ran,font=(body_font, 15, 'bold'), fg=text_color,anchor=W,width=20, bg=bgcolor_middle).place(x=x2+60,y=y2+220)
    Label(screen3, text=installs,font=(body_font, 15, 'bold'), fg=text_color,width=20, bg=bgcolor_middle).place(x=x2+310,y=y2+220)
        

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
                     
def stats():
    global screen3,cat,ran
    
    screen3 = Toplevel(screen)
    cat=StringVar()
    ran=StringVar()
    screen3.title("STATISTICS")
    adjustWindow(screen3)    
    
    
    Label(screen3, text="", width='500', height="20", bg=color1).pack() 
    Label(screen3, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg=text_color, bg=color1).place(x=475,y=10)
    Button(screen3, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen3.destroy).place(x=1380, y=55)
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\stats.png") # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(screen3,borderwidth=0, image=photo1) # attaching image to the label
    label.place(x=0, y=152)
    
    #Section 1
    x1=60# Change these parameters 
    y1=200# to shift the whole below section
    Label(screen3, text="", width=95, height=18, bg=bgcolor_middle).place(x=x1,y=y1)
    Label(screen3, text="Category Downloads",font=(body_font, 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+175,y=y1+10)
    droplist = OptionMenu(screen3, cat, *category,command=lambda x : fetch_installs(cat,x1,y1))
    droplist.config(font=('Open Sans',13),width=30)
    cat.set('--Select a Category--')
    droplist.place(x=x1+160, y=y1+90) 
    Label(screen3, text="Category",font=(body_font, 18, 'bold'), fg=text_color,width=20,anchor=W, bg=bgcolor_middle).place(x=x1+60,y=y1+170)
    Label(screen3, text="Downloads",font=(body_font, 18, 'bold'), fg=text_color,width=18,anchor=W, bg=bgcolor_middle).place(x=x1+310,y=y1+170)
    
    #Section2
    x2=800# Change these parameters 
    y2=200# to shift the whole below section
    rangelist=["10000-50000","50000-150000","150000-500000","500000-5000000",">5000000"]
    Label(screen3, text="", width=95, height=18, bg=bgcolor_middle).place(x=x2,y=y2)
    Label(screen3, text="Number of Downloads",font=(body_font, 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+175,y=y2+10)
    droplist = OptionMenu(screen3, ran, *rangelist,command=lambda x : fetch_downloads(ran,x2,y2))
    droplist.config(font=('Open Sans',13),width=30)
    ran.set('--Select a Range--')
    droplist.place(x=x2+160, y=y2+90)
    Label(screen3, text="Range",font=(body_font, 18, 'bold'), fg=text_color,width=20,anchor=W, bg=bgcolor_middle).place(x=x2+60,y=y2+170)
    Label(screen3, text="No. of Apps",font=(body_font, 18, 'bold'), fg=text_color,width=18,anchor=W, bg=bgcolor_middle).place(x=x2+310,y=y2+170)
    
    #Section 3
    x3=60# Change these parameters 
    y3=500# to shift the whole below section
    today = str(date.today())
    max_cat_download=category[installs_sum.index(max(installs_sum))]
    min_cat_download=category[installs_sum.index(min(installs_sum))]
    
    avg_number_of_installs = float(sum(installs_sum)/len(installs_sum))
    num_in_installs_sum_list = min(installs_sum,key=lambda x:abs(x-avg_number_of_installs))#gives me the closest number to avg in the installs_sum list
    avg_cat_download=category[installs_sum.index(num_in_installs_sum_list)]
    
    Label(screen3, text="", width=95, height=18, bg=bgcolor_middle).place(x=x3,y=y3)
    Label(screen3, text=max_cat_download+" Category has the MOST number of downloads\n as on "+today,font=(body_font, 15, 'bold'), fg='green', bg=bgcolor_middle,anchor=W).place(x=x3+20,y=y3+20)
    Label(screen3, text=avg_cat_download+" Category has AVERAGE number of downloads\n as on "+today,font=(body_font, 15, 'bold'), fg='yellow', bg=bgcolor_middle,anchor=W).place(x=x3+20,y=y3+100)
    Label(screen3, text=min_cat_download+" Category has the LEAST number of downloads\n as on "+today,font=(body_font, 15, 'bold'), fg='red', bg=bgcolor_middle,anchor=W).place(x=x3+20,y=y3+180)
    
    #Section 4
    high_rating = highest_rating()
    x4=800# Change these parameters 
    y4=500# to shift the whole below section
    Label(screen3, text="", width=95, height=18, bg=bgcolor_middle).place(x=x4,y=y4)
    Label(screen3, text="Highest Rating",font=(body_font, 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x4+240,y=y4+10)
    Label(screen3, text="Category with highest rating as on "+today+" is\n"+high_rating,font=(body_font, 18, 'bold'), fg=text_color, bg=bgcolor_middle,anchor=W).place(x=x4+20,y=y4+100)
    screen3.mainloop()

#STATS SECTION ENDS HERE-------------------------------------------------

#REGISTRATION SECTION STARTS HERE----------------------------------------    
def duplicateEntry(gender_value):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore")
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE Name='"+fullname.get()+"'AND PhoneNo='"+phoneno.get()+"'AND Gender='"+gender_value+"'AND Email='"+email.get()+"'AND Password='"+password.get()+"'"
    lst=cursor.execute(query)
    connection.commit()
    connection.close()
    if lst:
        return True
    return False
        
def register_user(x1,y1):
    if fullname.get() and email.get() and password.get() and repassword.get() and gender.get() and phoneno.get() : # checking for all empty values in entry field
        if tnc.get(): # checking for acceptance of agreement
            if re.match("^((\+)?(\d{2}[-]))?(\d{10}){1}?$",phoneno.get()):
                if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email.get()): # validating the email
                    if password.get() == repassword.get() and re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",password.get()): # checking both password match or not
                        # if u enter in this block everything is fine just enter the values in database
                        gender_value = 'male'
                        if gender.get() == 2:
                            gender_value = 'female'
                        status = duplicateEntry(gender_value)
                        if status==True:
                            Label(screen1, text="User Already Exists", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+210, y=y1+430)
                            return
                        else:
                            connection = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore") # database connection
                            cursor = connection.cursor()
                            insert_query = "INSERT INTO users(Name, PhoneNo, Gender, Email, Password) VALUES('"+ fullname.get() + "', '"+ phoneno.get() + "', '"+ gender_value + "', '"+ email.get() + "', '"+ password.get() + "');" # queries for inserting values
                            cursor.execute(insert_query) # executing the queries
                            connection.commit() # commiting the connection then closing it.
                            connection.close() # closing the connection of the database
                            Label(screen1, text="Registration Successfull", fg="green", font=(title_font, 16,'bold'), width='30', anchor=W,bg=bgcolor_middle).place(x=x1+210, y=y1+430) # printing successful registration message
                    else:
                        Label(screen1, text="Password invalid / does not match", fg="red", font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+210, y=y1+430)
                        return
                else:
                    Label(screen1, text="Please enter valid email id", fg="red", font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+210, y=y1+430)
                    return
            else:
                Label(screen1, text="Please enter valid contact number", fg="red", font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+210, y=y1+430)
                return
        else:
            Label(screen1, text="Please accept the agreement", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+210, y=y1+430)
            return
    else:
        Label(screen1, text="Please fill in all the details", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+210, y=y1+430)
        return
    
def register():
    global screen1, fullname, phoneno, email, password, repassword,gender, tnc # making all entry field variable global
    fullname = StringVar()
    phoneno = StringVar()
    gender = IntVar()
    email = StringVar()
    password = StringVar()
    repassword = StringVar()
    tnc = IntVar()
    screen1 = Toplevel(screen)
    screen1.title("REGISTRATION")
    adjustWindow(screen1) # configuring the window
    
    Label(screen1, text="", width='500', height="20", bg=color1).pack() 
    Label(screen1, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg='white', bg=color1).place(x=475,y=10)
    Button(screen1, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen1.destroy).place(x=1380, y=55)
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\welcome.png") 
    label = Label(screen1,borderwidth=0, image=photo1)
    label.place(x=0, y=152)
    
    x1=425
    y1=190
    Label(screen1, text="", bg=bgcolor_middle,width='100', height='35').place(x= x1, y= y1 )
    Label(screen1, text="Sign-Up Form", font=(title_font, 20, 'bold'),bg=bgcolor_middle, fg=text_color).place(x=x1+275,y=y1+10)
    Label(screen1, text="Full Name :", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+65)
    Entry(screen1, textvar=fullname, width=30).place(x=x1+275, y=y1+70)
    Label(screen1, text="Contact Number :", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+125)
    Entry(screen1, textvar=phoneno,width=30).place(x=x1+275, y=y1+130)
    Label(screen1, text="Gender :", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+185)
    Radiobutton(screen1, text="Male",font=(body_font, 13), variable=gender, value=1, bg=bgcolor_middle).place(x=x1+275, y=y1+185)
    Radiobutton(screen1, text="Female",font=(body_font, 13), variable=gender, value=2, bg=bgcolor_middle).place(x=x1+375, y=y1+185)
    Label(screen1, text="Email ID :", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+245)
    Entry(screen1, textvar=email,width=30).place(x=x1+275, y=y1+250)
    Label(screen1, text="Password :", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+305)
    Label(screen1, text="(Min. 8 characters,1 Number, 1 Upper Case, 1 Lower Case, 1 Special Character)", font=(body_font, 8), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+275, y=y1+330)
    Entry(screen1, textvar=password, show="*",width=30).place(x=x1+275, y=y1+310)
    Label(screen1, text="Confirm Password :", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+365)
    entry_4 = Entry(screen1, textvar=repassword, show="*",width=30)
    entry_4.place(x=x1+275, y=y1+370)
    Checkbutton(screen1, text="I accept all terms and conditions", variable=tnc, bg=bgcolor_middle, font=(body_font, 10, 'bold'), fg='black').place(x=x1+225, y=y1+400)
    Button(screen1, text='Submit', width=20, font=(body_font, 18, 'bold'), bg='#FF4040', fg=text_color,command=lambda : register_user(x1,y1)).place(x=x1+200, y=y1+465)
    screen1.mainloop()

#REGISTRATION SECTION ENDS HERE--------------------------------------------
    
#HOME PAGE SECTION STARTS HERE--------------------------------------------
def insert_review(entries,x1,y1):
    entry=[]
    for e in entries:
        entry.append(str(e.get()))
        
    for i in entry:
        if(i==""):
             Label(screen2b, text="Please fill in all the details", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+210, y=y1+160)
             return
         
    appname=entry[0]
    review=entry[1]
    
    #Check duplicate Entry
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore")
    cursor = connection.cursor()
    query = "SELECT * FROM reviews WHERE App='"+appname+"'AND Translated_Review='"+review+"'"
    lst=cursor.execute(query)
    connection.commit()
    connection.close()
    if lst:
        Label(screen2b, text="Review Already Exists", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+210, y=y1+160)
        return
    
    senti = TextBlob(review).sentiment
    
    sentimentpolarity=senti[0]
    sentimentsubjectivity=senti[1]
    
    sen = 'Neutral'
    if(sentimentpolarity > 0.0):
        sen = 'Positive'
    elif(sentimentpolarity < 0.0):
        sen = 'Negetive'
    
    sentimentpolarity=str(senti[0])
    sentimentsubjectivity=str(senti[1])
    
    Label(screen2b, text="Sentiment  : "+sen, font=(body_font, 15, 'bold'),width=22 ,fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+260)
    Label(screen2b, text="Sentiment Polarity : "+sentimentpolarity, font=(body_font, 15, 'bold'),width=22, fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+320)
    Label(screen2b, text="Sentiment Subjectivity : "+sentimentsubjectivity, font=(body_font, 15, 'bold'),width=22, fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+380)

    conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore")#,use_unicode=True,charset="utf8"
    cursor = conn.cursor()
    query = "INSERT INTO reviews VALUES('"+ appname + "', '"+ review + "', '"+ sen + "', '"+ sentimentpolarity + "', '"+ sentimentsubjectivity + "');"
    cursor.execute(query) 
    Label(screen2b, text="Added Review Successfully", fg="green",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+210, y=y1+160)
                                       
    conn.commit() 
    conn.close()
    return
    

def add_review():
    global screen2b
    
    screen2b = Toplevel(screen2)
    screen2b.title("ADD REVIEW")
    adjustWindow(screen2b) # configuring the window
    
    Label(screen2b, text="", width='500', height="20", bg=color1).pack() 
    Label(screen2b, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg='white', bg=color1).place(x=475,y=10)
    Button(screen2b, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen2b.destroy).place(x=1380, y=55)
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\home.png") 
    label = Label(screen2b,borderwidth=0, image=photo1)
    label.place(x=0, y=152)
    
    e=[]
    for i in range(2):#Increase as per the entries required
        e.append(i)
        
    x1=425
    y1=190
    Label(screen2b, text="", bg=bgcolor_middle,width='100', height='35').place(x= x1 , y= y1 )
    Label(screen2b, text="Review Form", font=(title_font, 23, 'bold'),bg=bgcolor_middle, fg=text_color).place(x=x1+250,y=y1+5)
    Label(screen2b, text="App Name :", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+60)
    e[0]=Entry(screen2b,font=('Open Sans',12), width=30)
    e[0].place(x=x1+275, y=y1+65)
    
    Label(screen2b, text="Review : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+120)
    e[1]=Entry(screen2b,font=('Open Sans',12),width=30)
    e[1].place(x=x1+275, y=y1+125)
   
    Button(screen2b, text='Submit', width=20, font=(body_font, 18, 'bold'), bg='#FF4040', fg=text_color,command=lambda : insert_review(e,x1,y1)).place(x=x1+200, y=y1+200)
    screen2b.mainloop()

def insert_app(entries,x1,y1):
    entry=[]
    for e in entries:
        entry.append(str(e.get()))
        
    for i in entry:
        if(i==""):
             Label(screen2a, text="Please fill in all the details", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
             return
         
    appname=entry[0]
    categoryname=entry[1]
    rating=entry[2]
    reviews=entry[3]
    size=entry[4]
    installs=entry[5]
    typ=entry[6]
    price=entry[7]
    contentrating=entry[8]
    genre=entry[9]
    lastupdated=entry[10]
    currentversion=entry[11]
    androidversion=entry[12]
    
    #Check duplicate entry
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore")
    cursor = connection.cursor()
    query = "SELECT * FROM apps WHERE App='"+appname+"'"
    lst=cursor.execute(query)
    connection.commit()
    connection.close()
    if lst:
        Label(screen2a, text="App Already Exists", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    
    if categoryname == "--select the category--": 
        Label(screen2a, text="Please select category", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    elif installs == "--select number of installs--": 
        Label(screen2a, text="Please select installs", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    elif typ == "--select the type--":
        Label(screen2a, text="Please select type", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    elif contentrating == "--select the content rating--":
        Label(screen2a, text="Please select content rating", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    elif genre == "--select the genre--": 
        Label(screen2a, text="Please select genre", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    elif androidversion == "--select the android version--":
        Label(screen2a, text="Please select android version", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    else:
        if(re.match("^\d+(\.\d{0,1})?$",rating) and int(rt)>=0 and int(rt)<=5):
            if(re.match("^[0-9]*$",reviews)):
                if(re.match("[0-9]+(\.[0-9]?)?M",size)):
                    if(re.match("^[0-9]*$",price)):
                        if(typ=='Free' and price>'0'):
                             Label(screen2a, text="Please select proper type", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
                             return    
                        date = lastupdated.split(', ')
                        year = date[1]
                        md= date[0].split()
                        month = md[0]
                        day = int(md[1])
                        if(month=='January' or month=='February' or month=='March' 
                           or month=='April' or month=='May' or month=='June' 
                           or month=='July' or month=='August' or month=='Spetember' 
                           or month=='October' or month=='November' or month=='December'):
                            if(re.match("[0-9][0-9][0-9][0-9]",year)):
                                no_days=31
                                year=int(year)
                                 
                                if(month=='February'):
                                    if (year % 4) == 0:  
                                        if (year % 100) == 0:  
                                            if (year % 400) == 0: 
                                                no_days=29
                                    no_days=28
                                    
                                if(month=='April' or month=='June' or month=='September'
                                   or month=='November'):
                                    no_days=30
                                if(1<day<no_days):
                                    if(re.match("^(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)$",currentversion)):
                                        if(currentversion=='0'):
                                            currentversion='Varies with device'
                                        conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore")#,use_unicode=True,charset="utf8"
                                        cursor = conn.cursor()
                                        query = "INSERT INTO apps VALUES('"+ appname + "', '"+ categoryname + "', '"+ rating + "', '"+ reviews + "', '"+ size + "', '"+ installs + "', '"+ typ + "', '"+ price + "', '"+ contentrating + "', '"+ genre + "', '"+ lastupdated + "', '"+ currentversion + "', '"+ androidversion + "');"
                                        
                                        cursor.execute(query) 
                                        conn.commit() 
                                        conn.close()
                                        Label(screen2a, text="Added App Successfully", fg="green",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)  
                                    else:
                                        Label(screen2a, text="Please enter valid current versiom", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
                                        return    
                                else:
                                    Label(screen2a, text="Please enter valid day", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
                                    return
                            else:
                                 Label(screen2a, text="Please enter valid year", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
                                 return
                        else:
                            Label(screen2a, text="Please enter valid month", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
                            return
                    else:
                        Label(screen2a, text="Please enter valid price", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
                        return
                else:
                    Label(screen2a, text="Please enter valid size", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
                    return
            else:
                Label(screen2a, text="Please enter valid number of reviews", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
                return
        else:
            Label(screen2a, text="Please enter valid rating", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
            return    
                                    
def add_app(apprecord):
    global screen2a
    
    screen2a = Toplevel(screen2)
    cat = StringVar()
    install = StringVar()
    typ = StringVar()
    cr = StringVar()
    genr = StringVar()
    andver = StringVar()
    
    screen2a.title("ADD APP")
    adjustWindow(screen2a) # configuring the window
    
    Label(screen2a, text="", width='500', height="20", bg=color1).pack() 
    Label(screen2a, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg='white', bg=color1).place(x=475,y=10)
    Button(screen2a, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen2a.destroy).place(x=1380, y=55)
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\home.png") 
    label = Label(screen2a,borderwidth=0, image=photo1)
    label.place(x=0, y=152)
    
    e=[]
    for i in range(13):#Increase as per the entries required
        e.append(i)
        
    x1=150
    y1=190
    
    for i in apprecord:
        Label(screen2a, text="", bg=bgcolor_middle,width='170', height='37').place(x= x1 , y= y1 )
        Label(screen2a, text="App Form", font=(title_font, 23, 'bold'),bg=bgcolor_middle, fg=text_color).place(x=x1+550,y=y1+5)
        Label(screen2a, text="App Name :", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+60)
        e[0]=Entry(screen2a,font=('Open Sans',12), width=30)
        e[0].place(x=x1+275, y=y1+65)
        e[0].insert(0,i[0])
    
        Label(screen2a, text="Category Name : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+120)
        droplist = OptionMenu(screen2a,cat, *category)
        droplist.config(font=('Open Sans',12),width=22)
        if(i[1]==""):
            cat.set('--select the category--')
        else:
            cat.set(i[1])
        droplist.place(x=x1+275, y=y1+125)
        e[1]=cat
    
        Label(screen2a, text="Rating : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+180)
        e[2]=Entry(screen2a,font=('Open Sans',12),width=22)
        e[2].place(x=x1+275, y=y1+185)
        Label(screen2a, text="Eg : 4.1(out of 5)", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+275, y=y1+210)
        e[2].insert(0,i[2])
        
        Label(screen2a, text="Reviews : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+240)
        e[3]=Entry(screen2a,font=('Open Sans',12),width=22)
        e[3].place(x=x1+275, y=y1+245)
        Label(screen2a, text="Eg : 10000", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+275, y=y1+270)
        e[3].insert(0,i[3])
        
        Label(screen2a, text="Size : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+300)
        e[4]=Entry(screen2a,font=('Open Sans',12),width=22)
        e[4].place(x=x1+275, y=y1+305)
        Label(screen2a, text="Eg : 8.7M (1Mb=1024Kb)", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+275, y=y1+330)
        e[4].insert(0,i[4])
    
        Label(screen2a, text="Installs : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+360)
        droplist = OptionMenu(screen2a,install, *installs)
        droplist.config(font=('Open Sans',12),width=22)
        if(i[5]==""):
            install.set('--select number of installs--')
        else:
            install.set(i[5])
        droplist.place(x=x1+275, y=y1+365)
        e[5]=install
        
        Label(screen2a, text="Type : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+420)
        droplist = OptionMenu(screen2a,typ, *types)
        droplist.config(font=('Open Sans',12),width=22)
        if(i[6]==""):
            typ.set('--select the type--')
        else:
            typ.set(i[6])
        droplist.place(x=x1+275, y=y1+425)
        e[6]=typ
    
        Label(screen2a, text="Price : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+480)
        e[7]=Entry(screen2a,font=('Open Sans',12),width=22)
        e[7].place(x=x1+275, y=y1+485)
        Label(screen2a, text="Eg : 100 (in rupees)", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+275, y=y1+510)
        e[7].insert(0,i[7])
        
        Label(screen2a, text="Content Rating : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+675, y=y1+60)
        droplist = OptionMenu(screen2a,cr, *contentrating)
        droplist.config(font=('Open Sans',12),width=22)
        if(i[8]==""):
            cr.set('--select the content rating--')
        else:
            cr.set(i[8])
        droplist.place(x=x1+875, y=y1+65)
        e[8]=cr
    
        Label(screen2a, text="Genres : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+675, y=y1+125)
        droplist = OptionMenu(screen2a,genr, *genres)
        droplist.config(font=('Open Sans',12),width=22)
        if(i[9]==""):
            genr.set('--select the genre--')
        else:
            genr.set(i[9])
        droplist.place(x=x1+875, y=y1+125)
        e[9]=genr
  
        Label(screen2a, text="Last Updated : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+675, y=y1+180)
        e[10]=Entry(screen2a,font=('Open Sans',12),width=22)
        e[10].place(x=x1+875, y=y1+185)
        Label(screen2a, text="Eg : November 29, 2017", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+875, y=y1+210)
        e[10].insert(0,i[10])
        
        Label(screen2a, text="Current Version : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+675, y=y1+240)
        e[11]=Entry(screen2a,font=('Open Sans',12),width=22)
        e[11].place(x=x1+875, y=y1+245)
        Label(screen2a, text="Eg : 1.0.9(Note: If version varies with device enter 0)", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+750, y=y1+270)
        e[11].insert(0,i[11])
        
        android=['Varies with device','1.0','1.1','1.5','1.6','2.0','2.1','2.0.1','2.2','2.3','2.3.1','2.3.2',
             '2.3.3','2.3.4','2.3.5','2.3.6','2.3.7','3.0','3.1','3.2','4.0.1','4.0.2',
             '4.0.3','4.0.4','4.1','4.2','4.3','4.4','4.4.1','4.4.2','4.4.3','4.4.4',
             '5.0','5.1','6.0','7.0','7.1','8.0.0','8.1.0','9.0']
    
        Label(screen2a, text="Android Version : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+675, y=y1+300)
        droplist = OptionMenu(screen2a,andver, *android)
        droplist.config(font=('Open Sans',12),width=22)
        if(i[12]==""):
            andver.set('--select the android version--')
        else:
            andver.set(i[12])
        droplist.place(x=x1+875, y=y1+305)
        e[12]=andver
        Label(screen2a, text="(Note: Select minimum required version)", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+875, y=y1+340)
        break
            
    Button(screen2a, text='Submit', width=20, font=(body_font, 18, 'bold'), bg='#FF4040', fg=text_color,command=lambda : insert_app(e,x1,y1)).place(x=x1+800, y=y1+380)
    screen2a.mainloop()

def delete_app(appname,x2,y2):
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore",use_unicode=True,charset="utf8")
    cursor = conn.cursor()
    query = "DELETE from apps WHERE App='"+appname+"'"
    cursor.execute(query)    
    conn.commit() # commiting the connection then closing it.
    conn.close() # closing the connection of the database
    Label(screen2, text="App Deleted",font=(title_font, 14, 'bold'), fg='green', bg=bgcolor_middle,width=20,anchor=W).place(x=x2+360,y=y2+330)  
          
def search(x2,y2,search_item):
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore",use_unicode=True,charset="utf8")
    cursor = conn.cursor()
    query = "SELECT * from apps WHERE App='"+search_item+"'"
    cursor.execute(query) # executing the queries
    apprecord = cursor.fetchall()        
    conn.commit() # commiting the connection then closing it.
    conn.close() # closing the connection of the database
    
    if(len(apprecord)==0):
        Label(screen2, text="App doesnt not exist",font=(title_font, 17, 'bold'), fg=text_color, bg=bgcolor_middle,width=50,anchor=W).place(x=x2+20,y=y2+50)
        return
    
    for i in apprecord:
            Label(screen2, text="App Name : "+i[0],font=(title_font, 17, 'bold'), fg=text_color, bg=bgcolor_middle,width=50,anchor=W).place(x=x2+20,y=y2+50)    
            Label(screen2, text="Category Name : "+i[1],font=(title_font, 17, 'bold'), fg=text_color, bg=bgcolor_middle,width=50,anchor=W).place(x=x2+20,y=y2+90)
            Label(screen2, text="Rating : "+i[2],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=25,anchor=W).place(x=x2+20,y=y2+130)  
            Label(screen2, text="Reviews : "+i[3],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=25,anchor=W).place(x=x2+20,y=y2+170)
            Label(screen2, text="Size : "+i[4],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=25,anchor=W).place(x=x2+20,y=y2+210)
            Label(screen2, text="Installs : "+i[5],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=25,anchor=W).place(x=x2+20,y=y2+250)
            Label(screen2, text="Type : "+i[6],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=25,anchor=W).place(x=x2+20,y=y2+290)
            Label(screen2, text="Price : "+i[7],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=25,anchor=W).place(x=x2+20,y=y2+330)
            Label(screen2, text="Content Rating : "+i[8],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=30,anchor=W).place(x=x2+300,y=y2+130)
            Label(screen2, text="Genres : "+i[9],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=35,anchor=W).place(x=x2+300,y=y2+170)
            Label(screen2, text="Last Updated : "+i[10],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=30,anchor=W).place(x=x2+300,y=y2+210)
            Label(screen2, text="Current Version : "+i[11],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=35,anchor=W).place(x=x2+300,y=y2+250)
            Label(screen2, text="Android Version : "+i[12],font=(title_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=35,anchor=W).place(x=x2+300,y=y2+290)
            Button(screen2, text='Delete', width=12, font=(body_font, 13, 'bold'), bg='#FF4040', fg=text_color,command=lambda : delete_app(i[0],x2,y2)).place(x=x2+350, y=y2+20)
            Button(screen2, text='Update', width=12, font=(body_font, 13, 'bold'), bg='#e79700', fg=text_color,command=lambda : add_app(apprecord)).place(x=x2+550, y=y2+20)

            break#Incase of multiple values it will only show the details of the first value
     

def compareCategory(cat,xx,yy):
    content_rating=['Everyone','Everyone 10+','Teen','Mature 17+','Adults only 18+']
    
    cat=str(cat.get())
    try:
        no_of_apps=0
        total_rating=0
        total_installs=0
        total_size=0
        size_counter=0
        free=0
        paid=0
        cat_con_rating=[0,0,0,0,0]
    
        Label(screen2c, text="CATEGORY : "+cat, font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=xx+40, y=yy+90)
    
    
        for index,row in apps.iterrows():
            if cat==row['Category']:
                no_of_apps+=1
                total_rating+=int(row['Rating'])
                total_installs+=int(row['Installs'])
                if row['Type']=='Free':
                    free+=1
                elif row['Type']=='Paid':
                    paid+=1
                if row['Content Rating']=='Everyone':
                    cat_con_rating[0]+=1
                elif row['Content Rating']=='Everyone 10+':
                    cat_con_rating[1]+=1
                elif row['Content Rating']=='Teen':
                    cat_con_rating[2]+=1
                elif row['Content Rating']=='Mature 17+':
                    cat_con_rating[3]+=1
                elif row['Content Rating']=='Adults only 18+':
                    cat_con_rating[4]+=1
                
                    
        Label(screen2c, text="Total number of apps:{0} ".format(str(no_of_apps)), font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=xx+40, y=yy+150)
 
        Label(screen2c, text="Average rating:"+str(round(total_rating/no_of_apps,2)), font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=xx+40, y=yy+210)

        Label(screen2c, text="Total number of installs:"+str(total_installs), font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=xx+40, y=yy+270)

        Label(screen2c, text="Total number of free apps:"+str(free), font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=xx+40, y=yy+330)

        Label(screen2c, text="Total number of paid apps:"+str(paid), font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=xx+40, y=yy+390)
    
        highest_value_con_rating = max(cat_con_rating)
        index = cat_con_rating.index(highest_value_con_rating)
    
        Label(screen2c, text="Maximum apps consists content rating:"+str(content_rating[index]), font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=xx+40, y=yy+450)

    
    except(ZeroDivisionError):
        return

def compare_Category():
    global screen2c
    
    screen2c = Toplevel(screen2)
    cat1 = StringVar()
    cat2 = StringVar()
    screen2c.title("COMPARE CATEGORY")
    adjustWindow(screen2c) # configuring the window
    
    Label(screen2c, text="", width='500', height="20", bg=color1).pack() 
    Label(screen2c, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg='white', bg=color1).place(x=475,y=10)
    Button(screen2c, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen2c.destroy).place(x=1380, y=55)
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\home.png") 
    label = Label(screen2c,borderwidth=0, image=photo1)
    label.place(x=0, y=152)
    
    x1=60
    y1=180
    Label(screen2c,width=95,height=38, bg=bgcolor_middle).place(x=x1, y=y1)
    Label(screen2c, text="Category 1 : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+40, y=y1+20)
    droplist = OptionMenu(screen2c,cat1, *category,command=lambda x:compareCategory(cat1,x1,y1))
    droplist.config(font=('Open Sans',12),width=22)
    cat1.set('--select the category--')
    droplist.place(x=x1+220, y=y1+20)
    
    x2=790
    y2=180
    Label(screen2c,width=95,height=38, bg=bgcolor_middle).place(x=x2, y=y2)
    Label(screen2c, text="Category 2 : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x2+40, y=y2+20)
    droplist = OptionMenu(screen2c,cat2, *category,command=lambda x:compareCategory(cat2,x2,y2))
    droplist.config(font=('Open Sans',12),width=22)
    cat2.set('--select the category--')
    droplist.place(x=x2+220, y=y2+20)
    
    screen2c.mainloop()
            
def home_page(user):
    global screen2
 
    screen2 = Toplevel(screen)
    search_item = StringVar()
    
    screen2.title("HOME")
    adjustWindow(screen2)
    
    Label(screen2, text="", width='500', height="20", bg=color1).pack() 
    Label(screen2, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg='white', bg=color1).place(x=475,y=10)
    Label(screen2, text="Welcome "+user[0][1],font=(title_font, 15, 'bold'), fg=text_color, bg=color1).place(x= 1350 , y= 30 )
    Button(screen2, text='Logout', width=7, font=(body_font, 11, 'bold'), bg=color3, fg=text_color, command=screen2.destroy).place(x=1385, y=65)
    Button(screen2, text="Add a new login", bg="#e79700", width=12, height=1, font=(body_font, 11, 'bold'), fg=text_color, command=register).place(x=1360,y=105)
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\home.png")
    label = Label(screen2,borderwidth=0, image=photo1)
    label.place(x=0, y=152)
    Button(screen2, text='Insight 1', width=15, font=(body_font, 23, 'bold'), bg=color3, fg=text_color,command=insight1).place(x=130, y=200)
    Button(screen2, text='Insight 2', width=15, font=(body_font, 23, 'bold'), bg=color3, fg=text_color,command=insight2).place(x=600, y=200)
    Button(screen2, text='Stats', width=15, font=(body_font, 23, 'bold'), bg=color3, fg=text_color,command=stats).place(x=1070, y=200)
    
    x2=700#Used in 2nd section
    y2=350
    
    #Admin Section
    x1=70
    y1=350
    Label(screen2, text="", width=70, height=22, bg=bgcolor_middle).place(x=x1,y=y1)
    e1=Entry(screen2 , width=41, font=('Open Sans',15))
    e1.place(x=x1+20,y=y1+50)
    e1.insert(0,'Type an App Name')
    
    apprecord=[]
    for i in range(2):
        apprecord.append([])
        for j in range(13):
            apprecord[i].append("")#for passing a parameter to add_app function
            
    Button(screen2, text='Search', width=12, font=(body_font, 13, 'bold'), bg="#FF4040", fg=text_color,command=lambda : search(x2,y2,e1.get())).place(x=x1+170, y=y1+100)
    Button(screen2, text='Add App', width=15, font=(body_font, 15, 'bold'), bg=color3, fg=text_color,command=lambda : add_app(apprecord)).place(x=x1+50, y=y1+200)
    Button(screen2, text='Add Review', width=15, font=(body_font, 15, 'bold'), bg=color3, fg=text_color,command=add_review).place(x=x1+250, y=y1+200)
    Button(screen2, text='Compare Category', width=15, font=(body_font, 15, 'bold'), bg=color3, fg=text_color,command=compare_Category).place(x=x1+160, y=y1+250)

    #Search Results Section
    Label(screen2, text="", width=100, height=25, bg=bgcolor_middle).place(x=x2,y=y2)
    Label(screen2, text="Search Results :",font=(title_font, 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x2+20,y=y2+10)
    screen2.mainloop()

#HOME PAGE SECTION ENDS HERE------------------------------------------------

#LOGIN SECTION STARTS HERE--------------------------------------------------    
def login_verify():
    global studentID
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore") # database connection
    cursor = connection.cursor()
    select_query = "SELECT * FROM users where email = '" + username_verify.get() + "' AND password = '" + password_verify.get() + "';" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    user = cursor.fetchall()
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    if user:
        userID = user[0][0]
        home_page(user) 
    else:
        messagebox.showerror("Error", "Invalid Username or Password") # displaying message for invalid details
     
def main_screen():
    global screen, username_verify, password_verify
    screen = Tk() # initializing the tkinter window
    username_verify = StringVar()
    password_verify = StringVar()
    screen.title("8-BIT STORE") # mentioning title of the window
    adjustWindow(screen) # configuring the window

    Label(screen, text="", width="500", height="20", bg=color1).pack()
    Label(screen, text="8-BIT ANALYSIS", font=(title_font, 70, 'bold'), fg='white', bg=color1).place(x=475,y=10)
    
    photo = PhotoImage(file="F:\\Python Class\\Project\\welcome.png")
    label = Label(screen,borderwidth=0, image=photo)
    label.place(x=0, y=152)
    
    x1=525
    y1=190
    Label(screen, text="", bg=bgcolor_middle,width='70', height='22').place(x=x1 , y=y1 )
    Label(screen, text="Please enter your login credentials", font=(title_font, 20, 'bold'),bg=bgcolor_middle, fg=text_color).place(x=x1+50,y=y1+10)  
    Label(screen, text="Username :", font=(body_font, 15, 'bold'),bg=bgcolor_middle, fg=text_color).place(x=x1+80,y=y1+105)
    Entry(screen, textvar=username_verify,font=(body_font,12)).place(x=x1+230,y=y1+110)
    Label(screen, text="Password :", font=(body_font, 15, 'bold'), bg=bgcolor_middle, fg=text_color).place(x=x1+80,y=y1+165)
    Entry(screen, textvar=password_verify,font=(body_font,12), show="*").place(x=x1+230,y=y1+170)
    Button(screen, text="LOGIN", bg="#e79700", width=15, height=1, font=(body_font, 13, 'bold'), fg=text_color, command=login_verify).place(x=x1+175,y=y1+250)
    screen.mainloop()

#LOGIN SECTION ENDS HERE-------------------------------------------------
    
data_wrangling() 
initialise()
main_screen()      
          

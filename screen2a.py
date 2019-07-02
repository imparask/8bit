from tkinter import *
from tkinter import messagebox
import re, pymysql
import pymysql
import pandas as pd
import time

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
    
        
   
def lists():
    global category,installs,types,genres,contentrating
    
    cat = apps.drop_duplicates(subset='Category', keep='first')
    category=[]
    for i in cat['Category']:
        category.append(i)
        
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
        
    contrat = apps.drop_duplicates(subset='Content Rating', keep='first')
    contentrating=[]
    for i in contrat['Content Rating']:
        contentrating.append(i)
        



def insert_app(entries,x1,y1):
    entry=[]
    for e in entries:
        entry.append(str(e.get()))
        
    print(entry)
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
    
    if categoryname == "--select the category--": 
        Label(screen2a, text="Please select category", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    elif installs == "--select number of installs--": 
        Label(screen2a, text="Please select installs", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    elif typ == "--select the type--":
        Label(screen2a, text="Please select type", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    elif contentrating == "--select the content rating--": # checking for selection of university
        Label(screen2a, text="Please select content rating", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    elif genre == "--select the genre--": # checking for selection of university
        Label(screen2a, text="Please select genre", fg="red",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)
        return
    else:
        if(re.match("[0-9](\.[0-9]{0,1}?)?",rating)):
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
                                    conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore")#,use_unicode=True,charset="utf8"
                                    cursor = conn.cursor()
                                    query = "INSERT INTO apps VALUES('"+ appname + "', '"+ categoryname + "', '"+ rating + "', '"+ reviews + "', '"+ size + "', '"+ installs + "', '"+ typ + "', '"+ price + "', '"+ contentrating + "', '"+ genre + "', '"+ lastupdated + "', '"+ currentversion + "', '"+ androidversion + "');"
                                    #(App,Category,Rating,Reviews,Size,Installs,Type,Price,Content Rating,Genres,Last Updated,Current Ver,Android Ver)
                                    print(query)
                                    cursor.execute(query) 
                                    conn.commit() 
                                    conn.close()
                                    Label(screen2a, text="Registration Successfull", fg="green",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+850, y=y1+450)  
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
                                    
        

def add_app():
    global screen2a
    
    screen2a = Tk()
    #screen2a = Toplevel(screen)
    cat = StringVar()
    install = StringVar()
    typ = StringVar()
    cr = StringVar()
    genr = StringVar()
    
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
    Label(screen2a, text="", bg=bgcolor_middle,width='170', height='37').place(x= x1 , y= y1 )
    Label(screen2a, text="App Form", font=(title_font, 23, 'bold'),bg=bgcolor_middle, fg=text_color).place(x=x1+550,y=y1+5)
    Label(screen2a, text="App Name :", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+60)
    e[0]=Entry(screen2a,font=('Open Sans',12), width=30)
    e[0].place(x=x1+275, y=y1+65)
    
    Label(screen2a, text="Category Name : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+120)
    droplist = OptionMenu(screen2a,cat, *category)
    droplist.config(font=('Open Sans',12),width=20)
    cat.set('--select the category--')
    droplist.place(x=x1+275, y=y1+125)
    e[1]=cat
    
    Label(screen2a, text="Rating : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+180)
    e[2]=Entry(screen2a,font=('Open Sans',12),width=20)
    e[2].place(x=x1+275, y=y1+185)
    Label(screen2a, text="Eg : 4.1", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+275, y=y1+210)
    
    Label(screen2a, text="Reviews : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+240)
    e[3]=Entry(screen2a,font=('Open Sans',12),width=20)
    e[3].place(x=x1+275, y=y1+245)
    Label(screen2a, text="Eg : 10000", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+275, y=y1+270)
    
    Label(screen2a, text="Size : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+300)
    e[4]=Entry(screen2a,font=('Open Sans',12),width=20)
    e[4].place(x=x1+275, y=y1+305)
    Label(screen2a, text="Eg : 8.7M (1Mb=1024Kb)", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+275, y=y1+330)
    
    
    Label(screen2a, text="Installs : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+360)
    droplist = OptionMenu(screen2a,install, *installs)
    droplist.config(font=('Open Sans',12),width=20)
    install.set('--select number of installs--')
    droplist.place(x=x1+275, y=y1+365)
    e[5]=install
    
    Label(screen2a, text="Type : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+420)
    droplist = OptionMenu(screen2a,typ, *types)
    droplist.config(font=('Open Sans',12),width=20)
    typ.set('--select the type--')
    droplist.place(x=x1+275, y=y1+425)
    e[6]=typ
    
    Label(screen2a, text="Price : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+480)
    e[7]=Entry(screen2a,font=('Open Sans',12),width=30)
    e[7].place(x=x1+275, y=y1+485)
    Label(screen2a, text="Eg : 100 (in rupees)", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+275, y=y1+510)
    
    Label(screen2a, text="Content Rating : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+675, y=y1+60)
    droplist = OptionMenu(screen2a,cr, *contentrating)
    droplist.config(font=('Open Sans',12),width=20)
    cr.set('--select the content rating--')
    droplist.place(x=x1+875, y=y1+65)
    e[8]=cr
    
    Label(screen2a, text="Genres : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+675, y=y1+125)
    droplist = OptionMenu(screen2a,genr, *genres)
    droplist.config(font=('Open Sans',12),width=20)
    genr.set('--select the genre--')
    droplist.place(x=x1+875, y=y1+125)
    e[9]=genr
  
    Label(screen2a, text="Last Updated : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+675, y=y1+180)
    e[10]=Entry(screen2a,font=('Open Sans',12),width=20)
    e[10].place(x=x1+875, y=y1+185)
    Label(screen2a, text="Eg : November 29, 2017", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+875, y=y1+210)
    
    Label(screen2a, text="Current Version : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+675, y=y1+240)
    e[11]=Entry(screen2a,font=('Open Sans',12),width=20)
    e[11].place(x=x1+875, y=y1+245)
    Label(screen2a, text="Eg : 1.0.9", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+875, y=y1+270)
    
    Label(screen2a, text="Android Version : ", font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+675, y=y1+300)
    e[12]=Entry(screen2a,font=('Open Sans',12),width=20)
    e[12].place(x=x1+875, y=y1+305)
    Label(screen2a, text="Eg : 2.3 and up", font=(body_font, 11,'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+875, y=y1+330)
    
    Button(screen2a, text='Submit', width=20, font=(body_font, 18, 'bold'), bg='#FF4040', fg=text_color,command=lambda : insert_app(e,x1,y1)).place(x=x1+800, y=y1+360)
    screen2a.mainloop()

data_wrangling()
lists()
add_app()
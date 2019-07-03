from textblob import TextBlob
from tkinter import *
from tkinter import messagebox
import re, pymysql

import pandas as pd

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
    
    #Check for duplicate entry
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
    
    Label(screen2b, text="Sentiment  : "+sen, font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+260)
    Label(screen2b, text="Sentiment Polarity : "+sentimentpolarity, font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+320)
    Label(screen2b, text="Sentiment Subjectivity : "+sentimentsubjectivity, font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle, anchor=W).place(x=x1+75, y=y1+380)
    

    conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore")#,use_unicode=True,charset="utf8"
    cursor = conn.cursor()
    query = "INSERT INTO reviews VALUES('"+ appname + "', '"+ review + "', '"+ sen + "', '"+ sentimentpolarity + "', '"+ sentimentsubjectivity + "');"
    #(App,Translated_Review,Sentiment,Sentiment_Polarity,Sentiment_Subjectivity)
    cursor.execute(query) 
    Label(screen2b, text="Added Review Successfully", fg="green",font=(title_font, 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=x1+210, y=y1+160)
                                       
    conn.commit() 
    conn.close()
    return
    

def add_review():
    global screen2b
    
    screen2b = Tk()
    #screen2a = Toplevel(screen)
    
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

add_review()
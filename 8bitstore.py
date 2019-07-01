from tkinter import *
from tkinter import messagebox
import re, pymysql
import numpy as np 
import pandas as pd 
from datetime import date

#Choose theme of window
color1 ='#CD3333'#TITLE COLOR
bgcolor_middle = '#5F9EA0'#BODY COLOR
color3 = '#00C957'#Button Color
text_color ='white'

def data_wrangling():
    global apps,review
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
                      
def stats():
    global screen3,cat,ran
    
    screen3 = Toplevel(screen)
    cat=StringVar()
    ran=StringVar()
    screen3.title("STATISTICS")
    adjustWindow(screen3)    
    
    
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
        
def register_user():
    if fullname.get() and email.get() and password.get() and repassword.get() and gender.get() and phoneno.get() : # checking for all empty values in entry field
        if tnc.get(): # checking for acceptance of agreement
            if re.match("^((\+)?(\d{2}[-]))?(\d{10}){1}?$",phoneno.get()):
                if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email.get()): # validating the email
                    if password.get() == repassword.get(): # checking both password match or not
                        # if u enter in this block everything is fine just enter the values in database
                        gender_value = 'male'
                        if gender.get() == 2:
                            gender_value = 'female'
                        status = duplicateEntry(gender_value)
                        if status==True:
                            Label(screen1, text="User Already Exists", fg="red",font=("calibri", 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=625, y=590)
                            return
                        else:
                            connection = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore") # database connection
                            cursor = connection.cursor()
                            insert_query = "INSERT INTO users(Name, PhoneNo, Gender, Email, Password) VALUES('"+ fullname.get() + "', '"+ phoneno.get() + "', '"+ gender_value + "', '"+ email.get() + "', '"+ password.get() + "');" # queries for inserting values
                            cursor.execute(insert_query) # executing the queries
                            connection.commit() # commiting the connection then closing it.
                            connection.close() # closing the connection of the database
                            Label(screen1, text="Registration Successfull", fg="green", font=("calibri", 16,'bold'), width='30', anchor=W,bg=bgcolor_middle).place(x=625, y=590) # printing successful registration message
                            Button(screen1, text='Proceed To Login', width=20, font=("Open Sans", 18, 'bold'), bg='#FF4040', fg='white',command=screen1.destroy).place(x=625, y=625) # button to navigate back to login page
                    else:
                        Label(screen1, text="Password does not match", fg="red", font=("calibri", 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=625, y=590)
                        return
                else:
                    Label(screen1, text="Please enter valid email id", fg="red", font=("calibri", 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=625, y=590)
                    return
            else:
                Label(screen1, text="Please enter valid contact number", fg="red", font=("calibri", 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=625, y=590)
                return
        else:
            Label(screen1, text="Please accept the agreement", fg="red",font=("calibri", 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=625, y=590)
            return
    else:
        Label(screen1, text="Please fill in all the details", fg="red",font=("calibri", 16,'bold'), width='30', anchor=W, bg=bgcolor_middle).place(x=625, y=590)
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
    Label(screen1, text="8-BIT ANALYSIS",font=("Calibri", 70, 'bold'), fg='white', bg=color1).place(x=475,y=10)
    Label(screen1, text="", bg='black', width='500', height='75').place(x= 0 , y= 152 )
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\welcome.png") # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(screen1,borderwidth=0, image=photo1,) # attaching image to the label
    label.place(x=0, y=152)
    Label(screen1, text="", bg=bgcolor_middle,width='100', height='35').place(x= 425 , y= 190 )
    Label(screen1, text="Sign-Up Form", font=("Calibri", 20, 'bold'),bg=bgcolor_middle, fg='white').place(x=700,y=200)
    Label(screen1, text="Full Name :", font=("Open Sans", 15, 'bold'), fg='white', bg=bgcolor_middle, anchor=W).place(x=500, y=275)
    Entry(screen1, textvar=fullname, width=30).place(x=700, y=280)
    Label(screen1, text="Contact Number :", font=("Open Sans", 15, 'bold'), fg='white', bg=bgcolor_middle, anchor=W).place(x=500, y=315)
    Entry(screen1, textvar=phoneno,width=30).place(x=700, y=320)
    Label(screen1, text="Gender :", font=("Open Sans", 15, 'bold'), fg='white', bg=bgcolor_middle, anchor=W).place(x=500, y=365)
    Radiobutton(screen1, text="Male",font=("Open Sans", 13), variable=gender, value=1, bg=bgcolor_middle).place(x=700, y=365)
    Radiobutton(screen1, text="Female",font=("Open Sans", 13), variable=gender, value=2, bg=bgcolor_middle).place(x=800, y=365)
    Label(screen1, text="Email ID :", font=("Open Sans", 15, 'bold'), fg='white', bg=bgcolor_middle, anchor=W).place(x=500, y=405)
    Entry(screen1, textvar=email,width=30).place(x=700, y=410)
    Label(screen1, text="Password :", font=("Open Sans", 15, 'bold'), fg='white', bg=bgcolor_middle, anchor=W).place(x=500, y=445)
    Entry(screen1, textvar=password, show="*",width=30).place(x=700, y=450)
    Label(screen1, text="Confirm Password :", font=("Open Sans", 15, 'bold'), fg='white', bg=bgcolor_middle, anchor=W).place(x=500, y=485)
    entry_4 = Entry(screen1, textvar=repassword, show="*",width=30)
    entry_4.place(x=700, y=490)
    Checkbutton(screen1, text="I accept all terms and conditions", variable=tnc, bg=bgcolor_middle, font=("Open Sans", 10, 'bold'), fg='black').place(x=650, y=550)
    Button(screen1, text='Submit', width=20, font=("Open Sans", 18, 'bold'), bg='#FF4040', fg='white',command=register_user).place(x=625, y=625)
    screen1.mainloop()

def home_page(user):
    global screen2,search_item
    
    screen2 = Toplevel(screen)
    search_item=StringVar()
    screen2.title("HOME")
    adjustWindow(screen2)
    
    Label(screen2, text="", width='500', height="20", bg=color1).pack() 
    Label(screen2, text="8-BIT ANALYSIS",font=("Calibri", 70, 'bold'), fg='white', bg=color1).place(x=475,y=10)
    Label(screen2, text="Welcome "+user[0][1],font=("Calibri", 15, 'bold'), fg='white', bg=color1).place(x= 1350 , y= 30 )
    Button(screen2, text='Logout', width=7, font=("Open Sans", 11, 'bold'), bg=color3, fg='white', command=screen2.destroy).place(x=1385, y=70)
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\home.png") # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(screen2,borderwidth=0, image=photo1) # attaching image to the label
    label.place(x=0, y=152)
    Button(screen2, text='Reviews', width=15, font=("Open Sans", 23, 'bold'), bg=color3, fg='white').place(x=130, y=175)#, command=reviews
    Button(screen2, text='Trends', width=15, font=("Open Sans", 23, 'bold'), bg=color3, fg='white').place(x=600, y=175)#,command=trends
    Button(screen2, text='Stats', width=15, font=("Open Sans", 23, 'bold'), bg=color3, fg='white',command=stats).place(x=1070, y=175)
    e1=Entry(screen2,textvar=search_item,width=80,font=('Open Sans',20))
    e1.place(x=150,y=450)
    e1.insert(0,'Type Category Name or App Name')
    Button(screen2, text='Search', width=15, font=("Open Sans", 18, 'bold'), bg="#FF4040", fg='white').place(x=650, y=525)#,command=search
    screen2.mainloop()
    
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
        #messagebox.showinfo("Congratulations !!", "Login Succesfull") # displaying message for successful login
        userID = user[0][0]
        home_page(user) # opening welcome window
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
    Label(screen, text="8-BIT ANALYSIS", font=("Calibri", 70, 'bold'), fg='white', bg=color1).place(x=475,y=10)
    Label(screen, text="", bg='black',width='500', height='75').place(x= 0 , y= 152 )
    photo = PhotoImage(file="F:\\Python Class\\Project\\welcome.png") # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(screen,borderwidth=0, image=photo) # attaching image to the label
    label.place(x=0, y=152)
    Label(screen, text="", bg=bgcolor_middle,width='70', height='22').place(x= 525 , y= 190 )
    Label(screen, text="Please enter your login credentials", font=("Calibri", 20, 'bold'),bg=bgcolor_middle, fg='white').place(x=575,y=200)  
    Label(screen, text="Username :", font=("Open Sans", 15, 'bold'),bg=bgcolor_middle, fg='white').place(x=625,y=295)
    Entry(screen, textvar=username_verify).place(x=775,y=300)
    Label(screen, text="Password :", font=("Open Sans", 15, 'bold'), bg=bgcolor_middle, fg='white').place(x=625,y=355)
    Entry(screen, textvar=password_verify, show="*").place(x=775,y=360)
    Button(screen, text="LOGIN", bg="#e79700", width=15, height=1, font=("Open Sans", 13, 'bold'), fg='white', command=login_verify).place(x=700,y=415)
    Button(screen, text="SIGN-UP", bg="#e79700", width=15, height=1, font=("Open Sans", 13, 'bold'), fg='white', command=register).place(x=700,y=475)
    screen.mainloop()

data_wrangling() 
categoryDownloads()#function used in stats
max_min_avg_downloads()#Function used in stats
main_screen()      
          
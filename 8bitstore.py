from tkinter import *
from tkinter import messagebox
import re, pymysql

#Choose theme of window
color1 ='#CD3333'#TITLE COLOR
bgcolor_middle = '#5F9EA0'#BODY COLOR
color3 = '#00C957'#Button Color

def adjustWindow(window):
    
    ws = screen.winfo_screenwidth() # width of the screen
    hs = screen.winfo_screenheight() # height of the screen
    w = ws # width for the window size
    h = hs# height for the window size
    x = (ws/2) - (w/2) # calculate x and y coordinates for the Tk window
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w-15, h-40, x, y)) # set the dimensions of the screen and where it is placed
    window.resizable(False, False) # disabling the resize option for the window
    window.configure(background='white')
 
def duplicateEntry(gender_value):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore")
    cursor = connection.cursor()
    #rows = cursor.fetchall()
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
    photo1 = PhotoImage(file="F:\\Python Class\\Project\\appstore.png") # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(screen1, image=photo1,bg="black") # attaching image to the label
    label.place(x=10, y=152)
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
    photo = PhotoImage(file="F:\\Python Class\\Project\\appstore.png") # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(screen,bg='black', image=photo, text="") # attaching image to the label
    label.place(x=10, y=152)
    Label(screen, text="", bg=bgcolor_middle,width='70', height='22').place(x= 525 , y= 190 )
    Label(screen, text="Please enter your login credentials", font=("Calibri", 20, 'bold'),bg=bgcolor_middle, fg='white').place(x=575,y=200)  
    Label(screen, text="Username :", font=("Open Sans", 15, 'bold'),bg=bgcolor_middle, fg='white').place(x=625,y=295)
    Entry(screen, textvar=username_verify).place(x=775,y=300)
    Label(screen, text="Password :", font=("Open Sans", 15, 'bold'), bg=bgcolor_middle, fg='white').place(x=625,y=355)
    Entry(screen, textvar=password_verify, show="*").place(x=775,y=360)
    Button(screen, text="LOGIN", bg="#e79700", width=15, height=1, font=("Open Sans", 13, 'bold'), fg='white').place(x=700,y=415)#, command=login_verify 
    Button(screen, text="SIGN-UP", bg="#e79700", width=15, height=1, font=("Open Sans", 13, 'bold'), fg='white', command=register).place(x=700,y=475)
    screen.mainloop()
    
main_screen()      
          
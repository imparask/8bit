from tkinter import *
from tkinter import messagebox
import re, pymysql

#Choose theme of window
color1 ='#CD3333'#TITLE COLOR
bgcolor_middle = '#5F9EA0'#BODY COLOR
color3 = '#00C957'#Button Color

def adjustWindow(window):
    
    ws = screen2.winfo_screenwidth() # width of the screen
    hs = screen2.winfo_screenheight() # height of the screen
    w = ws # width for the window size
    h = hs# height for the window size
    x = (ws/2) - (w/2) # calculate x and y coordinates for the Tk window
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w-15, h-40, x, y)) # set the dimensions of the screen and where it is placed
    window.resizable(False, False) # disabling the resize option for the window
    window.configure(background='white')

def home_page(user):
    global screen2,search_item
    screen2 = Tk()
    search_item=StringVar()
    #screen2 = Toplevel(screen1)
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
    Button(screen2, text='Stats', width=15, font=("Open Sans", 23, 'bold'), bg=color3, fg='white').place(x=1070, y=175)#,command=stats
    e1=Entry(screen2,textvar=search_item,width=80,font=('Open Sans',20))
    e1.place(x=150,y=450)
    e1.insert(0,'Type Category Name or App Name')
    Button(screen2, text='Search', width=15, font=("Open Sans", 18, 'bold'), bg="#FF4040", fg='white').place(x=650, y=525)#,command=search
    screen2.mainloop()

user = [[1,'Paras','9930835362']]
home_page(user)

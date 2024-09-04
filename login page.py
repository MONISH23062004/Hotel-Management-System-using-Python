from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk



login_window=Tk()
login_window.title("STM HOTELS")


screen_width=login_window.winfo_screenwidth()
screen_height=login_window.winfo_screenheight()
login_window.geometry(f"{screen_width}x{screen_height}")
login_window.resizable(width=True,height=True)
image=Image.open("C:\\Users\\monis\\OneDrive\\Desktop\\hotel management system\\images\\hotel.jpg")
image=image.resize((screen_width,screen_height),Image.LANCZOS)
backgroung_image=ImageTk.PhotoImage(image)
backgroung_label=Label(login_window,image=backgroung_image)
backgroung_label.place(x=0,y=0,relheight=1,relwidth=1)

label=Label(login_window,text="STM HOTELS",fg="Gold",font=("Algerian",40),bg="black")
label.place(x=0,y=0,width=1300,height=120)


image1=Image.open("C:\\Users\\monis\\OneDrive\\Desktop\\hotel management system\\images\\Logo1.jpg")
image1=image1.resize((120,120),Image.LANCZOS)
path=ImageTk.PhotoImage(image1)
path_label=Label(login_window,image=path,bd=0)
path_label.grid(row=0,column=0)

def open_main_window():
    login_window.destroy()  
    import Main
    Main.main()

def authentication():
    username1=entry1.get()
    password=entry2.get()

    if username1=="Monish" and password=="STM Hotels":
        messagebox.showinfo("Success","Login Successfully")
        open_main_window()
        
        
    else:
        messagebox.showerror("Error!","Invalid Username or Password. Please Try Again")

username=Label(login_window,text="User Name:",font=("Algerian",15))
username.place(x=400,y=200)
entry1=Entry(login_window,width=50)
entry1.place(x=540,y=200)

Pass=Label(login_window,text="Password:",font=("Algerian",15))
Pass.place(x=400,y=300)
entry2=Entry(login_window,show="*",width=50)
entry2.place(x=540,y=300)

login=Button(login_window,text="LOGIN",font=("Algerian",20),bg="Grey",command=authentication)
login.place(x=550,y=400)



login_window.mainloop()


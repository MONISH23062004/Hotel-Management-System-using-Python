from tkinter import *
from PIL import Image,ImageTk

def main():

    main_page_window=Tk()
    main_page_window.title("STM Hotels")
    main_page_window.geometry("1300x1300")
    main_page_window.resizable(height=True,width=True)

    image1=Image.open("C:\\Users\\monis\\OneDrive\\Desktop\\hotel management system\\images\\1st pic.jpg")
    image1=image1.resize((1270,150),Image.LANCZOS)
    path=ImageTk.PhotoImage(image1)
    path_label=Label(main_page_window,image=path,bd=0)
    path_label.grid(row=0,column=0)



    label=Label(main_page_window,text="STM HOTELS",font=("Algerian",40),bg="black",fg="Gold")
    label.place(x=0,y=152,width=1300)

    def open_customer_window():  
        import customer
        customer.main()

    customer=Button(main_page_window,text="Customer",font=("Algerian",20),bg="black",fg="gold",command=open_customer_window)
    customer.place(x=0,y=219,width=267)

    def open_room_window():
        import room
        room.main()

    room=Button(main_page_window,text="Room",font=("Algerian",20),bg="black",fg="gold",command=open_room_window)
    room.place(x=0,y=275,width=267)


    def open_booking_window():
        import booking
        booking.main()

    book=Button(main_page_window,text="Booking",font=("Algerian",20),bg="Black",fg="Gold",command=open_booking_window)
    book.place(x=0,y=330,width=267)



    image2=Image.open("C:\\Users\\monis\\OneDrive\\Desktop\\hotel management system\\images\\2.jpg")
    image2=image2.resize((1000,467),Image.LANCZOS)
    backgroung_image=ImageTk.PhotoImage(image2)
    backgroung_label=Label(main_page_window,image=backgroung_image)
    backgroung_label.place(x=267,y=217)

    image=Image.open("C:\\Users\\monis\\OneDrive\\Desktop\\hotel management system\\images\\4.jpg")
    image=image.resize((264,300),Image.LANCZOS)
    background=ImageTk.PhotoImage(image)
    backgroundlabel=Label(main_page_window,image=background)
    backgroundlabel.place(x=0,y=385)


    main_page_window.mainloop()

if __name__=="__main__":
    main()

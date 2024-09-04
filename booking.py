from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main():
    root=Tk()
    root.title("Room Update")

    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hms" 
    )

    mycursor=mydb.cursor()


    width=1050
    height=470
    screen_width=root.winfo_screenwidth()
    screen_height=root.winfo_screenheight()
    x=screen_width-width
    y=screen_height-height
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(width=True,height=True)
    heading=Label(root,text="Booking Details",font=("Algerian",30),fg="Gold",bg="Black")
    heading.place(x=0,y=0,width=1042)


    def display_room_numbers():
        mycursor.execute("SELECT room_no, room_type FROM room")
        room_info = mycursor.fetchall()

        # Fetch already booked room numbers
        mycursor.execute("SELECT DISTINCT room_no FROM booking")
        booked_room_numbers = mycursor.fetchall()

        # Filter out already booked room numbers from the available room numbers
        available_room_numbers = [room[0] for room in room_info if room[0] not in booked_room_numbers]

        # Create a dictionary to map room numbers to their types
        room_types = {room[0]: room[1] for room in room_info}

        return available_room_numbers, room_types



    def update_room_numbers():
        room_options = display_room_numbers()  # Fetch room numbers here
        combobox_room_no['values'] = room_options




    def calender():
        window=Toplevel(root)
        window.title("Select Date")
        data_entry=DateEntry(window,width=12, background="darkblue", foreground="white", borderwidth=2)
        data_entry.place(x=0,y=0)

        def get_entry():
            selected_data=data_entry.get_date()
            entry2.delete(0, END) 
            entry2.insert(0, selected_data.strftime("%Y-%m-%d"))
            update_room_numbers()
  
        button1=Button(window,text="Confirm Date.",command=get_entry)
        button1.place(x=50,y=50)



    def calender1():
        window1=Toplevel(root)
        window1.title("Check Out")
        data_entry1=DateEntry(window1,width=12,background="Blue",foreground="White",borderwidth=2)
        data_entry1.place(x=0,y=0)

        def get_entry1():
            selected_data1=data_entry1.get_date()
            entry3.delete(0,END)
            entry3.insert(0,selected_data1.strftime("%Y-%m-%d"))
            update_room_numbers()
        button2=Button(window1,text="Confirm Date.",command=get_entry1)
        button2.place(x=50,y=50)


    def days():
        indate = datetime.strptime(entry2.get(), "%Y-%m-%d")
        outdate = datetime.strptime(entry3.get(), "%Y-%m-%d")
        total_days = (outdate - indate).days
        entry5.delete(0, END)
        entry5.insert(0, str(total_days))

    def calculate_bill():
        # Calculate the number of days first
        days()
        
        roomtype = combobox.get()
        total_days = entry5.get()

        if not total_days:
            messagebox.showerror("Error", "Please enter the number of days.")
            return

        try:
            total_days = int(total_days)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for number of days.")
            return

        room_price = {"Single": 3500, "Double": 7000, "Suite": 10000, "Deluxe": 15000}
        
        
        if roomtype not in room_price:
            messagebox.showerror("Error", "Invalid room type selected.")
            return
        
        sub_total = room_price[roomtype] * int(total_days)
        entry6.delete(0, END)
        entry6.insert(0, sub_total)
        print("Subtotal calculated:", sub_total)
        
        tax_rate = 0.1
        tax = sub_total * tax_rate
        entry7.delete(0, END)
        entry7.insert(0, tax)

        total_cost = sub_total + tax
        entry8.delete(0, END)
        entry8.insert(0, total_cost)

    def add_booking():
        mail = entry0.get()  
        MobileNo = entry1.get()  
        Checkin = entry2.get()  
        checkout = entry3.get()  
        room_type = combobox.get()  
        room_no = combobox_room_no.get()  
        No_Of_Days = entry5.get()  
        sub_total = entry6.get()  
        tax = entry7.get()  
        total = entry8.get()  

        entry0.delete(0, END)
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry5.delete(0, END)
        entry6.delete(0, END)
        entry7.delete(0, END)
        entry8.delete(0, END)

        insert = "INSERT INTO booking (mail,contact , `check-in` ,`check-out` ,`room_type` ,`room_no`,`No_Of_Days`  , `sub_total` ,`tax` ,`total` ) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s, %s)"
        values = (mail, MobileNo, Checkin, checkout, room_type, room_no, No_Of_Days, sub_total, tax, total)

        mycursor.execute(insert, values)
        mydb.commit()

        customer_id = mycursor.lastrowid

        details_table.insert('', 'end', values=(customer_id, mail, MobileNo, Checkin, checkout, room_type, room_no, No_Of_Days, sub_total, tax, total))
        



    def display_customer_details():
    # Clear existing data in the Treeview widget
        details_table.delete(*details_table.get_children())

        # Fetch data from the booking table ordered by ID
        mycursor.execute("SELECT * FROM booking ORDER BY ID")
        rows = mycursor.fetchall()

        # Insert fetched data into the Treeview widget with updated IDs
        for index, row in enumerate(rows, start=1):
            details_table.insert('', 'end', values=(index, *row[1:]))


    def delete_customer():
        selected_item = details_table.selection()
        if selected_item:
            customer_id = details_table.item(selected_item)['values'][0]  # Get the ID of the selected item
            mycursor.execute("DELETE FROM booking WHERE ID = %s", (customer_id,))
            mydb.commit()  # Commit the transaction to reflect the changes in the database
            details_table.delete(selected_item)





    table_frame=LabelFrame(root,bd=5,relief=RIDGE,text="Room Details",font=("Algerian",12))
    table_frame.place(x=0,y=56,width=500,height=380)

    mail=Label(root,text="Mail Id:",font=("Algerian",12))
    mail.place(x=10,y=75)
    entry0=Entry(root,bd=5)
    entry0.place(x=160,y=75,width=150)


    contact=Label(root,text="Contact Number:",font=("Algerian",12))
    contact.place(x=10,y=100)
    entry1=Entry(root,bd=5)
    entry1.place(x=160,y=100,width=150)


    checkin=Label(root,text="CheckIn Date:",font=("Algerian",12))
    checkin.place(x=10,y=135)
    entry2=Entry(root,bd=5,)
    entry2.place(x=160,y=135,width=150)
    button=Button(root,text="Select Date.",command=calender)
    button.place(x=330,y=135)

    checkout=Label(root,text="CheckOut Date:",font=("Algerian",12))
    checkout.place(x=10,y=175)
    entry3=Entry(root,bd=5)
    entry3.place(x=160,y=175,width=150)
    button=Button(root,text="Select Date.",command=calender1)
    button.place(x=330,y=175)

    room=Label(root,text="Room Type:",font=("Algerian",12))
    room.place(x=10,y=210)
    options=["Single","Double","Suite","Deluxe"]
    combobox=ttk.Combobox(root,values=options)
    combobox.place(x=160,y=210,width=150)

    room_no = Label(root, text="Room No.:", font=("Algerian", 12))
    room_no.place(x=10, y=240)
    room_options, room_types = display_room_numbers()  # Fetch room numbers and types here
    combobox_room_no = ttk.Combobox(root, values=room_options)
    combobox_room_no.place(x=160, y=240, width=150)

    # Access the room type for the selected room number
    selected_room_no = combobox_room_no.get()
    selected_room_type = room_types.get(selected_room_no, "")  # Get the room type corresponding to the selected room number

    # Use selected_room_type as needed in your code


    No_Of_Days=Label(root,text="No. Of Days:",font=("Algerian",12))
    No_Of_Days.place(x=10,y=270)
    entry5=Entry(root,bd=5)
    entry5.place(x=160,y=270,width=150)
    button=Button(root,text="Calculate Days",command=days)
    button.place(x=330,y=270)

    sub_total=Label(root,text="Sub Total",font=("Algerian",12))
    sub_total.place(x=10,y=300)
    options=[3500,7]
    entry6=Entry(root,bd=5)
    entry6.place(x=160,y=300,width=150)


    tax=Label(root,text="Paid Tax:",font=("Algerian",12))
    tax.place(x=10,y=330)
    entry7=Entry(root,bd=5)
    entry7.place(x=160,y=330,width=150)

    cost=Label(root,text="Total Cost:",font=("Algerian",12))
    cost.place(x=10,y=360)
    entry8=Entry(root,bd=5)
    entry8.place(x=160,y=360,width=150)

    bill=Button(root,text="Generate Bill",bd=5,font=("Algerian",12),fg="gold",bg="black",command=calculate_bill)
    bill.place(x=25,y=390)

    add=Button(root,text="Add",bd=5,font=("Algerian",12),fg="gold",bg="black",command=add_booking)
    add.place(x=180,y=390)

    delete=Button(root,text="Delete",bd=5,font=("Algerian",12),fg="gold",bg="black",command=delete_customer)
    delete.place(x=250,y=390)

    table_frame=LabelFrame(root,bd=5,relief=RIDGE,text="View Details and Search System",font=("Algerian",12))
    table_frame.place(x=500,y=53,width=535,height=380)

    table=Frame(table_frame,bd=5,relief=RIDGE)
    table.place(x=0,y=10,width=525,height=350)

    scroll_x=ttk.Scrollbar(table,orient=HORIZONTAL)
    scroll_y=ttk.Scrollbar(table,orient=VERTICAL)

    details_table=ttk.Treeview(table,columns=("ID","mail","Mobile No.","Check-in","Check-out","Room-Type","Room-No.","No. Of Days","Sub_Total","Tax","Total-Cost"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

    scroll_x.pack(side=BOTTOM,fill=X)
    scroll_y.pack(side=RIGHT,fill=Y)

    scroll_x.config(command=details_table.xview)
    scroll_y.config(command=details_table.yview)


    details_table.heading("ID",text="ID")
    details_table.heading("mail",text="mail")
    details_table.heading("Mobile No.",text="Mobile No.")
    details_table.heading("Check-in",text="Check-in")
    details_table.heading("Check-out",text="Check-out")
    details_table.heading("Room-Type",text="Room-Type")
    details_table.heading("Room-No.",text="Room-No.")
    details_table.heading("No. Of Days",text="No. Of Days")
    details_table.heading("Sub_Total",text="Sub-Total")
    details_table.heading("Tax",text="Tax")
    details_table.heading("Total-Cost",text="Total-Cost")

    details_table["show"]="headings"


    details_table.column("ID",width=120)
    details_table.column("mail",width=200)
    details_table.column("Mobile No.",width=120)
    details_table.column("Check-in",width=120)
    details_table.column("Check-out",width=120)
    details_table.column("Room-Type",width=120)
    details_table.column("Room-No.",width=120)
    details_table.column("No. Of Days",width=120)
    details_table.column("Sub_Total",width=120)
    details_table.column("Tax",width=120)
    details_table.column("Total-Cost",width=120)



    details_table.pack(fill=BOTH,expand=1)

    display_customer_details()

    root.mainloop()

if __name__=="__main__":
    main()
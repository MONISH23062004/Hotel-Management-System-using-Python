from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from tkinter import messagebox

def main():
    root=Tk()
    root.title("CUSTOMER")
    width=1050
    height=470
    screen_width=root.winfo_screenwidth()
    screen_height=root.winfo_screenheight()
    x=screen_width-width
    y=screen_height-height
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(width=True,height=True)
    heading=Label(root,text="Customer Details",font=("Algerian",30),fg="Gold",bg="Black")
    heading.place(x=0,y=0,width=1050)

    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hms" 
    )

    mycursor=mydb.cursor()



    def add_customer():
        Name = entry1.get().center(40)
        DOB = entry2.get().center(40)
        Nation = entry3.get().center(40)
        Number = entry4.get().center(40)
        Mail = entry5.get().center(40)
        Address = combobox.get().center(40)
        City = entry7.get().center(40)
        PostalCode = entry8.get().center(40)
        State = entry9.get().center(40)
        
        insert = "INSERT INTO customer(Name, DOB, Nation, Number, Mail, Address, City, PostalCode, State) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (Name, DOB, Nation, Number, Mail, Address, City, PostalCode, State)

        mycursor.execute(insert, values)
        mydb.commit()

        # Fetch the auto-incremented ID of the inserted record
        customer_id = mycursor.lastrowid

        # Insert the ID along with other details into the details_table
        details_table.insert('', 'end', values=(customer_id, Name, DOB, Nation, Number, Mail, Address, City, PostalCode, State))

        # Clear entry fields after adding customer
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry4.delete(0, END)
        entry5.delete(0, END)
        entry7.delete(0, END)
        entry8.delete(0, END)
        entry9.delete(0, END)


    def display_customer_details():
        try:
            # Clear existing data in the Treeview widget
            for row in details_table.get_children():
                details_table.delete(row)

            # Fetch data from the room table with the desired column order
            mycursor.execute("SELECT ID, Name, DOB, Nation, Number, Mail, Address, City, PostalCode, State FROM customer")
            rows = mycursor.fetchall()

            # Insert fetched data into the Treeview widget with sequential IDs
            for idx, row in enumerate(rows, start=1):
                details_table.insert('', 'end', values=(idx,) + row[1:])
        except mysql.connector.Error as err:
            print(f"Error fetching data from database: {err}")
            messagebox.showerror("Error", f"Failed to fetch data from database: {err}")

    

    def delete_customer():
        selected_item = details_table.selection()
        if selected_item:
            customer_id = details_table.item(selected_item)['values'][0]
            print("Customer ID:", customer_id)  # Debugging

            try:
                # Construct and execute SQL query
                mycursor.execute("DELETE FROM customer WHERE ID = %s", (customer_id,))
                mydb.commit()
                print("Customer deleted successfully")  # Debugging

                # Remove item from GUI
                details_table.delete(selected_item)
            except mysql.connector.Error as err:
                print("Error:", err)  # Debugging


    def calender1():
        window1=Toplevel(root)
        window1.title("Check Out")
        data_entry1=DateEntry(window1,width=12,background="Blue",foreground="White",borderwidth=2)
        data_entry1.place(x=0,y=0)

        def get_entry1():
            selected_data1=data_entry1.get_date()
            entry2.delete(0,END)
            entry2.insert(0,selected_data1.strftime("%Y-%m-%d"))
        button2=Button(window1,text="Confirm Date.",command=get_entry1)
        button2.place(x=50,y=50)


    name=Label(root,text="Full Name:",font="Algerian")
    name.place(x=0,y=70)
    entry1=Entry(root,bd=5)
    entry1.place(x=160,y=77)

    dob=Label(root,text="Date of Birth:",font="Algerian")
    dob.place(x=0,y=110)
    entry2=Entry(root,bd=5)
    entry2.place(x=160,y=115)
    button=Button(root,text="Select Date",command=calender1,bg="black",fg="Gold",bd=5,font=("algerian",10))
    button.place(x=300,y=110)


    nation=Label(root,text="Nationality:",font="Algerian")
    nation.place(x=0,y=150)
    entry3=Entry(root,bd=5)
    entry3.place(x=160,y=155)

    number=Label(root,text="Phone Number:",font="Algerian")
    number.place(x=0,y=190)
    entry4=Entry(root,bd=5)
    entry4.place(x=160,y=195)

    mail=Label(root,text="Email:",font="Algerian")
    mail.place(x=0,y=230)
    entry5=Entry(root,bd=5)
    entry5.place(x=160,y=235)

    address=Label(root,text="Gender:",font="Algerian")
    address.place(x=0,y=270)
    options=["Male","Female"]
    combobox=ttk.Combobox(root,values=options)
    combobox.place(x=160,y=275)

    city=Label(root,text="City:",font="Algerian")
    city.place(x=0,y=310)
    entry7=Entry(root,bd=5)
    entry7.place(x=160,y=315)

    code=Label(root,text="Postal Code:",font="Algerian")
    code.place(x=0,y=350)
    entry8=Entry(root,bd=5)
    entry8.place(x=160,y=355)

    state=Label(root,text="State:",font="Algerian")
    state.place(x=0,y=390)
    entry9=Entry(root,bd=5)
    entry9.place(x=160,y=395)

    add=Button(root,text="Add",font=("Algerian",15),bg="black",fg="Gold",bd=5,command=add_customer)
    add.place(x=300,y=150,width=100)

    delete=Button(root,text="Delete",font=("Algerian",15),bg="black",fg="Gold",bd=5,command=delete_customer)
    delete.place(x=300,y=200,width=100)

    final=Label(root,text="")
    final.place(x=500,y=100)

    table_frame=LabelFrame(root,bd=2,relief=RIDGE,text="View Details",font=("Algerian",12))
    table_frame.place(x=400,y=65,width=635,height=400)


    table=Frame(table_frame,bd=5,relief=RIDGE)
    table.place(x=0,y=10,width=630,height=350)

    scroll_x=ttk.Scrollbar(table,orient=HORIZONTAL)
    scroll_y=ttk.Scrollbar(table,orient=VERTICAL)

    details_table=ttk.Treeview(table,columns=("ID","Full Name","DOB","Nationality","Phone Number","Email","Gender","City","Postal Code","State"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

    scroll_x.pack(side=BOTTOM,fill=X)
    scroll_y.pack(side=RIGHT,fill=Y)

    scroll_x.config(command=details_table.xview)
    scroll_y.config(command=details_table.yview)


    details_table.heading("ID",text="ID")
    details_table.heading("Full Name",text="Full Name")
    details_table.heading("DOB",text="D.O.B")
    details_table.heading("Nationality",text="Nationality")
    details_table.heading("Phone Number",text="Phone Number")
    details_table.heading("Email",text="Email")
    details_table.heading("Gender",text="Gender")
    details_table.heading("City",text="City")
    details_table.heading("Postal Code",text="Postal Code")
    details_table.heading("State",text="State")

    details_table["show"]="headings"

    details_table.column("ID",width=100)
    details_table.column("Full Name",width=150)
    details_table.column("DOB",width=150)
    details_table.column("Nationality",width=150)
    details_table.column("Phone Number",width=150)
    details_table.column("Email",width=150)
    details_table.column("Gender",width=150)
    details_table.column("City",width=150)
    details_table.column("Postal Code",width=150)
    details_table.column("State",width=150)


    details_table.pack(fill=BOTH,expand=1)

    display_customer_details()

    root.mainloop()

if __name__=="__main__":
    main()
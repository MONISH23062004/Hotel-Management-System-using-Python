from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

def main():
    root=Tk()
    root.title("Room Details")

    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hms" 
    )

    mycursor=mydb.cursor()

    def add():
        floor=combo1.get()
        room_no=entry2.get()
        room_type=combo2.get()

        insert= "INSERT INTO room (floor, room_no, room_type) VALUES (%s, %s, %s)"
        values = (floor, room_no, room_type)

        mycursor.execute(insert, values)
        mydb.commit()

        customer_id = mycursor.lastrowid

        details_table.insert('', 'end', values=(customer_id,floor,room_no,room_type))


        combo1.get()
        entry2.get()
        combo2.get()

    def display_customer_details():
        try:
            # Clear existing data in the Treeview widget
            for row in details_table.get_children():
                details_table.delete(row)

            # Fetch data from the room table with the desired column order
            mycursor.execute("SELECT ID, floor, room_no, room_type FROM room")
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
            values = details_table.item(selected_item)['values']
            customer_id = values[0]
            try:
                mycursor.execute("DELETE FROM room WHERE ID = %s", (customer_id,))
                mydb.commit()
                details_table.delete(selected_item)
                print(f"Record with ID {customer_id} deleted successfully.")
            except mysql.connector.Error as err:
                print(f"Error deleting record: {err}")
                messagebox.showerror("Error", f"Failed to delete record: {err}")
        else:
            messagebox.showinfo("Error", "Please select a record to delete.")



    width=1050
    height=470
    screen_width=root.winfo_screenwidth()
    screen_height=root.winfo_screenheight()
    x=screen_width-width
    y=screen_height-height
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(width=True,height=True)
    heading=Label(root,text="Room Details",font=("Algerian",30),fg="Gold",bg="Black")
    heading.place(x=0,y=0,width=1042)

    box1=LabelFrame(root,tex="New Room Add Details",relief=RIDGE,font=("Algerian",12),bd=10)
    box1.place(x=0,y=59,width=500,height=250)

    floor=Label(root,text="Floor:",font=("Algerian",12))
    floor.place(x=50,y=100)
    option=[1,2,3,4,5]
    combo1=ttk.Combobox(root,values=option)
    combo1.place(x=145,y=100)

    room_no=Label(root,text="Room No.:",font=("Algerian",12))
    room_no.place(x=50,y=150)
    entry2=Entry(root,bd=5)
    entry2.place(x=145,y=150,width=150)

    room_type=Label(root,text="Room Type:",font=("Algerian",12))
    room_type.place(x=50,y=200)
    options1=["Single","Double","Suite","Deluxe"]
    combo2=ttk.Combobox(root,values=options1)
    combo2.place(x=145,y=200)

    add=Button(root,bd=5,text="Add",fg="Gold",bg="Black",font=("Algerian",12),command=add)
    add.place(x=100,y=250)

    delete=Button(root,text="Delete",fg="Gold",bg="Black",font=("Algerian",12),bd=5,command=delete_customer)
    delete.place(x=200,y=250)

    box2=LabelFrame(root,tex="Show Room Details",relief=RIDGE,font=("Algerian",12),bd=10)
    box2.place(x=510,y=59,width=500,height=250)

    table=Frame(box2,bd=0,relief=RIDGE)
    table.place(x=0,y=10,width=480,height=200)

    scroll_x=ttk.Scrollbar(table,orient=HORIZONTAL)
    scroll_y=ttk.Scrollbar(table,orient=VERTICAL)

    details_table=ttk.Treeview(table,columns=("ID","Floor","Room-No.","Room-Type"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

    scroll_x.pack(side=BOTTOM,fill=X)
    scroll_y.pack(side=RIGHT,fill=Y)

    scroll_x.config(command=details_table.xview)
    scroll_y.config(command=details_table.yview)


    details_table.heading("ID",text="ID")
    details_table.heading("Floor",text="Floor")
    details_table.heading("Room-No.",text="Room-No.")
    details_table.heading("Room-Type",text="Room-Type")

    details_table["show"]="headings"

    details_table.column("ID",width=10)
    details_table.column("Floor",width=10)
    details_table.column("Room-No.",width=10)
    details_table.column("Room-Type",width=10)


    details_table.pack(fill=BOTH,expand=1)

    display_customer_details()


    root.mainloop()

if __name__=="__main__":
    main()

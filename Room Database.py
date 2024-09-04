import mysql.connector
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hms" 
)

mycursor=mydb.cursor()
mycursor.execute('''CREATE TABLE room(ID INT AUTO_INCREMENT PRIMARY KEY,floor int,room_no int,room_type varchar(50))''')

import mysql.connector
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hms" 
)

mycursor=mydb.cursor()
mycursor.execute('''CREATE TABLE customer (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    DOB DATE,
    Nation VARCHAR(255),
    Number VARCHAR(20),
    Mail VARCHAR(255),
    Address VARCHAR(255),
    City VARCHAR(255),
    PostalCode VARCHAR(20),
    State VARCHAR(255)
);
''')

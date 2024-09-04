import mysql.connector
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hms" 
)

mycursor=mydb.cursor()
mycursor.execute('''CREATE TABLE booking(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    mail varchar(50),
    contact BIGINT,
    `check-in` DATE,
    `check-out` DATE,
    `room_type` VARCHAR(20),
    `room_no` INT,
    `No_Of_Days` INT,
    `sub_total` INT,
    `tax` INT,
    `total` INT
)''')


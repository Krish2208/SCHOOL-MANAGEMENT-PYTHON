import mysql.connector
import hashlib
import getpass

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
)
cursor = mydb.cursor()
cursor.execute("CREATE DATABASE SCHOOL2")

mydb2 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="SCHOOL2",
)

cursor = mydb2.cursor()
cursor.execute("CREATE TABLE users (id VARCHAR(50) primary key, password VARCHAR(64) not null, class char(2) not null, section char(1) not null, name varchar(50) not null, role varchar(10) not null, verified bool default false)")
cursor.execute("create table students(admnNo int not null AUTO_INCREMENT,name varchar(50) not null, fatherName varchar(50), motherName varchar(50), dob date, mobileNo int(10), email varchar(50), primary key (admnNo));")
print("Creating Admin Account ")

try:
    name = input("Enter your Name : ")
    email = input("Enter your Email : ")
    pwd = getpass.getpass()
    hashed = hashlib.sha256(pwd.encode())
    password = hashed.hexdigest()

    cursor = mydb2.cursor()
    query = "INSERT INTO users (name, id, password, class, section, role, verified) VALUES (%s, %s, %s, %s, %s, %s, true)"
    val = (name, email, password, '0', '0', 'admin')
    cursor.execute(query, val)
    mydb2.commit()
except Exception as err:
    print('Error Occured : ', err)

def addNewClass(clas, sec):
    cursor = mydb2.cursor()
    query = "CREATE TABLE {}{}(rollNo int(6) primary key auto_increment, admnNo int not null, data text, FOREIGN KEY (admnNo) REFERENCES students(admnNo))".format(clas,sec)
    cursor.execute(query)

print("\nCreating Class Tables\n")
j = int(input("Enter no of Section in each class : "))
for i in range(1,13):
    for x in range(0,j):
        addNewClass(str(i), chr(65+x))

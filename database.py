import mysql.connector
import hashlib
import getpass
from prettytable import from_db_cursor

authenticated = False
current_user = None

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="SCHOOL",
)

if mydb.is_connected():
    print("Succesfully Connected to MySQL Database")
else:
    print("Unable to connect to the Database")


def register():
    try:
        name = input("Enter your Name : ")
        email = input("Enter your Email : ")
        pwd = getpass.getpass()
        clas = input("Enter the Class : ")
        sec = input("Enter the Section : ")
        hashed = hashlib.sha256(pwd.encode())
        password = hashed.hexdigest()

        cursor = mydb.cursor()
        query = "INSERT INTO users (name, id, password, class, section, role) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, email, password, clas, sec, 'teacher')
        cursor.execute(query, val)
        mydb.commit()
    except Exception as err:
        print('Error Occured : ', err)


def login():
    global authenticated
    global current_user
    try:
        email = input("Enter your Email : ")
        pwd = getpass.getpass()
        hashed = hashlib.sha256(pwd.encode())
        password = hashed.hexdigest()
        cursor = mydb.cursor()
        query = "SELECT * from users where id = '{}'".format(email)
        cursor.execute(query)
        if(len(cursor.fetchall()) == 0):
            print("The above Email is not registered")
        else:
            res = cursor.fetchall()[0]
            if(res[1] == password):
                if(res[6] == 1):
                    authenticated = True
                    current_user = res
                else:
                    print("This user is currently not verified by the Admin")
            else:
                print("Invalid Password")
    except Exception as err:
        print('Error Occured : ', err)


def addNewStudent():
    try:
        name = input("Enter Name : ")
        fatherName = input("Enter the Father's Name : ")
        motherName = input("Enter the Mother's Name : ")
        dob = input("Enter the DOB (yyyy-mm-dd) : ")
        mobileNo = int(input("Enter the Mobile No : "))
        email = input("Enter the Email : ")
        cursor = mydb.cursor()
        query = "INSERT INTO students (name, fatherName, motherName, dob, mobileNo, email) VALUES ('{}','{}','{}','{}',{},'{}')".format(
            name, fatherName, motherName, dob, mobileNo, email)
        cursor.execute(query)
        mydb.commit()
    except Exception as err:
        print('Error Occured : ', err)


def updateStudent():
    try:
        admnNo = int(input("Enter the Admission Number of the Student : "))
        cursor = mydb.cursor()
        query = "SELECT * from students where admnNo = {}".format(admnNo)
        cursor.execute(query)
        k = cursor.fetchall()
        if(len(k) == 0):
            print("404 Student Not Found")
        else:
            res = k[0]
            print(res)
            name = input("Enter Name : ")
            fatherName = input("Enter the Father's Name : ")
            motherName = input("Enter the Mother's Name : ")
            dob = input("Enter the DOB (yyyy-mm-dd) : ")
            mobileNo = int(input("Enter the Mobile No : "))
            email = input("Enter the Email : ")
            cursor = mydb.cursor()
            query = "UPDATE students set name='{}', fatherName='{}', motherName='{}', dob='{}' , mobileNo={} , email='{}' where admnNo={}".format(
                name, fatherName, motherName, dob, mobileNo, email, admnNo)
            cursor.execute(query)
            mydb.commit()
    except Exception as err:
        print("Error Occured : ", err)


def viewStudent():
    try:
        admnNo = int(input("Enter the Admission Number of the Student : "))
        cursor = mydb.cursor()
        query = "SELECT * from students where admnNo = {}".format(admnNo)
        cursor.execute(query)
        mytable = from_db_cursor(cursor)
        print(mytable)
    except Exception as err:
        print("Error Occured : ", err)


def viewAllStudent():
    try:
        cursor = mydb.cursor()
        query = "SELECT * from students"
        cursor.execute(query)
        mytable = from_db_cursor(cursor)
        print(mytable)
    except Exception as err:
        print("Error Occured : ", err)


def addClass():
    try:
        clas = int(input("Enter the Class : "))
        sec = input("Enter the section : ")
        query = "CREATE TABLE {}{}(rollNo int(6) primary key auto_increment, admnNo int not null, data text, FOREIGN KEY (admnNo) REFERENCES students(admnNo))".format(
            clas, sec)
        cursor = mydb.cursor()
        cursor.execute(query)
    except Exception as err:
        print("Error Occured : ", err)


def adminVerify():
    cursor = mydb.cursor()
    query = "SELECT * from users where verified=false"
    cursor.execute(query)
    res = cursor.fetchall()
    print("To verify enter 1 else enter 0")
    for i in res:
        print(
            "Name :- {}\tClass :- {}\tSection :- {}".format(i[4], i[2], i[3]))
        e = int(input("Enter :- "))
        if(e == 1):
            query = "UPDATE users set verified=true where id='{}'".format(i[0])
            cursor.execute(query)
            mydb.commit()


def adminRevoke():
    cursor = mydb.cursor()
    query = "Select id,name,class,section from users where verified=true"
    cursor.execute(query)
    mytable = from_db_cursor(cursor)
    print(mytable)
    print("\nTo Revoke any permission enter the id of the user")
    while True:
        n = input("\nEnter the ID to be revoked : ")
        query = "UPDATE users set verified=false where id='{}'".format(n)
        cursor.execute(query)
        mydb.commit()
        c = input("Do you want to revoke more(y/n) ? ")
        if c == 'n':
            break


def viewStaff():
    try:
        cursor = mydb.cursor()
        query = "SELECT name,id,class,section from users"
        cursor.execute(query)
        mytable = from_db_cursor(cursor)
        print(mytable)
    except Exception as err:
        print("Error Occured : ", err)


def refreshRollNo(c, s, roll):
    try:
        cursor = mydb.cursor()
        query = "Select admnNo from {}{}".format(c, s)
        cursor.execute(query)
        l = cursor.fetchall()
        if(roll == 0):
            lst = []
        else:
            lst = roll
        for i in l:
            lst.append(i[0])
        query = "truncate table {}{}".format(c, s)
        cursor.execute(query)
        mydb.commit()
        query = "SELECT admnNo from students where admnNo in {} order by name".format(
            tuple(lst))
        cursor.execute(query)
        l = cursor.fetchall()
        query2 = "INSERT INTO {}{} (admnNo) VALUES (%s)".format(c, s)
        cursor.executemany(query2, list(l))
        mydb.commit()
    except Exception as err:
        print("Error Occured : ", err)


def addStudentToClass(c, s):
    try:
        lst = list(eval(input(
            "Enter the Admission No. of Student to be added to your class(seperated by comma) : ")))
        refreshRollNo(c, s, lst)
    except Exception as err:
        print("Error Occured : ", err)


def viewStudentsClass(c, s):
    try:
        cursor = mydb.cursor()
        query = "Select {}{}.rollNo, students.* from {}{} inner join students on {}{}.admnNo=students.admnNo order by {}{}.rollNo".format(
            c, s, c, s, c, s, c, s)
        cursor.execute(query)
        mytable = from_db_cursor(cursor)
        print(mytable)
    except Exception as err:
        print("Error Occured : ", err)


def removeStudentFromClass(c, s):
    try:
        rollNo = int(
            input("Enter the Roll Number of the Student to be removed : "))
        cursor = mydb.cursor()
        query = "DELETE from {}{} where rollNo={}".format(c, s, rollNo)
        cursor.execute(query)
        mydb.commit()
        refreshRollNo(c, s, 0)
    except Exception as err:
        print("Error Occured : ", err)


def main():
    global authenticated
    global current_user
    print("Welcome to the School Management System")
    print("1. Login\n2. Register")
    for i in range(0, 5):
        if authenticated:
            break
        else:
            c1 = int(input("Enter the above choice : "))
            if(c1 == 1):
                login()
            elif(c1 == 2):
                register()
            else:
                print("Incorrect Choice")
    else:
        print("Exceeded the security Limit")
    if(authenticated):
        if(current_user[5] == 'admin'):
            adminVerify()
        else:
            addStudentToClass(12, 'A')


removeStudentFromClass(12, 'a')

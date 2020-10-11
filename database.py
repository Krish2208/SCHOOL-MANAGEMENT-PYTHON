import mysql.connector, hashlib, getpass

authenticated = False
current_user = None

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="gamescracy22",
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
        res = cursor.fetchall()[0]
        if(res[1]==password):
            if(res[6]==1):
                authenticated = True
                current_user = res
            else:
                print("This user is currently not verified by the Admin")
        else:
            print("Invalid Password")
    except Exception as err:
        print('Error Occured : ', err)

def admin_verify():
    cursor = mydb.cursor()
    query = "SELECT * from users where verified=false"
    cursor.execute(query)
    res = cursor.fetchall()
    print("To verify enter 1 else enter 0")
    for i in res:
        print("Name :- {}\tClass :- {}\tSection :- {}".format(i[4], i[2], i[3]))
        e = int(input("Enter :- "))
        if(e==1):
            query="UPDATE users set verified=true where id='{}'".format(i[0])
            cursor.execute(query)
            mydb.commit()

def main():
    global authenticated
    global current_user
    login()
    if(authenticated):
        if(current_user[5]== 'admin'):
            admin_verify()

main()
###Quiz using Python

import mysql.connector as my

con = my.connect(host = "127.0.0.1",user = "root",password ="root")

cur = con.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS quiz")

cur.execute("USE quiz")

admin = """CREATE TABLE IF NOT EXISTS admin(
            admin_id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
            );"""
student = """CREATE TABLE IF NOT EXISTS student(
            user_id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            roll_number INT NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            marks INT
            );"""
question = """CREATE TABLE IF NOT EXISTS question(
            question_number INT PRIMARY KEY AUTO_INCREMENT,
            question VARCHAR(255) NOT NULL,
            answer INT NOT NULL
            );"""
choices = """CREATE TABLE IF NOT EXISTS choices(
            question_number INT,
            choice VARCHAR(255) NOT NULL
            );"""

cur.execute(admin)
cur.execute(student)
cur.execute(question)
cur.execute(choices)


'''Checking if the id entered is present'''
def ifPresent(id,adm):
    try:
        if adm == True:
            qip = f"SELECT admin_id FROM admin WHERE admin_id = {id}"
        else:
            qip = f"SELECT user_id FROM student WHERE user_id = {id}"
        cur.execute(qip)
        reult = cur.fetchone()

        if result:
            return True
        else:
            print(f"{id} does not exists")
            return False
            
    except mysql.connector.Eror as err:
        print(f"Erroe : {err}")



'''Checking Password'''
def validatePassword(id,password,adm):
    try:
        if adm == True:
            qvp = f"SELECT password FROM admin WHERE admin_id = {id}"
        else:
            qvp = f"SELECT password FROM student WHERE user_id = {id}"
        cur.execute(qvp)
        vp = cur.fetchone()
        if vp:
            valid = vp[0]
            print(valid,vp)
            if valid == password:
                return True
            else:
                return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")



'''Name'''
def username(id,adm):
    try:
        if adm == True:
            qun = f"SELECT name FROM admin WHERE admin_id = {id}"
        else:
            qun = f"SELECT name FROM student WHERE user_id = {id}"
        cur.execute(qu)
        result = cur.fetchone()

        
        name = result[0]
        return name
        

    except my.Error as err:
        print(f"Error: {err}")



        
'''Login'''     
def login(id,password,adm):
    if ifPresent(id,adm) == False:
        return False
    if validatePassword(id,password,adm) == False:
        print("You Have Entered wrong password")
        password = input("Enter your password again : ")
        if validatePassword(id,password,adm) == False:
            print("You Have Entered wrong password")
            password = input("Enter your password again : ")
            if validatePassword(id,password,adm) == False:
                print("You have entered wrong password 3 times so the code is exiting")
                exit()
    print("\nWelcome! ",username(id,adm))
    

def addUser():
    name = input("Enter Name : ")
    roll = int(input("Enter your roll number : "))


def addAdmin():
    name = input("Enter Name : ")
    



def addQuestion():
    try:
        questions = []
        while True:
            q1 = input("Enter the question : ")
            a1 = input("Enter it's Answer : ")
            questions.append([q1,a1])
            temp = input("if you want to add another question,Enter Y/y : ")
            if temp != "Y" or temp != "y":
                break
        qaq = f"INSERT INTO question VALUES(%s,%s,%s);"
        cur.executemany(qaq,questions)

        options = []
        print("The answer is already included in the option you need to just give options")
        while True:
            n = 2
            opt = input(f"Enter the {n} option : ")
            temp = input("if you want to add more options then press Y/y : ")
            if temp != "Y" or temp != "y":
                break
            
    except my.Error as err:
        print(f"Error : {err}")



def quiz(id):
    print("YOUR QUIZ STARTS NOW")
    try:
        qq = "SELECT * FROM question"
        cur.execute(qq)
        result = cur.fetchall()
        qo = "SELECT * FROM choices"
        cur.execute(qq)
        result1 = cur.fetchall()



def stufunction(id):
    print("""CHOOSE AN OPTION :
    1. UPDATE NAME
    2. UPDATE PASSWORD
    3. GIVE QUIZ
    4. CHECK RESULT
    """)


def adminFunction(id):
    print("""CHOOSE AN OPTION :
    1. ADD QUESTION
    2. UPDATE QUESTION
    3. DELETE QUESTION
    4. ADD OPTION
    5. DELETE OPTION
    6. UPDATE ANSWER
    7. UPDATE NAME
    8. UPDATE PASSWORD
    9. CHECK MARKS
    10. REMOVE STUDENT
    11. DELETE ACCOUNT
    
    """)
        
        
 
c = ""

while c != "3":

    print("""WELCOME,
    1. LOGIN
    2. REGISTER
    3. EXIT
    """)
            
    c = input("CHOOSE AN OPTION : ")


    if c == "1":
        print("WELCOME TO THE LOGIN PAGE\n")
        while True:
            i = input("""HOW WOULD YOU LIKE TO LOGIN:
                      PRESS 1 FOR ADMIN
                      PRESS 2 FOR STUDENT
                      PRESS 3 TO GO BACK : """)
            if i == "1":
                adm = True
                login(id,password,adm)
                break
            elif i == "2":
                adm = False
                login(id,password,adm)
                break
            elif i == "3":
                break
            else:
                print("ENTER A VALID CHOICE! ")
        
    elif c == "2":
        print("WELCOME TO THE REGISTRATION PAGE\n")
        while True:
            i = input("""HOW WOULD YOU LIKE TO REGISTER:
                      PRESS 1 FOR ADMIN
                      PRESS 2 FOR STUDENT
                      PRESS 3 TO GO BACK : """)
            if i == "1":
                addAdmin()
                break
            elif i == "2":
                addUser()
                break
            elif i == "3":
                break
            else:
                print("ENTER A VALID CHOICE! ")

        
    elif c == "3":
        exit()

        
    else:
        print("ENTER A VALID CHOICE")



#################################################################
""" Just a basic quiz in cli made using python with the help of mysql """

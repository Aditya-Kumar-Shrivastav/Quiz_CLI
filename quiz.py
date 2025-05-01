###Quiz using Python

import mysql.connector as my

con = my.connect(host = "127.0.0.1",user = "root",password ="root")

cur = con.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS quiz;")

cur.execute("USE quiz;")

admin = """CREATE TABLE IF NOT EXISTS admin(
            admin_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
            );"""
student = """CREATE TABLE IF NOT EXISTS student(
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            roll_number INT NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            marks INT
            );"""
questions = """CREATE TABLE IF NOT EXISTS questions(
            question_number INT PRIMARY KEY AUTO_INCREMENT,
            question VARCHAR(255) NOT NULL,
            answer VARCHAR(255) NOT NULL
            );"""
choices = """CREATE TABLE IF NOT EXISTS choices(
            question_number INT,
            choice VARCHAR(255) NOT NULL
            );"""

cur.execute(admin)
cur.execute(student)
cur.execute(questions)
cur.execute(choices)


'''Checking if the id entered is present'''
def ifPresent( qid ,adm):
    try:
        if adm == True:
            qip = f"SELECT admin_id FROM admin WHERE admin_id = {qid};"
        else:
            qip = f"SELECT user_id FROM student WHERE user_id = {qid};"
        cur.execute(qip)
        result = cur.fetchone()

        if result:
            return True
        else:
            print(f"{qid} does not exists")
            return False
            
    except mysql.connector.Eror as err:
        print(f"Erroe : {err}")



'''Checking Password'''
def validatePassword(qid,password,adm):
    try:
        if adm == True:
            qvp = f"SELECT password FROM admin WHERE admin_id = {qid};"
        else:
            qvp = f"SELECT password FROM student WHERE user_id = {qid};"
        cur.execute(qvp)
        vp = cur.fetchone()
        if vp:
            valid = vp[0]
            
            if valid == password:
                return True
            else:
                return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")



'''Name'''
def username(qid,adm):
    try:
        if adm == True:
            qun = f"SELECT name FROM admin WHERE admin_id = {qid};"
        else:
            qun = f"SELECT name FROM student WHERE user_id = {qid};"
        cur.execute(qun)
        result = cur.fetchone()

        
        name = result[0]
        return name
        

    except my.Error as err:
        print(f"Error: {err}")



def findqn(q1):
    try:
        cur.execute(f"SELECT question_number FROM questions WHERE question = '{q1}';")
        qn = cur.fetchone()
        print("hi")
        
        return qn[0]
    except my.Error as err:
        print(f"Error : {err}")
        con.rollback()



def addQuestion():
    try:
        questionss = []
        while True:
            q1 = input("Enter the question : ")
            a1 = input("Enter it's Answer : ")
            #questionss.append([q1,a1])
            val = (q1,a1)
            qaq = f"INSERT INTO questions(question,answer) VALUES(%s,%s);"
            cur.execute(qaq,val)
            print("hi")
            con.commit()
            
            
            qNum = findqn(q1)
            options = []
            print("The answer is already included in the option you need to just give options")
            n = 2
            while True:
                opt = input(f"Enter the {n} option : ")
                options.append((qNum,opt))
                temp = input("if you want to add more options then press Y/y : ")
                if temp.upper() != "Y":
                    break
                n += 1
                
            qo = "INSERT INTO choices(question_number,choice) VALUES(%s,%s);"
            cur.executemany(qo,options)
            con.commit()
            temp = input("if you want to add another question,Enter Y/y : ")
            if temp.upper() != "Y":
                break
        


            
    except my.Error as err:
        print(f"Error : {err}")
        con.rollback()



def checkres(qid):
    try:
        qcr = f"SELECT marks FROM student WHERE user_id = {qid};"
        cur.execute(qcr)
        result = cur.fetchone()

        if len(result) == 0:
            print("YOU HAVE NOT GIVEN THE TEST|!")
        else:
            mark = result[0]
            if mark == None:
                
                return False
            else:
                print(f"YOU HAVE RECIEVED {mark} POINTS")
                return True
        

    except my.Error as err:
        print(f"Error: {err}")




def quiz(qid):
    if checkres(qid) == True:
        print("YOU HAVE ALREADY GIVEN THE TEST!")
        return
    print("YOUR QUIZ STARTS NOW")
    marks = 0
    wrongs = []
    
    try:
        qq = "SELECT * FROM questions;"
        
        cur.execute(qq)
        result = cur.fetchall()
        i = 1
        for q in result:
            
            opt = []
            print(f"Q{i}. {q[1].upper()}")
            cur.execute(f"SELECT choice FROM choices WHERE question_number = {q[0]};")
            ch = cur.fetchall()
            ch.append((q[2],))
            print(ch)

            """ADDING RANDOM""" ##########################WILL BE ADDED IN THE NEXT UPDATE
            checkdi = {}
            temp = q[0]
            k = 1
            for j in ch:

                print(f"    {k}. {j[0]}")
                checkdi[k] = j[0]
                
                k += 1
                
            ans = input("PLEASE SELECT AN OPTION : ")
            while int(ans) > len(ch) and int(ans) <= 0:
                ans = input("INVALID CHOICE.\nPLEASE SELECT AN OPTION : ")
            if checkdi[int(ans)] == q[2]:
                marks += 1
            else:
                wrongs.append(q[0])
            i += 1
        cur.execute(f"UPDATE student SET marks = {marks} WHERE user_id = {qid};")
        con.commit()

    except my.Error as err:
        print(f"Error : {err}")
        con.rollback()


def updata(qid,k,adm):
    name = ""
    pawd = ""
    if k == "name":
        name = input("ENTER UPDATED NAME : ")
        
    else:
        pawd = input("CREATE NEW YOUR PASSWORD : ")
        cPawd = input("ENTER YOUR PASSWORD AGAIN : ")
        while pawd != cPawd:
            pawd = input("PASSWORD DIDNOT MATCH.\nCREATE YOUR PASSWORD : ")
            cPawd = input("ENTER YOUR PASSWORD AGAIN : ")
    u = pawd
    if k == "name":
        u = name
    try:
        a = "student"
        b = "user_id"
        if adm == True:
            a = "admin"
            b = "admin_id"
            
        cur.execute(f"UPDATE {a} SET {k} = %s WHERE {b} = %s;",(u,qid))       
        #cur.execute(f"UPDATE {a} SET {k} = {u} WHERE {b} = {qid};")
        con.commit()
        print(f"YOUR {k.upper()} HAS BEEN UPDATED!")
    except my.Error as err:
        print(f"Error : {err}")
        con.rollback()
    


    

def stufunction(qid):
    
    adm = False
    sf = ""
    while sf != "5":
        print("""CHOOSE AN OPTION :
        1. UPDATE NAME
        2. UPDATE PASSWORD
        3. GIVE QUIZ
        4. CHECK RESULT
        5. BACK
        """)
        sf = input("\t\t: ")
        if sf == "1":
            k = "name"
            
            updata(qid,k,adm)
        elif sf == "2":
            k = "password"
            
            updata(qid,k,adm)
        elif sf == "3":
            quiz(qid)
        elif sf == "4":
            if checkres(qid) == None:
                print("YOU HAVE NOT GIVEN THE TEST!")
        elif sf == "5":
            break
        else:
            print("ENTER A VALID CHOICE")



def ado(ad):
    try:
        if ad[0] == "I":
            cho = input("ENTER OPTION : ")
        
            cur.execute(ad,(cho,))
            con.commit()
            print("OPTION HAS BEEN ADDED!")
            
        elif ad[0] == "U" :
            
            cho = input("ENTER CORRECT ANSWER : ")
        
            cur.execute(ad,(cho,))
            con.commit()
            print("ANSWER HAS BEEN UPDATED!")
            

        else:

            cho = input("ENTER OPTION : ")
            cur.execute(ad,(cho,))
            con.commit()
            print("OPTION HAS BEEN DELETED!")

            
    except my.Error as err:
        print(f"Error: {err}")
        con.rollback()



def updq(upd,qid):
    try:
        if upd == "U":
            ques = input("ENTER UPDATED YOUR QUESTION : ")
            cur.execute(f"UPDATE questions SET question = %s WHERE question_number = %s;",(ques,qid))
            con.commit()
            print("QUESTION HAS BEEN UPDATED!")

        else:

            cur.execute(f"DELETE FROM questions WHERE question_number = {qid};")
            con.commit()
            print("QUESTION HAS BEEN DELETED!")
        
    except my.Error as err:
        print(f"Error : {err}")
        con.rollback()


def checkM():
    try:
        cur.execute("SELECT name,roll_number,marks FROM student;")
        result = cur.fetchall()
        for i in result:
            print(f"    Name = {i[0]} , Roll Number = {i[1]} , marks = {i[2]}")
   
    except my.Error as err:
        print(f"Error : {err}")


def showq():
    try:
        cur.execute("SELECT * FROM questions;")
        result = cur.fetchall()
        for i in result:
            print(f"    Question Number = {i[0]} , Question = {i[1]} , answer = {i[2]}")
   
    except my.Error as err:
        print(f"Error : {err}")


def adminFunction(qid):
    
    adm = True
    sf = ""
    
    while sf != "13":
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
    12. SHOW ALL QUESTIONS WITH QUESTION NUMBER AND ANSWER
    13. BACK
    14. RESET TEST
    """)
        sf = input(": ")
        if sf == "1":

            addQuestion()
            
        elif sf == "2":
            
            qid = input("ENTER QUESTION NUMBER : ")
            upd = "U"
            updq(upd,qid)
            
        elif sf == "3":

            qid = input("ENTER QUESTION NUMBER : ")
            upd = "D"
            updq(upd,qid)

        elif sf == "4":

            qid = input("ENTER QUESTION NUMBER : ")
            ad = "INSERT INTO choices(choice) VALUES(%s);"
            ado(ad)

        elif sf == "5":

            qid = input("ENTER QUESTION NUMBER : ")
            ad = f"DELETE FROM choices WHERE question_number = {qid} AND choice = %s;"
            ado(ad)

        elif sf == "6":

            qid = input("ENTER QUESTION NUMBER : ")
            ad = f"UPDATE questions SET answer = %s WHERE question_number = {qid};"
            ado(ad)

        elif sf == "7":
            
            k = "name"
            updata(qid,k,adm)
            
        elif sf == "8":
            
            k = "password"    
            updata(qid,k,adm)

        elif sf == "9":

            checkM()

        elif sf == "10":
            try:
                sid = int(input("ENTER STUDENT ROLL NUMBER : "))
                cur.execute(f"DELETE FROM student WHERE roll_number = {sid};")
                con.commit()
                print("STUDENT REMOVED!")
            except my.Error as err:
                print(f"Error : {err}")
                con.rollback()


        elif sf == "11":
            try:
                cur.execute(f"DELETE FROM admin WHERE admin_id = {qid};")
                con.commit()
                print("ACCOUNT REMOVED!")
                return
            except my.Error as err:
                print(f"Error : {err}")
                con.rollback()

        elif sf == "12":
            
            showq()

        elif sf == "13":
            break

        elif sf == "14":
            try:
                
                cur.execute(f"UPDATE student SET marks = NULL")
                print("TEST HAS BEEN RESET!")
                con.commit()

            except my.Error as err:
                print(f"Error : {err}")
                con.rollback()

        else:
            print("ENTER A VALID CHOICE")




def addUser():
    name = input("Enter Name : ")
    roll = int(input("Enter your roll number : "))
    pawd = input("CREATE YOUR PASSWORD : ")
    cPawd = input("ENTER YOUR PASSWORD AGAIN : ")
    while pawd != cPawd:
        pawd = input("PASSWORD DID NOT MATCH.\nCREATE YOUR PASSWORD : ")
        cPawd = input("ENTER YOUR PASSWORD AGAIN : ")
    
    try:
        vals = (name,pawd,roll,)
        print(type(roll))
        cur.execute("INSERT INTO student(name,password,roll_number) VALUES(%s,%s,%s);",vals)
        con.commit()
        cur.execute("SELECT user_id FROM student WHERE roll_number = %s",(roll,))
        qid = cur.fetchone()
        print(qid)
        print("YOUR ID IS :",qid[0])
        stufunction(qid[0])
    except my.Error as err:
        print(f"Error: {err}")
        con.rollback()
    


def addAdmin():
    
    name = input("ENTER NAME : ")
    pwd = input("ENTER ADMIN PASSWORD : ")
    if pwd != "root":
        pwd = input("WRONG PASSWORD.\nTRY AGAIN : ")
        if pwd != "root":
            print("WRONG PASSWORD.\nCANNOT LOGIN YOU AS ADMINB KINDLY ASK ADMINISTRATOR ABOUT PASSWORD")
            return
    pawd = input("CREATE YOUR PASSWORD : ")
    cPawd = input("ENTER YOUR PASSWORD AGAIN : ")
    while pawd != cPawd:
        pawd = input("PASSWORD DIDNOT MATCH.\nCREATE YOUR PASSWORD : ")
        cPawd = input("ENTER YOUR PASSWORD AGAIN : ")
    
    try:
        vals = (name,pawd)
        cur.execute("INSERT INTO admin(name,password) VALUES(%s,%s);",vals)
        con.commit()
        cur.execute("SELECT admin_id FROM admin WHERE name = %s AND password = %s",vals)
        qid = cur.fetchone()
        print("YOUR ID IS :",qid[0])
        adminFunction(qid[0])
    
    except my.Error as err:
        print(f"Error: {err}")
        con.rollback()
    




'''Login'''     
def login(adm):
    qid = int(input("ENTER YOUR ID : "))
    if ifPresent(qid,adm) == False:
        return False
    password = input("ENTER YOUR PASSWORD : ")
    if validatePassword(qid,password,adm) == False:
        print("You Have Entered wrong password")
        password = input("Enter your password again : ")
        if validatePassword(qid,password,adm) == False:
            print("You Have Entered wrong password")
            password = input("Enter your password again : ")
            if validatePassword(qid,password,adm) == False:
                print("You have entered wrong password 3 times so the code is exiting")
                exit()
    print("\nWelcome! ",username(qid,adm))
    if adm == True:
        adminFunction(qid)
    else:
        stufunction(qid)



 
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
                login(adm)
                break
            elif i == "2":
                adm = False
                login(adm)
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

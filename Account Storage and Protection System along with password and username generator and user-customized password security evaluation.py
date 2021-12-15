from random import randint as randint
import mysql.connector
import sys
print("To be sure that you are an authorised user, please comply with the follwing steps")
p=input("Enter the password of MySQL application:\n")
try:
    con=mysql.connector.connect(host='localhost',user='root',password=p,auth_plugin='mysql_native_password')
    cur=con.cursor()
except:
    print("User not detected;program shutting down to avoid possible data theft")
    sys.exit()
cur.execute('CREATE DATABASE IF NOT EXISTS locker;')
con.commit()
cur.execute('USE LOCKER;')
def pwdgenerate():
    pwd=""
    sc=chr(randint(33,46))+chr(randint(33,46))
    d=chr(randint(48,57))+chr(randint(48,57))
    uc=chr(randint(65,90))+chr(randint(65,90))
    lc=chr(randint(97,122))+chr(randint(97,122))
    r=chr(randint(58,64))+chr(randint(58,64))
    L1=list(sc)+list(d)+list(uc+lc)+list(r)
    L2=[]
    while len(L2)!=10:
        i=randint(0,9)
        if i not in L2:
            L2.append(i)
    for i in L2:
        pwd=pwd+L1[i]
    return pwd
def unamegenerate():
    l1=[]
    a=chr(randint(33,46))+chr(randint(33,46))
    b=chr(randint(48,57))+chr(randint(48,57))
    c=chr(randint(65,90))+chr(randint(97,122))
    d=chr(randint(58,64))+chr(randint(58,64))
    L1=list(a)+list(b)+list(c)+list(d)
    L2=[];username=""
    while len(L2)!=8:
        i=randint(0,7)
        if i not in L2:
            L2.append(i)
    for i in L2:
        username=username+L1[i]
    return username
def evaluatemanualpwd(mgp):
    if len(mgp)<10:
        return False
    else:
        l1=[ord(i) for i in mgp]
        l1.sort()
        l2=[33,46,48,57,58,64,65,90,97,122]
        lc=0
        for i in l1:
            if i in (l2[0],l2[1]):
                lc+=1
            else:
                if lc<2:
                    return False
                    break
                else:
                    lc=0
                    l2=l2[2:]
            if lc==2:
                lc=0
                l2=l2[2:]
        else:
            return True
def store(uname,pw,ty):
    if ty=="":
        cur.execute("INSERT INTO usernamepw(username,password) VALUES (%s,%s);",(uname,pw))
    else:
        cur.execute("INSERT INTO usernamepw VALUES (%s,%s,%s);",(uname,pw,ty))
    con.commit()
    print("Data successfully stored")
    return
def display():
    print("Enter 1 for displaying all stored username-password pair along with their type")
    print("Enter 2 for displaying stored username-password pairs for specific type")
    try:
        ch=int(input())
    except:
        print("Invalid Datatpe Input; attempt once more")
        display()
    if ch==1:
        cur.execute("SELECT * FROM usernamepw;")
        recs=cur.fetchall()
        print("Format of Display: Username, Password, Account Type")
        for i in recs:
            for j in i:
                print(j,end="\t")
            print()
        if len(recs)==0:
            print("No registered data detected")
    elif ch==2:
        cur.execute("SELECT type FROM usernamepw;")
        recs1=cur.fetchall()
        print("Enter the account type for which you want to see the username-password pair:\n")
        ty=input()
        if (ty,) in recs1:
            cur.execute("SELECT username,password FROM usernamepw WHERE Type LIKE %s;",(ty,))
            recs2=cur.fetchall()
            print("Format of Display: Username, Password")
            for i in recs2:
                for j in i:
                    print(j,end="\t")
                print()
            if len(recs2)==0:
                print("No registered data detected")
        else:
            print("Requested type isn't available;control returned to main menu")
    else:
        print("Invalid Input;control returned to main menu")
def edit():
    print("Enter 1 if you wish to change type of multiple same account types at once")
    print("Enter 2 if you wish to change the details of a username-password pair")
    try:
        ch=int(input())
    except:
        print("Only integral values accepted; you will be re-routed to ths sub-part again")
        edit()
    if ch==1:
        print("Enter the account type which you wish to change")
        t=input()
        print("Enter the new account type you wish to update the previous account type with")
        new=input()
        cur.execute("SELECT type FROM usernamepw;")
        trecs=cur.fetchall()
        if (t,) in trecs:
            cur.execute("UPDATE usernamepw SET type=%s WHERE type LIKE %s;",(new,t))
            con.commit();print("Dataset updated")
        else:
            print("Account type to be changed doesn't exist; rerouting to main menu")
    elif ch==2:
        print("Enter the username of the account whose information you want to edit\n")
        u=input()
        print("Enter the password of the account whose information you want to edit\n")
        pw=input()
        cur.execute("SELECT username,password FROM usernamepw;")
        recs=cur.fetchall()
        if (u,pw) in recs:
            pass
        else:
            print("Requested pair isn't available; returning to main menu")
            return
        print("Enter 1 if you wish to change the username")
        print("Enter 2 if you wish to change the password")
        print("Enter 3 if you wish to change its type")
        try:
            c=int(input())
        except:
            print("Invalid Datatype entry;rerouting to main function")
        if c==1:
            print("Enter Y for another randomly generated username")
            print("Enter anything else for storing customized username")
            uname=""
            if input().lower()=="y":
                uname=unamegenerate()
            else:
                uname=input("Enter custom username:\n")
            cur.execute("UPDATE usernamepw SET username=%s WHERE username LIKE %s AND password LIKE %s;",(uname,u,pw))
            con.commit();
            print("New data stored in primary storage")
        elif c==2:
            print("Enter Y for another randomly generated password")
            print("Enter anything else for storing customized password")
            pwd=""
            if input().lower()=="y":
                pwd=pwdgenerate()
            else:
                pwd=input("Enter custom password:\n")
                print("Enter Y for evaluating custom password according to program standards")
                print("Enter anything else for non-evaluation")
                if input().lower()=="y":
                    r=evaluatemanualpwd(pwd)
                    if r==True:
                        print("Password upto program standards;updating dataset")
                    else:
                        print("Password has failed program standards")
                        print("Enter Y for replacing it with a random generated password")
                        print("Enter anything else to proceed ahead with saving the custom password")
                        if input().lower()=="y":
                            pwd=pwdgenerate()
                cur.execute("SELECT password FROM usernamepw;")
                if (pwd,) not in cur.fetchall():
                    cur.execute("UPDATE usernamepw SET password=%s WHERE username LIKE %s AND password LIKE %s;",(pwd,u,pw))
                    con.commit();print("Dataset updated")
                else:
                    print("Custom password can't be stored due to possible duplication of password")
                    return
        elif c==3:
            print("Enter the new account type for the username-password pair")
            t=input()
            cur.execute("UPDATE usernamepw SET type=%s WHERE username LIKE %s AND password LIKE %s;",(t,uname,pw))
            con.commit();print("Dataset updated")
        else:
            print("Invalid Input;returning to Main Menu")
            return
    else:
        print("Invalid Input; you are being re-routed to main menu")
        return
def delete():
    print("Enter 1 if you wish to delete a particular username-password-type pair")
    print("Enter 2 if you wish to delete the username-password-type pairs by type")
    print("Enter 3 if you wish to delete the entire stored data")
    try:
        ch=int(input())
    except:
        print("Incompatible datatype choice entered; try again :)")
        delete()
    if ch==1:
        u=input("Enter the username whose username-password pair you want to delete\n")
        pw=input("Enter the password whose username-password pair you want to delete\n")
        cur.execute("SELECT username,password FROM usernamepw;")
        recs=cur.fetchall()
        if (u,pw) in recs:
            cur.execute("DELETE FROM usernamepw WHERE username=%s AND password=%s;",(u,pw))
            con.commit()
        else:
            print("Specified data set not present in database-recommend viewing registered database before further actions")
    elif ch==2:
        t=input("Enter the type of the accounts which you want to erase from storage\n")
        cur.execute("SELECT type FROM usernamepw;")
        trecs=cur.fetchall()
        if (t,) in trecs:
            cur.execute("DELETE FROM usernamepw where type=%s",(t,))
            con.commit()
        else:
            print("Specified type isn't present-recommned viewing the registered databse before further actions")
    elif ch==3:
        cur.execute("DELETE  FROM usernamepw;")
        con.commit()
    else:
        print("Invalid choice; you'll be returned to main menu")
        return
#Main
print("Welcome User!")
print("This is a program developed for the purpose of",end=" ")
print("generating random username and password, as well as",end=" ")
print("storing account username and password, along with",end=" ")
print("facility to evaluate user-generated passwords")
cur.execute("CREATE TABLE IF NOT EXISTS usernamepw(username varchar(100)BINARY, password varchar(100)BINARY, type varchar(100) DEFAULT 'UNKNOWN',UNIQUE(password), PRIMARY KEY(username,password));")
con.commit()
while True:
    print("Enter S for storing data")
    print("Enter E for editing stored data")
    print("Enter D for deleting stored data")
    print("Enter Display for display of data")
    print("Enter Exit for exiting the program\n")
    c=input()
    if c.lower()=='s':
        print("Enter Y if you wish to have a computer generated username")
        print("Enter any other character if you wish to add custom username")
        if input().lower()=='y':
            uname=unamegenerate()
        else:
            uname=input("Enter custom username:\n")
        print("Enter Y if you wish to have a computer generated password")
        print("Enter any other character if you wish to add custom password")
        if input().lower()=='y':
            pw=pwdgenerate()
        else:
            pw=input("Enter custom password:\n")
            print("Enter Y if you wish to have the program evaluate the custom password")
            print("Enter any other character if you don't wish to do so")
            if input().lower()=='y':
                result=evaluatemanualpwd(pw)
                if result==True:
                    print("Password is strong by program standards")
                else:
                    print("Password isn't strong by program standards")
                    print("Enter Y if you wish to have a computer generated password")
                    print("Enter any other character if you don't wish to")
                    if input().lower()=='y':
                        pw=pwdgenerate()
        print("Enter Y if you wish to add account type")
        print("Enter any other character if you don't wish to");ty=""
        if input().lower()=='y':
            ty=input("Enter account type:\n")
        cur.execute("SELECT password FROM usernamepw;")
        recs=cur.fetchall()
        if (pw,) not in recs:
            store(uname,pw,ty)
        else:
            print("Provided username-password pair is already registered")
    elif c.lower()=="e":
        edit()
    elif c.lower()=="d":
        delete()
    elif c.lower()=="display":
        display()
    elif c.lower()=="exit":
        print("We will safeguard your data safely user")
        print("We wish you a good day")
        break
    else:
        print("Wrong Input;please enter a viable input")

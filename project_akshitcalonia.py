import mysql.connector
import time
mydb = mysql.connector.connect(host="localhost", user="root", passwd="dps123", charset="utf8")
cur = mydb.cursor()
cur.execute("Create database if not exists AKHospital")
cur.execute("use AKHospital")
cur.execute("create table if not exists Patient(PNo varchar(9) primary key, Patient_Name varchar(25), Diagnosis varchar(30), DOB date, RoomNo integer(3));")
cur.execute("create table if not exists Log(PNo varchar(20) primary key, passw varchar(20));")
cur.execute("create table if not exists Doctor(D_id varchar(20) primary key, Dname varchar(20), Dspecial varchar(30));")
cur.execute("create table if not exists info(bed_id varchar(20) primary key, Pfloor varchar(2), Pname varchar(30));")
mydb.commit()



#To admit Patient
def insert_data():
    while True:
        try:
            n = int(input("How many records you want to enter : "))
            break
        except Exception:
            print("*"*20, "\nError!! Try again enting data in numeric form!\n", "*"*20)
    for i in range(n):
        PNo = input("Enter a Patient ID : ")
        Patient_Name = input("Enter Patient Name : ")
        Diagnosis = input(f"Enter Medical Condition for {Patient_Name} : ")
        while True:
            DOB = input("Enter the Date in correct format (yyyy/mm/dd) : ")
            if int(DOB[5:7])<=12 and int(DOB[9:11])<=31:
                break
            else:
                print("Try again and enter the correct date")
                
        RoomNo = input("Enter the Room Number : ")

        try:
            cur.execute("insert into Patient values('"+PNo+"', '"+Patient_Name+"', '"+Diagnosis+"', '"+DOB+"', '"+RoomNo+"')")
            mydb.commit()
            print("RECORDS ADDED SUCCESSFULLY IN SYSTEM!\n")

        except Exception:
            print("*"*20, "\nError!! Try again enting with unique Patient ID!\n", "*"*20)       
            break
        need = input("Does this Patient Need a bed ?? (y/n): ").lower()
        
        if need == "y":
            cur.execute("select count(bed_id) from info;")
            for i in cur:
                if int(i[0])<1000:
                    Pfloor = input("\nEnter that floor you prefer (G/1/2/3/4/5/6/7/8) : ")
                    cur.execute("insert into info values('"+PNo+"', '"+Pfloor+"', '"+Patient_Name+"')")
                    print(f"Patient has been succesfully assigned a bed with ID = {PNo}")
                else:
                    print("No beds are available. Try contacting us for emergency cases (Can be found on info portal)")




# To Update Patient details
def update():
    while True:
        try:
            n = int(input("How many records to update? : "))
            break
        except Exception:
            print("*"*20, "\nError!! Try again enting data in the numeric form!\n", "*"*20)
            
    for i in range(1, n+1):
        PNo = input(f"Enter Patient ID for your update No. {i} here : ")
        print("Here are the Details\n")
        cur.execute("select * from Patient where PNo = '"+PNo+"';")
        for i in cur:
            print(f"Patient ID is {i[0]}, Patient Name is Mr/Ms{i[1]}, diagnosed as {i[2]}; DOB is {i[3]}, and Room Number is {i[4]}")
        what = input("Enter which info you want to update? \n(Press 1 for Name\nPress 2 for diagnosis\nPress 3 for DOB\nPress 4 for Room No.) : ")

        if what == "1": 
            Patient_Name = input("Enter Patient Updated Name : ")
            try:
                cur.execute("update Patient set Patient_Name = '"+Patient_Name+"' where PNo = '"+PNo+"';")
                mydb.commit()
                print("RECORD SUCCESSFULLY UPDATED!")
            except Exception:
                print("*"*20, "\nError!! Try again enting data in the mentioned format!\n", "*"*20)
                break
            
        elif what == "2":
            Diagnosis = input(f"Enter Updated Medical Condition for ID {PNo} : ")
            cur.execute("update Patient set Diagnosis = '"+Diagnosis+"' where PNo = '"+PNo+"';")
            mydb.commit()
            print("RECORD SUCCESSFULLY UPDATED!")
            
        elif what == "3":
            DOB = input("Enter the Updated Date in correct format (yyyy/mm/dd) : ")
            try:
                cur.execute("update Patient set DOB = '"+DOB+"' where PNo = '"+PNo+"';")
                mydb.commit()
                print("RECORD SUCCESSFULLY UPDATED!")
            except Exception:
                print("*"*20, "\nError!! Try again enting data in the mentioned format!\n", "*"*20)
                break
            
        elif what == "4":
            RoomNo = input("Enter the Updated Room Number : ")
            cur.execute("update Patient set RoomNo = '"+RoomNo+"' where PNo = '"+PNo+"';")
            mydb.commit()
            print("RECORD SUCCESSFULLY UPDATED!")

        else:
            print("Try Later!")




# To delete/discharge Patient
def delete():
    while True:
        try:
            n = int(input("How many records to Delete (Patients to discharge) ? : "))
            break
        except Exception:
            print("*"*20, "\nError!! Try again enting data in the numeric form!\n", "*"*20)
            
    for i in range(n):
        PNo = input("Enter the Patient ID to be deleted/discharged from records : ")
        try:
            cur.execute("delete from Patient where PNo = '"+PNo+"';")
            cur.execute("delete from info where bed_id = '"+PNo+"';")
            mydb.commit()
            print("RECORDS DELETED SUCCESSFULLY FROM SYSTEM and Patient is Discharged!")

        except Exception:
            print("*"*20, "\nError!! Try again entering valid data!\n", "*"*20)
            break




# To View Patient details
def view():
    cur.execute("Select * from Patient")
    data=cur.fetchall()
    mydb.commit()
    err = False
    def columnnm(name):
        v = "SELECT LENGTH("+name+") FROM Patient WHERE LENGTH("+name+") = (SELECT MAX(LENGTH("+name+")) FROM Patient) LIMIT 1;"
        cur.execute(v)
        data = cur.fetchall()
        mydb.commit()
        try:
            return data[0][0]
        except Exception:
            err = True
    widths = []
    columns = []
    tavnit = '|'
    separator = '+'
    for cd in cur.description:
        try:
            widths.append(max(columnnm(cd[0]), len(cd[0])))
            columns.append(cd[0])
        except Exception:
            err = True
    if err == False:
        for w in widths:
            tavnit += " %-"+"%ss |" % (w,)
            separator += '-'*w + '--+'
        print(separator)
        print(tavnit % tuple(columns))
        print(separator)
        for row in data:
            print(tavnit % row)
        print(separator)
    else:
        print("No Data Found! Try Later!")


# To search a Patient
def searchit():
    cur.execute("Select * from Patient")
    nm = input("Enter Patient's Name to view/search for : ")
    fnd = False
    for i in cur:
        if i[1] == nm:
            fnd = True
            print("DETAILS FOUND ! ")
            print(f"Patient ID is {i[0]}\nPatient Name is Mr/Ms{i[1]}\nDiagnosed as {i[2]}\n DOB is {i[3]}\nRoom Number is {i[4]}")
    if fnd == False:
        print("No details found! Try Later")





# For Logging In the User        
def cuslogin():
    print(f"Logging in ", end = "")
    for i in range(5, 0, -1):
        print(f"{i}, ", end = "")
        time.sleep(0.5)
    print("\nWelcome to the LOGIN Portal!")
    
    ps = "uk"
    while True:
        PNo = input(f"Enter the LOGIN ID :  ")
        upass = input("Enter the Password : ")
        cur.execute("select * from Log")
        m = False
        for i in cur:
            if PNo in i and upass in i:
                print("\nLOGIN Success!")
                m = True
                ps = "go"
        
        if m == False:
            print("LOGIN ID/Password didn't match. Try again or of register yourself!")
            print("Enter 1 to Try again\nEnter 2 to exit LOGIN window")
            d = input("Please tell : ")
            if d == "1":
                continue
            elif d == "2":
                break
            
        elif m == True:
            break
        
    if ps == "go":
        while True:
            print("\nWelcome to Your Portal !")
            print("Press 1 to Add Patient Details (Admitting a patient)")
            print("Press 2 to Update Patient Details")
            print("Press 3 to Delete Patient (for discharging)")
            print("Press 4 to view a Patient Detail")
            print("Press 5 to check all records in Management!")
            print("Press 0 to LOG OUT")
            r = int(input("Enter the Desired Action  :  "))
            if r == 1:
                insert_data()
            elif r == 2:
                update()
            elif r == 3:
                delete()
            elif r == 4:
                searchit()
            elif r == 5:
                view()
            elif r == 0:
                print("Logging out in ", end = "")
                for i in range(5, 0, -1):
                    print(f"{i} , ", end = "")
                    time.sleep(0.5)
                print("\nLogged Out Success!")
                break
            else:
                print("Invalid Input Given, try again !")
                




# To register New User    
def newreg():
    print("\nWelcome to New USER Registration Portal!")
    n = int(input("How many User you want to register ? : "))
    for i in range(1, n+1):
        print(f"Let's start with details for User No. {i}")
        nm = input("Enter the User Name : ")
        while True:
            PNo = input(f"Enter a unique UserID for {nm}:  ")
            cur.execute("Select * from Log")
            k = False
            for i in cur:
                if PNo in i:
                    print("This ID already exists, try something else!")
                    k = True
            if k == False:
                print("This ID is unique! We're good to go :)")
                break
        passw = input(f"Enter a password (Do not Share with anyone else) for {nm}'s account :  ")
        cur.execute("insert into Log values('"+PNo+"', '"+passw+"')")
        mydb.commit()
    print("User(s) added SUCCESSFULLY!")
    t = input("\nWant to proceed to LOGIN? (Y/N): ").upper()
    if t == "Y":
        cuslogin()
        



# Doctor Login       
def doclog():
    print("Welcome to DOCTOR REGISTER!")
    n = int(input("How many doctors to register : "))
    for i in range(1, n+1):
        Dname = input(f"Enter Doctor Number {i}'s Name : ")
        D_id = input(f"Create an ID for Mr/Ms {Dname} : ")
        Dspecial = input(f"Enter the speciality for {Dname} : ")
        cur.execute("insert into Doctor values('"+D_id+"', '"+Dname+"', '"+Dspecial+"')")
        mydb.commit()
    print("REGISTERED SUCCESSFULLY!")
    j = input("Continue to LogIN ? (y/n) : ").lower()
    if j == "y":
        while True:
            print("\nPress 1 to view all Patients and their details")
            print("Press 2 to update a patient details")
            print("Press 3 to know about occupied BEDS")
            print("Press 0 to EXIT the window !")
            ch = int(input("Enter a choice : "))
            if ch == 1:
                view()
            elif ch == 2:
                update()
            elif ch == 3:
                cur.execute("select count(bed_id) from info;")
                for i in cur:
                    print("Occupied beds = ", i[0])
                    print("AVAILABLE BEDS = ", 1000-i[0])
            elif ch == 0:
                break
            else:
                print("Invalid choice, Try again!")
    else:
        print("Thank You to register the Doctor!")
        





# Information about available Beds      
def hospbeds():
    while True:
        print("\nWelcome to Information Portal!")
        print("Press 1 to know about Beds and its patient in Hospital")
        print("Press 2 to count total number of available beds (out of 1000)")
        print("Press 0 to EXIT (Go back to Main Menu)")
        chh = int(input("Enter your choice : "))
        if chh == 1:
            cur.execute("select * from info;")
            for i in cur:
                print(f"Bed ID is {i[0]}, Patient on it is Mr/Ms. {i[2]}, on the floor no.{i[1]}")
        elif chh == 2:
            cur.execute("select count(bed_id) from info;")
            for i in cur:
                print("Occupied beds = ", i[0])
                print("AVAILABLE BEDS = ", 1000-i[0])
        elif chh == 0:
            print("Window Exited!")
            break
        else:
            print("Invalid Input Recieved !")



        
# General Information    
def hospinfo():
    print("Contact us at: enquiries.ggn@Akhopsital.com")
    print("Our mailing address is\nA-98/178\nNear IGI Airport\nDelhi\nPincode - 110012")

    



# MAIN MENU
print("-"*64,"\n","~"*7, "\tWelcome to AKHospital Management Frontdesk\t", "~"*7,"\n","-"*64)
while True:
    print("\nPress 1 for Customer Login (If account already exists)")
    print("Press 2 to Register as a New User")
    print("Press 3 for Doctor LOGIN")
    print("Press 4 to know about available beds and occupied patients")
    print("Press 5 to know more about Hospital Policies and other info....")
    print("Press 0 to Exit")
    try:
        ch = int(input("Enter your action   :   "))
    except Exception:
        print("You're requested to enter details correctly.")

    if ch == 1:
        cuslogin()
    elif ch == 2:
        newreg()
    elif ch == 3:
        doclog()
    elif ch == 4:
        hospbeds()
    elif ch == 5:
        hospinfo()
    elif ch == 0:
        print("Thank You for using the Hospital Management Desk!\nWe appreciate you seeing back!")
        break
    else:
        print("Unrognizable Input recieved, Try again ! ")








        

import cx_Oracle
import getpass #gets password without echoing
import random
import datetime

class Patient_Info_Update():
    
    def __init__(self):
        pass
    
    def main(self):
	
        f = open('credentials', 'r')
        #[-1] to trim \n
        username = f.readline()[:-1]
        password = f.readline()[:-1]
        #password = getpass.getpass() # could use this to get password, but doesn't work with IDE

        self.con = cx_Oracle.connect(username + '/' + \
	                        password + '@gwynne.cs.ualberta.ca:1521/CRS')

	
        cont = self.getInputs()
        if cont == 0:
            return 1  
	    
        #self.executeStatement()
        self.con.close()
        return 1	
	
	
	
    def printOptions(self):
        print()	
        print("[1] Enter new Patient")
        print("[2] Edit Existing Patient")
        print("[3] Return to main menu.")
    
    def getInputs(self):
        while 1:
            self.name_update = False
            self.address_update = False
            self.birth_update = False
            self.phone_update = False
            self.printOptions()
            ans = input("Enter a choice: ")
            if ans == "1":
                
                self.HCN = self.getUniqueHCN()

                self.printSeparator()
                self.name = self.getName()

                go=True
                self.printSeparator()
                while go:
                    self.address,go = self.getAddress()
               
                go=True
                self.printSeparator()
                while go:                
                    self.birth,go = self.getBirthDate()		

                self.printSeparator()
                self.phone = self.getPhone()

                self.printSeparator()
                print("Patient Name: " + self.name)
                print("Patient Address: " + self.address)
                print("Patient Birth Date: " + self.birth)
                print("Patient Phone Number: " + self.phone)
                print()
                while 1: 
                    conf = input("Confirm information (y/n)")
                    if conf == "y":
                        print("Information confirmed.")
                        return 1
                    elif conf == "n":
                        print("Information not confirmed, returning to start.")
                        break
                    else:
                        print("Invalid choice, pick 'y' or 'n'")
		    

            elif ans == "2":
                go=True		
                self.printSeparator()
                while go:
                    self.patient,go = self.getPatient()
                not_done = True
                while not_done:
                    print()
                    print("[1] Update patient name.")
                    print("[2] Update patient address.")
                    print("[3] Update patient birth date.")
                    print("[4] Update patient phone number.")
                    print("[5] Return to menu.")
                    check = input("Enter an option: ")
                    if check == "1":
                        self.printSeparator()
                        self.name = self.getName()
                        self.name_update = True
                        ask = input("Update another value? (y/n): ")
                        while 1:
                            if ask == "y":
                                break
                            elif ask == "n":
                                not_done = False
                                break
                            else:
                                print("Invalid input. ")
                                print()
                    elif check == "2":
                        go=True
                        self.printSeparator()
                        while go:
                            self.address,go = self.getAddress()
                        self.address_update = True
                        ask = input("Update another value? (y/n): ")
                        while 1:
                            if ask == "y":
                                break
                            elif ask == "n":
                                not_done = False
                                break
                            else:
                                print("Invalid input. ")
                                print()
                    elif check == "3":
                        go=True
                        self.printSeparator()
                        while go:                
                            self.birth,go = self.getBirthDate()	
                        self.birth_update = True
                        ask = input("Update another value? (y/n): ")
                        while 1:
                            if ask == "y":
                                break
                            elif ask == "n":
                                not_done = False
                                break
                            else:
                                print("Invalid input. ")
                                print()
                    elif check == "4":
                        self.printSeparator()
                        self.phone = self.getPhone()
                        self.phone_update = True
                        ask = input("Update another value? (y/n): ")
                        while 1:
                            if ask == "y":
                                break
                            elif ask == "n":
                                not_done = False
                                break
                            else:
                                print("Invalid input. ")
                                print()
                    elif check == "5":
                        break
                    else:
                        print("Invalid input.")
                        print()
                self.printSeparator()
                if self.name_update:
                    print("Patient Name: " + self.name)
                if self.address_update:                
                    print("Patient Address: " + self.address)
                if self.birth_update:                
                    print("Patient Birth Date: " + self.birth)
                if self.phone_update:                
                    print("Patient Phone Number: " + self.phone)
                print()
                while 1: 
                    conf = input("Confirm updates (y/n): ")
                    if conf == "y":
                        print("Information confirmed.")
                        return 1
                    elif conf == "n":
                        print("Information not confirmed, returning to start.")
                        break
                    else:
                        print("Invalid choice, pick 'y' or 'n'")                

            elif ans == "3":
                return 0		
            else:
                print("Invalid choice.")
        

		
		
		
		
		
    def input_check(input):
        try:
            check = eval(input)    
            if check not in [1,2,3,4,5]:
                return 0
            else:
                return check
        except:
            return 0	


    def getPhone(self):
        ans = True	
        while ans:
            print()
            phone = input("Input Patient Phone Number (10-digits): ")
            if phone.isdigit() and len(phone) == 10:		
                reply = input("Confirm patient name :: " + phone + " :: (y/n): ")
                if reply == "y":
                    ans = False
                elif reply == "n":		
                    print("Phone incorrect, returning to start.")		 
                else:
                    print("Invalid input, returning to start.")
            else:                
                print("Invalid input. Enter phone as a single number without spaces or dashes.")
                print()
        return phone        	
	
		

    def getName(self):
        ans = True	
        while ans:
            print()
            name = input("Input Patient Name: ")
            reply = input("Confirm patient name :: " + name + " :: (y/n): ")
            if reply == "y":
                ans = False
            elif reply == "n":		
                print("Name incorrect, enter again.")		
            else:
                print("Invalid input, enter again.")
        return name

    def getAddress(self):
        not_allowed = [chr(34), chr(39)]  
        ans = True
        while ans:
            print()
            address = input("Enter Address: ")
            reply = input("Confirm patient address :: " + address + " :: (y/n): ")
            if reply == "y":
                for each in address:
                    if each in not_allowed:
                        print("Apostrophe and Quotation characters are disallowed.")
                        return False, True
                if len(address) > 200:
                    print("Address entry exceeds character limit of 200.")
                    return False, True
                else:
                    return address, False
            elif reply == "n":
                print("Address incorrect, enter again.")
            else:
                print("Invalid input, enter again.")

    def getBirthDate(self):
        print()
        string = input('Enter Birth Date "yyyy/mm/dd": ')
        if len(string) != 10:
            print("Invalid input.")
            return False, True
        else:
            year = string[0:4]
            month = string[5:7]
            day = string[8:]
            correctDate = None
            if self.isNumber(year) and self.isNumber(month) and self.isNumber(day) and string[4] == "/" and string[7] == "/":
                try:
                    newDate = datetime.datetime(int(year),int(month),int(day))
                    correctDate = True
                except ValueError:
                    correctDate = False
            if correctDate:
                return string,False
            else:
                print("Invalid date.")
                return False, True
		
	
    def goodNumber(self,string,case):
        if case == "D":
            curs = self.con.cursor()
            curs.execute("select * from doctor where employee_no like'"+string+"'")
            rows = curs.fetchall()
            if len(rows) == 0:
                return False
            else:
                return True
        elif case == "T":
            curs = self.con.cursor()
            curs.execute("select * from test_record where test_id like '"+string+"'")
            rows = curs.fetchall()
            if len(rows) ==0:
                return False
            else:
                return True
        else:
            curs = self.con.cursor()
            curs.execute("select * from patient where health_care_no like'"+string+"'")
            rows = curs.fetchall()
            if len(rows) == 0:
                return False
            else:
                return True
        
    def isReal(self,string,case):
        if case == "D":
            curs = self.con.cursor()
            curs.execute("select * from doctor d, patient p where d.health_care_no=p.health_care_no and p.name like'"+string+"'")
            rows = curs.fetchall()
            if len(rows) == 0:
                return False
            else:
                return True
        elif case == "T":
            curs = self.con.cursor()
            curs.execute("select * from test_type where test_name like'"+string+"'")
            rows = curs.fetchall()
            if len(rows) == 0:
                return False
            else:
                return True
        elif case == "L":
            curs = self.con.cursor()
            curs.execute("select * from medical_lab where lab_name like '"+string+"'")
            rows = curs.fetchall()
            if len(rows) == 0:
                return False
            else:
                return True
        elif case == "R":
            curs = self.con.cursor()
            curs.execute("select * from test_record where test_id like '"+string+"'")
            rows = curs.fetchall()
            if len(rows) == 0:
                return False
            else:
                return True
        else:
            curs = self.con.cursor()
            curs.execute("select * from patient where name like'"+string+"'")
            rows = curs.fetchall()
            if len(rows) == 0:
                return False
            else:
                return True
    
    
    def isNumber(self, string):
        return string.isdigit()
    
	
    def getTestRecord(self, p_no):
        curs = self.con.cursor()
	
        curs.execute("select * from test_record where patient_no like'"+str(p_no)+"'")
	
        rows = curs.fetchall()
	
        for row in rows:
            print(row)
	
        print()
        string = input('Enter Test ID: ')
	
        if self.isNumber(string):
            if self.isReal(string, "R"):
                print("Test ID selected is", int(string))
                return int(string), False
            else:
                print("Invalid test id.")
                return False, True
		
	
    # returns the patient_no on success
    def getPatient(self):
        curs = self.con.cursor()

        curs.execute("select name,health_care_no from patient p")

        rows = curs.fetchall()
        
        for row in rows:
            print(row)
        
        string = input('Enter Patient name or number: ')
        
        if self.isNumber(string):
            if self.goodNumber(string,"P"):
                print("patient health care number is",int(string))
                return int(string),False
            else:
                print("Invalid health care number.")
                print()
                return False,True
        else:
            if self.isReal(string,"P"):
                return self.getPatientNumber(string),False
            else:
                print(string,"is not a real patient, try again")
                return False,True

    def getPatientNumber(self,string):
        curs = self.con.cursor()

        curs.execute("select health_care_no from patient p where p.name like '"+string+"'")

        rows = curs.fetchall()
        
        for row in rows:
            id1=int(row[0])
        return id1

        
    
    def printSeparator(self):
        print("")
        print("-----------------------")
        print("")
        

    def getUniqueHCN(self):
        
        curs = self.con.cursor()
        curs.execute("select health_care_no from patient")

        rows = curs.fetchall()

        while (True):
            health_care_no = random.randint(0, 10**3)

            if all(health_care_no != row[0] for row in rows):
                return health_care_no


    def executeStatement(self):
        print("******EXECUTING STATEMENT******")
	

        curs = self.con.cursor()
        curs.execute("update test_record set medical_lab='" + str(self.m_lab) + "', result='" + str(self.testResult) + "', test_date=TO_DATE('" + str(self.testDate) + "', 'YYYY-MM-DD') where test_id=" + str(self.testId))


        self.printSeparator()
        self.con.commit()
        
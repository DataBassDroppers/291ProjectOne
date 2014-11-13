import cx_Oracle
import getpass #gets password without echoing
import datetime

class Medical_Test():
    
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
        
        self.executeStatement()
        self.con.close()
        return 1
        
        
    def getInputs(self):
        print()
        print("[1] Enter Test Result Information.")
        print("[2] Return to main menu.")

       
        while 1:
            ans = input("Enter a choice: ")
            if ans == "1":
                break
            elif ans == "2":
                return 0
            else:
                print("Invalid choice.")



	
	
        go=True
        self.printSeparator()
        while go:
            self.patient,go = self.getPatient()
	    
        go=True
        self.printSeparator()
        while go:
            self.testId,go = self.getTestRecord(self.patient)	
	
	
        go=True
        self.printSeparator()
        while go:
            self.m_lab,go = self.getM_Lab()
       
        # testDate gets a string of "yyyy,mm,dd"
        go=True
        self.printSeparator()
        while go:
            self.testDate,go = self.getTestDate()
        
        go=True
        self.printSeparator()
        while go:
            self.testResult,go = self.getTestResult()
    
        self.printSeparator()
        
        return 1


    def getTestResult(self):
        not_allowed = [chr(34), chr(39)]  
        result = input("Enter Result: ")
        for each in result:
            if each in not_allowed:
                print("Apostrophe and Quotation characters are disallowed.")
                return False, True
        if len(result) > 1024:
            print("Result entry exceeds character limit of 1024.")
            return False, True
        else:
            return result, False

    
    def getM_Lab(self):
        curs = self.con.cursor()

        curs.execute('select lab_name from medical_lab m')

        rows = curs.fetchall()

        for row in rows:
            print(row)
        string = input('Enter Medical Lab Name: ')

        if self.isReal(string,"L"):
            print("Lab name is:", string)
            return string,False
        else:
            print("Invalid lab name")
            return False,True
	
    def getTestDate(self):
        string = input('Enter Test Date "yyyy/mm/dd": ')
        if len(string) != 10:
            print("Invalid input.")
            return False, True
        else:
            year = string[0:4]
            month = string[5:7]
            day = string[8:]
            if self.isNumber(year) and self.isNumber(month) and self.isNumber(day) and string[4] == "/" and string[7] == "/":
                correctDate = None
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
                print("Invalid health care number")
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

        curs.execute("select * from patient p where p.name like '"+string+"'")

        rows = curs.fetchall()
        tmp = []
        if len(rows) > 1:
            while 1:
                print()
                print("Health Care Number | Name | Address | Date of Birth | Phone number")
                for row in rows:
                    print(row)
                    tmp.append(str(row[0]))
                pick = input("Enter ID of correct patient: ")
                if pick in tmp:
                    return pick
                else:
                    print("Incorrect value, enter valid ID of correct patient.")
        else:
            return rows[0][0]
        
    
    def printSeparator(self):
        print("")
        print("-----------------------")
        print("")
        


    def executeStatement(self):
        print("******EXECUTING STATEMENT******")
	

        curs = self.con.cursor()
        curs.execute("update test_record set medical_lab='" + str(self.m_lab) + "', result='" + str(self.testResult) + "', test_date=TO_DATE('" + str(self.testDate) + "', 'YYYY-MM-DD') where test_id=" + str(self.testId))


        self.printSeparator()
        self.con.commit()
        
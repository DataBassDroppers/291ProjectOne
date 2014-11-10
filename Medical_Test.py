import cx_Oracle
import getpass #gets password without echoing
import random

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

        self.getInputs()

        if self.patientCanTakeTest():
            self.executeStatement()
            self.con.close()
            # return 1 on success
            return 1
        else:
            print("Sorry this patient cannot take this type of test, please try again")
            self.con.close()
            self.main()
            

        
    def getInputs(self):
        go=True
        
        self.printSeparator()
        
        while go:
            self.m_lab,go = self.getM_Lab()
       
       
        go=True
        self.printSeparator()
        while go:
            self.testName,go = self.getTestName()
        
        
        go=True
        self.printSeparator()
        while go:
            self.patient,go = self.getPatient()
        self.printSeparator()
 
        #self.patient= self.getPatient()


    
    def getM_Lab(self):
        curs = self.con.cursor()

        curs.execute('select lab_name, from medical_lab m')
        #curs.execute('select name,employee_no from doctor d,patient p where p.health_care_no=d.health_care_no')

        rows = curs.fetchall()

        for row in rows:
            print(row)
        string = input('Enter Medical Lab Name')

        if self.isReal(string,"L"):
	    print("Lab name is:", string)
	    return string,False
	else:
	    print("Invalid lab name")
	    return False,True


    def goodNumber(self,string,case):
        if case == "D":
            curs = self.con.cursor()
            curs.execute("select * from doctor where employee_no like'"+string+"'")
            rows = curs.fetchall()
            if len(rows) == 0:
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
        else:
            curs = self.con.cursor()
            curs.execute("select * from patient where name like'"+string+"'")
            rows = curs.fetchall()
            if len(rows) == 0:
                return False
            else:
                return True
        
    def getDoctorNumber(self,string):
        
     
        curs = self.con.cursor()
        curs.execute("select employee_no from doctor d,patient p where p.name like '"+string+"' and p.health_care_no=d.health_care_no")
        rows = curs.fetchall()
        
        for row in rows:
            id1=int(row[0])
        print(string,"employee id is",id1)
        return id1
    
    
    def isNumber(self, string):
        return string.isdigit()
    

    def getTestName(self):
    
        curs = self.con.cursor()
        curs.execute('select test_name from test_type')
        rows = curs.fetchall()
        for row in rows:
            print(row)
            
        string = input('Enter test name: ')
        if self.isReal(string,"T"):
            return string,False 
        else:
            print("Not a real test, please try again")
            return False, True
    
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
        print(string,"employee id is",id1)
        return id1
        
    
    def printSeparator(self):
        print("")
        print("-----------------------")
        print("")
        

    def patientCanTakeTest(self):

        statement = "select * \
                     from not_allowed na, test_type t, patient p \
                     where t.type_id = na.test_id \
                     and p.health_care_no = na.health_care_no \
                     and p.health_care_no = " + str(self.patient) + " \
                     and t.test_name like '" + self.testName+"'"  

        curs = self.con.cursor()

        curs.execute(statement)
        cantTakeTest = curs.fetchall()

        if len(cantTakeTest) > 0:
            return False

        return True




    def executeStatement(self):
        print("******EXECUTING STATEMENT******")

        self.typeId = self.getTypeIdFromTestName(self.testName)

        self.testId = self.getUniqueTestId()

        curs = self.con.cursor()
        curs.execute("insert into test_record (test_id, type_id, patient_no, employee_no) values (" + str(self.testId) + ", " + str(self.typeId) + ", " + str(self.patient) + "," + str(self.doctor) + ")")

        self.con.commit()
        
    def getTypeIdFromTestName(self, string):
        
        curs = self.con.cursor()

        curs.execute("select type_id from test_type where \
                      test_name = '" + self.testName + "'")

        rows = curs.fetchall()

        if len(rows) != 1 :
            print('Error getting test type id.')
            return ""

        return rows[0][0]


    def getUniqueTestId(self):
        
        curs = self.con.cursor()
        curs.execute("select test_id from test_record")

        rows = curs.fetchall()

        while (True):
            testId = random.randint(0, 10**3)

            if all(testId != row[0] for row in rows):
                return testId	
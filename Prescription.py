import cx_Oracle
import getpass #gets password without echoing


class Prescription():

    def __init__(self):
        pass

    def main(self):

        f = open('credentials', 'r')
        
        username = f.readline()[:-1] #[-1] to trim \n
        password = f.readline()[:-1]
        
        #password = getpass.getpass() # could use this to get password, but doesn't work with IDE
        
        
        self.con = cx_Oracle.connect(username + '/' + \
                                password + '@gwynne.cs.ualberta.ca:1521/CRS')
        
        

        self.getInputs()

        if self.patientCanTakeTest() and self.labCanDoTest():
            self.executeStatement()
        else:
            print("Sorry this patient cannot take this type of test, please try again")
            self.main()
            

        
    def getInputs(self):
        go=True
        
        self.printSeparator()
        
        while go:
            self.doctor,go = self.getDoctor()
       
       
       
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


    
    def getDoctor(self):
        curs = self.con.cursor()

        curs.execute('select name,employee_no from doctor d,patient p where p.health_care_no=d.health_care_no')

        rows = curs.fetchall()

        for row in rows:
            print(row)
        string = input('Enter Doctor name or number: ')

        if self.isNumber(string):
            if self.goodNumber(string,"D"):
                print("employee id is",int(string))
                return int(string),False
            else:
                print("Invalid employee id")
                return False,True
        else:
            if self.isReal(string,"D"):
                return self.getDoctorNumber(string),False
            else:
                print(string,"is not a real doctor, try again")
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
        

    #checks if entered input doesn't violate database constraints. If input is
    #invalid, prints an error message as to why.
    def labCanDoTest(self):

        #TODO: get self.labName, 
        statement = 'select count(*) \
                        from can_conduct c, test_type t \
                        where t.type_id = c.test_id \
                        and c.lab_name = ' + self.labName + ' \
                        and t.test_name = ' + self.testName

        curs = self.con.cursor()

        curs.execute(statement)
        canDoTest = curs.fetchAll()[0]

        if canDoTest > 0:
            #print error message
            return True

        return False

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
            #print error message
            return False

        return True







    

    def executeStatement(self):
        print("******EXECUTING STATEMENT******")




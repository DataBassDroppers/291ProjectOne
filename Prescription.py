import cx_Oracle
import getpass #gets password without echoing


class Prescription():

    def __init(self):
        pass

    def main(self):

        f = open('credentials', 'r')
        
        username = f.readline()[:-1] #[-1] to trim \n
        password = f.readline()[:-1]
        
        #password = getpass.getpass() # could use this to get password, but doesn't work with IDE
        
        
        self.con = cx_Oracle.connect(username + '/' + \
                                password + '@gwynne.cs.ualberta.ca:1521/CRS')
        
        

        self.getInputs()

        if self.checkConstraints():
            self.executeStatement()

        
    def getInputs(self):
        self.printSeparator()
        self.doctor = self.getDoctor()
        self.printSeparator()
        self.testname = self.getTestName()
        self.printSeparator()
        self.patient = self.getPatient()
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
            print("employee id is",int(string))
            return int(string)
        else:
            return self.getDoctorNumber(string)

    
    def getDoctorNumber(self,string):
        
     
        curs = self.con.cursor()

        curs.execute("select employee_no from doctor d,patient p where p.name like '%"+string+"%' and p.health_care_no=d.health_care_no")

        rows = curs.fetchall()
        
        for row in rows:
            id1=int(row[0])
        print(string,"employee id is",id1)
        return id1
    
    
    def isNumber(self, string):
        return string.isdigit()
    

    def getTestName(self):
        string = input('Enter test name: ')
        print("test name entered",string)
        return string
    
    def getPatient(self):
        curs = self.con.cursor()

        curs.execute("select name,health_care_no from patient p")

        rows = curs.fetchall()
        
        for row in rows:
            print(row)
        
        
        string = input('Enter Patient name or number: ')

        if self.isNumber(string):
            print("patient id is",int(string))
            return int(string)
        else:
            return self.getPatientNumber(string)
            
    def getPatientNumber(self,string):
        curs = self.con.cursor()

        curs.execute("select health_care_no from patient p where p.name like '%"+string+"%'")

        rows = curs.fetchall()
        
        for row in rows:
            id1=int(row[0])
        print(string,"employee id is",id1)
        return id1
        
    
    def printSeparator(self):
        print("")
        print("-----------------------")
        print("")
        
    
    
    def checkConstraints(self):
        return True

    def executeStatement(self):
        print(self.doctor)



    #if __name__ == '__main__':
    #    Prescription.run()

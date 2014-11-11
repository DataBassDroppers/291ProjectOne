import cx_Oracle
import getpass #gets password without echoing
import random
import time


class SearchEngine():
    
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
        
        print("Press 1 for patient search")
        print("Press 2 for doctor search")
        
        print("")
        go=True                        
        while go:                    
            choice=input("What would you like to search by ?")
            if choice == "1":
                go=False
                self.patientSearch()
            elif choice == "2":
                go=False
                self.doctorSearch()
            else:
                print("Invalid input")
            
    def patientSearch(self):
        go=True
        while go:
            patient,go=self.getPatient()
        curs = self.con.cursor()
        curs.execute("select p.health_care_no,p.name,t.test_name,r.test_date,r.result from \
                          patient p, test_type t, test_record r \
                          where \
                          r.patient_no="+str(patient)+" \
                          and \
                          p.health_care_no=r.patient_no \
                          and \
                          t.type_id=r.type_id")
        rows = curs.fetchall()
        
        for row in rows: 
            list1=[]
            counter=0
            for x in row:       
                if counter == 3:
                    x=(x.strftime("%Y-%m-%d %H:%M:%S"))
                    x=x[:-9]
                counter+=1
                list1.append(x)
            print(tuple(list1))
            
            
    def doctorSearch(self):
        go=True
        while go:
            print("Please enter doctor name or employee id")
            doctor,go=self.getDoctor()
            
        start=self.getDate("S")
        end=self.getDate("E")
 
        curs = self.con.cursor()
        curs.execute("select p.health_care_no,p.name,t.test_name,r.prescribe_date \
                              from patient p, test_name t, test_record r \
                              where t.employee_id="+str(doctor)+"\
                              and \
                              r.prescribe_date >= '"+start+"' \
                              and \
                              r.prescribe_date <= '"+end+"' \
                              and \
                              p.health_care_no = r.patient_no")
        rows = curs.fetchall()        
        
        for row in rows: 
            list1=[]
            counter=0
            for x in row:       
                if counter == 3:
                    x=(x.strftime("%Y-%m-%d %H:%M:%S"))
                    x=x[:-9]
                counter+=1
                list1.append(x)
            print(tuple(list1))    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    def getDate(self,case):
        go=True
        while go:
            if case == "S":
                date=input("Please enter start prescribe date in format DD/MM/YYYY")
            else:
                date=input("Please enter end prescribe date in format DD/MM/YYYY")
            try:
                int(date[:2])
                int(date[3:5])
                int(date[6:]) 
                    
            except ValueError:
                print("Invalid input")
            else:
                if (0 <= int(date[:2])) and (int(date[:2]) <= 31) and (0 <= int(date[3:5])) and ( int(date[3:5])<= 12):
                    go=False
                else:
                    print("Invalid input")
            
        return date    
            
            
            
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
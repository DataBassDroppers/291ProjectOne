import cx_Oracle
import getpass #gets password without echoing
import random
import time


class SearchEngine():
    
    def __init__(self):
        pass
    
    def main(self, credentials):

        self.con = cx_Oracle.connect(credentials[0] + '/' + \
                                         credentials[1] + '@gwynne.cs.ualberta.ca:1521/CRS')	

        print()
        print("[1] Patient search.")
        print("[2] Doctor search.")
        print("[3] At risk patients.")
        print()
        go=True                        
        while go:                    
            choice=input("Enter search option: ")
            if choice == "1":
                go=False
                self.patientSearch()
            elif choice == "2":
                go=False
                self.doctorSearch()
            elif choice == "3":
                go=False
                self.alarmingAgeSearch()
            else:
                print("Invalid input.")
        return 1
            
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
                    if x is not None: 
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
                              from patient p, test_type t, test_record r, doctor d \
                              where d.employee_no="+str(doctor)+"\
                              and \
                              d.employee_no = r.employee_no \
                              and \
                              t.type_id = r.type_id \
                              and \
                              r.prescribe_date >= to_date('"+start+"', 'DD/MM/YYYY') \
                              and \
                              r.prescribe_date <= to_date('"+end+"', 'DD/MM/YYYY') \
                              and \
                              p.health_care_no = r.patient_no")
        rows = curs.fetchall()        
        
        for row in rows: 
            list1=[]
            counter=0
            for x in row:       
                if counter == 3:
                    if x is not None:
                        x=(x.strftime("%Y-%m-%d %H:%M:%S"))
                        x=x[:-9]
                counter+=1
                list1.append(x)
            print(tuple(list1))
            

    def alarmingAgeSearch(self):

        go=True
        while go:
            print("Please enter a test type")
            testName,go=self.getTestName()


        typeId = self.getTypeIdFromTestName(testName)
        
                


        curs = self.con.cursor()

        try:
            curs.execute("DROP VIEW medical_risk")
        except cx_Oracle.DatabaseError:
            pass
        
        curs.execute("CREATE VIEW medical_risk(medical_type,alarming_age,abnormal_rate) AS \
SELECT c1.type_id,min(c1.age),ab_rate\
 FROM  (SELECT   t1.type_id, count(distinct t1.patient_no)/count(distinct t2.patient_no) ab_rate\
      FROM     test_record t1, test_record t2\
      WHERE    t1.result <> 'normal' AND t1.type_id = t2.type_id\
      GROUP BY t1.type_id\
      ) r,\
     (SELECT   t1.type_id,age,COUNT(distinct p1.health_care_no) AS ab_cnt\
      FROM     patient p1,test_record t1,\
               (SELECT DISTINCT trunc(months_between(sysdate,p1.birth_day)/12) AS age FROM patient p1) \
      WHERE    trunc(months_between(sysdate,p1.birth_day)/12)>=age\
               AND p1.health_care_no=t1.patient_no\
               AND t1.result<>'normal'\
      GROUP BY age,t1.type_id\
      ) c1, \
      (SELECT  t1.type_id,age,COUNT(distinct p1.health_care_no) AS cnt\
       FROM    patient p1, test_record t1,\
      	       (SELECT DISTINCT trunc(months_between(sysdate,p1.birth_day)/12) AS age FROM patient p1)\
       WHERE trunc(months_between(sysdate,p1.birth_day)/12)>=age\
             AND p1.health_care_no=t1.patient_no\
       GROUP BY age,t1.type_id\
      ) c2\
 WHERE  c1.age = c2.age AND c1.type_id = c2.type_id AND c1.type_id = r.type_id \
       AND c1.ab_cnt/c2.cnt>=2*r.ab_rate\
 GROUP BY c1.type_id,ab_rate")

        curs.execute("SELECT DISTINCT name, address, phone\
  FROM   patient p, medical_risk m\
  WHERE  trunc(months_between(sysdate,birth_day)/12) >= m.alarming_age \
  AND m.medical_type = " + str(typeId) + "\
  AND       p.health_care_no NOT IN (SELECT patient_no\
                                FROM   test_record t\
                                WHERE  m.medical_type = t.type_id\
                                AND t.result IS NOT NULL\
                               )")

        rows = curs.fetchall()

        print("\nPatients who are above the alarming age and have not been tested:")
        for row in rows:
            print(row)
        

        
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




    def getTypeIdFromTestName(self, testName):
        
        curs = self.con.cursor()

        curs.execute("select type_id from test_type where \
                      test_name = '" + testName + "'")

        rows = curs.fetchall()

        if len(rows) != 1 :
            print('Error getting test type id.')
            return ""

        return rows[0][0]        
            
            
            
            
    def getDate(self,case):
        go=True
        while go:
            if case == "S":
                date=input("Please enter start prescribe date in format DD/MM/YYYY: ")
            else:
                date=input("Please enter end prescribe date in format DD/MM/YYYY: ")
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

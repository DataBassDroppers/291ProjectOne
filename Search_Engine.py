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
                            
        go=True                        
        while go:                    
            print("Press 1 for patient search")
            choice=input("What would you like to search by ?")
            if choice == "1":
                go=False
                self.patientSearch()
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
                    #print(type((x.strftime("%Y-%m-%d %H:%M:%S"))))
                    x=(x.strftime("%Y-%m-%d %H:%M:%S"))
                    x=x[:-9]
                counter+=1
                list1.append(x)
            print(tuple(list1))
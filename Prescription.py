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
        
        
        con = cx_Oracle.connect(username + '/' + \
                                password + '@gwynne.cs.ualberta.ca:1521/CRS')
        
        
        curs = con.cursor()

        curs.execute('select name, health_care_no from patient')

        rows = curs.fetchall()

        for row in rows:
            print(row)
        

        self.getInputs()

        if self.checkConstraints():
            self.executeStatement()

        
    def getInputs(self):

        self.doctor = self.getDoctor()


    def getDoctor(self):
        
        string = input('Enter Doctor name or number: ')

        if self.isEmployeeNumber(string):
            self.numberWasEntered = True
        else:
            self.numberWasEntered = False

        return string
    
    def isEmployeeNumber(self, string):
        return string.isdigit()













        

    def checkConstraints(self):
        return True

    def executeStatement(self):
        print(self.doctor)



    #if __name__ == '__main__':
    #    Prescription.run()

import cx_Oracle
import getpass #gets password without echoing
import random

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
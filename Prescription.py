import cx_Oracle
#import getpass #gets password without echoing

class Prescription():

    #if __name__ == '__main__':
    #    Prescription().run()
        
    def __main__():
        
        #password = getpass.getpass() # could use this to get password, but doesn't work with IDE
        
        f = open('credentials', 'r')
        
        username = f.readline()[:-1] #[-1] to trim \n
        password = f.readline()[:-1]
        
        
        con = cx_Oracle.connect(username + '/' + \
                                password + '@gwynne.cs.ualberta.ca:1521/CRS')
        
        


    
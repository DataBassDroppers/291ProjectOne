import cx_Oracle



class Prescription():

    #if __name__ == '__main__':
    #    Prescription().run()
        
    def __main__():
        user = input('Username: ')
        password = input('Password: ')
        


        con = cx_Oracle.connect(user + '/' + \
                                password + '@gwynne.cs.ualberta.ca:1521:CRS')
        
        


    
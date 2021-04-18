from AppRent import *

if __name__ == '__main__':
    host="localhost"
    user="root"
    password=""
    db="PeminjamanBuku"
    conn = AppDatabase(host,user,password,db)
    service = AppService(conn)  
    gui = AppUI("Neugierig Bibliothek","1000x650",service)
    
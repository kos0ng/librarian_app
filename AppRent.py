from tkinter import Tk, Label, Button, Entry,Canvas, ttk,END
import mysql.connector
from datetime import datetime,timedelta

class bookDTO():
    def __init__(self,judul,pengarang,penerbit,id_kategori,barcode,tersedia,total,id_buku):
        self.judul=judul
        self.pengarang=pengarang
        self.penerbit=penerbit
        self.id_kategori=str(id_kategori)
        self.barcode=str(barcode)
        self.tersedia=str(tersedia)
        self.total=str(total)
        self.id_buku = str(id_buku)

class mahasiswaDTO():
    def __init__(self,nim,nama):
        self.nim = str(nim)
        self.nama = str(nama)

class AppDatabase():
    def __init__(self,host,user,password,db):
        self.db = mysql.connector.connect(host=host,user=user,password=password,db=db)
        self.cursor = self.db.cursor()

class AppService():
    def __init__(self,conn):
        self.conn=conn

    def searchBook(self,judul):
        conn=self.conn
        query="select judul,pengarang,penerbit,id_kategori,barcode,exemplar_tersedia,exemplar_total,id_buku from buku where judul like '%"+judul+"%'"
        conn.cursor.execute(query)
        return conn.cursor.fetchall()

    def searchMahasiswa(self,nim):
        conn=self.conn
        query="select * from mahasiswa where nim="+nim
        conn.cursor.execute(query)
        return conn.cursor.fetchall()

    def insertPeminjaman(self,id_buku,nim,tanggal):
        conn=self.conn
        query = "INSERT INTO peminjaman (id_buku, nim, tanggal_kembali) VALUES (%s, %s, %s)"
        val = (id_buku, nim, tanggal)
        conn.cursor.execute(query,val)
        conn.db.commit()
    
    def searchPeminjaman(self,nim):
        conn=self.conn
        query="select id_peminjaman,judul from peminjaman join buku on peminjaman.id_buku=buku.id_buku where nim="+nim
        conn.cursor.execute(query)
        return conn.cursor.fetchall()
    
    def deletePeminjaman(self,id_peminjaman):
        conn=self.conn
        query="delete from peminjaman where id_peminjaman="+id_peminjaman
        conn.cursor.execute(query)
        conn.db.commit()

    def bukuTerpopuler(self):
        currentMonth = datetime.now().month
        conn=self.conn
        result={}
        query="select judul from peminjaman join buku on peminjaman.id_buku=buku.id_buku where MONTH(tanggal_kembali)="+str(currentMonth)
        conn.cursor.execute(query)
        tmp=conn.cursor.fetchall()
        for i in tmp:
            if(i[0] not in result):
                result[i[0]]=0
        for i in tmp:
            result[i[0]]+=1
        fix_result=dict(sorted(result.items(), key=lambda item: item[1],reverse=True))
        return fix_result



class AppUI():
    def __init__(self,title,size,service):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(size)
        self.service = service
        self.bookDTO = bookDTO
        self.tc = ttk.Notebook(self.root)
        self.t1 = ttk.Frame(self.tc)
        self.t2 = ttk.Frame(self.tc)
        service = self.service
        root = self.root
        tc = self.tc
        t1 = self.t1
        t2 = self.t2
        tc.add(t1, text='Cari')
        tc.add(t2, text='Laporan')
        tc.pack()
        tc.place(x=0, y=80)
    
        # self.label_spa_1 = ttk.Label(text="", width=25).grid(row=3, column=2)
        now = datetime.today().strftime('%Y-%m-%d')
        self.label_spa_1 = ttk.Label(text="Neugierig bibliothek", width=25).grid(row=3, column=1)
        self.label_spa_1 = ttk.Label(text="", width=25).grid(row=3, column=2)
        self.label_spa_1 = ttk.Label(text="", width=25).grid(row=3, column=3)
        self.label_spa_1 = ttk.Label(text=now, width=25).grid(row=3, column=4)
        self.label_spa_2 = ttk.Label(text="Ilse. Str No.21", width=25).grid(row=4, column=1)
        self.label_spa_3 = ttk.Label(text="Berlin - 12053", width=25).grid(row=5, column=1)

        self.label_cari= ttk.Label(t1, text ="Cari", width=25).grid(row =1, column=1)
        self.label_spasi_cari_1 = ttk.Label(t1, text="", width=15).grid(row=1, column=3)
        self.label_spasi_3= ttk.Label(t1, text="", width=15).grid(row=2, column=1)
        self.label_spasi_5 = ttk.Label(t1, text="", width=15).grid(row=4, column=1)
        self.label_spasi_6 = ttk.Label(t1, text="", width=15).grid(row=5, column=1)
        self.label_buku = ttk.Label(t1, text="BUKU", width=15).grid(row=6, column=1)

        self.entry_cari = ttk.Entry(t1, width=25)
        self.entry_cari.grid(row =1, column=2)

        self.button = ttk.Button(t1, text="CARI" ,width=20,command= self.submitJudul).grid(row=1,column=4)

        self.label_judul = ttk.Label(t1, text="Judul", width=25).grid(row=7,column=1)
        self.label_pengarang = ttk.Label(t1, text="Pengarang", width=25).grid(row=8,column=1)
        self.label_penerbit = ttk.Label(t1, text="Penerbit", width=25).grid(row=9,column=1)
        self.label_klasi = ttk.Label(t1, text="No. Klasifikasi",  width=25).grid(row=10,column=1)
        self.label_barcode = ttk.Label(t1, text="No. Barcode",  width=25).grid(row=11,column=1)
        self.label_exem = ttk.Label(t1, text="Jumlah Exemplar", width=25).grid(row=12,column=1)

        self.label_errorcari = ttk.Label(t1, text="", width=40)
        self.label_errorcari.grid(row=5, column=2)
        
        self.value_judul = ttk.Entry(t1,text="",width=40,state='disabled')
        self.value_judul.grid(row = 7,column=2)
        self.value_pengarang = ttk.Entry(t1,text="",width=40,state='disabled')
        self.value_pengarang.grid(row = 8,column=2)
        self.value_penerbit = ttk.Entry(t1,text="",width=40,state='disabled')
        self.value_penerbit.grid(row = 9,column=2)
        self.value_klasi = ttk.Entry(t1,text="",width=40,state='disabled')
        self.value_klasi.grid(row = 10,column=2)
        self.value_barcode = ttk.Entry(t1,text="",width=40,state='disabled')
        self.value_barcode.grid(row = 11,column=2)
        self.value_exem = ttk.Entry(t1,text="",width=40,state='disabled')
        self.value_exem.grid(row = 12,column=2)
        

        self.label_a = ttk.Label(t1, text="", width=15).grid(row=13, column=1)
        self.label_cari_nim = ttk.Label(t1, text="Nomor Induk Mahasiswa", width=25).grid(row=14, column=1)
        self.label_spasi_b = ttk.Label(t1, text="", width=15).grid(row=15, column=1)
        self.label_spasi_c = ttk.Label(t1, text="", width=15).grid(row=17, column=1)

        self.label_mahasiswa = ttk.Label(t1, text="Member", width=15).grid(row=19, column=1)
        
        self.label_errornim = ttk.Label(t1, text="", width=40)
        self.label_errornim.grid(row=17, column=2)
        self.entry_nim = ttk.Entry(t1, width=25)
        self.entry_nim.grid(row=14, column=2)
        self.label_spasi_cari_2 = ttk.Label(t1, text="", width=15).grid(row=14, column=3)
        self.button_cari_2 = ttk.Button(t1, text="CARI", width=20,command= self.submitNIM).grid(row=14, column=4)
        
        self.button_pinjam = ttk.Button(t1, text="PINJAM", width=20,command=self.submitPinjam)
        self.button_pinjam.grid(row=16, column=4)

        self.label_nama = ttk.Label(t1, text="Nama", width=25).grid(row=20, column=1)
        self.label_nim = ttk.Label(t1, text="Nomor Induk Mahasiswa", width=25).grid(row=21, column=1)
        self.label_tanggal_kembali = ttk.Label(t1, text="Tanggal Kembali", width=25).grid(row=22, column=1)
        self.label_peminjaman = ttk.Label(t1, text="Peminjaman", width=26).grid(row=23, column=1)


        self.value_nim = ttk.Entry(t1,text="",width=40,state='disabled')
        self.value_nim.grid(row = 20,column=2)
        self.value_nama = ttk.Entry(t1,text="",width=40,state='disabled')
        self.value_nama.grid(row = 21,column=2)
        self.value_tanggal = ttk.Entry(t1,text="",width=40,state='disabled')
        self.value_tanggal.grid(row = 22,column=2)

        self.id_peminjaman_1 = Entry(t1, width=25,state='disabled')
        self.id_peminjaman_1.grid(row=27, column=1)
        self.id_peminjaman_2 = Entry(t1, width=25,state='disabled')
        self.id_peminjaman_2.grid(row=28, column=1)
        self.entry_peminjaman_1 = Entry(t1, width=25,state='disabled')
        self.entry_peminjaman_1.grid(row=27, column=2)
        self.entry_peminjaman_2 = Entry(t1, width=25,state='disabled')
        self.entry_peminjaman_2.grid(row=28, column=2)

        self.button_kembalikan_1= ttk.Button(t1, text="KEMBALIKAN", width=20,state='disabled',command= lambda: self.submitKembalikan(1))
        self.button_kembalikan_1.grid(row=27, column=4)
        self.button_kembalikan_2 = ttk.Button(t1, text="KEMBALIKAN", width=20,state='disabled',command= lambda: self.submitKembalikan(2))
        self.button_kembalikan_2.grid(row=28, column=4)
        
        self.label_spa2_1 = ttk.Label(t2,text="", width=25).grid(row=1, column=2)
        self.label_spa2_2 = ttk.Label(t2,text="", width=25).grid(row=2, column=2)
        self.label_spa2_3 = ttk.Label(t2,text="", width=25).grid(row=3, column=2)
        self.label_spa2_4 = ttk.Label(t2,text="", width=25).grid(row=4, column=2)
        self.label_spa2_5 = ttk.Label(t2,text="", width=25).grid(row=5, column=1)
        self.label_spa2_5 = ttk.Label(t2,text="", width=25).grid(row=6, column=1)
        self.button_refresh = ttk.Button(t2, text="REFRESH", width=10,command=self.bukuTerpopuler).grid(row=4, column=2)
        self.label_judulterbanyak = ttk.Label(t2, text="5 Judul Terpopuler didalam 1 bulan", width=30)
        self.label_judulterbanyak.grid(row=5    , column=2)
        self.bukuTerpopuler()
        root.mainloop()
    
    def bukuTerpopuler(self):
        t2=self.t2
        result=self.service.bukuTerpopuler()
        ttk.Label(t2,text="Jumlah Peminjaman", width=25).grid(row=7, column=2)
        ttk.Label(t2,text="Judul Buku", width=25).grid(row=7, column=3)
        for j in range(5):
            ttk.Label(t2,text='', width=25).grid(row=8+j, column=2)
            ttk.Label(t2,text='', width=25).grid(row=8+j, column=3)
        i=0
        for key, value in result.items():
            ttk.Label(t2,text=value, width=25).grid(row=8+i, column=2)
            ttk.Label(t2,text=key, width=25).grid(row=8+i, column=3)
            if(i==4):
                break
            i+=1

    def submitKembalikan(self,id_button):
        if(id_button==1 and self.nim!=-1):
            id_peminjaman=self.id_peminjaman_1.get()
            self.service.deletePeminjaman(id_peminjaman)
            self.checkPinjam(self.nim)
        elif(id_button==2 and self.nim!=-1):
            id_peminjaman=self.id_peminjaman_2.get()
            self.service.deletePeminjaman(id_peminjaman)
            self.checkPinjam(self.nim)

    def submitJudul(self):
        judul = self.entry_cari.get()
        result = self.service.searchBook(judul)
        if(len(result)>0):
            tmp = result[0]
            book = bookDTO(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7])
            self.id_buku = book.id_buku
            self.value_judul['state']='normal'
            self.value_judul.delete(0,END)
            self.value_judul.insert(0,book.judul)
            self.value_judul['state']='disabled'
            self.value_pengarang['state']='normal'
            self.value_pengarang.delete(0,END)
            self.value_pengarang.insert(0,book.pengarang)
            self.value_pengarang['state']='disabled'
            self.value_penerbit['state']='normal'
            self.value_penerbit.delete(0,END)
            self.value_penerbit.insert(0,book.penerbit)
            self.value_penerbit['state']='disabled'
            self.value_klasi['state']='normal'
            self.value_klasi.delete(0,END)
            self.value_klasi.insert(0,book.id_kategori)
            self.value_klasi['state']='disabled'
            self.value_barcode['state']='normal'
            self.value_barcode.delete(0,END)
            self.value_barcode.insert(0,book.barcode)
            self.value_barcode['state']='disabled'
            self.value_exem['state']='normal'
            self.value_exem.delete(0,END)
            self.value_exem.insert(0,book.tersedia+"/"+book.total)
            self.value_exem['state']='disabled'
            self.label_errorcari.configure(text="")
            # print(self.id_buku)
        else:
            self.label_errorcari.configure(text="Judul BUKU Tidak Ditemukan",foreground='red')
            self.id_buku=-1
            self.value_judul['state']='normal'
            self.value_judul.delete(0,END)
            self.value_judul['state']='disabled'
            self.value_pengarang['state']='normal'
            self.value_pengarang.delete(0,END)
            self.value_pengarang['state']='disabled'
            self.value_penerbit['state']='normal'
            self.value_penerbit.delete(0,END)
            self.value_penerbit['state']='disabled'
            self.value_klasi['state']='normal'
            self.value_klasi.delete(0,END)
            self.value_klasi['state']='disabled'
            self.value_barcode['state']='normal'
            self.value_barcode.delete(0,END)
            self.value_barcode['state']='disabled'
            self.value_exem['state']='normal'
            self.value_exem.delete(0,END)
            self.value_exem['state']='disabled'
        self.t1.update()

    def submitNIM(self):
        nim = self.entry_nim.get()
        result = self.service.searchMahasiswa(nim)
        if(len(result)>0):
            self.label_errornim.configure(text="")
            tmp = result[0]
            now = datetime.today()
            oneweek = timedelta(days=7)
            t = now+oneweek
            fix_time = t.strftime('%Y-%m-%d')
            mahasiswa = mahasiswaDTO(tmp[0],tmp[1])
            self.nim = mahasiswa.nim
            self.value_nim['state']='normal'
            self.value_nim.delete(0,END)
            self.value_nim.insert(0,mahasiswa.nim)
            self.value_nim['state']='disabled'
            self.value_nama['state']='normal'
            self.value_nama.delete(0,END)
            self.value_nama.insert(0,mahasiswa.nama)
            self.value_nama['state']='disabled'
            self.value_tanggal['state']='normal'
            self.value_tanggal.delete(0,END)
            self.value_tanggal.insert(0,fix_time)
            self.value_tanggal['state']='disabled'
            self.checkPinjam(self.nim)
        else:
            self.nim = -1
            self.label_errornim.configure(text="NIM Tidak Ditemukan",foreground='red')
            self.value_nim['state']='normal'
            self.value_nim.delete(0,END)
            self.value_nim['state']='disabled'
            self.value_nama['state']='normal'
            self.value_nama.delete(0,END)
            self.value_nama['state']='disabled'
            self.value_tanggal['state']='normal'
            self.value_tanggal.delete(0,END)
            self.value_tanggal['state']='disabled'
            self.entry_peminjaman_1['state']='normal'
            self.entry_peminjaman_1.delete(0,END)
            self.entry_peminjaman_1['state']='disabled'
            self.entry_peminjaman_2['state']='normal'
            self.entry_peminjaman_2.delete(0,END)
            self.entry_peminjaman_2['state']='disabled'
            self.id_peminjaman_1['state']='normal'
            self.id_peminjaman_1.delete(0,END)
            self.id_peminjaman_1['state']='disabled'
            self.id_peminjaman_2['state']='normal'
            self.id_peminjaman_2.delete(0,END)
            self.id_peminjaman_2['state']='disabled'
            self.button_kembalikan_1['state']='disabled'
            self.button_kembalikan_2['state']='disabled'

        self.t1.update()

    def checkPinjam(self,nim):
        result=self.service.searchPeminjaman(nim)
        if(len(result)==2):
            self.id_peminjaman_1['state']='normal'
            self.id_peminjaman_1.delete(0,END)
            self.id_peminjaman_1.insert(0,result[0][0])
            self.id_peminjaman_1['state']='disabled'
            self.entry_peminjaman_1['state']='normal'
            self.entry_peminjaman_1.delete(0,END)
            self.entry_peminjaman_1.insert(0,result[0][1])
            self.entry_peminjaman_1['state']='disabled'
            self.id_peminjaman_2['state']='normal'
            self.id_peminjaman_1.delete(0,END)
            self.id_peminjaman_2.insert(0,result[1][0])
            self.id_peminjaman_2['state']='disabled'
            self.entry_peminjaman_2['state']='normal'
            self.entry_peminjaman_2.delete(0,END)
            self.entry_peminjaman_2.insert(0,result[1][1])
            self.entry_peminjaman_2['state']='disabled'
            self.button_kembalikan_1['state']='normal'
            self.button_kembalikan_2['state']='normal'
        elif(len(result)==1):
            self.id_peminjaman_1['state']='normal'
            self.id_peminjaman_1.delete(0,END)
            self.id_peminjaman_1.insert(0,result[0][0])
            self.id_peminjaman_1['state']='disabled'
            self.entry_peminjaman_1['state']='normal'
            self.entry_peminjaman_1.delete(0,END)
            self.entry_peminjaman_1.insert(0,result[0][1])
            self.entry_peminjaman_1['state']='disabled'
            self.button_kembalikan_1['state']='normal'
            self.entry_peminjaman_2['state']='normal'
            self.entry_peminjaman_2.delete(0,END)
            self.entry_peminjaman_2['state']='disabled'
            self.id_peminjaman_2['state']='normal'
            self.id_peminjaman_2.delete(0,END)
            self.id_peminjaman_2['state']='disabled'
            self.button_kembalikan_2['state']='disabled'
        else:
            self.entry_peminjaman_1['state']='normal'
            self.entry_peminjaman_1.delete(0,END)
            self.entry_peminjaman_1['state']='disabled'
            self.entry_peminjaman_2['state']='normal'
            self.entry_peminjaman_2.delete(0,END)
            self.entry_peminjaman_2['state']='disabled'
            self.id_peminjaman_1['state']='normal'
            self.id_peminjaman_1.delete(0,END)
            self.id_peminjaman_1['state']='disabled'
            self.id_peminjaman_2['state']='normal'
            self.id_peminjaman_2.delete(0,END)
            self.id_peminjaman_2['state']='disabled'
            self.button_kembalikan_1['state']='disabled'
            self.button_kembalikan_2['state']='disabled'

    def submitPinjam(self):
        try:
            nim = self.nim
        except Exception as e:
            nim = -1
        try:
            id_buku = self.id_buku
        except Exception as e:
            id_buku = -1
        if(id_buku!=-1 and nim!=-1):
            if(len(self.service.searchPeminjaman(nim))>=2):
                self.label_errorcari.configure(text="Telah melebihi Quota Peminjaman!",foreground='red')    
            else:
                # print("PINJAM "+str(id_buku))
                self.service.insertPeminjaman(id_buku,nim,self.value_tanggal.get())
                self.label_errorcari.configure(text="Sukses meminjam!",foreground='green')
                self.checkPinjam(nim)
        else:
            self.label_errorcari.configure(text="Harus memilih buku dan mahasiswa terlebih dahulu!",foreground='red',width=40)
        self.t1.update()

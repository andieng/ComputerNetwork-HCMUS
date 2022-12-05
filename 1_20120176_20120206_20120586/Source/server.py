#from os import curdir
import os
import time
from datetime import datetime
import socket
import threading
import pyodbc
import json
from urllib.request import urlopen
import traceback
import schedule

import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import scrolledtext
from PIL import Image,ImageTk # Hình ảnh



#file (phải để tên đầy đủ, để tên ngắn sẽ không execute trong file .sql được)
PATH = "D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/"
FILE_TODAY_NAME = "D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_today.json"
FILE_TODAY_TEMP = "D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_today_temp.json"
FILE_TYPE = ".json"
TYPE_NAME = "data_"

#other
FORMAT = "utf8"
URL = "https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now"

#connection
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8000
ADDR=(HOST, PORT)

#database
DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = "LAPTOP-KTHHM3B2\ESTHER"
DATABASE_NAME = "Socket_TyGiaVang"
ACCOUNT_TABLE = "Account"
DATA_TABLE = "ThongTinVang"

#option
LOGIN = "login" 
SIGNUP = "signup" 
LOGOUT = "logout"
SEARCH = "search"
STOP_CONNECTION = "stop"


LiveAccount=[]
ID=[]
Ad=[]
active_clients=[]
off_clients=[]

def checkAccount(username):
    for row in LiveAccount:
        parse = row.find("-")
        parseCheck = row[(parse+1): ]
        if parseCheck == username:
            return False
    return True      

def removeLiveAccount(addr):
    for row in LiveAccount:
        parse = row.find("-")
        parseCheck = row[:parse]

        if parseCheck == str(addr):
            parse = row.find("-")
            Ad.remove(parseCheck)
            username = row[(parse+1): ]
            ID.remove(username)
            LiveAccount.remove(row)
            #conn.sendall("True".encode(FORMAT))

def serverLoginCheck(username, password):
    cursor = connectToDB().cursor()
    cursor.execute(f"select u.username from {ACCOUNT_TABLE} u")

    if checkAccount(username) == False:
        return 0
    #check admin
    
    for row in cursor:
        #get row in databse (ex: "('account1', )")
        parse=str(row)
        #get characters from position 2  (ex: "account1', )")
        parseCheck = parse[2: ]
        #number of characters before "'" (ex: "account1', )" then parse = "8")
        parse = parseCheck.find("'")
        #get characters from position 0 to position parse (ex: parse = "8" then parseCheck = "account1")
        parseCheck = parseCheck[:parse]
        
        if parseCheck == username:
            cursor.execute(f"select u.password from {ACCOUNT_TABLE} u where u.username=(?)",(username))
            parse = str(cursor.fetchone())
            print(parse)
            parseCheck = parse[2: ]
            print(parseCheck)
            parse = parseCheck.find("'")
            print(parse)
            parseCheck = parseCheck[:parse]
            print(parseCheck)
            if password == parseCheck:
                return 1

    return 2

def serverLogin(sck):
    #receIve username
    user = sck.recv(1024).decode(FORMAT)
    print("username:--" + user + "--")

    sck.sendall(user.encode(FORMAT))

    #receive password
    pwd = sck.recv(1024).decode(FORMAT)
    print("password:--" + pwd + "--")

    #check if account is existed, if existed then accepted
    accepted = serverLoginCheck(user, pwd)

    if accepted == 1:
        ID.append(user)
        account = str(Ad[Ad.__len__()-1])+"-"+str(ID[ID.__len__()-1])
        LiveAccount.append(account)

    print ("accept:", accepted)
    sck.sendall(str(accepted).encode(FORMAT))
    print("end")

def serverSignupCheck(username):
    if username == "admin":
        return False

    cursor = connectToDB().cursor()
    cursor.execute(f"select u.username from {ACCOUNT_TABLE} u")
    
    for row in cursor:
        #get row in databse (ex: "('account1', )")
        parse=str(row)
        #get characters from position 2  (ex: "account1', )")
        parseCheck = parse[2: ]
        #number of characters before "'" (ex: "account1', )" then parse = "8")
        parse = parseCheck.find("'")
        #get characters from position 0 to position parse (ex: parse = "8" then parseCheck = "account1")
        parseCheck = parseCheck[:parse]
        

        if parseCheck == username:
            return 0
    return 1

def serverSignup(sck, addr):
    #receive username
    user = sck.recv(1024).decode(FORMAT)
    print("username:--" + user + "--")

    sck.sendall(user.encode(FORMAT))

    #receive password
    pwd = sck.recv(1024).decode(FORMAT)
    print("password:--" + pwd + "--")

    #check if account is existed
    accepted = serverSignupCheck(user)
    print("accepted: ", accepted)
    sck.sendall(str(accepted).encode(FORMAT))

    if accepted == 1:
        insertUser(user, pwd)

        #add client address to live account
        Ad.append(str(addr))
        ID.append(user)
        account = str(Ad[Ad.__len__()-1]) + "-" + str(ID[ID.__len__()-1])
        LiveAccount.append(account)
    
    print("End")

#Check if text has certain characters
def checkText(text, key):
    text.find(key) == 1 #not found
    text.find(key) != 1 #found

def getDateData(cursor):
    cursor.execute(f"select day from {DATA_TABLE}")
    data = []
    for row in cursor:
        parse=str(row)
        parseCheck =parse[2:]
        parse= parseCheck.find("'")
        parseCheck= parseCheck[:parse]
        data.append(parseCheck)
    return data  

#Check each row if it has given brand or not
#Then append data
def searchDateData(date):
    res = []
    cursor = connectToDB().cursor()
    data = getDateData(cursor)
    if date == "Ngày":
        return "Empty"
    else:
        for row in data:
            if row == date:
                details=[]
                cursor.execute(f"select * from {DATA_TABLE} where day =(?)", (date))
                #print("---date---")
                for row in cursor:
                    #print(row)
                    details.append(row)
                #print("---")
                return details

#Get company column's data from database
def getBrandData(cursor):
    cursor.execute(f"select company from {DATA_TABLE}")
    data = []
    for row in cursor:
        parse=str(row)
        parseCheck =parse[2:]
        parse= parseCheck.find("'")
        parseCheck= parseCheck[:parse]
        data.append(parseCheck)
    return data  

#Check each row if it has given brand or not
#Then append data
def searchBrandData(brand):
    res = []
    cursor = connectToDB().cursor()
    data = getBrandData(cursor)
    if brand == "Nhãn":
        return "Empty"
    else:
        for row in data:
            if row == brand:
                details=[]
                cursor.execute(f"select * from {DATA_TABLE} where company =(?)", (brand))
                #print("---brand---")
                for row in cursor:
                    #print(row)
                    details.append(row)
                #print("---")
                return details

#Get type column's data from database
def getTypeData(cursor):
    cursor.execute(f"select type from {DATA_TABLE}")
    data = []
    for row in cursor:
        parse=str(row)
        parseCheck =parse[2:]
        parse= parseCheck.find("'")
        parseCheck= parseCheck[:parse]
        data.append(parseCheck)
    return data  

#Check each row if it has given type or not
#Then append data
def searchTypeData(type):
    res = []
    cursor = connectToDB().cursor()
    data = getTypeData(cursor)
    tmp = '%' + type + '%'
    if type == "Loại":
           return "Empty"
    else:
        for row in data:
            if checkText(row, type) != 1:
                details=[]
                cursor.execute(f"select * from {DATA_TABLE} where type like (?)", tmp)
                #print("---type---")
                for row in cursor:
                    #print(row)
                    details.append(row)
                #print("---")
                return details

#Get place column's data from database
def getPlaceData(cursor):
    cursor.execute(f"select brand from {DATA_TABLE}")
    data = []
    for row in cursor:
        parse=str(row)
        parseCheck =parse[2:]
        parse= parseCheck.find("'")
        parseCheck= parseCheck[:parse]
        data.append(parseCheck)
    return data  

#Check each row if it has given place or not
#Then append data
def searchPlaceData(place):
    res = []
    cursor = connectToDB().cursor()
    data = getPlaceData(cursor)
    if place == "Thành phố":
        return "Empty"
    else:
        for row in data:
            if row == place:
                details=[]
                cursor.execute(f"select * from {DATA_TABLE} where brand =(?)", place)
                #print("---place---")
                for row in cursor:
                    #print(row)
                    details.append(row)
                #print("---")
                return details

def mergeData(a, b):
    data=[]
    for i in a:
        for j in b:
            if j == i:
                data.append(j)
    return data

#Check if each list has same row or not
#Then get those duplicated rows

def getDetails(a, b, c, d):
    if a == "Empty" and b != "Empty" and c != "Empty" and d != "Empty":
        details = mergeData(b, c)
        details = mergeData(details, d)
        return details

    elif b == "Empty" and a != "Empty" and c != "Empty" and d != "Empty":
        details = mergeData(a, c)
        details = mergeData(details, d)
        return details

    elif c == "Empty" and b != "Empty" and a != "Empty" and d != "Empty":
        details = mergeData(a, b)
        details = mergeData(details, d)
        return details

    elif d == "Empty" and b != "Empty" and a != "Empty" and c != "Empty":
        details = mergeData(b, a)
        details = mergeData(details, c)
        return details

    elif a == "Empty" and b == "Empty" and c != "Empty" and d != "Empty":
        details = mergeData(c, d)
        return details

    elif a == "Empty" and c == "Empty" and b != "Empty" and d != "Empty":
        details = mergeData(b, d)
        return details
        
    elif b == "Empty" and c == "Empty" and a != "Empty" and d != "Empty":
        details = mergeData(a, d)
        return details

    elif a == "Empty" and d == "Empty" and b != "Empty" and c != "Empty":
        details = mergeData(b, c)
        return details

    elif b == "Empty" and d == "Empty" and a != "Empty" and c != "Empty":
        details = mergeData(a, c)
        return details

    elif d == "Empty" and c == "Empty" and a != "Empty" and b != "Empty":
        details = mergeData(b, a)
        return details

    elif a == "Empty" and b == "Empty" and c == "Empty" and d != "Empty":
        details = d
        return details
    
    elif a == "Empty" and b == "Empty" and c != "Empty" and d == "Empty":
        details = c
        return details

    elif a == "Empty" and b != "Empty" and c == "Empty" and d == "Empty":
        details = b
        return details

    elif a != "Empty" and b == "Empty" and c == "Empty" and d == "Empty":
        details = a
        return details

    else:
        details = mergeData(a, b)
        details = mergeData(details, c)
        details = mergeData(details, d)
        return details

'''
def getDetails(a, b):
    data=[]
    if b == data:
        return a 
    else:
        for i in a:
            for j in b:
                if j == i:
                    data.append(j)
        return data
'''

def clientSearch(sck):

    date = sck.recv(1024).decode(FORMAT)
    sck.sendall(date.encode(FORMAT))

    brand = sck.recv(1024).decode(FORMAT)
    sck.sendall(brand.encode(FORMAT))

    type = sck.recv(1024).decode(FORMAT)
    sck.sendall(type.encode(FORMAT))

    place = sck.recv(1024).decode(FORMAT)
   
    if date == "Ngày" and brand == "Nhãn" and type == "Loại" and place == "Thành phố":
        msg = "Choose one"
        sck.sendall(msg.encode(FORMAT))
        return
    
    #if date == "Ngày" or (brand == "Nhãn" and type == "Loại" and place == "Thành phố"):
        #msg = "Day"
        #sck.sendall(msg.encode(FORMAT))
        #return

    else:
        dateData = searchDateData(date)
        brandData = searchBrandData(brand)
        typeData = searchTypeData(type)
        placeData = searchPlaceData(place)
       
        if dateData == None or brandData == None or typeData == None or placeData == None:
            msg = "No"
            sck.sendall(msg.encode(FORMAT))
            return
        
        else:
            #details = getDetails(dateData, brandData)
            #details = getDetails(details, typeData)
            #details = getDetails(details, placeData)
            details = getDetails(dateData, brandData, typeData, placeData)

            if details == None or len(details) == 0:
                msg = "No"
                sck.sendall(msg.encode(FORMAT))
                return
            else:
                msg = "Yes"
                sck.sendall(msg.encode(FORMAT))
                sck.recv(1024)
                #print(details)

                for row in details:
                    for data in row:
                        data = str(data)
                    
                        if data == "":
                            msg = "Rong"
                            sck.sendall(msg.encode(FORMAT))
                            sck.recv(1024)
                        else:
                            #print(data)
                            sck.sendall(data.encode(FORMAT))
                            sck.recv(1024)
                    msg = "next"
                    sck.sendall(msg.encode(FORMAT))
                    sck.recv(1024)

                msg = "endloop"
                sck.sendall(msg.encode(FORMAT))
   
     

def insertUser(username, password):
    cursor = connectToDB().cursor()
    cursor.execute(f"insert into {ACCOUNT_TABLE}(username,password) values(?,?);",(username,password))
    cursor.commit()


def connectToDB():
    conn = pyodbc.connect(f'DRIVER={DRIVER_NAME};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes')
    conn.autocommit = True
    return conn



def changeOnHover(button, colorOnHover, colorOnLeave): # Hàm thay đổi màu khi di chuột vào và ra khỏi button
    # adjusting backgroung of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover))

    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave))


def ask_exit(exit_button):
    check_quit=messagebox.askokcancel("Thoát", "Bạn chắc chắc muốn thoát chương trình ?")
    if check_quit==True:
        root.destroy()
        exit()
def exit_button():

    exit_button=Button(root, command=lambda: ask_exit(exit_button),text='Ấn để Thoát',activebackground='Light salmon',fg='black',font=('Arial',10))
    exit_button.place(x=146,y=533)
    changeOnHover(exit_button, 'DarkOliveGreen1','SystemButtonFace')

def server_main() : #Dùng Thread để kết nối các client khi Ip nhaapjd dúng
    global root
    root=tk.Tk() #Khởi tạo widget 
    root.geometry('500x650') 
    root.title("SERVER - Tỷ giá vàng Việt Nam")
    root.resizable(False,False)
    load = Image.open("server.jpg") # 4 dòng: lấy và hiển thị hình ảnh trong widget
    render = ImageTk.PhotoImage(load)
    img = Label(root, image=render)
    img.place(x=0, y=0)
   
    group1 = LabelFrame(root, text=" Đã Kết nối", padx=5, pady=5) # 2 dòng tạo Frame thứ 1
    group1.grid(row=1, column=0, columnspan=3, padx=15, pady=70, sticky=E + W + N + S)
    txtbox = scrolledtext.ScrolledText(group1, width=43, height=10) # 2 dòng tạo text box thứ 1 với thanh scroll bar
    txtbox.grid(row=1, column=0, sticky=E + W + N + S)
    txtbox.config(state='disabled')
    group2 = LabelFrame(root, text=" Dừng kết nối", padx=5, pady=5) # 2 dòng tạo Frame thứ 2
    group2.grid(row=2, column=0, columnspan=3, padx=15, pady=0, sticky=E + W + N + S)
    txtbox_2 = scrolledtext.ScrolledText(group2, width=43, height=10) # 2 dòng tạo text box thứ 2 với thanh scroll bar
    txtbox_2.grid(row=2, column=0, sticky=E + W + N + S)
    txtbox_2.config(state='disabled')

    def start_socket():
        global active_count
        global off_count
        global s

        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(ADDR)
        except Exception:
            traceback.print_exc()
            messagebox.showerror('Có lỗi xảy ra', 'Không thực hiện bind địa chỉ được')
            root.destroy()
            exit(1)

        s.listen(5)
        
        text_active_count = Label(root,text="Số kết nối\nhiện tại",bg='#def4ff',fg='black',font=('Arial',9))
        text_active_count.place(x=418,y=120)
        text_off_count = Label(root,text="Số kết nối\nđã dừng",bg='#def4ff',fg='black',font=('Arial',9))
        text_off_count.place(x=418,y=380)
        active_count = Label(root,text=len(active_clients),bg='#def4ff',fg='limegreen',font=('Arial',30))
        active_count.place(x=435,y=155)
        off_count = Label(root,text=len(off_clients),bg='#def4ff',fg='red',font=('Arial',30))
        off_count.place(x=435,y=415)

        def handleClient(conn: socket, addr):
            global active_count
            global off_count

            while True:
                try:
                    option = conn.recv(1024).decode(FORMAT)
                    if option == LOGIN:
                        Ad.append(str(addr))
                        serverLogin(conn)

                    elif option == SIGNUP:
                        serverSignup(conn, addr)

                    elif option == LOGOUT:
                        removeLiveAccount(addr)

                    elif option == SEARCH:
                        clientSearch(conn)
                    
                    elif option == STOP_CONNECTION:
                        break
                except:
                    break

            removeLiveAccount(addr)      #Tìm account của client có trong live account không, có thì xóa
            text_2 = "Đã dừng kết nối với"+str(addr)+"\n"
            txtbox_2.config(state="normal")
            txtbox_2.insert(tk.END,text_2) 
            txtbox_2.config(state='disabled')
            conn.close()
            active_clients.remove(conn)
            
            #active_number_digits = len(str(active_count))
            active_count.config(text=len(active_clients))

            off_clients.append(conn)
            #off_number_digits = len(str(off_count))
            off_count.config(text=len(off_clients))
            
        txtbox.config(state='normal')
        txtbox.insert(tk.END,"Chờ kết nối từ client...\n") #In trạng thái đang chờ
        txtbox.config(state='disabled')

        while True:
            conn,addr=s.accept()
            thread=threading.Thread(target=handleClient,args=(conn,addr))
            thread.daemon = True
            thread.start() 
            
            active_clients.append(conn)

            active_count.config(text=len(active_clients))

            text_1 = 'Đã kết nối với '+str(addr)+'\n'
            txtbox.config(state='normal')
            txtbox.insert(tk.END,text_1) # Thêm thông báo kết nối vào cuối của box trên
            txtbox.config(state='disabled')

    def start_thread_socket(): #Tạo thread khởi động socket ( phải tách ra thread riêng vì lồng vòng lặp với mainloop)
        start_button.config(state='disabled')
        changeOnHover(start_button,'SystemButtonFace','SystemButtonFace')
        thread_start_socket=threading.Thread(target=start_socket, daemon=True)
        thread_start_socket.start()
    def Create_start_socket_button():
        global start_button
        start_button = Button(root, command=start_thread_socket, text='Nhấn vào để khởi động', activebackground='Light salmon',fg='black', font=('Arial', 9))
        start_button.place(x=126, y=270)
        changeOnHover(start_button,'DarkOliveGreen1','SystemButtonFace')
    Create_start_socket_button()
    exit_button()
    def on_closing():
        check=messagebox.askokcancel("Thoát chương trình", " Bạn có chắc chắn muốn thoát? ")
        if check==True:
            root.destroy()
            exit()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

######SCRAPING FUNCTIONS

#Hàm cào dữ liệu từ API
def scraping(url, file_name):
    try:
        r = urlopen(url)                                    #Mở URL
        text = json.loads(r.read())                         #Load dạng json
        with open(file_name, 'w') as myFile:                #Mở file để thêm dữ liệu vào
            json.dump(text['golds'][0], myFile)             #Ghi dữ liệu vào file
    #Lỗi từ API
    except Exception:
        print(f'[SCRAPING ERROR]')
        traceback.print_exc()
        return False                                        #Nếu lấy dữ liệu không thành công
    
    return True                                             #Nếu lấy dữ liệu thành công

#Hàm chỉnh sửa tên file các ngày trước
def rename_list_file():
    #Xóa file 10 ngày trước (file data_10.json)
    os.remove(f"{PATH}{TYPE_NAME}10{FILE_TYPE}") 

    #Sửa tên file data_1 -> 9 thành data_2 -> 10
    for i in range(9, 0, -1):
        os.rename(f"{PATH}{TYPE_NAME}{i}{FILE_TYPE}", f"{PATH}{TYPE_NAME}{i+1}{FILE_TYPE}")

    #Sửa tên file chứa dữ liệu ngày hôm qua (data_today -> data_1)
    os.rename(f"{FILE_TODAY_NAME}", f"{PATH}{TYPE_NAME}1{FILE_TYPE}")

    #Sửa tên file chứa dữ liệu ngày hôm nay (data_today_temp -> data_today)
    os.rename(f"{FILE_TODAY_TEMP}", f"{FILE_TODAY_NAME}")                                

#Hàm trả về ngày cập nhật đầy đủ của dữ liệu API
def get_date(file_name):
    with open(file_name, 'r', encoding=FORMAT) as myFile:       #Mở file để đọc, encode tránh lỗi dấu tiếng Việt
        text = myFile.read().encode(FORMAT)                     #Đọc file, encode text đọc được tránh lỗi dâu
        data = json.loads(text)                                 #Load dạng json
        date = data['date']                                     #Truy cập vào mục date chứa ngày

    return date                                                

#Hàm khởi tạo các file data nếu các file này chưa được tạo
def check_create_files():
    if not os.path.isfile(FILE_TODAY_NAME):
        scraping(URL, FILE_TODAY_NAME)
    for i in range(1, 11):
        if not os.path.isfile(f'{PATH}{TYPE_NAME}{i}{FILE_TYPE}'):
            f = open(f"{PATH}{TYPE_NAME}{i}{FILE_TYPE}", 'w')
            f.close() 

#Hàm kết nối đến database
def connectDatabase():
    conn = pyodbc.connect(f'DRIVER={DRIVER_NAME};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes')
    conn.autocommit = True
    return conn

#Hàm đưa dữ liệu cập nhật gần nhất từ file json vào bảng trong database
def updateDataToday(file_name, conn):
    cur = conn.cursor()
    date = get_date(file_name)
    cur.execute(
        f"DELETE FROM {DATA_TABLE} WHERE day = {date}"
        "DECLARE @json_today nvarchar(max);"
        f"SELECT @json_today = BulkColumn FROM OPENROWSET (BULK '{file_name}', SINGLE_CLOB) import;"
        f"INSERT INTO {DATA_TABLE} SELECT * FROM OPENJSON (@json_today, '$.value')" 
        "WITH"
        "("
        "	[buy]		nvarchar(50),"
        "	[sell]		nvarchar(50),"
        "	[company]	nvarchar(50),"
        "	[brand]		nvarchar(50),"
        "	[updated]	nvarchar(50),"
        "	[brand1]	nvarchar(50),"
        "	[day]		nvarchar(50),"
        "	[id]		nvarchar(50),"
        "	[type]		nvarchar(50),"
        "	[code]		nvarchar(50)"
        ");" 
        f"DELETE FROM {DATA_TABLE} WHERE company = '1Coin';"
    )

#Hàm xóa dữ liệu cũ nhất trong database (của file data_10.json)
def deleteOldData(file_name, conn):
    cur = conn.cursor()
    date = get_date(file_name)
    cur.execute(f"DELETE FROM {DATA_TABLE} WHERE day = {date}")

#Hàm cập nhật dữ liệu bắt đầu từ thời gian start_time
def update_data(start_time):
    update_time = time.time()
    now = datetime.now()
    t = int(round(update_time - start_time) / 1800) + 1

    conn = connectDatabase()
    #Nếu lây dữ liệu thành công
    if scraping(URL, FILE_TODAY_TEMP):
        
        #Nếu ngày của file today vừa cập nhật khác ngày của file today trước đó
        if get_date(FILE_TODAY_TEMP) != get_date(FILE_TODAY_NAME):
            old_file_name = f'{PATH}{TYPE_NAME}10{FILE_TYPE}'

            #Nếu file 10 ngày trước (data_10.json) không rỗng
            if os.stat(old_file_name).st_size != 0:
                #Xóa dữ liệu 10 ngày trước trong bảng của database
                deleteOldData(old_file_name, conn)
            
            #Xóa file json 10 ngày trước (data_10.json) và chỉnh sửa tên các file data
            rename_list_file()
        
        #Nếu ngày của file today vừa cập nhật trùng ngày của file today trước đó
        else:

            #Chỉ thay thế file today trước đó (data_today.json) bằng file today vừa cập nhật (data_today_temp.json)
            #Không xóa các file dữ liệu cũ
            os.remove(f"{FILE_TODAY_NAME}")
            os.rename(f"{FILE_TODAY_TEMP}", f"{FILE_TODAY_NAME}")

        #Cập nhật dữ liệu vừa thay thế lên bảng trong database
        updateDataToday(FILE_TODAY_NAME, conn)
        print(f'[{now}] Đã cập nhật dữ liệu lần thứ {t}')

    #Nếu lấy dữ liệu không thành công
    else:
        print(f'[{now}] Lần thứ {t} không cập nhật được dữ liệu')

#Hàm cập nhật mỗi 30 phút
def update_data_every_30_minutes():
    start_time = time.time()
    update_data(start_time)
    next = time.time()

    schedule.every(1800).seconds.do(update_data, next)
    while True:
        schedule.run_pending()


#___________

t = threading.Thread(target=update_data_every_30_minutes,daemon=True)
t.start()
server_main()
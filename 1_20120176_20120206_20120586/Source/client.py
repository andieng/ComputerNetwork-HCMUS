import socket
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Scrollbar, messagebox
import numpy as np
from PIL import ImageTk,Image
from datetime import datetime,timedelta


#other
FORMAT = "utf8"

#connection
PORT = 8000

#options
LOGIN = "login"
SIGNUP = "signup"
LOGOUT = "logout"
SEARCH = "search"
STOP_CONNECTION = "stop"


def setup_socket(host):
    try:
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address=(host, PORT)
        client.connect(address)
    except:
        return False
    return True

def changeOnHover(button, colorOnHover, colorOnLeave): # Hàm thay đổi màu khi di chuột vào và ra khỏi button
            # adjusting backgroung of the widget
            # background on entering widget
            button.bind("<Enter>", func=lambda e: button.config(
                background=colorOnHover))

            # background color on leving widget
            button.bind("<Leave>", func=lambda e: button.config(
                background=colorOnLeave))

#GUI initialize
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        global client_input
        client_input=StringVar()
        self.geometry('800x600')
        self.title("Tỷ giá vàng Việt Nam")
        self.iconbitmap(r'favicon.ico')
        self.resizable(width=False, height=False)

        container = tk.Frame(self)

        container.pack(side="top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames ={}
        for f in (startPage, signinPage, homePage):
            frame = f(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[f] = frame

        self.frames[startPage].tkraise()
      
    def showPage(self, frameClass):
        self.frames[frameClass].tkraise()

    global wrong_IP_input
    wrong_IP_input = None
    def checkIp(self, curFrame):
        host_name = curFrame.clientInput.get() #Lấy địa chỉ đã nhập trong box 
        try:
            host = socket.gethostbyname(host_name)
        except:
            messagebox.showerror('Có lỗi xảy ra', 'Không tìm thấy server')
            Button(self,command=self.checkIp(), text=' Check IP',activebackground='light salmon',fg='black', font=('Arial', 11))

        else:
            socket_check = setup_socket(host)
            if socket_check == True:
                self.showPage(signinPage)
            else:
                messagebox.showerror('Có lỗi xảy ra', 'Không kết nối được với server')
                Button(self,command=self.checkIp(), text=' Check IP',activebackground='light salmon',fg='black', font=('Arial', 11))


    #close program
    def appClose(self):
        if messagebox.askokcancel("Thoát chương trình", " Bạn có chắc chắn muốn thoát? "):
            self.destroy()
            try:
                option = STOP_CONNECTION
                client.sendall(option.encode(FORMAT))
            except:
                pass
            finally:
                client.close()
    
    def logIn(self, curFrame, sck):
        try:
            #input username and password
            user = curFrame.sign_in_username.get()
            pwd = curFrame.sign_in_password.get()

            #check if all fields are filled
            if user == "" or pwd == "":
                messagebox.showerror('Có lỗi xảy ra', 'Cần điền đủ thông tin!')
                return

            #notice server
            option = LOGIN
            sck.sendall(option.encode(FORMAT))
            
            #send username and password 
            sck.sendall(user.encode(FORMAT))
            print("input: ", user)
            sck.recv(1024)

            sck.sendall(pwd.encode(FORMAT))
            print("input: ", pwd)

            #check if login is accepted
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: "+ accepted)

            if accepted == "1":
                self.showPage(homePage)
                
            elif accepted == "2":
                messagebox.showerror('Có lỗi xảy ra', 'Sai tên tài khoản hoặc mật khẩu')
            
            elif accepted == "0":
                messagebox.showerror('Có lỗi xảy ra', 'Tài khoản đã đăng nhập')

        except:
            messagebox.showerror('Có lỗi xảy ra', 'Server không phản hồi')
            print("Server không phản hồi")

    def stopConnection(self, sck):
        try:
            option = STOP_CONNECTION
            sck.sendall(option.encode(FORMAT))
            self.showPage(startPage)
        except:
            messagebox.showerror('Có lỗi xảy ra', 'Server không phản hồi')
            print("Server không phản hồi")
        finally:
            client.close()

    def logOut(self, curFrame, sck):
        try:
            option = LOGOUT
            sck.sendall(option.encode(FORMAT))
            self.showPage(signinPage)
            curFrame.labelWarning["text"] = ""
            curFrame.dropBoxDate.current(0)
            curFrame.dropBoxBrand.current(0)
            curFrame.dropBoxType.current(0)
            curFrame.dropBoxPlace.current(0)
            x = curFrame.myTree.get_children()
            for item in x:
                curFrame.myTree.delete(item)
        except:
            messagebox.showerror('Có lỗi xảy ra', 'Server không phản hồi')
            print("Server không phản hồi")
    

    def signUp(self, curFrame, sck):
        try:
            #input username and password
            user = curFrame.sign_up_username.get()
            pwd = curFrame.sign_up_password.get()

            #check if all fields are filled
            if user == "" or pwd == "":
                messagebox.showerror('Có lỗi xảy ra', 'Thiếu thông tin')
                return
            
            if (len(user) > 50 or len(pwd) > 50): # Nếu vượt quá bất kỳ chuỗi nào vượt quá 50 kí tự
                messagebox.showerror('Có lỗi xảy ra', 'Tối đa 50 kí tự!')
                return

            #notice server
            option = SIGNUP
            sck.sendall(option.encode(FORMAT))

            #send username and password to server
            sck.sendall(user.encode(FORMAT))
            print("input: ", user)

            sck.recv(1024).decode(FORMAT)
            sck.sendall(pwd.encode(FORMAT))
            print("input: ", pwd)

            #check if login is accepted
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: " + accepted)
            print(accepted)

            if accepted == "1":
                self.showPage(homePage)
            else:
                messagebox.showerror('Có lỗi xảy ra', 'Tên đăng ký đã tồn tại')

        except:
            messagebox.showerror('Có lỗi xảy ra', 'Server không phản hồi')
            print("404") 

class startPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        global client_input
        client_input=StringVar()
        #self.geometry('600x400')

        title=Label(self,fg='black', font=('Arial', 20))
        title.place(x=65,y=15)
        title.config(text='TRA CỨU TỈ GIÁ VÀNG VIỆT NAM ')
        load = Image.open("ipbg.jpg") # 4 dòng: lấy và hiển thị hình ảnh trong widget
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
        input_IP=Label(self,text='Nhập IP', bg='#e6ffe2', fg='black',font=('Arial',15))
        input_IP.place(x=250,y=250)
        #textbox_IP = Entry(self, textvariable=client_input, fg='black', font=('Arial', 11)) # Tạo box entry cho nhập địa chỉ IP
        self.clientInput = tk.Entry(self, fg='black', font=('Arial', 11))
        self.clientInput.place(x=350, y=255)

        button_ip=Button(self,command=lambda: appController.checkIp(self), text='Check IP',activebackground='light salmon',fg='black',font=('Arial',11))
        button_ip.place(x=350,y=315)
        self.changeOnHover(button_ip, 'DarkOliveGreen1', 'SystemButtonFace')

    def changeOnHover(self, button, colorOnHover, colorOnLeave): # Hàm thay đổi màu khi di chuột vào và ra khỏi button
        # adjusting backgroung of the widget
        # background on entering widget
        button.bind("<Enter>", func=lambda e: button.config(
            background=colorOnHover))

        # background color on leving widget
        button.bind("<Leave>", func=lambda e: button.config(
            background=colorOnLeave))

class signinPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#def4ff")

        sign_up_username=StringVar()

        imgBg = ImageTk.PhotoImage(Image.open("bg.png"))
        labelTitle = tk.Label(self,image=imgBg, bg="#def4ff")
        labelTitle.image = imgBg
        labelTitle.place(x = 46, y = 7)

        label_1= Label(self, text='Tên đăng ký', bg="#def4ff", fg='black',font=('Arial',12))
        label_1.place(x = 113, y = 375)
        self.sign_up_username = tk.Entry(self, textvariable=sign_up_username, fg='black', font=('Arial',11))
        self.sign_up_username.place(x=113,y=396)

        label_2= Label(self, text='Mật khẩu', bg="#def4ff", fg='black',font=('Arial',12))
        label_2.place(x = 113, y = 446)
        self.sign_up_password = tk.Entry(self, fg='black', font=('Arial',11),show='*')
        self.sign_up_password.place(x=113,y=469)
        #label_3= Label(self, text='Xác nhận mật khẩu', fg='black',font=('Arial',11))
        #label_3.grid(row=2, column=0, padx=5, pady=10)
        #self.sign_up_checkpassword = tk.Entry(self, fg='black', font=('Arial',11),show='*')
        #self.sign_up_checkpassword.place(x=150,y=98)

        label_6 = Label(self, text='            ', fg='black', font=('Arial', 11)) # Tạo label trống để ghi đè lên label báo hiệu đăng ký thành công hay không
        label_6.grid(row=5, column=0, padx=5, pady=10)

        label_4= Label(self, text='Tên đăng nhập', bg="#def4ff", fg='black',font=('Arial',12))
        label_4.place(x = 489, y = 82)
        self.sign_in_username = tk.Entry(self, fg='black', font=('Arial',11))
        self.sign_in_username.place(x=489,y=106)

        label_5= Label(self, text='Mật khẩu', bg="#def4ff", fg='black',font=('Arial',12))
        label_5.place(x = 489, y = 156)
        self.sign_in_password = tk.Entry(self, fg='black', font=('Arial',11), show='*')
        self.sign_in_password.place(x=489,y=179)

        imgSignup = ImageTk.PhotoImage(Image.open("signup.png"))
        button_1=Button(self, image=imgSignup, command=lambda: appController.signUp(self, client), bg="#def4ff", fg='black', font=('Arial',11))
        button_1.image = imgSignup
        button_1.place(x=129,y=535)
        #self.changeOnHover(button_1, 'LightGoldenrod1', 'SystemButtonFace')     

        imgSignin = ImageTk.PhotoImage(Image.open("signin.png"))
        button_2=Button(self, image=imgSignin, command=lambda: appController.logIn(self, client), bg="#def4ff", fg='black', font=('Arial',11))
        button_2.image = imgSignin
        button_2.place(x=506,y=263)
        #self.changeOnHover(button_2, 'LightGoldenrod1', 'SystemButtonFace')
        
        imgStop = ImageTk.PhotoImage(Image.open("stop.png"))
        stopButton = Button(self, image=imgStop,command=lambda: appController.stopConnection(client), bg="#def4ff")
        stopButton.image=imgStop
        stopButton.place(x=21,y=558)

    def changeOnHover(self, button, colorOnHover, colorOnLeave): # Hàm thay đổi màu khi di chuột vào và ra khỏi button
        # adjusting backgroung of the widget
        # background on entering widget
        button.bind("<Enter>", func=lambda e: button.config(
            background=colorOnHover))

        # background color on leving widget
        button.bind("<Leave>", func=lambda e: button.config(
            background=colorOnLeave))


class homePage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self,parent)
        self.configure(bg="#a8b7ff")

        imgBg = ImageTk.PhotoImage(Image.open("background.png"))
        labelTitle = tk.Label(self,image=imgBg, bg="#a8b7ff")
        labelTitle.image = imgBg
        labelTitle.place(x = 13.0, y = 0.0)

        now = datetime.now().date()
        self.dropBoxDate = ttk.Combobox(self, value=["Ngày",  f"{now - timedelta(10)}", f"{now - timedelta(9)}", f"{now - timedelta(8)}", f"{now - timedelta(7)}", f"{now - timedelta(6)}", f"{now - timedelta(5)}", f"{now - timedelta(4)}", f"{now - timedelta(3)}", f"{now - timedelta(2)}", f"{now - timedelta(1)}", f"{now}"], width=10, font="Verdana 12 bold")
        self.dropBoxDate.current(0)
        self.dropBoxDate.place(x = 64, y = 123)

        self.dropBoxBrand = ttk.Combobox(self, value=["Nhãn", "DOJI", "3BANKS", "2GROUP", "1OTHER"], width=10, font="Verdana 12 bold")
        self.dropBoxBrand.current(0)
        self.dropBoxBrand.place(x = 241, y = 123)

        self.dropBoxType = ttk.Combobox(self, value=["Loại", "SJC", "Nhẫn", "Nữ trang", "AVPL / DOJI", "Nguyên liệu", "Kim Ngưu", 'Kim Thần Tài', 'Lộc Phát Tài', "Kim Ngân Tài", "Hưng Thịnh Vượng"], width=10, font="Verdana 12 bold")
        self.dropBoxType.current(0)
        self.dropBoxType.place(x = 413, y = 123)

        self.dropBoxPlace = ttk.Combobox(self, value=["Thành phố", "Hà Nội", "Hồ Chí Minh"], width=10, font="Verdana 12 bold")
        self.dropBoxPlace.current(0)
        self.dropBoxPlace.place(x = 599, y = 123)

        imgSearch = ImageTk.PhotoImage(Image.open("searching.png"))
        buttonSearch = tk.Button(self, image=imgSearch, bg="#a8b7ff", command=self.searchData)
        buttonSearch.image = imgSearch
        buttonSearch.place(x = 326, y = 176)

        imgSignin = ImageTk.PhotoImage(Image.open("signin.png"))
        Button(self, image=imgSignin, command=lambda: appController.logIn(self, client), bg="#def4ff", fg='black', font=('Arial',11))


        imgLogout = ImageTk.PhotoImage(Image.open("logout.png"))
        global client
        #buttonLogout = tk.Button(self, image=imgLogout, bg="#a8b7ff", command=lambda: appController.showPage(signinPage))
        buttonLogout = tk.Button(self, image=imgLogout, bg="#a8b7ff", command=lambda:appController.logOut(self,client))
        buttonLogout.image = imgLogout
        buttonLogout.place(x = 383, y = 519)

        labelLogout = tk.Label(self, text="Log out", bg="#a8b7ff")
        labelLogout.config(font=("Courier", 15))
        labelLogout.place(x = 355, y = 556)

        self.labelWarning = tk.Label(self, text="", bg="#a8b7ff")
        self.labelWarning.config(font=("Courier", 15))
        self.labelWarning.place(x = 350, y = 480)

        #Treeview configure
        #Create treeview frame
        self.treeFrame = tk.Frame(self, bg="steelblue1")
        #Create treeview
        self.myTree = ttk.Treeview(self.treeFrame)
        
        columns = ('Date', 'Buy', 'Sell', 'Brand', 'Type', 'Place')
        self.myTree = ttk.Treeview(self, columns=columns, show='headings')

        self.myTree.column('Date', anchor=CENTER, stretch=NO, width=80)
        self.myTree.heading('Date', text='Ngày')

        self.myTree.column('Buy', anchor=CENTER, stretch=NO, width=80)
        self.myTree.heading('Buy', text='Bán')

        self.myTree.column('Sell', anchor=CENTER, stretch=NO, width=80)
        self.myTree.heading('Sell', text="Mua")

        self.myTree.column('Brand', anchor=CENTER, stretch=NO, width=80)
        self.myTree.heading('Brand', text="Nhãn")

        self.myTree.column('Type', anchor=CENTER, stretch=NO, width=80)
        self.myTree.heading('Type', text="Loại")

        self.myTree.column('Place', anchor=CENTER, stretch=NO, width=80)
        self.myTree.heading('Place',text="Thành phố")

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.myTree.yview)
        self.myTree.configure(yscroll=scrollbar.set)
        scrollbar.place(x = 647, y = 250, height = 225)

        self.myTree.place(x = 165, y = 250)
    
    def receivedData(self):
        row=[]
        details=[]
        data = ""

        while True:
            data = client.recv(1024).decode(FORMAT)
            
            if data[-7:] == "endloop":
                break  

            if data != "next":

                if data == "Rong":
                    client.sendall(data.encode(FORMAT))
                    data = ""

                row.append(data)
                details.append(row)
                #print(details)
                row=[]
                client.sendall(data.encode(FORMAT))
                #print("---")
            
            if data == "next":
                client.sendall(data.encode(FORMAT))
                #print("---")

            continue
                            
        #print("---")  
        return details

    def removeBrackets(self, a):
        s = str(a)
        s = s.replace("['", '')
        s = s.replace("']", '')
        return s

    #Change date format from yy-mm-dd to yymmdd
    def convertDate(self, date):
        if date == "Ngày":
            return date
        else:
            date = datetime.strptime(date, "%Y-%m-%d").strftime('%Y%m%d')
            return date

    def searchData(self):
        
            try:
                self.labelWarning["text"] = ""
                date = self.convertDate(self.dropBoxDate.get())
                brand = self.dropBoxBrand.get()
                type = self.dropBoxType.get()
                place = self.dropBoxPlace.get()
                option = SEARCH

                tmp=[]

                client.sendall(option.encode(FORMAT))
                self.treeFrame.pack_forget()

                client.sendall(date.encode(FORMAT))
                client.recv(1024)
                
                client.sendall(brand.encode(FORMAT))
                client.recv(1024)

                client.sendall(type.encode(FORMAT))
                client.recv(1024)

                client.sendall(place.encode(FORMAT))
                
                msg = client.recv(1024).decode(FORMAT)
                client.sendall(msg.encode(FORMAT))

                if (msg == "No"):
                    x = self.myTree.get_children()
                    for item in x:
                        self.myTree.delete(item)
                    self.labelWarning["text"] = "Not found"
                    self.labelWarning.place(x = 344, y = 480)
                    return

                if (msg == "Choose one"):
                    self.labelWarning["text"] = "Choose one"
                    self.labelWarning.place(x = 336, y = 480)
                    return
                
                else:
                    x = self.myTree.get_children()
                    for item in x:
                        self.myTree.delete(item)

                    tmp = self.receivedData()

                    n = len(tmp)

                    if n == 0 :
                        self.labelWarning["text"] = "Not found"
                        self.labelWarning.place(x = 350, y = 480)
                    else:
                        if n > 1:
                            details = np.array_split(tmp, (n)/10)
                        else:
                            details = tmp
                        
                        details = np.unique(details, axis = 0)
                        m = len(details)

                        #print("___details____")
                        #for i in details:
                            #print(i)

                        for i in range(m):
                            
                            tmpD = self.removeBrackets(details[i][6])
                            tmpD = datetime.strptime(tmpD, "%Y%m%d").strftime('%d/%m/%Y')
                            tmpB = self.removeBrackets(details[i][0])
                            tmpS = self.removeBrackets(details[i][1])
                            tmpBr = self.removeBrackets(details[i][2])
                            tmpT = self.removeBrackets(details[i][8])
                            tmpP = self.removeBrackets(details[i][3])
            
                            self.myTree.insert('', 'end',text="",values=(tmpD, tmpB, tmpS, tmpBr, tmpT, tmpP))
                
            except:
                messagebox.showerror('Có lỗi xảy ra', 'Server không phản hồi')
                print("Server không phản hồi")




#__________
app = App()
app.protocol("WM_DELETE_WINDOW", app.appClose)
app.mainloop()

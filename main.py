############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2
import os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import json

import pyodbc
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

with open("config.json") as config:
    data = json.load(config)

mssql = data["mssql"]

server = mssql["server"]
database = mssql["database"]
username = mssql["username"]
password = mssql["password"]

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                      server+';DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = cnxn.cursor()

cursor.execute("""if not exists (select * from sysobjects where name='Students' and xtype='U')
   CREATE TABLE Students
	(
		Id int identity(1,1),
		UserId int,
		[Name] nvarchar(500),
		[Date] nvarchar(100)
	);""")
print("create table successfully")

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################


def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

###################################################################################


def contact():
    mess._show(title='Contact us',
               message="Please contact us on : 'shubhamkumar8180323@gmail.com' ")

###################################################################################


def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='M???t s??? file y??u c???u b??? l???i, vui l??ng ki???m tra',
                   message='Vui l??ng li??n h??? ????? ???????c h??? tr???')
        window.destroy()

###################################################################################


def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('M???t kh???u c?? kh??ng ???????c ????? tr???ng',
                                'Vui l??ng nh???p m???t kh???u m???i', show='*')
        if new_pas == None:
            mess._show(title='Kh??ng c?? m???t kh???u n??o ???????c nh???p',
                       message='Vui l??ng th??? l???i')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='?????i m???t kh???u',
                       message='?????i th??nh c??ng!!')
            return
    op = (old.get())
    newp = (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='L???i', message='Nh???p l???i m???t kh???u!!!')
            return
    else:
        mess._show(title='Wrong Password',
                   message='M???t kh???u c?? sai.')
        return
    mess._show(title='Password Changed',
               message='?????i th??nh c??ng!!')
    master.destroy()

###################################################################################


def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master, text='    Nh???p m???t kh???u m???i',
                    bg='white', font=('times', 12, ' bold '))
    lbl4.place(x=10, y=10)
    global old
    old = tk.Entry(master, width=25, fg="black", relief='solid',
                   font=('times', 12, ' bold '), show='*')
    old.place(x=180, y=10)
    lbl5 = tk.Label(master, text='   Nh???p m???t kh???u m???i',
                    bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black", relief='solid',
                   font=('times', 12, ' bold '), show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Nh???p l???i m???t kh???u m???i',
                    bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',
                    font=('times', 12, ' bold '), show='*')
    nnew.place(x=180, y=80)
    cancel = tk.Button(master, text="Cancel", command=master.destroy, fg="black", bg="red",
                       height=1, width=25, activebackground="white", font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48",
                      height=1, width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################


def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Kh??ng t??m th???y m???t kh???u c??',
                                'Vui l??ng nh???p l???i m???t kh???u c??', show='*')
        if new_pas == None:
            mess._show(title='Kh??ng c?? m???t kh???u n??o ???????c nh???p',
                       message='M???t kh???u m???i tr???ng')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered',
                       message='C???p nh???t m???t kh???u m???i th??nh c??ng!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Sai m???t kh???u',
                   message='B???n ???? nh???p sai m???t kh???u')

######################################################################################


def clear():
    txt.delete(0, 'end')
    res = "Xin ch???p ???nh tr?????c khi ??i???m danh n???u b???n ch??a ch???p tr?????c ????y"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Ch???p ???nh  >>>  2)L??u th??ng tin"
    message1.configure(text=res)

#######################################################################################


def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

########################################################################################


def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='Ch??a c?? ai ????ng k??',
                   message='Vui l??ng ????ng k?? tr?????c khi ??i???m danh!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "L??u th??ng tin th??nh c??ng"
    message1.configure(text=res)
    message.configure(text='T???ng s??? ???? ????ng k??: ' + str(ID[0]))

# 3


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################


def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing',
                   message='Nh???n L??u th??ng tin ????? ?????t l???i!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing',
                   message='Th??ng tin ch??a ?????')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date),
                                  '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('??i???m danh', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
        print(attendance[0], attendance[2], attendance[4] + attendance[6])
        cursor.execute("""
            INSERT INTO Students (UserId, Name, Date)
            VALUES (?,?,?)""", attendance[0], str(attendance[2]), str(attendance[4]) + ' ' + str(attendance[6]))
        cnxn.commit()
        print("insert success")
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
        cursor.execute("""
            INSERT INTO Students (UserId, Name, Date) 
            VALUES (?,?,?)""",attendance[0], str(attendance[2]), str(attendance[4]) + ' ' + str(attendance[6]))

        cnxn.commit()
        print("insert success")
        print(attendance[0], attendance[2], attendance[4] + attendance[6])
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(
                        str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year = date.split("-")

mont ={'01':'January',
      '02': 'February',
      '03': 'March',
      '04': 'April',
      '05': 'May',
      '06': 'June',
      '07': 'July',
      '08': 'August',
      '09': 'September',
      '10': 'October',
      '11': 'November',
      '12': 'December'
      }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True, False)
window.title("Attendance System")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="#00aeff")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#00aeff")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="H??? th???ng ??i???m danh b???ng nh???n di???n khu??n m???t" , fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="orange", bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both', expand=1)
tick()

head2 = tk.Label(frame2, text="                       T???o m???i th??ng tin                       ", fg="black", bg="#3ece48" ,font=('times', 17, ' bold ') )
head2.grid(row=0, column=0)

head1 = tk.Label(frame1, text="                       ???? ????ng k??                       ", fg="black", bg="#3ece48" ,font=('times', 17, ' bold ') )
head1.place(x=0, y=0)

lbl = tk.Label(frame2, text="ID", width=20  ,height=1  ,fg="black"  ,bg="#00aeff" ,font=('times', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame2, width=32 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="H??? v?? t??n", width=20  ,fg="black"  ,bg="#00aeff" ,font=('times', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2, width=32 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="Vui l??ng ch???p ???nh tr?????c khi ??i???m danh" , bg="#00aeff" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" , bg="#00aeff" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="??i???m danh", width=20  ,fg="black"  ,bg="#00aeff"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

res = 0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='T???ng s??? h???c sinh : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window, relief='ridge')
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='?????i m???t kh???u', command= change_pass)
filemenu.add_command(label='Li??n h???', command= contact)
filemenu.add_command(label='Tho??t', command = window.destroy)
menubar.add_cascade(label='Help', font=('times', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

tv = ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0', width=82)
tv.column('name', width=130)
tv.column('date', width=133)
tv.column('time', width=133)
tv.grid(row=2, column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0', text ='ID')
tv.heading('name', text ='T??n')
tv.heading('date', text ='Ng??y')
tv.heading('time', text ='Gi???')

###################### SCROLLBAR ################################

scroll = ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2, column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="X??a", command=clear  , fg="black"  ,bg="#ea2a2a"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="X??a", command=clear2  , fg="black"  ,bg="#ea2a2a"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=335, y=172)
takeImg = tk.Button(frame2, text="Ch???p ???nh", command=TakeImages  , fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame2, text="L??u ???nh", command=psw , fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="??i???m danh", command=TrackImages  , fg="black"  ,bg="yellow"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30, y=50)
quitWindow = tk.Button(frame1, text="Tho??t", command=window.destroy  , fg="black"  ,bg="red"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################

import tkinter as tk
from tkinter import font as tkfont
#import cv2 as cv
#import serial
#from pyzbar.pyzbar import decode
from audioop import add
from optparse import Option
from tkinter import *


#self == refers to the template to call itself (object)
#


# #class PiController():
#     #def __init__(self, Hui):
#         self.HUI = Hui
#         self.listening = False
#         self.debug = True
#         self.startMarker = '<'
#         self.endMarker = '>'
#         self.dataStarted = False
#         self.dataBuf = ""
#         self.messageComplete = False
#         self.vid = cv.VideoCapture(0)
#         self.serialPort = None
#         self.parse_file()
    
#     def parse_file(self):
#         self.setupSerial("9600","/dev/ttyACM0")
        
#     def setupSerial(self, baudRate, serialPortName):
#         self.serialPort = serial.Serial(port= serialPortName, baudrate = baudRate, timeout=0, rtscts=True)

#         print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))
#         self.waitForArduino()

#     def sendToArduino(self, stringToSend):
#         stringWithMarkers = (self.startMarker)
#         stringWithMarkers += stringToSend
#         stringWithMarkers += (self.endMarker)

#         self.serialPort.write(stringWithMarkers.encode('utf-8')) # encode needed for Python3
       
#     def recvLikeArduino(self):
#         if self.serialPort.inWaiting() > 0 and self.messageComplete == False or self.listening is True:
#             x = self.serialPort.read().decode("utf-8") # decode needed for Python3
        
#             if self.dataStarted == True:
#                 if x != self.endMarker:
#                     self.dataBuf = self.dataBuf + x
#                 else:
#                     self.dataStarted = False
#                     self.messageComplete = True
#             elif x == self.startMarker:
#                 self.dataBuf = ''
#                 self.dataStarted = True
    
#         if (self.messageComplete == True):
#             self.messageComplete = False
#             return self.dataBuf
#         else:
#             return "XXX" 

#     def waitForArduino(self):
#         print("Waiting for Arduino to reset")
     
#         msg = ""
#         while msg.find("Arduino is ready") == -1:
#             msg = self.recvLikeArduino()
#             if not (msg == 'XXX'): 
#                 print(msg)

#     def read_qr(self, frame):
#         value = decode(frame)
#         if len(value) == 0:
#             return None

#         return value[0].data.decode("utf-8") 

#     def scan_input(self):
#         if self.debug:
#             print("Camera On")
#         while True:
#             self.HUI.update()
#             ret, frame = self.vid.read()
#             if ret == True:
#                 qr_value = self.read_qr(frame)

#             if qr_value is None: continue
#             else: return qr_value

#     def speak(self, qr_value):
#         self.sendToArduino(qr_value)

#     def listen(self):
#         while True:
#             arduinoReply = self.recvLikeArduino()
#             if not (arduinoReply == 'XXX'):
#                 return arduinoReply
#             self.HUI.update()
        

class HuiController(tk.Tk):
     def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.tmp = None

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #Intro Page 
        self.frames['start'] = start(parent=self.container, controller=self)
        self.frames['start'].grid(row=0, column= 0, sticky= "nsew")
        #Manual Entry page
        self.frames['manual'] = manual(parent=self.container, controller=self)
        self.frames['manual'].grid(row=0, column= 0, sticky= "nsew")

    #Show a frame for the given page name
     def show_frame(self, page_name, data = None):
        if page_name == 'choice':
            self.create_choice(page_name, data)
            frame = self.frames[page_name]
            frame.tkraise()
        else:
            frame = self.frames[page_name]
            frame.tkraise()


     def create_choice(self, page_name, data):
        self.frames[page_name] = choice(parent=self.container, controller=self, data=data)
        self.frames[page_name].grid(row=0, column= 0, sticky= "nsew")

     def give_bool(self, val):
        self.tmp = val

class manual(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg= "#d459de") # Pink background
        self.controller = controller

        #************OPTION ONE*******************
        optionsOne = [
            'hop1',
            'hop2',
            'hop3',
            'hop4',
            'hop5',
            'hop6',
            'hop7',
            'hop8',
            'hop9',
            'hop10'
        ]
        userSelect = StringVar()
        userSelect.set(optionsOne[0])

        drop = OptionMenu(self, userSelect, *optionsOne)
        drop.grid(row = 1, column = 1)

        #for amount of pills
        amount = Spinbox(self, from_ = 0, to = 30)
        amount.grid(row = 1, column = 10, columnspan = 1)



        # label = tk.Label (self, text= "Please Scan QR", width= 20, height= 5, font= ("Comic Sans Ms",50), bg= "#d459de")    
        # controller.attributes('-fullscreen', True)
        # label.pack(side="top", fill= "x", pady=10)   
        # choice_button = tk.Button(self, text= "Correct Information", font= ("Copper Black", 20), fg= "green",
        # command= lambda: controller.show_frame("choice", "bofa,balls,12345"))
        # choice_button.pack(side= "bottom", fill= "x", pady=5) 

#Startup Page :: Main
class start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg= "#d459de") #Pink Background
        
        #to select button
        self.controller = controller
        label = tk.Label (self, text= "Scan QR Code Below: ", width= 20, height= 5, font= ("Comic Sans Ms",50), bg= "#d459de")    
        controller.attributes('-fullscreen', True)
        label.pack(side="top", fill= "x", pady=10)   
        choice_button = tk.Button(self, text= "Testing Page", font= (20), fg= "black",
        command= lambda: controller.show_frame("manual", "bofa,balls,12345"))
        choice_button.pack(side= "bottom", fill= "x", pady=5) 

#Yes and No Check
class choice(tk.Frame):
     def __init__(self, parent, controller, data):
        tk.Frame.__init__(self, parent, bg= "#d459de")
        self.controller = controller
        

        #*********Output Green and Red Clicking Symbols*************

        #Main Intro Question that will Output onto screen after barcode is scanned
        introQuestion = Label(self, text = "Hello (last, first), #ORDERNUMBER :")
        #Indicating where location is on grid(aesthetic purposes)
        introQuestion.grid(row=1, column=1)

        introQuestionTwo = Label(self, text = "Proceed to Fill?")
        introQuestionTwo.grid(row=1, column=2)

        #defining function of Green Button
        def greenButton():
            greenLabel = Label(self, text = "Proceeding to Fill...")
            greenLabel.grid(row=4, column=1)

        greenButton = Button(self, text = "YES", command=greenButton, font = ('Oswald', 20) , fg  ='#FEC923')
        controller.attributes('-fullscreen', True)
        greenButton.grid(row=3, column=3)


        #defining function of Red Button
        def redButton():
            redLabel = Label(self, text = "Order Cancelled" )
            redLabel.grid(row=4, column=1)

        redButton = Button(self, text = "NO", command=redButton, font = ('Oswald', 20), fg ='#592A8A')
        redButton.grid(row=3, column=2)

        # label1 = tk.Label(self, text= f"{data[2]}", bg= "#d459de", font= ("Calibri",50), height= 1)
        # label1.pack(side= "top", fill= "x", pady=5)
        # Label2 = tk.Label(self, text= f"{data[1]} {data[0]}",bg= "#d459de", font= ("Calibri", 50), height= 1)
        # Label2.pack(side= "top", fill= "x", pady=5)
        # button1 = tk.Button(self, text= "Correct Information", font= ("Copper Black", 20), fg= "green",
        # command= lambda: controller.give_bool(True))
        # button1.pack(side= "bottom", fill= "x", pady=5)
        # button2 = tk.Button(self, text= "Incorrect Information", font= ("Copper Black", 20), fg= "red",
        # command= lambda: controller.give_bool(False))
        # button2.pack(side= "bottom", fill= "x", pady=5)
        # button3 = tk.Button(self, text= "Manual Entry Mode", font=("lato",20),
        # command= lambda: controller.show_frame("mm"))
        # button3.pack(side= "bottom", fill= "x", pady=5)

#when user chooses yes
class yes(tk.Tk):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

#when user chooses no?  
class mm(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg= "#d459de")
        self.controller = controller
        #label1 = tk.Label


hui = HuiController()
hui.show_frame("start")
hui.mainloop()
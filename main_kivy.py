from tkinter.constants import COMMAND
from typing import Text
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, ThreeLineListItem, ThreeLineAvatarListItem, OneLineListItem, OneLineIconListItem
from kivymd.uix.list import IconLeftWidget,ImageLeftWidget
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton, MDRectangleFlatButton, MDIconButton
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField,MDTextFieldRect
import pandas as pd
from kivy.lang import Builder
from kivymd.toast import toast
import cv2
from kivymd.utils import asynckivy
import numpy as np
import face_recognition
import os
from datetime import datetime
from tkinter import *
from tkinter import messagebox

from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from playsound import playsound
from gtts import gTTS


Window.size = (800,400)
Window.title = "Smart Attendance System Using Face Recognition"



newScreen = """
ScreenManager:
   
    MenuScreen:
    ProfileScreen:
    Gallery:
<MenuScreen>:
    name : 'menu'
    BoxLayout:
        orientation : 'vertical'
        MDToolbar:
            left_action_items:[["face-recognition"]]
            title : 'Smart Attendance System using Face Recognition'
        MDLabel:
            text:""
            halign : 'center'
        Image:
            source  : "C:/Desktop/Face_Attend/fr123.png"
            pos_hint: {'center_x':0.7,'center_y':0.2}
            size_hint_x : 12
            height : "20dp"
            width : "80dp"
            size_hint_y : 12
    

    
        
    MDRectangleFlatIconButton:
        icon : 'account-supervisor-outline'
        text:'Add a New Profile'
         
        
        pos_hint:{'center_x':0.2 , 'center_y':0.7}
        on_press : 
            root.manager.current = 'Profile'
            root.manager.transition.direction = 'left'
    MDFloatingActionButton:
        icon :"microsoft-excel"
        pos_hint : {'center_x':0.1,'center_y':0.1}
        on_release : app.op()
        
    MDRectangleFlatIconButton:
        icon : 'calendar-alert'
        text:'Take Attendance ' 
        
        pos_hint:{'center_x':0.2 , 'center_y':0.5}
        on_press : app.att(self)
    MDRectangleFlatIconButton:
        icon : 'cancel'
        text:'Quit' 
        
        pos_hint:{'center_x':0.2 , 'center_y':0.1}
        on_press : 
            root.manager.transition.direction = 'right'
            root.manager.current = 'Profile'
    MDRectangleFlatIconButton:
        icon : 'group'
        text:'See Peoples' 
        
        pos_hint:{'center_x':0.2 , 'center_y':0.3}
        on_press :
            root.manager.transition.direction = 'right'
            root.manager.current = 'Gall'
        
    
        







<ProfileScreen>:
    name : 'Profile'
    
    MDTextField:
        mode: "rectangle"
        fill_color: 0, 0, 0, .4
        id : naam
        hint_text : 'Enter your Name' 
        pos_hint:{'center_x':0.7 , 'center_y':0.7}
        size_hint_x:None
        width : 180
    MDTextField:
        id : rollno
        
        mode: "rectangle"
        fill_color: 0, 0, 0, .4
        hint_text : 'Please enter your roll no'
        pos_hint:{'center_x':0.7 , 'center_y':0.5}
        size_hint_x:None
        width : 180
    MDRectangleFlatIconButton:
    
        icon : "camera"
        text : 'Capture'
        
        pos_hint:{'center_x':0.8 , 'center_y':0.3}
        on_press : app.click(self)

    MDRectangleFlatIconButton:
        icon : "arrow-left-thick"
        text : 'Back'
        pos_hint:{'center_x':0.6, 'center_y':0.3}
        on_release : 
            root.manager.current = 'menu'
            root.manager.transition.direction = 'right'
    BoxLayout:
        orientation : 'vertical'


        MDToolbar:
            
            title:'Add a new Profile'
            left_action_items : [["human-male-girl"]]
    
        MDLabel:
            text : ''
            halign : 'center'
        Image :
            source : "adduser.png"
            pos_hint: {'center_x':0.3,'center_y':0.2}
            size_hint : (3,3)
            
 
 
        
<Gallery>
    name:'Gall'
    MDScrollViewRefreshLayout:
        BoxLayout:
            ScrollView:
                MDList:
                    id:con   
                    ImageLeftWidget:
                        id : im
                     
    MDFloatingActionButton:
        icon:'arrow-left-thick'
        on_press:root.manager.current = 'menu'
            
                    
            
            
            
   
    
        


    
    
    



"""


class MenuScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass
class Gallery(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MenuScreen(name  = 'menu'))
sm.add_widget(ProfileScreen(name  = 'Profile'))
sm.add_widget(Gallery(name = 'Gall'))


class DemoApp(MDApp):
    title = "Smart Attendance System using Face Recognition"
    #this is for opening the excel sheet

    def op(self):
        file_loc = "C:\Desktop\Face_Attend\output.csv"
        os.system('"%s"' % file_loc)











    # this for ScreenShot

    def click(self,obj):
        hello=self.root.get_screen('Profile').ids.naam.text

        roll = self.root.get_screen('Profile').ids.rollno.text
        cam = cv2.VideoCapture(0)
        # cv2.namedWindow("MHSSP Smart Attendance System")
        img_c = 0
        while True:

            ret, frame = cam.read()
            # cv2.imshow("Frame",frame)
            if not ret:
                print("Faolded")
            cv2.imshow("Registration Window", frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
            elif key % 256 == 32:
                img_res = str(hello) + "_" + str(roll) + ".jpg"
                cv2.resize(frame,(250,200))
                cv2.imwrite("./ImagesBasic/" + img_res, frame)
                self.dlog = MDDialog(title="Profile Save",text="You have been registered as : "+ hello,size_hint=(0.7,1),buttons=[
                    MDFlatButton(text="Cancel",on_release=self.cl)
                ])
                self.soundplayer()
                self.dlog.open()

                img_c += 1
        cam.release()

    #This close fun for Dialog

    def cl(self,obj):
        self.dlog.dismiss()



    def soundplayer(self):
        username1 = self.root.get_screen('Profile').ids.naam.text
        username2 = self.root.get_screen('Profile').ids.rollno.text
        audio = gTTS("Appka Registeration safal hoa  " + username1,lang='hi')
        AudioSave = str(username1) + ".mp3"

        audio.save(AudioSave)

        playsound(AudioSave)
        os.remove(AudioSave)

    def att(self,obj):

        path = 'ImagesBasic'
        images = []
        className = []
        myList = os.listdir(path)
        print(myList)

        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            className.append(os.path.splitext(cl)[0])

        print(className)


        def findencodings(images):
            encodelist = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodelist.append(encode)

            return encodelist

        def markattend(name):
            with open('Attendance.csv', 'r+') as f:
                mydataList = f.readline()
                namelist = []


                for line in mydataList:
                    entry = line.split(',')
                    namelist.append(entry[0])
                if name not in namelist:
                    now = datetime.now()
                    dateString = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{name},{dateString}')
                    data = pd.read_csv("Attendance.csv")
                    data.drop_duplicates(subset="Name", keep="first", inplace=True)
                    df = data
                    df.to_csv("New_Att.csv")
        toast("Attendance has been recorded Successfully")
        encodelistknown = findencodings(images)
        print("Encoding Completed!!!")

        def Sounder(name):
            date_string = datetime.now().strftime("%d%m%Y%H%M%S")

            audio = gTTS(text=name,lang="en")
            AudioSave = "voice" + date_string + ".mp3"
            audio.save(AudioSave)

            playsound(AudioSave)
            os.remove(AudioSave)

        cap = cv2.VideoCapture(0)
        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            faceCur = face_recognition.face_locations(imgS)
            encodeCur = face_recognition.face_encodings(imgS, faceCur)

            for encodeFace, faceloc in zip(encodeCur, faceCur):
                matches = face_recognition.compare_faces(encodelistknown, encodeFace)
                faceDis = face_recognition.face_distance(encodelistknown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = className[matchIndex].upper()
                    # print(name)
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markattend(name)


                else:
                    name = className[matchIndex].upper()
                    # print(name)
                    unknown = "UNKNOWN"
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255,0,0), cv2.FILLED)
                    cv2.putText(img, unknown, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    Sounder(unknown)
            cv2.imshow('webcam', img)
            k = cv2.waitKey(1)
            if k == ord("q"):
                break

    # this is for main Screen
    def build(self):
        #scrn = Screen()
        # theme the color
        self.screen = Builder.load_string(newScreen)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"


        # label

        #l1 = MDLabel(text="ML Based Smart Attendance System ", halign="auto", theme_text_color="Custom",
                    # text_color=(0, 0, 1, 1), font_style="H5", pos_hint={'center_x': 0.7, 'center_y': 0.9})
        #scrn.add_widget(l1)

        #self.Name = MDTextField(text="Enter the Name", pos_hint={'center_x': 0.3, 'center_y': 0.5}, size_hint_x=None,
                           #width=180)
        #scrn.add_widget(self.Name)
        #self.Id = MDTextField(text="Enter your Roll No ", pos_hint={'center_x': 0.6, 'center_y': 0.5}, size_hint_x=None,
                  #       width=180)
        #scrn.add_widget(self.Id)

       # self.Attendance = MDRectangleFlatButton(text="Take Attendance", pos_hint={'center_x': 0.3, 'center_y': 0.3}
                                                #,on_release=self.att)
        #scrn.add_widget(self.Attendance)
        #self.ScreenShot = MDRectangleFlatButton(text="Save My Profile", pos_hint={'center_x': 0.7, 'center_y': 0.3}
                                                #,on_release=self.click)
        #scrn.add_widget(self.ScreenShot)

        return self.screen


    def on_start(self):
        path = "ImagesBasic"

        myList = os.listdir(path)
        # print(myList)


        for images in os.listdir(path):
            joined = os.path.join(path, images)

            #print(image)
            items = self.screen.get_screen('Gall').ids.con.add_widget(
            ThreeLineAvatarListItem(text=f'{images}'))

            ima = self.screen.get_screen('Gall').ids.im.add_widget(
                ImageLeftWidget(source="facebook.png")
            )


DemoApp().run()
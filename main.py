from tkinter import *
from PIL import ImageTk, Image
from datetime import datetime
import pygame
import sqlite3
import gc
import random
import copy
from threading import Timer


pygame.init()
pygame.mixer.music.load("RUDE - Eternal Youth.mp3")
pygame.mixer.music.play(loops=-1)
volumeLevels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
initialVolumeIndex = 4
pygame.mixer.music.set_volume(volumeLevels[initialVolumeIndex])

userLoggedIn = False
username = ''
userRole = ''

class Root(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Knowledge Quiz")
        self.geometry("950x650+200+10")
        self.iconbitmap('pictures/brainlogo.ico')
        self.resizable(0, 0)
        # Setup Frame
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.pageList = [MainMenu, Settings, LogIn, GameMode, Category, CategorySuggest]

        for F in self.pageList:
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)


    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()



class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.backgroundImage = ImageTk.PhotoImage(Image.open("pictures/backgroundMainMenu.jpg"))
        self.backgroundLabel = Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.imgBtn = PhotoImage(file = "pictures/btnMenu.png")
        self.imgBtnPress = PhotoImage(file = "pictures/btnMenuDark.png")
        self.imgBtnSmall = PhotoImage(file = "pictures/btnMenuSmall.png")
        self.imgBtnSmallDark = PhotoImage(file = "pictures/btnMenuSmallDark.png")

        self.btnPlay = Button(self, compound=CENTER, text="PLAY", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="#68a302",
                              bg="#fee2ca", activebackground="#fee2cd", activeforeground="#68a302", command=lambda: controller.show_frame(GameMode))  # 7eba00
        self.btnPlay.bind("<Enter>", lambda event: self.btnPlay.configure(image = self.imgBtnPress))
        self.btnPlay.bind("<Leave>", lambda event: self.btnPlay.configure(image=self.imgBtn))
        self.btnPlay.pack(pady=(210, 15), padx=30)

        self.btnTopScore = Button(self, compound=CENTER, text="TOP SCORE", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="#6f54b8",
                                  bg="#fee2cd", activebackground="#fee2cd", activeforeground="#6f54b8", command=self.createTopScore)
        self.btnTopScore.bind("<Enter>", lambda event: self.btnTopScore.configure(image = self.imgBtnPress))
        self.btnTopScore.bind("<Leave>", lambda event: self.btnTopScore.configure(image=self.imgBtn))
        self.btnTopScore.pack(pady=(0, 15), padx=30)

        self.btnLogIn = Button(self, compound=CENTER, text="LOGIN", font=("Rokkitt", 18, "bold"),
                                  image=self.imgBtn, borderwidth=0, fg="#c49000",
                                  bg="#fde2cf", activebackground="#fee1cf", activeforeground="#c49000",
                                  command=self.createLogIn)
        self.btnLogIn.bind("<Enter>", lambda event: self.btnLogIn.configure(image=self.imgBtnPress))
        self.btnLogIn.bind("<Leave>", lambda event: self.btnLogIn.configure(image=self.imgBtn))
        self.btnLogIn.pack(pady=(0, 15), padx=30)

        self.btnSettings = Button(self, compound=CENTER, text="SETTINGS", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="#01728f",
                                  bg="#fee1cf", activebackground="#fee1cf", activeforeground="#01728f", command=lambda: controller.show_frame(Settings))
        self.btnSettings.bind("<Enter>", lambda event: self.btnSettings.configure(image = self.imgBtnPress))
        self.btnSettings.bind("<Leave>", lambda event: self.btnSettings.configure(image = self.imgBtn))
        self.btnSettings.pack(pady=(0, 15), padx=30)

        self.btnExit = Button(self, compound=CENTER, text="EXIT", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="red",
                              bg="#fee2d4", activebackground="#fee2d4", activeforeground="red", command=self.quit)
        self.btnExit.bind("<Enter>", lambda event: self.btnExit.configure(image = self.imgBtnPress))
        self.btnExit.bind("<Leave>", lambda event: self.btnExit.configure(image = self.imgBtn))
        self.btnExit.pack(pady=(0, 15), padx=30)

    def createTopScore(self):
        frame = TopScore(app.container, app)
        app.frames[TopScore] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        app.show_frame(TopScore)

    def createStatistics(self):
        frame = Statistics(app.container, app)
        app.frames[Statistics] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        app.show_frame(Statistics)

    def createLogIn(self):
        frame = LogIn(app.container, app)
        app.frames[LogIn] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        app.show_frame(LogIn)

    def logout(self):
        global userLoggedIn, username, userRole

        app.frames[MainMenu].lblUser.destroy()
        app.frames[MainMenu].btnPlay.destroy()
        app.frames[MainMenu].btnSettings.destroy()
        app.frames[MainMenu].btnTopScore.destroy()
        app.frames[MainMenu].btnLogIn.destroy()
        app.frames[MainMenu].btnStatistics.destroy()
        app.frames[MainMenu].btnSuggest.destroy()
        app.frames[MainMenu].btnReview.destroy()
        app.frames[MainMenu].btnLogout.destroy()
        app.frames[MainMenu].btnExit.destroy()

        app.frames[MainMenu].btnPlay = Button(app.frames[MainMenu], compound=CENTER, text="PLAY", font=("Rokkitt", 18, "bold"), image=app.frames[MainMenu].imgBtn,
                              borderwidth=0, fg="#68a302",
                              bg="#fee2ca", activebackground="#fee2cd", activeforeground="#68a302",
                              command=lambda: app.show_frame(GameMode))  # 7eba00
        app.frames[MainMenu].btnPlay.bind("<Enter>", lambda event: app.frames[MainMenu].btnPlay.configure(image=app.frames[MainMenu].imgBtnPress))
        app.frames[MainMenu].btnPlay.bind("<Leave>", lambda event: app.frames[MainMenu].btnPlay.configure(image=app.frames[MainMenu].imgBtn))
        app.frames[MainMenu].btnPlay.pack(pady=(210, 15), padx=30)

        app.frames[MainMenu].btnTopScore = Button(app.frames[MainMenu], compound=CENTER, text="TOP SCORE", font=("Rokkitt", 18, "bold"),
                                  image=app.frames[MainMenu].imgBtn, borderwidth=0, fg="#6f54b8",
                                  bg="#fee2cd", activebackground="#fee2cd", activeforeground="#6f54b8",
                                  command=app.frames[MainMenu].createTopScore)
        app.frames[MainMenu].btnTopScore.bind("<Enter>", lambda event: app.frames[MainMenu].btnTopScore.configure(image=app.frames[MainMenu].imgBtnPress))
        app.frames[MainMenu].btnTopScore.bind("<Leave>", lambda event: app.frames[MainMenu].btnTopScore.configure(image=app.frames[MainMenu].imgBtn))
        app.frames[MainMenu].btnTopScore.pack(pady=(0, 15), padx=30)

        app.frames[MainMenu].btnLogIn = Button(app.frames[MainMenu], compound=CENTER, text="LOGIN", font=("Rokkitt", 18, "bold"),
                               image=app.frames[MainMenu].imgBtn, borderwidth=0, fg="#c49000",
                               bg="#fde2cf", activebackground="#fee1cf", activeforeground="#c49000",
                               command=app.frames[MainMenu].createLogIn)
        app.frames[MainMenu].btnLogIn.bind("<Enter>", lambda event: app.frames[MainMenu].btnLogIn.configure(image=app.frames[MainMenu].imgBtnPress))
        app.frames[MainMenu].btnLogIn.bind("<Leave>", lambda event: app.frames[MainMenu].btnLogIn.configure(image=app.frames[MainMenu].imgBtn))
        app.frames[MainMenu].btnLogIn.pack(pady=(0, 15), padx=30)

        app.frames[MainMenu].btnSettings = Button(app.frames[MainMenu], compound=CENTER, text="SETTINGS", font=("Rokkitt", 18, "bold"),
                                  image=app.frames[MainMenu].imgBtn, borderwidth=0, fg="#01728f",
                                  bg="#fee1cf", activebackground="#fee1cf", activeforeground="#01728f",
                                  command=lambda: app.show_frame(Settings))
        app.frames[MainMenu].btnSettings.bind("<Enter>", lambda event: app.frames[MainMenu].btnSettings.configure(image=app.frames[MainMenu].imgBtnPress))
        app.frames[MainMenu].btnSettings.bind("<Leave>", lambda event: app.frames[MainMenu].btnSettings.configure(image=app.frames[MainMenu].imgBtn))
        app.frames[MainMenu].btnSettings.pack(pady=(0, 15), padx=30)

        app.frames[MainMenu].btnExit = Button(app.frames[MainMenu], compound=CENTER, text="EXIT", font=("Rokkitt", 18, "bold"), image=app.frames[MainMenu].imgBtn,
                              borderwidth=0, fg="red",
                              bg="#fee2d4", activebackground="#fee2d4", activeforeground="red", command=app.frames[MainMenu].quit)
        app.frames[MainMenu].btnExit.bind("<Enter>", lambda event: app.frames[MainMenu].btnExit.configure(image=app.frames[MainMenu].imgBtnPress))
        app.frames[MainMenu].btnExit.bind("<Leave>", lambda event: app.frames[MainMenu].btnExit.configure(image=app.frames[MainMenu].imgBtn))
        app.frames[MainMenu].btnExit.pack(pady=(0, 15), padx=30)

        username = ''
        userRole = ''
        userLoggedIn = False



class Settings(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.imgBtn = PhotoImage(file = "pictures/btnSettings.png")
        self.imgBtnPress = PhotoImage(file="pictures/btnSettingsDark.png")
        self.imgBtnDown = PhotoImage(file="pictures/btnSettingsDown.png")
        self.imgBtnUp = PhotoImage(file="pictures/btnSettingsUp.png")
        self.imgBtnDownDark = PhotoImage(file="pictures/btnSettingsDownDark.png")
        self.imgBtnUpDark = PhotoImage(file="pictures/btnSettingsUpDark.png")
        self.imgBtnBack = PhotoImage(file="pictures/btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="pictures/btnBackDark.png")

        self.backgroundImage = ImageTk.PhotoImage(Image.open("pictures/backgroundSettings.jpg"))
        self.backgroundLabel = Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.lblMusic = Label(self, text = "Music", font=("Rokkitt", 24, "bold"), bg = "#fee2ca", fg = "#ba5a00")
        self.lblMusic.grid(row = 0, column = 1, pady = (225,20), sticky = W)

        self.lblVolume = Label(self, text = "Volume", font=("Rokkitt", 24, "bold"), bg = "#fee2cc", fg = "#ba5a00")
        self.lblVolume.grid(row=1, column=1, sticky = W)

        self.btnOn = Button(self, compound = CENTER, text = "On", image = self.imgBtn, border = 0, font=("Rokkitt", 18, "bold"),
                            bg = "#fee2ca", fg="#68a302", activebackground = "#fee2ca", activeforeground = "#68a302", command = self.start_music)
        self.btnOn.bind("<Enter>", lambda event: self.btnOn.configure(image=self.imgBtnPress))
        self.btnOn.bind("<Leave>", lambda event: self.btnOn.configure(image=self.imgBtn))
        self.btnOn.grid(row=0, column=2, pady = (225,20), padx = 20)

        self.btnOff = Button(self, compound = CENTER, text = "Off", image = self.imgBtn, border = 0, font=("Rokkitt", 18, "bold"),
                             bg = "#fde2d1", fg="red", activebackground = "#fde2d1", activeforeground = "red", command = self.stop_music)
        self.btnOff.bind("<Enter>", lambda event: self.btnOff.configure(image=self.imgBtnPress))
        self.btnOff.bind("<Leave>", lambda event: self.btnOff.configure(image=self.imgBtn))
        self.btnOff.grid(row=0, column=3, pady = (225,20))

        self.btnDown = Button(self, image = self.imgBtnDown, border = 0, font=("Rokkitt", 18, "bold"),
                              bg = "#fee2ca", activebackground = "#fee2ca", command = self.decreaseVolume)
        self.btnDown.bind("<Enter>", lambda event: self.btnDown.configure(image=self.imgBtnDownDark))
        self.btnDown.bind("<Leave>", lambda event: self.btnDown.configure(image=self.imgBtnDown))
        self.btnDown.grid(row=1, column=2, padx = 20)

        self.btnUp = Button(self, image = self.imgBtnUp, border = 0, font=("Rokkitt", 18, "bold"),
                            bg = "#fde2d1", activebackground = "#fde2d1", command = self.increaseVolume)
        self.btnUp.bind("<Enter>", lambda event: self.btnUp.configure(image=self.imgBtnUpDark))
        self.btnUp.bind("<Leave>", lambda event: self.btnUp.configure(image=self.imgBtnUp))
        self.btnUp.grid(row=1, column=3)

        self.btnBack = Button(self, compound = CENTER, text = "Back", image = self.imgBtnBack, border = 0, font=("Rokkitt", 18, "bold"),
                              bg = "#fee0c4", fg="black", activebackground = "#fee0c4", activeforeground = "black",
                              command = lambda: controller.show_frame(MainMenu))
        self.btnBack.bind("<Enter>", lambda event: self.btnBack.configure(image=self.imgBtnBackDark))
        self.btnBack.bind("<Leave>", lambda event: self.btnBack.configure(image=self.imgBtnBack))
        self.btnBack.grid(row=2, column=0, padx = (30,108), pady = (180,0))

    def stop_music(self):
        pygame.mixer.music.pause()

    def start_music(self):
        pygame.mixer.music.unpause()

    def increaseVolume(self):
        global initialVolumeIndex
        if initialVolumeIndex < 8:
            initialVolumeIndex += 1
            pygame.mixer.music.set_volume(volumeLevels[initialVolumeIndex])

    def decreaseVolume(self):
        global initialVolumeIndex
        if initialVolumeIndex > 0:
            initialVolumeIndex -= 1
            pygame.mixer.music.set_volume(volumeLevels[initialVolumeIndex])



class TopScore(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.backgroundImage = ImageTk.PhotoImage(Image.open("pictures/backgroundTopScore.jpg"))
        self.backgroundLabel = Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.imgBtnBack = PhotoImage(file="pictures/btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="pictures/btnBackDark.png")

        self.scoreFrame = LabelFrame(self, bg = "#cddbfe", relief = RAISED)
        self.scoreFrame.grid(row = 0, column = 1, pady = (175,0))

        self.scroll = Scrollbar(self.scoreFrame, bg = "#cddbfe")
        self.scroll.pack(side = RIGHT, fill = Y)

        self.scoreBox = Listbox(self.scoreFrame, width = 33, height = 11, font=("Rokkitt", 15), bg = "#ffdfbe", fg = "#7d3b00",
                                yscrollcommand = self.scroll.set, selectmode = SINGLE)
        self.scoreBox.pack(side = LEFT)

        self.scroll.configure(command = self.scoreBox.yview)

        self.conn = sqlite3.connect('mdsproject.db')
        self.c = self.conn.cursor()

        self.c.execute("SELECT username, max_score FROM userinfo WHERE max_score IS NOT NULL ORDER BY max_score DESC")
        self.records = self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        for i in range(len(self.records)):
            self.scoreBox.insert(END, "  " + str(i+1) + ".     " + str(self.records[i][1]) + "        " + self.records[i][0])

        self.btnBack = Button(self, compound=CENTER, text="Back", image=self.imgBtnBack, border=0,
                              font=("Rokkitt", 18, "bold"),
                              bg="#fee0c4", fg="black", activebackground="#fee0c4", activeforeground="black",
                              command=lambda: [self.abort(), controller.show_frame(MainMenu), self.destroy(),
                                               self.kill()])
        self.btnBack.bind("<Enter>", lambda event: self.btnBack.configure(image=self.imgBtnBackDark))
        self.btnBack.bind("<Leave>", lambda event: self.btnBack.configure(image=self.imgBtnBack))
        self.btnBack.grid(row=2, column=0, padx=(30, 75), pady=(58, 0))

    def kill(self):
        del self
        gc.collect()

    def abort(self):
        del app.frames[TopScore]


class Statistics(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.backgroundImage = ImageTk.PhotoImage(Image.open("pictures/backgroundLogIn.jpg"))
        self.backgroundLabel = Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.imgBtnBack = PhotoImage(file="pictures/btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="pictures/btnBackDark.png")

        self.lblStatistics = Label(self, text="Statistics", font=("Rokkitt", 60, "bold"), bg="#fee6cd", fg="#a8b9ff")
        self.lblStatistics.grid(row=0, column=0, columnspan = 2, padx=(315, 0), pady=(10, 0))

        self.lblUser = Label(self, text="User:", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblUser.grid(row=1, column=0, padx=(170, 0), pady=(40, 0), sticky = E)

        self.lblUserR = Label(self, text=username, font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="#d18e08")
        self.lblUserR.grid(row=1, column=1, padx=(30, 0), pady=(40, 0))

        self.lblNrMeciuri = Label(self, text="Finished games:", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblNrMeciuri.grid(row=2, column=0, padx=(170, 0), pady=(10, 0), sticky = E)

        self.lblNrMeciuriR = Label(self, text="", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="#4dafff")
        self.lblNrMeciuriR.grid(row=2, column=1, padx=(30, 0), pady=(10, 0))

        self.lblMaxScore = Label(self, text="Best score:", font=("Rokkitt", 20, "bold"), bg="#fee6cd",
                                  fg="green")
        self.lblMaxScore.grid(row=3, column=0, padx=(170, 0), pady=(10, 0), sticky = E)

        self.lblMaxScoreR = Label(self, text="", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="black")
        self.lblMaxScoreR.grid(row=3, column=1, padx=(30, 0), pady=(10, 0))

        self.lblMinScore = Label(self, text="Worst score:", font=("Rokkitt", 20, "bold"), bg="#fee6cd",
                                 fg="red")
        self.lblMinScore.grid(row=4, column=0, padx=(170, 0), pady=(10, 0), sticky = E)

        self.lblMinScoreR = Label(self, text="", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="black")
        self.lblMinScoreR.grid(row=4, column=1, padx=(30, 0), pady=(10, 0))

        self.lblCateg = Label(self, text="Last category played:", font=("Rokkitt", 20, "bold"), bg="#fee6cd",
                                 fg="#b05e11")
        self.lblCateg.grid(row=5, column=0, padx=(170, 0), pady=(10, 0), sticky = E)

        self.lblCategR = Label(self, text="", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="purple")
        self.lblCategR.grid(row=5, column=1, padx=(30, 0), pady=(10, 0))

        self.lblDate = Label(self, text="Date of last game:", font=("Rokkitt", 20, "bold"), bg="#fee6cd",
                              fg="#b05e11")
        self.lblDate.grid(row=6, column=0, padx=(170, 0), pady=(10, 0), sticky = E)

        self.lblDateR = Label(self, text="", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="purple")
        self.lblDateR.grid(row=6, column=1, padx=(30, 0), pady=(10, 0))


        self.conn = sqlite3.connect('mdsproject.db')
        self.c = self.conn.cursor()

        self.c.execute("SELECT nr_meciuri, max_score, min_score, last_categ, last_time FROM userinfo WHERE username = ?", (username,))
        self.records = self.c.fetchall()

        self.nrMeciuri = self.records[0][0]
        self.maxScore = self.records[0][1]
        self.minScore = self.records[0][2]
        self.lastCateg = self.records[0][3]
        self.lastTime = self.records[0][4]

        self.lblNrMeciuriR.configure(text = str(self.nrMeciuri))

        if self.maxScore == None:
            self.lblMaxScoreR.configure(text="none")
        else:
            self.lblMaxScoreR.configure(text = str(self.maxScore))

        if self.minScore == None:
            self.lblMinScoreR.configure(text="none")
        else:
            self.lblMinScoreR.configure(text = str(self.minScore))

        if self.lastCateg == None:
            self.lblCategR.configure(text="none")
        else:
            self.lblCategR.configure(text =self.lastCateg)

        if self.lastTime == None:
            self.lblDateR.configure(text="none")
        else:
            self.lblDateR.configure(text =self.lastTime)

        self.conn.commit()
        self.conn.close()


        self.btnBack = Button(self, compound=CENTER, text="Back", image=self.imgBtnBack, border=0,
                              font=("Rokkitt", 18, "bold"),
                              bg="#fee6cd", fg="black", activebackground="#fee6cd", activeforeground="black",
                              command=lambda: [self.abort(), controller.show_frame(MainMenu), self.destroy(),
                                               self.kill()])
        self.btnBack.bind("<Enter>", lambda event: self.btnBack.configure(image=self.imgBtnBackDark))
        self.btnBack.bind("<Leave>", lambda event: self.btnBack.configure(image=self.imgBtnBack))
        self.btnBack.grid(row=7, column=0, padx=(30, 0), pady=(70, 0), sticky = W)

    def kill(self):
        del self
        gc.collect()

    def abort(self):
        del app.frames[Statistics]



class Review(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.configure(bg = "#fee6cd")

        self.imgBtnBack = PhotoImage(file="pictures/btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="pictures/btnBackDark.png")
        self.imgBtnSmall = PhotoImage(file="pictures/btnMenuSmall.png")
        self.imgBtnSmallDark = PhotoImage(file="pictures/btnMenuSmallDark.png")


        self.qstFrame = LabelFrame(self, bg = "#cddbfe", relief = RAISED, width = 900, height = 550)
        self.qstFrame.grid(row = 0, column = 0, columnspan = 2, padx = (30, 0), pady = (20, 0))

        self.scroll1 = Scrollbar(self.qstFrame, bg = "#cddbfe")
        self.scroll1.pack(side = RIGHT, fill = Y)

        self.scroll2 = Scrollbar(self.qstFrame, bg="#cddbfe", orient = HORIZONTAL)
        self.scroll2.pack(side = BOTTOM, fill = X)

        self.qstBox = Listbox(self.qstFrame, width = 66, height = 11, font=("Rokkitt", 18), bg = "#ffdfbe", fg = "#7d3b00",
                                yscrollcommand = self.scroll1.set, xscrollcommand = self.scroll2.set, selectmode = SINGLE)
        self.qstBox.pack(side = LEFT)

        self.scroll1.configure(command = self.qstBox.yview)
        self.scroll2.configure(command=self.qstBox.xview)

        self.conn = sqlite3.connect('mdsproject.db')
        self.c = self.conn.cursor()

        self.c.execute("SELECT * FROM suggested_qst")
        self.records = self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        for i in range(len(self.records)):
            self.qstBox.insert(END, "  ID: " + str(self.records[i][0]) + " |  Categoria:  " + self.records[i][1] + "  | " +
                               " " + self.records[i][2] + " | {" +
                                self.records[i][3] + " | " +
                                self.records[i][4] + " | " +
                                self.records[i][5] + " | " +
                                self.records[i][6] + "} | " +
                               " Numar raspuns corect: " + str(self.records[i][7]) +"   ")

        self.btnYes = Button(self, compound=CENTER, text="YES", image=self.imgBtnSmall, border=0,
                              font=("Rokkitt", 16, "bold"),
                              bg="#fee6cd", fg="green", activebackground="#fee6cd", activeforeground="green",
                              command = self.yesAction)
        self.btnYes.bind("<Enter>", lambda event: self.btnYes.configure(image=self.imgBtnSmallDark))
        self.btnYes.bind("<Leave>", lambda event: self.btnYes.configure(image=self.imgBtnSmall))
        self.btnYes.grid(row=1, column=0, padx=(0, 10), pady=(20, 0), sticky = E)

        self.btnNo = Button(self, compound=CENTER, text="NO", image=self.imgBtnSmall, border=0,
                              font=("Rokkitt", 16, "bold"),
                              bg="#fee6cd", fg="red", activebackground="#fee6cd", activeforeground="red",
                              command = self.noAction)
        self.btnNo.bind("<Enter>", lambda event: self.btnNo.configure(image=self.imgBtnSmallDark))
        self.btnNo.bind("<Leave>", lambda event: self.btnNo.configure(image=self.imgBtnSmall))
        self.btnNo.grid(row=1, column=1, padx=(10, 0), pady=(20, 0), sticky = W)

        self.btnBack = Button(self, compound=CENTER, text="Back", image=self.imgBtnBack, border=0,
                              font=("Rokkitt", 18, "bold"),
                              bg="#fee6cd", fg="black", activebackground="#fee6cd", activeforeground="black",
                              command=lambda: [self.abort(), controller.show_frame(MainMenu), self.destroy(),
                                               self.kill()])
        self.btnBack.bind("<Enter>", lambda event: self.btnBack.configure(image=self.imgBtnBackDark))
        self.btnBack.bind("<Leave>", lambda event: self.btnBack.configure(image=self.imgBtnBack))
        self.btnBack.grid(row=2, column=0, padx=(30, 75), pady=(46, 0), sticky = W)

    def noAction(self):
        if self.qstBox.curselection():
            s = self.qstBox.get(self.qstBox.curselection())
            i = 6
            nr = ''
            while s[i].isdigit():
                nr += s[i]
                i += 1
            nr = int(nr)

            self.conn = sqlite3.connect('mdsproject.db')
            self.c = self.conn.cursor()

            self.c.execute("DELETE FROM suggested_qst where id = ?", (nr,))

            self.conn.commit()
            self.conn.close()

            self.abort()
            self.destroy()
            self.kill()
            app.frames[LogIn].createReview()

    def yesAction(self):
        if self.qstBox.curselection():
            s = self.qstBox.get(self.qstBox.curselection())
            i = 6
            nr = ''
            while s[i].isdigit():
                nr += s[i]
                i += 1
            nr = int(nr)

            self.conn = sqlite3.connect('mdsproject.db')
            self.c = self.conn.cursor()

            self.c.execute("SELECT * FROM suggested_qst WHERE id = ?", (nr,))

            self.records = self.c.fetchall()

            categ = self.records[0][1]
            qst = self.records[0][2]
            ans1 = self.records[0][3]
            ans2 = self.records[0][4]
            ans3 = self.records[0][5]
            ans4 = self.records[0][6]
            crr_ans = int(self.records[0][7])

            self.conn.commit()
            self.conn.close()

            self.conn = sqlite3.connect('mdsproject.db')
            self.c = self.conn.cursor()

            self.c.execute(
                "INSERT INTO " + categ + " (question, ans1, ans2, ans3, ans4, correct_ans) VALUES (?,?,?,?,?,?)",
                (qst, ans1, ans2, ans3, ans4, self.records[0][crr_ans+2])
            )


            self.conn.commit()
            self.conn.close()

            self.conn = sqlite3.connect('mdsproject.db')
            self.c = self.conn.cursor()

            self.c.execute("DELETE FROM suggested_qst where id = ?", (nr,))

            self.conn.commit()
            self.conn.close()


            self.abort()
            self.destroy()
            self.kill()
            app.frames[LogIn].createReview()

    def kill(self):
        del self
        gc.collect()

    def abort(self):
        del app.frames[Review]



class CategorySuggest(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.configure(bg = "#fee6cd")

        self.imgBtnBack = PhotoImage(file="pictures/btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="pictures/btnBackDark.png")
        self.imgBtnMixed = PhotoImage(file="pictures/btnMixed.png")
        self.imgBtnMixedDark = PhotoImage(file="pictures/btnMixedDark.png")
        self.imgBtnMate = PhotoImage(file="pictures/btnMate.png")
        self.imgBtnMateDark = PhotoImage(file="pictures/btnMateDark.png")
        self.imgBtnArte = PhotoImage(file="pictures/btnArte.png")
        self.imgBtnArteDark = PhotoImage(file="pictures/btnArteDark.png")
        self.imgBtnBio = PhotoImage(file="pictures/btnBio.png")
        self.imgBtnBioDark = PhotoImage(file="pictures/btnBioDark.png")
        self.imgBtnIst = PhotoImage(file="pictures/btnIst.png")
        self.imgBtnIstDark = PhotoImage(file="pictures/btnIstDark.png")
        self.imgBtnSport = PhotoImage(file="pictures/btnSport.png")
        self.imgBtnSportDark = PhotoImage(file="pictures/btnSportDark.png")
        self.imgBtnChimie = PhotoImage(file="pictures/btnChimie.png")
        self.imgBtnChimieDark = PhotoImage(file="pictures/btnChimieDark.png")
        self.imgBtnGeo = PhotoImage(file="pictures/btnGeo.png")
        self.imgBtnGeoDark = PhotoImage(file="pictures/btnGeoDark.png")
        self.imgBtnDiv = PhotoImage(file="pictures/btnDiv.png")
        self.imgBtnDivDark = PhotoImage(file="pictures/btnDivDark.png")

        self.lblSelect = Label(self, text = "SELECT\nCATEGORY", font=("Rokkitt", 30, "bold"), bg = "#fee6cd", fg = "#b05e11")
        self.lblSelect.grid(row = 0, column = 1, sticky = NSEW, pady=(20,50))

        self.btnMate = Button(self, compound=CENTER, height=80, image=self.imgBtnMate, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343", text="Matematică",
                              font=("Rokkitt", 25, "bold"),
                              bg="#fee6cd", fg="#af4343",
                              command = lambda :self.createSuggestForm("matematica"))
        self.btnMate.bind("<Enter>", lambda event: self.btnMate.configure(image=self.imgBtnMateDark))
        self.btnMate.bind("<Leave>", lambda event: self.btnMate.configure(image=self.imgBtnMate))
        self.btnMate.grid(row=2, column=0, padx=(40, 86), pady=(25,25))

        self.btnArte = Button(self, compound=CENTER, height=80, image=self.imgBtnArte, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="Arte",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = lambda :self.createSuggestForm("arte_divertisment"))
        self.btnArte.bind("<Enter>", lambda event: self.btnArte.configure(image=self.imgBtnArteDark))
        self.btnArte.bind("<Leave>", lambda event: self.btnArte.configure(image=self.imgBtnArte))
        self.btnArte.grid(row=3, column=0, padx=(40, 86))

        self.btnBio = Button(self, compound=CENTER, height=80, image=self.imgBtnBio, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343", text="Biologie",
                              font=("Rokkitt", 25, "bold"),
                              bg="#fee6cd", fg="#af4343",
                             command = lambda :self.createSuggestForm("biologie"))
        self.btnBio.bind("<Enter>", lambda event: self.btnBio.configure(image=self.imgBtnBioDark))
        self.btnBio.bind("<Leave>", lambda event: self.btnBio.configure(image=self.imgBtnBio))
        self.btnBio.grid(row = 1, column = 1)

        self.btnIst = Button(self, compound=CENTER, height=80, image=self.imgBtnIst, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="Istorie",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = lambda :self.createSuggestForm("istorie"))
        self.btnIst.bind("<Enter>", lambda event: self.btnIst.configure(image=self.imgBtnIstDark))
        self.btnIst.bind("<Leave>", lambda event: self.btnIst.configure(image=self.imgBtnIst))
        self.btnIst.grid(row=2, column=1, pady=(25,25))

        self.btnSport = Button(self, compound=CENTER, height=80, image=self.imgBtnSport, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="Sport",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343",
                               command = lambda :self.createSuggestForm("sport"))
        self.btnSport.bind("<Enter>", lambda event: self.btnSport.configure(image=self.imgBtnSportDark))
        self.btnSport.bind("<Leave>", lambda event: self.btnSport.configure(image=self.imgBtnSport))
        self.btnSport.grid(row=3, column=1)

        self.btnChimie = Button(self, compound=CENTER, height=80, image=self.imgBtnChimie, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="Chimie",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = lambda :self.createSuggestForm("chimie"))
        self.btnChimie.bind("<Enter>", lambda event: self.btnChimie.configure(image=self.imgBtnChimieDark))
        self.btnChimie.bind("<Leave>", lambda event: self.btnChimie.configure(image=self.imgBtnChimie))
        self.btnChimie.grid(row = 1, column = 2, padx=(86, 0))

        self.btnGeo = Button(self, compound=CENTER, height=80, image=self.imgBtnGeo, border=0,
                               activebackground="#fee6cd", activeforeground="#af4343", text="Geografie",
                               font=("Rokkitt", 25, "bold"),
                               bg="#fee6cd", fg="#af4343", command = lambda :self.createSuggestForm("geografie"))
        self.btnGeo.bind("<Enter>", lambda event: self.btnGeo.configure(image=self.imgBtnGeoDark))
        self.btnGeo.bind("<Leave>", lambda event: self.btnGeo.configure(image=self.imgBtnGeo))
        self.btnGeo.grid(row=2, column=2, padx=(86, 0), pady=(25,25))

        self.btnDiv = Button(self, compound=CENTER, height=80, image=self.imgBtnDiv, border=0,
                               activebackground="#fee6cd", activeforeground="#af4343", text="Diverse",
                               font=("Rokkitt", 25, "bold"),
                               bg="#fee6cd", fg="#af4343",
                             command = lambda :self.createSuggestForm("diverse"))
        self.btnDiv.bind("<Enter>", lambda event: self.btnDiv.configure(image=self.imgBtnDivDark))
        self.btnDiv.bind("<Leave>", lambda event: self.btnDiv.configure(image=self.imgBtnDiv))
        self.btnDiv.grid(row = 1, column = 0, padx=(40, 86))


        self.btnBack = Button(self, compound=CENTER, text="Back", image=self.imgBtnBack, border=0,
                              font=("Rokkitt", 18, "bold"),
                              bg="#fee6cd", fg="black", activebackground="#fee6cd", activeforeground="black",
                              command=lambda: controller.show_frame(MainMenu))
        self.btnBack.bind("<Enter>", lambda event: self.btnBack.configure(image=self.imgBtnBackDark))
        self.btnBack.bind("<Leave>", lambda event: self.btnBack.configure(image=self.imgBtnBack))
        self.btnBack.grid(row=4, column=0, sticky = W, padx=(30, 0), pady=(70, 0))

    def createSuggestForm(self, category):
        frame = SuggestForm(app.container, app, category)
        app.frames[SuggestForm] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        app.show_frame(SuggestForm)




class SuggestForm(Frame):
    categ = ''
    def __init__(self, parent, controller, category):
        Frame.__init__(self, parent)

        self.categ = category

        self.configure(bg = "#fee6cd")

        self.imgBtnBack = PhotoImage(file="pictures/btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="pictures/btnBackDark.png")

        self.lblSuggest = Label(self, text="Suggest a Question", font=("Rokkitt", 50, "bold"), bg="#fee6cd", fg="#a8b9ff")
        self.lblSuggest.grid(row=0, column=0, columnspan=2, padx=(130, 0), pady=(0, 0))

        self.lblQst = Label(self, text="Question:", font=("Rokkitt", 18, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblQst.grid(row=1, column=0, padx=(70, 0), pady=(20, 0), sticky=E)

        self.entryQst = Entry(self, font=("Rokkitt", 18), fg="#b05e11", width = 35)
        self.entryQst.grid(row=1, column=1, padx=(30, 0), pady=(10, 0))

        self.lblAns1 = Label(self, text="Answer 1:", font=("Rokkitt", 18, "bold"), bg="#fee6cd",
                                  fg="#b05e11")
        self.lblAns1.grid(row=2, column=0, padx=(70, 0), pady=(6, 0), sticky=E)

        self.entryAns1 = Entry(self, font=("Rokkitt", 18), fg="#b05e11")
        self.entryAns1.grid(row=2, column=1, padx=(30, 0), pady=(6, 0))

        self.lblAns2 = Label(self, text="Answer 2:", font=("Rokkitt", 18, "bold"), bg="#fee6cd",
                                 fg="#b05e11")
        self.lblAns2.grid(row=3, column=0, padx=(70, 0), pady=(6, 0), sticky=E)

        self.entryAns2 = Entry(self, font=("Rokkitt", 18), fg="#b05e11")
        self.entryAns2.grid(row=3, column=1, padx=(30, 0), pady=(6, 0))

        self.lblAns3 = Label(self, text="Answer 3:", font=("Rokkitt", 18, "bold"), bg="#fee6cd",
                                 fg="#b05e11")
        self.lblAns3.grid(row=4, column=0, padx=(70, 0), pady=(6, 0), sticky=E)

        self.entryAns3 = Entry(self, font=("Rokkitt", 18), fg="#b05e11")
        self.entryAns3.grid(row=4, column=1, padx=(30, 0), pady=(6, 0))

        self.lblAns4 = Label(self, text="Answer 4:", font=("Rokkitt", 18, "bold"), bg="#fee6cd",
                              fg="#b05e11")
        self.lblAns4.grid(row=5, column=0, padx=(70, 0), pady=(6, 0), sticky=E)

        self.entryAns4 = Entry(self, font=("Rokkitt", 18), fg="#b05e11")
        self.entryAns4.grid(row=5, column=1, padx=(30, 0), pady=(6, 0))

        self.lblCorrectAns = Label(self, text="Correct answer number:", font=("Rokkitt", 18, "bold"), bg="#fee6cd",
                             fg="#b05e11")
        self.lblCorrectAns.grid(row=6, column=0, padx=(70, 0), pady=(6, 0), sticky=E)

        self.entryCorrectAns = Entry(self, font=("Rokkitt", 18), fg="#b05e11")
        self.entryCorrectAns.grid(row=6, column=1, padx=(30, 0), pady=(6, 0))

        self.lblWarning = Label(self, text="", font=("Rokkitt", 18, "bold"), bg="#fee6cd", fg="red")
        self.lblWarning.grid(row=7, column=0, columnspan=2, padx=(130, 0), pady=(10, 0))

        self.btnSubmit = Button(self, compound=CENTER, text="SUBMIT", image=self.imgBtnBack, border=0,
                              font=("Rokkitt", 18, "bold"),
                              bg="#fee6cd", fg="black", activebackground="#fee6cd", activeforeground="black",
                              command = self.submit)
        self.btnSubmit.bind("<Enter>", lambda event: self.btnSubmit.configure(image=self.imgBtnBackDark))
        self.btnSubmit.bind("<Leave>", lambda event: self.btnSubmit.configure(image=self.imgBtnBack))
        self.btnSubmit.grid(row=8, column=0, columnspan = 2, padx=(130, 0), pady=(10, 0))

        self.btnBack = Button(self, compound=CENTER, text="Back", image=self.imgBtnBack, border=0,
                              font=("Rokkitt", 18, "bold"),
                              bg="#fee6cd", fg="black", activebackground="#fee6cd", activeforeground="black",
                              command=lambda: [self.abort(), controller.show_frame(CategorySuggest), self.destroy(),
                                               self.kill()])
        self.btnBack.bind("<Enter>", lambda event: self.btnBack.configure(image=self.imgBtnBackDark))
        self.btnBack.bind("<Leave>", lambda event: self.btnBack.configure(image=self.imgBtnBack))
        self.btnBack.grid(row=9, column=0, padx=(30, 75), pady=(44, 0), sticky = W)

    def submit(self):
        qst = self.entryQst.get()
        ans1 = self.entryAns1.get()
        ans2 = self.entryAns2.get()
        ans3 = self.entryAns3.get()
        ans4 = self.entryAns4.get()
        correctAns = self.entryCorrectAns.get()

        if not qst or not ans1 or not ans2 or not ans3 or not ans4 or not correctAns:
            self.lblWarning.configure(text="Camp gol!", fg="red")
            self.lblWarning.after(1500, lambda: self.lblWarning.configure(text=""))
        else:
            if correctAns not in ['1', '2', '3', '4']:
                self.lblWarning.configure(text="Raspunsul corect este in intervalul 1-4!", fg="red")
                self.lblWarning.after(1500, lambda: self.lblWarning.configure(text=""))
            else:
                conn = sqlite3.connect('mdsproject.db')
                c = conn.cursor()

                c.execute(
                    "INSERT INTO suggested_qst (category, question, ans1, ans2, ans3, ans4, crr_ans_nr) VALUES (?,?,?,?,?,?,?)",
                    (self.categ, qst, ans1, ans2, ans3, ans4, int(correctAns))
                    )

                self.lblWarning.configure(text="Intrebare trimisa!", fg="green")
                self.lblWarning.after(1500, lambda: self.lblWarning.configure(text=""))

                self.entryQst.delete(0, END)
                self.entryAns1.delete(0, END)
                self.entryAns2.delete(0, END)
                self.entryAns3.delete(0, END)
                self.entryAns4.delete(0, END)
                self.entryCorrectAns.delete(0, END)

                conn.commit()
                conn.close()

    def kill(self):
        del self
        gc.collect()

    def abort(self):
        del app.frames[SuggestForm]



class LogIn(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.imgBtnBack = PhotoImage(file="pictures/btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="pictures/btnBackDark.png")

        self.imgBtnLogin = PhotoImage(file="pictures/btnLogin.png")
        self.imgBtnLoginDark = PhotoImage(file="pictures/btnLoginDark.png")

        self.backgroundImage = ImageTk.PhotoImage(Image.open("pictures/backgroundLogIn.jpg"))
        self.backgroundLabel = Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.lblLogIn = Label(self, text = "Login Credentials", font=("Rokkitt", 26, "bold"), bg = "#fee6cd", fg = "#b05e11")
        self.lblLogIn.grid(row=0, column=0, columnspan=2, padx=(310, 0), pady=(10, 0))

        self.lblUser1 = Label(self, text="Username", font=("Rokkitt", 16, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblUser1.grid(row=1, column=0, padx=(300, 0), pady=(10, 0))

        self.entryUser1 = Entry(self, font=("Rokkitt", 16), fg="#b05e11")
        self.entryUser1.grid(row=1, column=1, padx=(20, 0), pady=(10, 0))

        self.lblPass1 = Label(self, text="Password", font=("Rokkitt", 16, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblPass1.grid(row=2, column=0, padx=(300, 0), pady=(10, 0))

        self.entryPass1 = Entry(self, font=("Rokkitt", 16), fg="#b05e11", show = '*')
        self.entryPass1.grid(row=2, column=1, padx=(20, 0), pady=(10, 0))

        self.lblWarning1 = Label(self, text="", font=("Rokkitt", 16, "bold"), bg="#fee6cd", fg="red")
        self.lblWarning1.grid(row=3, column=0, columnspan=2, padx=(300, 0), pady=(10, 0))

        self.btnLogIn = Button(self, compound=CENTER, text="Login", image=self.imgBtnLogin, border=0,
                              font=("Rokkitt", 16, "bold"),
                              bg="#fee6cd", fg="black", activebackground="#fee6cd", activeforeground="black",
                               command = self.login
                              )
        self.btnLogIn.bind("<Enter>", lambda event: self.btnLogIn.configure(image=self.imgBtnLoginDark))
        self.btnLogIn.bind("<Leave>", lambda event: self.btnLogIn.configure(image=self.imgBtnLogin))
        self.btnLogIn.grid(row=4, column=0, columnspan=2, padx=(300, 0), pady=(10, 0))

        self.lblSignUp = Label(self, text="Sign Up Credentials", font=("Rokkitt", 26, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblSignUp.grid(row=5, column=0, columnspan=2, padx=(310, 0), pady=(10, 0))

        self.lblUser2 = Label(self, text="Username", font=("Rokkitt", 16, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblUser2.grid(row=6, column=0, padx=(300, 0), pady=(10, 0))

        self.entryUser2 = Entry(self, font=("Rokkitt", 16), fg="#b05e11")
        self.entryUser2.grid(row=6, column=1, padx=(20, 0), pady=(10, 0))

        self.lblPass2 = Label(self, text="Password", font=("Rokkitt", 16, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblPass2.grid(row=7, column=0, padx=(300, 0), pady=(10, 0))

        self.entryPass2 = Entry(self, font=("Rokkitt", 16), fg="#b05e11", show = '*')
        self.entryPass2.grid(row=7, column=1, padx=(20, 0), pady=(10, 0))

        self.lblWarning2 = Label(self, text="", font=("Rokkitt", 16, "bold"), bg="#fee6cd", fg="red")
        self.lblWarning2.grid(row=8, column=0, columnspan=2, padx=(300, 0), pady=(10, 0))

        self.btnSignUp = Button(self, compound=CENTER, text="Sign Up", image=self.imgBtnLogin, border=0,
                               font=("Rokkitt", 16, "bold"),
                               bg="#fee6cd", fg="black", activebackground="#fee6cd", activeforeground="black",
                                command = self.signup
                               )
        self.btnSignUp.bind("<Enter>", lambda event: self.btnSignUp.configure(image=self.imgBtnLoginDark))
        self.btnSignUp.bind("<Leave>", lambda event: self.btnSignUp.configure(image=self.imgBtnLogin))
        self.btnSignUp.grid(row=9, column=0, columnspan=2, padx=(300, 0), pady=(10, 0))

        self.btnBack = Button(self, compound = CENTER, text = "Back", image = self.imgBtnBack, border = 0, font=("Rokkitt", 18, "bold"),
                              bg = "#fee6cd", fg="black", activebackground = "#fee6cd", activeforeground = "black",
                              command=lambda: [self.abort(), controller.show_frame(MainMenu), self.destroy(),
                                               self.kill()])
        self.btnBack.bind("<Enter>", lambda event: self.btnBack.configure(image=self.imgBtnBackDark))
        self.btnBack.bind("<Leave>", lambda event: self.btnBack.configure(image=self.imgBtnBack))
        self.btnBack.grid(row=10, column=0, padx = (30,0), pady = (39,0), sticky = W)

    def signup(self):
        user = self.entryUser2.get()
        passw = self.entryPass2.get()

        if not user or not passw:
            self.lblWarning2.configure(text = "Camp gol!", fg="red")
            self.lblWarning2.after(1500, lambda: self.lblWarning2.configure(text = ""))
        else:
            if len(passw)<6 or (user[0] == ' ' or user[len(user)-1] == ' ') or (' ' in passw):
                if len(passw)<6:
                    self.lblWarning2.configure(text="Parola necesita minim 6 caractere!", fg="red")
                    self.lblWarning2.after(1500, lambda: self.lblWarning2.configure(text=""))
                if user[0] == ' ' or user[len(user)-1] == ' ':
                    self.lblWarning2.configure(text="Fara spatiu la inceput si sfarsit!", fg="red")
                    self.lblWarning2.after(1500, lambda: self.lblWarning2.configure(text=""))
                if ' ' in passw:
                    self.lblWarning2.configure(text="Parola nu trebuie sa contina spatii!", fg="red")
                    self.lblWarning2.after(1500, lambda: self.lblWarning2.configure(text=""))
            else:
                conn = sqlite3.connect('mdsproject.db')
                c = conn.cursor()

                c.execute("SELECT * FROM userinfo WHERE username = ?", (user,))
                records = c.fetchall()

                conn.commit()
                conn.close()

                if len(records) != 0:
                    self.lblWarning2.configure(text="Utilizatorul exista deja!", fg="red")
                    self.lblWarning2.after(1500, lambda: self.lblWarning2.configure(text=""))
                else:
                    conn = sqlite3.connect('mdsproject.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO userinfo VALUES (:username, :password, :role, :nr_meciuri, :max_score, :min_score, :last_categ, :last_time)",
                                   {
                                       'username': user,
                                       'password': passw,
                                       'role': 'user',
                                       'nr_meciuri': 0,
                                       'max_score': None,
                                       'min_score': None,
                                       'last_categ': None,
                                       'last_time': None,
                                   }
                                   )

                    self.lblWarning2.configure(text="Inregistrare efectuata!", fg="green")
                    self.lblWarning2.after(1500, lambda: self.lblWarning2.configure(text=""))

                    self.entryUser2.delete(0, END)
                    self.entryPass2.delete(0, END)

                    conn.commit()
                    conn.close()


    def login(self):
        global userLoggedIn, username, userRole
        user = self.entryUser1.get()
        passw = self.entryPass1.get()
        if not user or not passw:
            self.lblWarning1.configure(text = "Camp gol!", fg="red")
            self.lblWarning1.after(1500, lambda: self.lblWarning1.configure(text = ""))
        else:
            conn = sqlite3.connect('mdsproject.db')
            c = conn.cursor()

            c.execute("SELECT username, password, role FROM userinfo WHERE username = ?", (user,))
            records = c.fetchall()

            conn.commit()
            conn.close()

            if len(records) == 0:
                self.lblWarning1.configure(text="Utilizator inexistent!", fg="red")
                self.lblWarning1.after(1500, lambda: self.lblWarning1.configure(text=""))
            else:
                if passw != records[0][1]:
                    self.lblWarning1.configure(text="Parola incorecta!", fg="red")
                    self.lblWarning1.after(1500, lambda: self.lblWarning1.configure(text=""))
                else:
                    userLoggedIn = True
                    username = user
                    userRole = records[0][2]

                    app.frames[MainMenu].btnPlay.destroy()
                    app.frames[MainMenu].btnSettings.destroy()
                    app.frames[MainMenu].btnTopScore.destroy()
                    app.frames[MainMenu].btnLogIn.destroy()
                    app.frames[MainMenu].btnExit.destroy()

                    app.frames[MainMenu].lblUser = Label(app.frames[MainMenu], text="Connected as " + username, font=("Rokkitt", 16, "bold"), bg="#cddbfe", fg="#b05e11")
                    app.frames[MainMenu].lblUser.grid(row=0, column=0, columnspan = 2, pady=(200, 30), padx=(205, 0))

                    app.frames[MainMenu].btnPlay = Button(app.frames[MainMenu], compound=CENTER, text="PLAY",
                                                            font=("Rokkitt", 18, "bold"), image=app.frames[MainMenu].imgBtnSmall,
                                                            borderwidth=0, fg="#68a302",
                                                            bg="#fee1c7", activebackground="#fee1c7", activeforeground="#68a302",
                                                            command = lambda: app.show_frame(GameMode))
                    app.frames[MainMenu].btnPlay.bind("<Enter>", lambda event: app.frames[MainMenu].btnPlay.configure(
                        image=app.frames[MainMenu].imgBtnSmallDark))
                    app.frames[MainMenu].btnPlay.bind("<Leave>", lambda event: app.frames[MainMenu].btnPlay.configure(
                        image=app.frames[MainMenu].imgBtnSmall))
                    app.frames[MainMenu].btnPlay.grid(row = 1, column = 0, pady=(0, 15), padx=(235, 0))

                    app.frames[MainMenu].btnTopScore = Button(app.frames[MainMenu], compound=CENTER, text="TOP SCORE",
                                                          font=("Rokkitt", 18, "bold"), image=app.frames[MainMenu].imgBtnSmall,
                                                          borderwidth=0, fg="#6f54b8",
                                                          bg="#fde2c7", activebackground="#fde2c7", activeforeground="#6f54b8",
                                                          command=lambda: app.frames[MainMenu].createTopScore())
                    app.frames[MainMenu].btnTopScore.bind("<Enter>", lambda event: app.frames[MainMenu].btnTopScore.configure(
                        image=app.frames[MainMenu].imgBtnSmallDark))
                    app.frames[MainMenu].btnTopScore.bind("<Leave>", lambda event: app.frames[MainMenu].btnTopScore.configure(
                        image=app.frames[MainMenu].imgBtnSmall))
                    app.frames[MainMenu].btnTopScore.grid(row=2, column=0, pady=(0, 15), padx=(235, 0))

                    app.frames[MainMenu].btnSettings = Button(app.frames[MainMenu], compound=CENTER, text="SETTINGS",
                                                              font=("Rokkitt", 18, "bold"), image=app.frames[MainMenu].imgBtnSmall,
                                                              borderwidth=0, fg="#01728f",
                                                              bg="#fee2cc", activebackground="#fee2cc", activeforeground="#01728f",
                                                              command=lambda: app.show_frame(Settings))
                    app.frames[MainMenu].btnSettings.bind("<Enter>", lambda event: app.frames[MainMenu].btnSettings.configure(
                        image=app.frames[MainMenu].imgBtnSmallDark))
                    app.frames[MainMenu].btnSettings.bind("<Leave>", lambda event: app.frames[MainMenu].btnSettings.configure(
                        image=app.frames[MainMenu].imgBtnSmall))
                    app.frames[MainMenu].btnSettings.grid(row=3, column=0, pady=(0, 15), padx=(235, 0))

                    app.frames[MainMenu].btnStatistics = Button(app.frames[MainMenu], compound=CENTER, text="STATISTICS",
                                                                font=("Rokkitt", 18, "bold"),
                                                                image=app.frames[MainMenu].imgBtnSmall,
                                                                borderwidth=0, fg="#cf00c8",
                                                                bg="#fde2cf", activebackground="#fde2cf", activeforeground="#cf00c8",
                                                                command=app.frames[MainMenu].createStatistics)
                    app.frames[MainMenu].btnStatistics.bind("<Enter>", lambda event: app.frames[MainMenu].btnStatistics.configure(
                        image=app.frames[MainMenu].imgBtnSmallDark))
                    app.frames[MainMenu].btnStatistics.bind("<Leave>", lambda event: app.frames[MainMenu].btnStatistics.configure(
                        image=app.frames[MainMenu].imgBtnSmall))
                    app.frames[MainMenu].btnStatistics.grid(row=1, column=1, pady=(0, 15), padx=30)

                    app.frames[MainMenu].btnSuggest = Button(app.frames[MainMenu], compound=CENTER, text="SUGGEST",
                                                              font=("Rokkitt", 18, "bold"), image=app.frames[MainMenu].imgBtnSmall,
                                                              borderwidth=0, fg="#b0b315",
                                                              bg="#fee3d2", activebackground="#fee3d2", activeforeground="#b0b315",
                                                              command = lambda: app.show_frame(CategorySuggest))
                    app.frames[MainMenu].btnSuggest.bind("<Enter>", lambda event: app.frames[MainMenu].btnSuggest.configure(
                        image=app.frames[MainMenu].imgBtnSmallDark))
                    app.frames[MainMenu].btnSuggest.bind("<Leave>", lambda event: app.frames[MainMenu].btnSuggest.configure(
                        image=app.frames[MainMenu].imgBtnSmall))


                    app.frames[MainMenu].btnReview = Button(app.frames[MainMenu], compound=CENTER, text="REVIEW",
                                                             font=("Rokkitt", 18, "bold"), image=app.frames[MainMenu].imgBtnSmall,
                                                             borderwidth=0, fg="#b0b315",
                                                             bg="#fee3d2", activebackground="#fee3d2", activeforeground="#b0b315",
                                                             command=self.createReview)
                    app.frames[MainMenu].btnReview.bind("<Enter>", lambda event: app.frames[MainMenu].btnReview.configure(
                        image=app.frames[MainMenu].imgBtnSmallDark))
                    app.frames[MainMenu].btnReview.bind("<Leave>", lambda event: app.frames[MainMenu].btnReview.configure(
                        image=app.frames[MainMenu].imgBtnSmall))

                    if userRole == 'user':
                        app.frames[MainMenu].btnSuggest.grid(row=2, column=1, pady=(0, 15), padx=30)
                    else:
                        app.frames[MainMenu].btnReview.grid(row=2, column=1, pady=(0, 15), padx=30)



                    app.frames[MainMenu].btnLogout = Button(app.frames[MainMenu], compound=CENTER, text="LOGOUT",
                                                            font=("Rokkitt", 18, "bold"), image=app.frames[MainMenu].imgBtnSmall,
                                                            borderwidth=0, fg="#c49000",
                                                            bg="#fee2d4", activebackground="#fee2d4", activeforeground="#c49000",
                                                            command=app.frames[MainMenu].logout)
                    app.frames[MainMenu].btnLogout.bind("<Enter>", lambda event: app.frames[MainMenu].btnLogout.configure(
                        image=app.frames[MainMenu].imgBtnSmallDark))
                    app.frames[MainMenu].btnLogout.bind("<Leave>", lambda event: app.frames[MainMenu].btnLogout.configure(
                        image=app.frames[MainMenu].imgBtnSmall))
                    app.frames[MainMenu].btnLogout.grid(row=3, column=1, pady=(0, 15), padx=30)

                    app.frames[MainMenu].btnExit = Button(app.frames[MainMenu], compound=CENTER, text="EXIT",
                                                          font=("Rokkitt", 18, "bold"), image=app.frames[MainMenu].imgBtnSmall,
                                                          borderwidth=0, fg="red",
                                                          bg="#fde2d1", activebackground="#fde2d1", activeforeground="red",
                                                          command=app.frames[MainMenu].quit)
                    app.frames[MainMenu].btnExit.bind("<Enter>", lambda event: app.frames[MainMenu].btnExit.configure(
                        image=app.frames[MainMenu].imgBtnSmallDark))
                    app.frames[MainMenu].btnExit.bind("<Leave>", lambda event: app.frames[MainMenu].btnExit.configure(
                        image=app.frames[MainMenu].imgBtnSmall))
                    app.frames[MainMenu].btnExit.grid(row=4, column=0, columnspan=2, pady=(0, 15), padx=(205, 0))

                    app.show_frame(MainMenu)


    def createReview(self):
        frame = Review(app.container, app)
        app.frames[Review] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        app.show_frame(Review)

    def kill(self):
        del self
        gc.collect()

    def abort(self):
        del app.frames[LogIn]


class GameMode(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.backgroundImage = ImageTk.PhotoImage(Image.open("pictures/backgroundGameMode.jpg"))
        self.backgroundLabel = Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)


        self.imgBtnBack = PhotoImage(file="pictures/btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="pictures/btnBackDark.png")
        self.imgBtnSolo = PhotoImage(file="pictures/btnSolo.png")
        self.imgBtnSoloDark = PhotoImage(file="pictures/btnSoloDark.png")
        self.imgBtnPvp = PhotoImage(file="pictures/btnPvp.png")
        self.imgBtnPvpDark = PhotoImage(file="pictures/btnPvpDark.png")
        self.imgBtnPvpSr = PhotoImage(file="pictures/btnPvpSr.png")
        self.imgBtnPvpSrDark = PhotoImage(file="pictures/btnPvpSrDark.png")

        self.lblSelect = Label(self, text = "SELECT MODE", font=("Rokkitt", 42, "bold"), bg = "#fee6cd", fg = "#b05e11")
        self.lblSelect.grid(row = 0, column = 1, sticky = NSEW, pady=(30,110))

        self.btnSolo = Button(self, compound = CENTER, height = 190,image = self.imgBtnSolo, border = 0,
                              activebackground="#fee6cd", activeforeground="#af4343", text = "Solo",
                              font=("Rokkitt", 25, "bold"),
                              bg = "#fee6cd", fg = "#af4343", command = lambda: controller.show_frame(Category))
        self.btnSolo.bind("<Enter>", lambda event: self.btnSolo.configure(image=self.imgBtnSoloDark))
        self.btnSolo.bind("<Leave>", lambda event: self.btnSolo.configure(image=self.imgBtnSolo))
        self.btnSolo.grid(row = 1, column = 0, padx=(44,0))

        self.btnPvp = Button(self, compound=CENTER, height=190, image=self.imgBtnPvp, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343", text="PvP",
                              font=("Rokkitt", 25, "bold"),
                              bg="#fee6cd", fg="#af4343", command = self.startGamePvP)
        self.btnPvp.bind("<Enter>", lambda event: self.btnPvp.configure(image=self.imgBtnPvpDark))
        self.btnPvp.bind("<Leave>", lambda event: self.btnPvp.configure(image=self.imgBtnPvp))
        self.btnPvp.grid(row = 1, column = 1)

        self.btnPvpSr = Button(self, compound=CENTER, height=190, image=self.imgBtnPvpSr, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="PvP\nSpeedrun",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = self.startGamePvpSr)
        self.btnPvpSr.bind("<Enter>", lambda event: self.btnPvpSr.configure(image=self.imgBtnPvpSrDark))
        self.btnPvpSr.bind("<Leave>", lambda event: self.btnPvpSr.configure(image=self.imgBtnPvpSr))
        self.btnPvpSr.grid(row = 1, column = 2)

        self.btnBack = Button(self, compound=CENTER, text="Back", image=self.imgBtnBack, border=0,
                              font=("Rokkitt", 18, "bold"),
                              bg="#fee6cd", fg="black", activebackground="#fee6cd", activeforeground="black",
                              command=lambda: controller.show_frame(MainMenu))
        self.btnBack.bind("<Enter>", lambda event: self.btnBack.configure(image=self.imgBtnBackDark))
        self.btnBack.bind("<Leave>", lambda event: self.btnBack.configure(image=self.imgBtnBack))
        self.btnBack.grid(row=2, column=0, sticky = W, padx=(30, 0), pady=(142, 0))

    def startGamePvP(self):
        frame = GamePvP(app.container, app)
        app.frames[GamePvP] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        app.show_frame(GamePvP)

    def startGamePvpSr(self):
        frame = GamePvPSr(app.container, app)
        app.frames[GamePvPSr] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        app.show_frame(GamePvPSr)




class Category(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.configure(bg = "#fee6cd")

        self.imgBtnBack = PhotoImage(file="pictures/btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="pictures/btnBackDark.png")
        self.imgBtnMixed = PhotoImage(file="pictures/btnMixed.png")
        self.imgBtnMixedDark = PhotoImage(file="pictures/btnMixedDark.png")
        self.imgBtnMate = PhotoImage(file="pictures/btnMate.png")
        self.imgBtnMateDark = PhotoImage(file="pictures/btnMateDark.png")
        self.imgBtnArte = PhotoImage(file="pictures/btnArte.png")
        self.imgBtnArteDark = PhotoImage(file="pictures/btnArteDark.png")
        self.imgBtnBio = PhotoImage(file="pictures/btnBio.png")
        self.imgBtnBioDark = PhotoImage(file="pictures/btnBioDark.png")
        self.imgBtnIst = PhotoImage(file="pictures/btnIst.png")
        self.imgBtnIstDark = PhotoImage(file="pictures/btnIstDark.png")
        self.imgBtnSport = PhotoImage(file="pictures/btnSport.png")
        self.imgBtnSportDark = PhotoImage(file="pictures/btnSportDark.png")
        self.imgBtnChimie = PhotoImage(file="pictures/btnChimie.png")
        self.imgBtnChimieDark = PhotoImage(file="pictures/btnChimieDark.png")
        self.imgBtnGeo = PhotoImage(file="pictures/btnGeo.png")
        self.imgBtnGeoDark = PhotoImage(file="pictures/btnGeoDark.png")
        self.imgBtnDiv = PhotoImage(file="pictures/btnDiv.png")
        self.imgBtnDivDark = PhotoImage(file="pictures/btnDivDark.png")

        self.lblSelect = Label(self, text = "SELECT\nCATEGORY", font=("Rokkitt", 30, "bold"), bg = "#fee6cd", fg = "#b05e11")
        self.lblSelect.grid(row = 0, column = 1, sticky = NSEW, pady=(20,50))

        self.btnMixed = Button(self, compound = CENTER, height = 80,image = self.imgBtnMixed, border = 0,
                              activebackground="#fee6cd", activeforeground="#af4343", text = "Mixed",
                              font=("Rokkitt", 25, "bold"),
                              bg = "#fee6cd", fg = "#af4343",command = lambda :self.startGame("mixed"))
        self.btnMixed.bind("<Enter>", lambda event: self.btnMixed.configure(image=self.imgBtnMixedDark))
        self.btnMixed.bind("<Leave>", lambda event: self.btnMixed.configure(image=self.imgBtnMixed))
        self.btnMixed.grid(row = 1, column = 0, padx=(40, 86))

        self.btnMate = Button(self, compound=CENTER, height=80, image=self.imgBtnMate, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343", text="Matematică",
                              font=("Rokkitt", 25, "bold"),
                              bg="#fee6cd", fg="#af4343", command = lambda :self.startGame("matematica"))
        self.btnMate.bind("<Enter>", lambda event: self.btnMate.configure(image=self.imgBtnMateDark))
        self.btnMate.bind("<Leave>", lambda event: self.btnMate.configure(image=self.imgBtnMate))
        self.btnMate.grid(row=2, column=0, padx=(40, 86), pady=(25,25))

        self.btnArte = Button(self, compound=CENTER, height=80, image=self.imgBtnArte, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="Arte",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = lambda :self.startGame("arte_divertisment"))
        self.btnArte.bind("<Enter>", lambda event: self.btnArte.configure(image=self.imgBtnArteDark))
        self.btnArte.bind("<Leave>", lambda event: self.btnArte.configure(image=self.imgBtnArte))
        self.btnArte.grid(row=3, column=0, padx=(40, 86))

        self.btnBio = Button(self, compound=CENTER, height=80, image=self.imgBtnBio, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343", text="Biologie",
                              font=("Rokkitt", 25, "bold"),
                              bg="#fee6cd", fg="#af4343", command = lambda :self.startGame("biologie"))
        self.btnBio.bind("<Enter>", lambda event: self.btnBio.configure(image=self.imgBtnBioDark))
        self.btnBio.bind("<Leave>", lambda event: self.btnBio.configure(image=self.imgBtnBio))
        self.btnBio.grid(row = 1, column = 1)

        self.btnIst = Button(self, compound=CENTER, height=80, image=self.imgBtnIst, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="Istorie",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = lambda :self.startGame("istorie"))
        self.btnIst.bind("<Enter>", lambda event: self.btnIst.configure(image=self.imgBtnIstDark))
        self.btnIst.bind("<Leave>", lambda event: self.btnIst.configure(image=self.imgBtnIst))
        self.btnIst.grid(row=2, column=1, pady=(25,25))

        self.btnSport = Button(self, compound=CENTER, height=80, image=self.imgBtnSport, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="Sport",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = lambda :self.startGame("sport"))
        self.btnSport.bind("<Enter>", lambda event: self.btnSport.configure(image=self.imgBtnSportDark))
        self.btnSport.bind("<Leave>", lambda event: self.btnSport.configure(image=self.imgBtnSport))
        self.btnSport.grid(row=3, column=1)

        self.btnChimie = Button(self, compound=CENTER, height=80, image=self.imgBtnChimie, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="Chimie",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = lambda :self.startGame("chimie"))
        self.btnChimie.bind("<Enter>", lambda event: self.btnChimie.configure(image=self.imgBtnChimieDark))
        self.btnChimie.bind("<Leave>", lambda event: self.btnChimie.configure(image=self.imgBtnChimie))
        self.btnChimie.grid(row = 1, column = 2, padx=(86, 0))

        self.btnGeo = Button(self, compound=CENTER, height=80, image=self.imgBtnGeo, border=0,
                               activebackground="#fee6cd", activeforeground="#af4343", text="Geografie",
                               font=("Rokkitt", 25, "bold"),
                               bg="#fee6cd", fg="#af4343", command = lambda :self.startGame("geografie"))
        self.btnGeo.bind("<Enter>", lambda event: self.btnGeo.configure(image=self.imgBtnGeoDark))
        self.btnGeo.bind("<Leave>", lambda event: self.btnGeo.configure(image=self.imgBtnGeo))
        self.btnGeo.grid(row=2, column=2, padx=(86, 0), pady=(25,25))

        self.btnDiv = Button(self, compound=CENTER, height=80, image=self.imgBtnDiv, border=0,
                               activebackground="#fee6cd", activeforeground="#af4343", text="Diverse",
                               font=("Rokkitt", 25, "bold"),
                               bg="#fee6cd", fg="#af4343")
        self.btnDiv.bind("<Enter>", lambda event: self.btnDiv.configure(image=self.imgBtnDivDark))
        self.btnDiv.bind("<Leave>", lambda event: self.btnDiv.configure(image=self.imgBtnDiv))
        self.btnDiv.grid(row=3, column=2, padx=(86, 0))


        self.btnBack = Button(self, compound=CENTER, text="Back", image=self.imgBtnBack, border=0,
                              font=("Rokkitt", 18, "bold"),
                              bg="#fee6cd", fg="black", activebackground="#fee6cd", activeforeground="black",
                              command=lambda: controller.show_frame(GameMode))
        self.btnBack.bind("<Enter>", lambda event: self.btnBack.configure(image=self.imgBtnBackDark))
        self.btnBack.bind("<Leave>", lambda event: self.btnBack.configure(image=self.imgBtnBack))
        self.btnBack.grid(row=4, column=0, sticky = W, padx=(30, 0), pady=(70, 0))

    def startGame(self, category):
        frame = Game(app.container, app, category)
        app.frames[Game] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        app.show_frame(Game)



class Game(Frame):
    categ = ''
    def __init__(self, parent, controller, category):
        Frame.__init__(self, parent)

        self.configure(bg = "#fee6cd")

        self.t = 15
        self.oneOutCount = 3
        self.twoOutCount = 2
        self.nrFrame = 0
        self.score = 0
        self.categ = category

        self.imgBtnStart = PhotoImage(file="pictures/btnStart.png")
        self.imgBtnStartDark = PhotoImage(file="pictures/btnStartDark.png")
        self.imgBtnQst = PhotoImage(file="pictures/btnQst.png")
        self.imgBtnQstDark = PhotoImage(file="pictures/btnQstDark.png")
        self.imgBtnUtils = PhotoImage(file = "pictures/btnUtils.png")
        self.imgBtnUtilsDark = PhotoImage(file="pictures/btnUtilsDark.png")
        self.imgBtnQstRight = PhotoImage(file = "pictures/btnQstRight.png")
        self.imgBtnQstWrong = PhotoImage(file = "pictures/btnQstWrong.png")


        self.conn = sqlite3.connect('mdsproject.db')
        self.c = self.conn.cursor()

        if category == "mixed":
            self.c.execute("SELECT * FROM biologie UNION SELECT * FROM chimie UNION SELECT * FROM arte_divertisment UNION SELECT * FROM istorie UNION SELECT * FROM geografie UNION SELECT * FROM matematica UNION SELECT * FROM sport UNION SELECT * FROM diverse")
        else:
            self.c.execute("SELECT * FROM " + category)

        self.records = self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        self.indexes = random.sample(range(0, len(self.records)), 20)


        self.container = LabelFrame(self,width = 920, height = 630, bg = "#fee6cd", border = 1, relief = SUNKEN)
        self.container.pack(pady = 10)

        self.btnStart = Button(self.container, compound=CENTER, height=80, image=self.imgBtnStart, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="START",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = self.beginTest)
        self.btnStart.bind("<Enter>", lambda event: self.btnStart.configure(image=self.imgBtnStartDark))
        self.btnStart.bind("<Leave>", lambda event: self.btnStart.configure(image=self.imgBtnStart))
        self.btnStart.place(x=350, y=260)

        self.lbl = Label()
        self.qst = Message()
        self.btn1 = Button()
        self.btn2 = Button()
        self.btn3 = Button()
        self.btn4 = Button()

        self.btnQuit = Button()
        self.btnOneOut = Button()
        self.btnTwoOut = Button()

        self.lblScore = Label()
        self.lblName = Label()
        self.entry = Entry()
        self.btnSubmit = Button()

    def beginTest(self):
        self.container.destroy()
        self.createNewFrame(self.nrFrame)

    def countdown(self):
        if self.t>0:
            if not self.btnPressed:
                self.lbl.config(text = str(self.t))
            self.t -= 1
            self.lbl.after(1000, self.countdown)
        elif self.t == 0:
            self.container.destroy()
            self.btnQuit.destroy()
            self.btnOneOut.destroy()
            self.btnTwoOut.destroy()
            if self.nrFrame<20:
                self.t = 15
                self.createNewFrame(self.nrFrame)
            elif self.nrFrame == 20:
                self.lblScore = Label(self, font=("Rokkitt", 36, "bold"), bg = "#fee6cd", fg = "#b05e11",
                                      text="Your Score: " + str(self.score))
                self.lblScore.pack(pady=(50,0))

                if not userLoggedIn:
                    self.lblMsg1 = Label(self, font=("Rokkitt", 24, "bold"), bg="#fee6cd", fg="red", #b05e11
                                          text="Nu sunteti autentificat!")
                    self.lblMsg1.pack(pady=(40, 0))

                    self.lblMsg2 = Label(self, font=("Rokkitt", 24, "bold"), bg="#fee6cd", fg="red",
                                         text="Pentru a va salva scorul trebuie sa fiti autentificat!")
                    self.lblMsg2.pack(pady=(10, 0))
                else:
                    self.conn = sqlite3.connect('mdsproject.db')
                    self.c = self.conn.cursor()

                    self.c.execute("SELECT nr_meciuri, max_score, min_score FROM userinfo WHERE username = ?", (username,))
                    self.records = self.c.fetchall()

                    self.nrMeciuri = self.records[0][0]
                    self.maxScore = self.records[0][1]
                    self.minScore = self.records[0][2]

                    self.conn.commit()
                    self.conn.close()

                    self.nrMeciuri += 1

                    if self.maxScore == None or self.minScore == None:
                        self.lblMsg1 = Label(self, font=("Rokkitt", 26, "bold"), bg="#fee6cd", fg="green",  # b05e11
                                             text="Primul scor obtinut!")
                        self.lblMsg1.pack(pady=(50, 0))

                        self.lblMsg2 = Label(self, font=("Rokkitt", 26, "bold"), bg="#fee6cd", fg="green",
                                             text="Felicitari!")
                        self.lblMsg2.pack(pady=(10, 0))

                        self.maxScore = self.score
                        self.minScore = self.score

                    elif self.score <= self.maxScore:
                        self.lblMsg = Label(self, font=("Rokkitt", 26, "bold"), bg="#fee6cd", fg="red",  # b05e11
                                             text="Nu ati reusit sa va depasiti recordul de: " + str(self.maxScore))
                        self.lblMsg.pack(pady=(50, 0))

                        if self.score < self.minScore:
                            self.minScore = self.score

                    elif self.score > self.maxScore:
                        self.lblMsg = Label(self, font=("Rokkitt", 26, "bold"), bg="#fee6cd", fg="green",  # b05e11
                                            text="V-ati depasit recordul de: " + str(self.maxScore))
                        self.lblMsg.pack(pady=(50, 0))

                        self.maxScore = self.score


                    crtTime = datetime.now().strftime("%d/%m/%Y %H:%M")

                    self.conn = sqlite3.connect('mdsproject.db')
                    self.c = self.conn.cursor()

                    self.c.execute(
                        "UPDATE userinfo SET nr_meciuri = ?, max_score = ?, min_score = ?, last_categ = ?, last_time = ? WHERE username = ?",
                        (self.nrMeciuri, self.maxScore, self.minScore, self.categ, crtTime, username)
                        )

                    self.conn.commit()
                    self.conn.close()


                self.btnQuit = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                                      activebackground="#fee6cd", activeforeground="#af4343",
                                      font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                                      text="QUIT",
                                      command=lambda: [self.abort(), app.show_frame(MainMenu), self.destroy(),
                                                       self.kill()])
                self.btnQuit.bind("<Enter>", lambda event: self.btnQuit.configure(image=self.imgBtnUtilsDark))
                self.btnQuit.bind("<Leave>", lambda event: self.btnQuit.configure(image=self.imgBtnUtils))
                self.btnQuit.pack(padx=(50, 0), pady=(120, 0), side=LEFT)

    def createNewFrame(self, number):
        self.btnPressed = False
        self.container = LabelFrame(self, width=920, height=630, bg="#fee6cd", border=0, relief=SUNKEN)
        self.container.pack(pady=10)

        randomIndex = random.sample([1, 2, 3, 4], 4)

        self.lbl = Label(self.container, font=("Rokkitt", 30, "bold"), bg = "#fee6cd", fg = "#b05e11")
        self.lbl.pack()

        self.qst = Message(self.container, width = 700, justify = CENTER, font=("Rokkitt", 18), bg = "#fee6cd", fg = "#b05e11",
                           text = self.records[self.indexes[number]][0])
        self.qst.pack(fill = BOTH)

        self.btn1 = Button(self.container, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                                activebackground="#fee6cd", activeforeground="#af4343",
                                font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text = self.records[self.indexes[number]][randomIndex[0]], command= lambda: self.btnClicked(self.btn1))
        self.btn1.bind("<Enter>", lambda event: self.btn1.configure(image=self.imgBtnQstDark))
        self.btn1.bind("<Leave>", lambda event: self.btn1.configure(image=self.imgBtnQst))
        self.btn1.pack(pady = (30,0))

        self.btn2 = Button(self.container, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records[self.indexes[number]][randomIndex[1]], command= lambda: self.btnClicked(self.btn2))
        self.btn2.bind("<Enter>", lambda event: self.btn2.configure(image=self.imgBtnQstDark))
        self.btn2.bind("<Leave>", lambda event: self.btn2.configure(image=self.imgBtnQst))
        self.btn2.pack(pady = (20,0))

        self.btn3 = Button(self.container, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records[self.indexes[number]][randomIndex[2]], command= lambda: self.btnClicked(self.btn3))
        self.btn3.bind("<Enter>", lambda event: self.btn3.configure(image=self.imgBtnQstDark))
        self.btn3.bind("<Leave>", lambda event: self.btn3.configure(image=self.imgBtnQst))
        self.btn3.pack(pady = (20,0))

        self.btn4 = Button(self.container, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records[self.indexes[number]][randomIndex[3]], command= lambda: self.btnClicked(self.btn4))
        self.btn4.bind("<Enter>", lambda event: self.btn4.configure(image=self.imgBtnQstDark))
        self.btn4.bind("<Leave>", lambda event: self.btn4.configure(image=self.imgBtnQst))
        self.btn4.pack(pady = (20,0))

        self.btnQuit = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343",
                              font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                              text="QUIT",
                              command=lambda: [self.abort(), app.show_frame(MainMenu), self.destroy(),
                                               self.kill()])
        self.btnQuit.bind("<Enter>", lambda event: self.btnQuit.configure(image=self.imgBtnUtilsDark))
        self.btnQuit.bind("<Leave>", lambda event: self.btnQuit.configure(image=self.imgBtnUtils))
        self.btnQuit.pack(padx = (92,30), pady=(20, 0), side=LEFT)

        self.btnOneOut = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343",
                              font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                              text="Eliminate 1", command = self.eliminateOne)
        self.btnOneOut.bind("<Enter>", lambda event: self.btnOneOut.configure(image=self.imgBtnUtilsDark))
        self.btnOneOut.bind("<Leave>", lambda event: self.btnOneOut.configure(image=self.imgBtnUtils))
        self.btnOneOut.pack(padx=(30, 30), pady=(20, 0), side=LEFT)

        if(self.oneOutCount == 0):
            self.btnOneOut.configure(state = 'disabled')

        self.btnTwoOut = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                                activebackground="#fee6cd", activeforeground="#af4343",
                                font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                                text="Eliminate 2", command = self.eliminateTwo)
        self.btnTwoOut.bind("<Enter>", lambda event: self.btnTwoOut.configure(image=self.imgBtnUtilsDark))
        self.btnTwoOut.bind("<Leave>", lambda event: self.btnTwoOut.configure(image=self.imgBtnUtils))
        self.btnTwoOut.pack(padx=(30, 30), pady=(20, 0), side=LEFT)

        if (self.twoOutCount == 0):
            self.btnTwoOut.configure(state='disabled')

        self.nrFrame += 1
        self.countdown()

    def btnClicked(self, btn):
        self.btnPressed = True
        text = self.records[self.indexes[self.nrFrame - 1]][5]
        self.lbl.configure(text = "")
        self.btn1['command'] = 0
        self.btn2['command'] = 0
        self.btn3['command'] = 0
        self.btn4['command'] = 0

        self.btn1.unbind("<Enter>")
        self.btn2.unbind("<Enter>")
        self.btn3.unbind("<Enter>")
        self.btn4.unbind("<Enter>")
        self.btn1.unbind("<Leave>")
        self.btn2.unbind("<Leave>")
        self.btn3.unbind("<Leave>")
        self.btn4.unbind("<Leave>")

        self.btnOneOut['state'] = 'disabled'
        self.btnTwoOut['state'] = 'disabled'

        self.btn1.configure(image=self.imgBtnQstWrong, fg = "black", activeforeground = "black", relief = SUNKEN)
        self.btn2.configure(image=self.imgBtnQstWrong, fg = "black", activeforeground = "black", relief = SUNKEN)
        self.btn3.configure(image=self.imgBtnQstWrong, fg = "black", activeforeground = "black", relief = SUNKEN)
        self.btn4.configure(image=self.imgBtnQstWrong, fg = "black", activeforeground = "black", relief = SUNKEN)

        if text == self.btn1['text']:
            self.btn1.configure(image=self.imgBtnQstRight)
        if text == self.btn2['text']:
            self.btn2.configure(image=self.imgBtnQstRight)
        if text == self.btn3['text']:
            self.btn3.configure(image=self.imgBtnQstRight)
        if text == self.btn4['text']:
            self.btn4.configure(image=self.imgBtnQstRight)

        if text == btn['text']:
            self.score += 100
            self.score += self.t * 10

        self.t = 2

    def eliminateOne(self):
        text = self.records[self.indexes[self.nrFrame - 1]][5]
        buttons = [button for button in [self.btn1, self.btn2, self.btn3, self.btn4] if button['text'] != text]
        index = random.randint(0,2)
        buttons[index]['state'] = 'disabled'
        self.oneOutCount -= 1
        self.score -= 25
        self.btnOneOut['state'] = 'disabled'
        self.btnTwoOut['state'] = 'disabled'

    def eliminateTwo(self):
        text = self.records[self.indexes[self.nrFrame - 1]][5]
        buttons = [button for button in [self.btn1, self.btn2, self.btn3, self.btn4] if button['text'] != text]
        indexes = random.sample(range(0, 3), 2)
        buttons[indexes[0]]['state'] = 'disabled'
        buttons[indexes[1]]['state'] = 'disabled'
        self.twoOutCount -= 1
        self.score -= 50
        self.btnOneOut['state'] = 'disabled'
        self.btnTwoOut['state'] = 'disabled'


    def kill(self):
        del self
        gc.collect()

    def abort(self):
        del app.frames[Game]




class GamePvP(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.configure(bg = "#fee6cd")

        self.scorPlayer1 = 0
        self.scorPlayer2 = 0

        self.numePlayer1 = ''
        self.numePlayer2 = ''

        self.rspCorect1 = 0
        self.rspCorect2 = 0

        self.isPlaying1 = False
        self.isPlaying2 = False

        self.t = 15
        self.oneOutCount = 3
        self.twoOutCount = 2
        self.nr_frame = 0
        self.score = 0
        self.corecte = 0


        self.imgBtnStart = PhotoImage(file="pictures/btnStart.png")
        self.imgBtnStartDark = PhotoImage(file="pictures/btnStartDark.png")
        self.imgBtnQst = PhotoImage(file="pictures/btnQst.png")
        self.imgBtnQstDark = PhotoImage(file="pictures/btnQstDark.png")
        self.imgBtnUtils = PhotoImage(file = "pictures/btnUtils.png")
        self.imgBtnUtilsDark = PhotoImage(file="pictures/btnUtilsDark.png")
        self.imgBtnQstRight = PhotoImage(file = "pictures/btnQstRight.png")
        self.imgBtnQstWrong = PhotoImage(file = "pictures/btnQstWrong.png")


        self.conn = sqlite3.connect('mdsproject.db')
        self.c = self.conn.cursor()

        self.c.execute("SELECT * FROM biologie UNION SELECT * FROM chimie UNION SELECT * FROM arte_divertisment UNION SELECT * FROM istorie UNION SELECT * FROM geografie UNION SELECT * FROM matematica UNION SELECT * FROM sport UNION SELECT * FROM diverse")


        self.records = self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        self.indexes = random.sample(range(0, len(self.records)), 20)


        self.container = LabelFrame(self,width = 920, height = 630, bg = "#fee6cd", border = 1, relief = SUNKEN)
        self.container.pack(pady = 10)

        self.lblPlayer1 = Label(self.container, text="Player 1", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblPlayer1.place(x=420, y=20)

        self.entryPlayer1 = Entry(self.container, font=("Rokkitt", 20), fg="#b05e11")
        self.entryPlayer1.place(x=325, y=80)

        self.lblPlayer2 = Label(self.container, text="Player 2", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblPlayer2.place(x=420, y=140)

        self.entryPlayer2 = Entry(self.container, font=("Rokkitt", 20), fg="#b05e11")
        self.entryPlayer2.place(x=325, y=200)

        self.lblWarning = Label(self, text="", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="red")
        self.lblWarning.place(x=340, y=320)


        self.btnStart = Button(self.container, compound=CENTER, height=80, image=self.imgBtnStart, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="START",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = self.pressStart)
        self.btnStart.bind("<Enter>", lambda event: self.btnStart.configure(image=self.imgBtnStartDark))
        self.btnStart.bind("<Leave>", lambda event: self.btnStart.configure(image=self.imgBtnStart))
        self.btnStart.place(x=350, y=400)

        self.lbl = Label()
        self.qst = Message()
        self.btn1 = Button()
        self.btn2 = Button()
        self.btn3 = Button()
        self.btn4 = Button()

        self.btnQuit = Button()
        self.btnOneOut = Button()
        self.btnTwoOut = Button()

        self.lblScore = Label()

    def pressStart(self):
        numePlayer1 = self.entryPlayer1.get()
        numePlayer2 = self.entryPlayer2.get()

        if not numePlayer1 or not numePlayer2 or numePlayer1 == numePlayer2:
            self.lblWarning.configure(text="Nume diferite obligatorii!", fg="red")
            self.lblWarning.after(1500, lambda: self.lblWarning.configure(text=""))
        else:
            self.numePlayer1 = numePlayer1
            self.numePlayer2 = numePlayer2
            self.isPlaying1 = True
            self.beginTest()

    def beginTest(self):
        self.container.destroy()
        self.createNewFrame(self.nr_frame)

    def countdown(self):
        if self.t>0:
            if not self.btnPressed:
                self.lbl.config(text = str(self.t))
            self.t -= 1
            self.lbl.after(1000, self.countdown)
        elif self.t == 0:
            self.container.destroy()
            self.btnQuit.destroy()
            self.btnOneOut.destroy()
            self.btnTwoOut.destroy()
            if self.nr_frame<20:
                self.t = 15
                self.createNewFrame(self.nr_frame)
            elif self.nr_frame == 20:

                if self.isPlaying2:
                    self.scorPlayer2 = self.score
                    self.rspCorect2 = self.corecte

                    self.isPlaying2 = False

                    self.lblResultPlayer1 = Label(self, font=("Rokkitt", 22, "bold"), bg="#fee6cd", fg="#b05e11",
                                          text=self.numePlayer1 +" a obtinut scorul " + str(self.scorPlayer1) + " cu "
                                               + str(self.rspCorect1) + " intrebari corecte!")
                    self.lblResultPlayer1.pack(pady=(100, 0))

                    self.lblResultPlayer2 = Label(self, font=("Rokkitt", 22, "bold"), bg="#fee6cd", fg="#b05e11",
                                                  text=self.numePlayer2 + " a obtinut scorul " + str(
                                                      self.scorPlayer2) + " cu "
                                                       + str(self.rspCorect2) + " intrebari corecte!")
                    self.lblResultPlayer2.pack(pady=(50, 0))

                    self.lblResult = Label(self, font=("Rokkitt", 24, "bold"), bg="#fee6cd", fg="green",
                                                  text="")
                    self.lblResult.pack(pady=(50, 0))

                    if self.scorPlayer1 > self.scorPlayer2:
                        self.lblResult.configure(text = "Castigator: " + self.numePlayer1)
                    elif self.scorPlayer1 < self.scorPlayer2:
                        self.lblResult.configure(text="Castigator: " + self.numePlayer2)
                    else:
                        if self.rspCorect1 > self.rspCorect2:
                            self.lblResult.configure(text="Castigator: " + self.numePlayer1)
                        elif self.rspCorect1 < self.rspCorect2:
                            self.lblResult.configure(text="Castigator: " + self.numePlayer2)
                        else:
                            self.lblResult.configure(text="Remiza!")

                    self.btnQuit = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                                          activebackground="#fee6cd", activeforeground="#af4343",
                                          font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                                          text="QUIT",
                                          command=lambda: [self.abort(), app.show_frame(MainMenu), self.destroy(),
                                                           self.kill()])
                    self.btnQuit.bind("<Enter>", lambda event: self.btnQuit.configure(image=self.imgBtnUtilsDark))
                    self.btnQuit.bind("<Leave>", lambda event: self.btnQuit.configure(image=self.imgBtnUtils))
                    self.btnQuit.pack(padx=(50, 0), pady=(120, 0), side=LEFT)

                if self.isPlaying1:
                    self.scorPlayer1 = self.score
                    self.rspCorect1 = self.corecte

                    self.t = 15
                    self.oneOutCount = 3
                    self.twoOutCount = 2
                    self.nr_frame = 0
                    self.score = 0
                    self.corecte = 0

                    self.isPlaying1 = False
                    self.isPlaying2 = True

                    random.shuffle(self.indexes)

                    self.lblReady = Label(self, font=("Rokkitt", 36, "bold"), bg="#fee6cd", fg="#b05e11",
                                          text="Ready Player 2?")
                    self.lblReady.pack(pady=(100, 0))

                    self.btnGo = Button(self, compound=CENTER, height=80, image=self.imgBtnStart, border=0,
                                        activebackground="#fee6cd", activeforeground="#af4343", text="GO",
                                        font=("Rokkitt", 25, "bold"),
                                        bg="#fee6cd", fg="#af4343",
                                        command=lambda: [self.lblReady.destroy(), self.btnGo.destroy(),
                                                         self.btnQuit.destroy(), self.createNewFrame(self.nr_frame)])
                    self.btnGo.bind("<Enter>", lambda event: self.btnGo.configure(image=self.imgBtnStartDark))
                    self.btnGo.bind("<Leave>", lambda event: self.btnGo.configure(image=self.imgBtnStart))
                    self.btnGo.pack(pady=(50, 0))

                    self.btnQuit = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                                          activebackground="#fee6cd", activeforeground="#af4343",
                                          font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                                          text="QUIT",
                                          command=lambda: [self.abort(), app.show_frame(MainMenu), self.destroy(),
                                                           self.kill()])
                    self.btnQuit.bind("<Enter>", lambda event: self.btnQuit.configure(image=self.imgBtnUtilsDark))
                    self.btnQuit.bind("<Leave>", lambda event: self.btnQuit.configure(image=self.imgBtnUtils))
                    self.btnQuit.pack(padx=(50, 0), pady=(120, 0), side=LEFT)





    def createNewFrame(self, number):
        self.btnPressed = False
        self.container = LabelFrame(self, width=920, height=630, bg="#fee6cd", border=0, relief=SUNKEN)
        self.container.pack(pady=10)

        randomIndex = random.sample([1, 2, 3, 4], 4)

        self.lbl = Label(self.container, font=("Rokkitt", 30, "bold"), bg = "#fee6cd", fg = "#b05e11")
        self.lbl.pack()

        self.qst = Message(self.container, width = 700, justify = CENTER, font=("Rokkitt", 18), bg = "#fee6cd", fg = "#b05e11",
                           text = self.records[self.indexes[number]][0])
        self.qst.pack(fill = BOTH)

        self.btn1 = Button(self.container, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                                activebackground="#fee6cd", activeforeground="#af4343",
                                font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text = self.records[self.indexes[number]][randomIndex[0]], command= lambda: self.btnClicked(self.btn1))
        self.btn1.bind("<Enter>", lambda event: self.btn1.configure(image=self.imgBtnQstDark))
        self.btn1.bind("<Leave>", lambda event: self.btn1.configure(image=self.imgBtnQst))
        self.btn1.pack(pady = (30,0))

        self.btn2 = Button(self.container, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records[self.indexes[number]][randomIndex[1]], command= lambda: self.btnClicked(self.btn2))
        self.btn2.bind("<Enter>", lambda event: self.btn2.configure(image=self.imgBtnQstDark))
        self.btn2.bind("<Leave>", lambda event: self.btn2.configure(image=self.imgBtnQst))
        self.btn2.pack(pady = (20,0))

        self.btn3 = Button(self.container, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records[self.indexes[number]][randomIndex[2]], command= lambda: self.btnClicked(self.btn3))
        self.btn3.bind("<Enter>", lambda event: self.btn3.configure(image=self.imgBtnQstDark))
        self.btn3.bind("<Leave>", lambda event: self.btn3.configure(image=self.imgBtnQst))
        self.btn3.pack(pady = (20,0))

        self.btn4 = Button(self.container, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records[self.indexes[number]][randomIndex[3]], command= lambda: self.btnClicked(self.btn4))
        self.btn4.bind("<Enter>", lambda event: self.btn4.configure(image=self.imgBtnQstDark))
        self.btn4.bind("<Leave>", lambda event: self.btn4.configure(image=self.imgBtnQst))
        self.btn4.pack(pady = (20,0))

        self.btnQuit = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343",
                              font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                              text="QUIT",
                              command=lambda: [self.abort(), app.show_frame(MainMenu), self.destroy(),
                                               self.kill()])
        self.btnQuit.bind("<Enter>", lambda event: self.btnQuit.configure(image=self.imgBtnUtilsDark))
        self.btnQuit.bind("<Leave>", lambda event: self.btnQuit.configure(image=self.imgBtnUtils))
        self.btnQuit.pack(padx = (92,30), pady=(20, 0), side=LEFT)

        self.btnOneOut = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343",
                              font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                              text="Eliminate 1", command = self.eliminateOne)
        self.btnOneOut.bind("<Enter>", lambda event: self.btnOneOut.configure(image=self.imgBtnUtilsDark))
        self.btnOneOut.bind("<Leave>", lambda event: self.btnOneOut.configure(image=self.imgBtnUtils))
        self.btnOneOut.pack(padx=(30, 30), pady=(20, 0), side=LEFT)

        if(self.oneOutCount == 0):
            self.btnOneOut.configure(state = 'disabled')

        self.btnTwoOut = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                                activebackground="#fee6cd", activeforeground="#af4343",
                                font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                                text="Eliminate 2", command = self.eliminateTwo)
        self.btnTwoOut.bind("<Enter>", lambda event: self.btnTwoOut.configure(image=self.imgBtnUtilsDark))
        self.btnTwoOut.bind("<Leave>", lambda event: self.btnTwoOut.configure(image=self.imgBtnUtils))
        self.btnTwoOut.pack(padx=(30, 30), pady=(20, 0), side=LEFT)

        if (self.twoOutCount == 0):
            self.btnTwoOut.configure(state='disabled')

        self.nr_frame += 1
        self.countdown()

    def btnClicked(self, btn):
        self.btnPressed = True
        text = self.records[self.indexes[self.nr_frame - 1]][5]
        self.lbl.configure(text = "")
        self.btn1['command'] = 0
        self.btn2['command'] = 0
        self.btn3['command'] = 0
        self.btn4['command'] = 0

        self.btn1.unbind("<Enter>")
        self.btn2.unbind("<Enter>")
        self.btn3.unbind("<Enter>")
        self.btn4.unbind("<Enter>")
        self.btn1.unbind("<Leave>")
        self.btn2.unbind("<Leave>")
        self.btn3.unbind("<Leave>")
        self.btn4.unbind("<Leave>")

        self.btnOneOut['state'] = 'disabled'
        self.btnTwoOut['state'] = 'disabled'

        self.btn1.configure(image=self.imgBtnQstWrong, fg = "black", activeforeground = "black", relief = SUNKEN)
        self.btn2.configure(image=self.imgBtnQstWrong, fg = "black", activeforeground = "black", relief = SUNKEN)
        self.btn3.configure(image=self.imgBtnQstWrong, fg = "black", activeforeground = "black", relief = SUNKEN)
        self.btn4.configure(image=self.imgBtnQstWrong, fg = "black", activeforeground = "black", relief = SUNKEN)

        if text == self.btn1['text']:
            self.btn1.configure(image=self.imgBtnQstRight)
        if text == self.btn2['text']:
            self.btn2.configure(image=self.imgBtnQstRight)
        if text == self.btn3['text']:
            self.btn3.configure(image=self.imgBtnQstRight)
        if text == self.btn4['text']:
            self.btn4.configure(image=self.imgBtnQstRight)

        if text == btn['text']:
            self.score += 100
            self.score += self.t * 10
            self.corecte += 1

        self.t = 2

    def eliminateOne(self):
        text = self.records[self.indexes[self.nr_frame - 1]][5]
        buttons = [button for button in [self.btn1, self.btn2, self.btn3, self.btn4] if button['text'] != text]
        index = random.randint(0,2)
        buttons[index]['state'] = 'disabled'
        self.oneOutCount -= 1
        self.score -= 25
        self.btnOneOut['state'] = 'disabled'
        self.btnTwoOut['state'] = 'disabled'

    def eliminateTwo(self):
        text = self.records[self.indexes[self.nr_frame - 1]][5]
        buttons = [button for button in [self.btn1, self.btn2, self.btn3, self.btn4] if button['text'] != text]
        indexes = random.sample(range(0, 3), 2)
        buttons[indexes[0]]['state'] = 'disabled'
        buttons[indexes[1]]['state'] = 'disabled'
        self.twoOutCount -= 1
        self.score -= 50
        self.btnOneOut['state'] = 'disabled'
        self.btnTwoOut['state'] = 'disabled'


    def kill(self):
        del self
        gc.collect()

    def abort(self):
        del app.frames[GamePvP]



class GamePvPSr(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.configure(bg = "#fee6cd")

        self.numePlayer1 = ''
        self.numePlayer2 = ''

        self.rspCorect1 = 0
        self.rspCorect2 = 0

        self.rspGresit1 = 0
        self.rspGresit2 = 0

        self.nrFrame1 = 0
        self.nrFrame2 = 0

        self.quitPressed1 = False
        self.quitPressed2 = False

        self.t = 200



        self.imgBtnStart = PhotoImage(file="pictures/btnStart.png")
        self.imgBtnStartDark = PhotoImage(file="pictures/btnStartDark.png")
        self.imgBtnQst = PhotoImage(file="pictures/btnQst.png")
        self.imgBtnQstDark = PhotoImage(file="pictures/btnQstDark.png")
        self.imgBtnUtils = PhotoImage(file = "pictures/btnUtils.png")
        self.imgBtnUtilsDark = PhotoImage(file="pictures/btnUtilsDark.png")
        self.imgBtnQstRight = PhotoImage(file = "pictures/btnQstRight.png")
        self.imgBtnQstWrong = PhotoImage(file = "pictures/btnQstWrong.png")


        self.conn = sqlite3.connect('mdsproject.db')
        self.c = self.conn.cursor()

        self.c.execute("SELECT * FROM biologie UNION SELECT * FROM chimie UNION SELECT * FROM arte_divertisment UNION SELECT * FROM istorie UNION SELECT * FROM geografie UNION SELECT * FROM matematica UNION SELECT * FROM sport UNION SELECT * FROM diverse")


        self.records1 = self.c.fetchall()
        self.records2 = copy.deepcopy(self.records1)

        self.conn.commit()
        self.conn.close()

        random.shuffle(self.records1)
        random.shuffle(self.records2)


        self.container = LabelFrame(self,width = 920, height = 630, bg = "#fee6cd", border = 1, relief = SUNKEN)
        self.container.pack(pady = 10)

        self.lblPlayer1 = Label(self.container, text="Player 1", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblPlayer1.place(x=420, y=20)

        self.entryPlayer1 = Entry(self.container, font=("Rokkitt", 20), fg="#b05e11")
        self.entryPlayer1.place(x=325, y=80)

        self.lblPlayer2 = Label(self.container, text="Player 2", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblPlayer2.place(x=420, y=140)

        self.entryPlayer2 = Entry(self.container, font=("Rokkitt", 20), fg="#b05e11")
        self.entryPlayer2.place(x=325, y=200)

        self.lblWarning = Label(self, text="", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="red")
        self.lblWarning.place(x=340, y=320)


        self.btnStart = Button(self.container, compound=CENTER, height=80, image=self.imgBtnStart, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="START",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343", command = self.pressStart)
        self.btnStart.bind("<Enter>", lambda event: self.btnStart.configure(image=self.imgBtnStartDark))
        self.btnStart.bind("<Leave>", lambda event: self.btnStart.configure(image=self.imgBtnStart))
        self.btnStart.place(x=350, y=400)

        self.lblInfo = Label(self.container, text="Player1: A,S,D,F, X-pass | Player2: H,J,K,L, M-pass", font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="#b05e11")
        self.lblInfo.place(x = 180, y = 550)

        self.lblTime = Label()

        self.qstP1 = Message()
        self.btn1P1 = Button()
        self.btn2P1 = Button()
        self.btn3P1 = Button()
        self.btn4P1 = Button()
        self.holder1 = LabelFrame()

        self.qstP2 = Message()
        self.btn1P2 = Button()
        self.btn2P2 = Button()
        self.btn3P2 = Button()
        self.btn4P2 = Button()
        self.holder2 = LabelFrame()

        self.framePlayers = LabelFrame()

        self.framePlayer1 = LabelFrame()
        self.framePlayer2 = LabelFrame()

        self.btnPass1 = Button()
        self.btnPass2 = Button()

        self.btnQuit = Button()



    def pressStart(self):
        numePlayer1 = self.entryPlayer1.get()
        numePlayer2 = self.entryPlayer2.get()

        if not numePlayer1 or not numePlayer2 or numePlayer1 == numePlayer2:
            self.lblWarning.configure(text="Nume diferite obligatorii!", fg="red")
            self.lblWarning.after(1500, lambda: self.lblWarning.configure(text=""))
        else:
            self.numePlayer1 = numePlayer1
            self.numePlayer2 = numePlayer2
            app.geometry("1500x700+10+30")
            self.container.destroy()

            self.lblTime = Label(self, font=("Rokkitt", 20, "bold"), bg="#fee6cd", fg="#b05e11", text="200")
            self.lblTime.pack()

            self.framePlayers = LabelFrame(self, width = 1500, height = 650, border = 0, bg = "#fee6cd")
            self.framePlayers.pack(fill = BOTH, padx = 0, pady = 0, anchor = CENTER, expand = 1)
            self.framePlayers.focus_force()

            self.framePlayer1 = LabelFrame(self.framePlayers, bg = "#fee6cd", border = 1, relief = SUNKEN)
            self.framePlayer2 = LabelFrame(self.framePlayers, bg = "#fee6cd", border = 1, relief = SUNKEN)

            self.framePlayer1.grid(row=0, column=0, sticky="nsew", padx=(5,2), pady=2)
            self.framePlayer2.grid(row=0, column=1, sticky="nsew", padx=(2,5), pady=2)

            self.framePlayers.grid_columnconfigure(0, weight=1, uniform="group1")
            self.framePlayers.grid_columnconfigure(1, weight=1, uniform="group1")
            self.framePlayers.grid_rowconfigure(0, weight=1)

            self.btnQuit = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                                   activebackground="#fee6cd", activeforeground="#af4343",
                                   font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                                   text="QUIT",

                                    command=self.finish
                                   )
            self.btnQuit.bind("<Enter>", lambda event: self.btnQuit.configure(image=self.imgBtnUtilsDark))
            self.btnQuit.bind("<Leave>", lambda event: self.btnQuit.configure(image=self.imgBtnUtils))
            self.btnQuit.pack()

            self.createNewFramePlayer1(self.nrFrame1)
            self.createNewFramePlayer2(self.nrFrame2)
            self.countdown()

    def createNewFramePlayer1(self, number):
        self.btnPressed = False
        self.holder1 = LabelFrame(self.framePlayer1, width=920, height=630, bg="#fee6cd", border=0, relief=SUNKEN)
        self.holder1.pack(pady=10)

        randomIndex = random.sample([1, 2, 3, 4], 4)

        self.qstP1 = Message(self.holder1, width=700, justify=CENTER, font=("Rokkitt", 18), bg="#fee6cd", fg="#b05e11",
                           text=self.records1[number][0])
        self.qstP1.pack(fill=BOTH)

        self.btn1P1 = Button(self.holder1, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records1[number][randomIndex[0]], command=lambda: self.btnClicked1(self.btn1P1))
        self.framePlayers.bind('<a>', lambda a: self.btnClicked1(self.btn1P1, a))
        self.btn1P1.bind("<Enter>", lambda event: self.btn1P1.configure(image=self.imgBtnQstDark))
        self.btn1P1.bind("<Leave>", lambda event: self.btn1P1.configure(image=self.imgBtnQst))
        self.btn1P1.pack(pady=(30, 0))

        self.btn2P1 = Button(self.holder1, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records1[number][randomIndex[1]], command=lambda: self.btnClicked1(self.btn2P1))
        self.framePlayers.bind('<s>', lambda a: self.btnClicked1(self.btn2P1, a))
        self.btn2P1.bind("<Enter>", lambda event: self.btn2P1.configure(image=self.imgBtnQstDark))
        self.btn2P1.bind("<Leave>", lambda event: self.btn2P1.configure(image=self.imgBtnQst))
        self.btn2P1.pack(pady=(20, 0))

        self.btn3P1 = Button(self.holder1, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records1[number][randomIndex[2]], command=lambda: self.btnClicked1(self.btn3P1))
        self.framePlayers.bind('<d>', lambda a: self.btnClicked1(self.btn3P1, a))
        self.btn3P1.bind("<Enter>", lambda event: self.btn3P1.configure(image=self.imgBtnQstDark))
        self.btn3P1.bind("<Leave>", lambda event: self.btn3P1.configure(image=self.imgBtnQst))
        self.btn3P1.pack(pady=(20, 0))

        self.btn4P1 = Button(self.holder1, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records1[number][randomIndex[3]], command=lambda: self.btnClicked1(self.btn4P1))
        self.framePlayers.bind('<f>', lambda a: self.btnClicked1(self.btn4P1, a))
        self.btn4P1.bind("<Enter>", lambda event: self.btn4P1.configure(image=self.imgBtnQstDark))
        self.btn4P1.bind("<Leave>", lambda event: self.btn4P1.configure(image=self.imgBtnQst))
        self.btn4P1.pack(pady=(20, 0))

        self.btnPass1 = Button(self.framePlayer1, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                               activebackground="#fee6cd", activeforeground="#af4343",
                               font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                               text="PASS",

                                command=lambda: [self.holder1.destroy(),
                                                self.btnPass1.destroy(),
                                                 self.createNewFramePlayer1(self.nrFrame1)]
                               )
        self.framePlayers.bind('<x>', lambda a: [self.holder1.destroy(),
                                                 self.btnPass1.destroy(),
                                                 self.createNewFramePlayer1(self.nrFrame1)])
        self.btnPass1.bind("<Enter>", lambda event: self.btnPass1.configure(image=self.imgBtnUtilsDark))
        self.btnPass1.bind("<Leave>", lambda event: self.btnPass1.configure(image=self.imgBtnUtils))
        self.btnPass1.pack(pady=(20, 0))

        self.nrFrame1 += 1



    def btnClicked1(self, btn, event = None):

        text = self.records1[self.nrFrame1-1][5]
        self.btn1P1['command'] = 0
        self.btn2P1['command'] = 0
        self.btn3P1['command'] = 0
        self.btn4P1['command'] = 0

        self.btn1P1.unbind("<Enter>")
        self.btn2P1.unbind("<Enter>")
        self.btn3P1.unbind("<Enter>")
        self.btn4P1.unbind("<Enter>")
        self.btn1P1.unbind("<Leave>")
        self.btn2P1.unbind("<Leave>")
        self.btn3P1.unbind("<Leave>")
        self.btn4P1.unbind("<Leave>")
        self.framePlayers.unbind('<a>')
        self.framePlayers.unbind('<s>')
        self.framePlayers.unbind('<d>')
        self.framePlayers.unbind('<f>')
        self.framePlayers.unbind('<x>')


        self.btn1P1.configure(image=self.imgBtnQstWrong, fg="black", activeforeground="black", relief=SUNKEN)
        self.btn2P1.configure(image=self.imgBtnQstWrong, fg="black", activeforeground="black", relief=SUNKEN)
        self.btn3P1.configure(image=self.imgBtnQstWrong, fg="black", activeforeground="black", relief=SUNKEN)
        self.btn4P1.configure(image=self.imgBtnQstWrong, fg="black", activeforeground="black", relief=SUNKEN)

        if text == self.btn1P1['text']:
            self.btn1P1.configure(image=self.imgBtnQstRight)
        if text == self.btn2P1['text']:
            self.btn2P1.configure(image=self.imgBtnQstRight)
        if text == self.btn3P1['text']:
            self.btn3P1.configure(image=self.imgBtnQstRight)
        if text == self.btn4P1['text']:
            self.btn4P1.configure(image=self.imgBtnQstRight)

        if text == btn['text']:
            self.rspCorect1 += 1
        else:
            self.rspGresit1 += 1

        timer = Timer(0.800, lambda: [self.holder1.destroy(), self.btnPass1.destroy(),
                                      self.createNewFramePlayer1(self.nrFrame1)])
        timer.start()



    def createNewFramePlayer2(self, number):
        self.btnPressed = False
        self.holder2 = LabelFrame(self.framePlayer2, width=920, height=630, bg="#fee6cd", border=0, relief=SUNKEN)
        self.holder2.pack(pady=10)

        randomIndex = random.sample([1, 2, 3, 4], 4)

        self.qstP2 = Message(self.holder2, width=700, justify=CENTER, font=("Rokkitt", 18), bg="#fee6cd", fg="#b05e11",
                           text=self.records2[number][0])
        self.qstP2.pack(fill=BOTH)

        self.btn1P2 = Button(self.holder2, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records2[number][randomIndex[0]], command=lambda: self.btnClicked2(self.btn1P2))
        self.framePlayers.bind('<h>', lambda a: self.btnClicked2(self.btn1P2, a))
        self.btn1P2.bind("<Enter>", lambda event: self.btn1P2.configure(image=self.imgBtnQstDark))
        self.btn1P2.bind("<Leave>", lambda event: self.btn1P2.configure(image=self.imgBtnQst))
        self.btn1P2.pack(pady=(30, 0))

        self.btn2P2 = Button(self.holder2, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records2[number][randomIndex[1]], command=lambda: self.btnClicked2(self.btn2P2))
        self.framePlayers.bind('<j>', lambda a: self.btnClicked2(self.btn2P2, a))
        self.btn2P2.bind("<Enter>", lambda event: self.btn2P2.configure(image=self.imgBtnQstDark))
        self.btn2P2.bind("<Leave>", lambda event: self.btn2P2.configure(image=self.imgBtnQst))
        self.btn2P2.pack(pady=(20, 0))

        self.btn3P2 = Button(self.holder2, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records2[number][randomIndex[2]], command=lambda: self.btnClicked2(self.btn3P2))
        self.framePlayers.bind('<k>', lambda a: self.btnClicked2(self.btn3P2, a))
        self.btn3P2.bind("<Enter>", lambda event: self.btn3P2.configure(image=self.imgBtnQstDark))
        self.btn3P2.bind("<Leave>", lambda event: self.btn3P2.configure(image=self.imgBtnQst))
        self.btn3P2.pack(pady=(20, 0))

        self.btn4P2 = Button(self.holder2, compound=CENTER, height=55, image=self.imgBtnQst, border=0,
                           activebackground="#fee6cd", activeforeground="#af4343",
                           font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                           text=self.records2[number][randomIndex[3]], command=lambda: self.btnClicked2(self.btn4P2))
        self.framePlayers.bind('<l>', lambda a: self.btnClicked2(self.btn4P2, a))
        self.btn4P2.bind("<Enter>", lambda event: self.btn4P2.configure(image=self.imgBtnQstDark))
        self.btn4P2.bind("<Leave>", lambda event: self.btn4P2.configure(image=self.imgBtnQst))
        self.btn4P2.pack(pady=(20, 0))


        self.btnPass2 = Button(self.framePlayer2, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                               activebackground="#fee6cd", activeforeground="#af4343",
                               font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                               text="PASS",

                                command=lambda: [self.holder2.destroy(),
                                                self.btnPass2.destroy(),
                                                 self.createNewFramePlayer2(self.nrFrame2)]
                               )
        self.framePlayers.bind('<m>', lambda a: [self.holder2.destroy(),
                                                self.btnPass2.destroy(),
                                                 self.createNewFramePlayer2(self.nrFrame2)])
        self.btnPass2.bind("<Enter>", lambda event: self.btnPass2.configure(image=self.imgBtnUtilsDark))
        self.btnPass2.bind("<Leave>", lambda event: self.btnPass2.configure(image=self.imgBtnUtils))
        self.btnPass2.pack(pady=(20, 0))

        self.nrFrame2 += 1

    def btnClicked2(self, btn, event = None):

        text = self.records2[self.nrFrame2-1][5]
        self.btn1P2['command'] = 0
        self.btn2P2['command'] = 0
        self.btn3P2['command'] = 0
        self.btn4P2['command'] = 0

        self.btn1P2.unbind("<Enter>")
        self.btn2P2.unbind("<Enter>")
        self.btn3P2.unbind("<Enter>")
        self.btn4P2.unbind("<Enter>")
        self.btn1P2.unbind("<Leave>")
        self.btn2P2.unbind("<Leave>")
        self.btn3P2.unbind("<Leave>")
        self.btn4P2.unbind("<Leave>")
        self.framePlayers.unbind('<h>')
        self.framePlayers.unbind('<j>')
        self.framePlayers.unbind('<k>')
        self.framePlayers.unbind('<l>')
        self.framePlayers.unbind('<m>')


        self.btn1P2.configure(image=self.imgBtnQstWrong, fg="black", activeforeground="black", relief=SUNKEN)
        self.btn2P2.configure(image=self.imgBtnQstWrong, fg="black", activeforeground="black", relief=SUNKEN)
        self.btn3P2.configure(image=self.imgBtnQstWrong, fg="black", activeforeground="black", relief=SUNKEN)
        self.btn4P2.configure(image=self.imgBtnQstWrong, fg="black", activeforeground="black", relief=SUNKEN)

        if text == self.btn1P2['text']:
            self.btn1P2.configure(image=self.imgBtnQstRight)
        if text == self.btn2P2['text']:
            self.btn2P2.configure(image=self.imgBtnQstRight)
        if text == self.btn3P2['text']:
            self.btn3P2.configure(image=self.imgBtnQstRight)
        if text == self.btn4P2['text']:
            self.btn4P2.configure(image=self.imgBtnQstRight)

        if text == btn['text']:
            self.rspCorect2 += 1
        else:
            self.rspGresit2 += 1


        timer = Timer(0.800, lambda: [self.holder2.destroy(), self.btnPass2.destroy(), self.createNewFramePlayer2(self.nrFrame2)])
        timer.start()




    def kill(self):
        del self
        gc.collect()

    def abort(self):
        del app.frames[GamePvPSr]


    def countdown(self):
        if self.t>0:
            self.lblTime.config(text = str(self.t))
            self.t -= 1
            self.lblTime.after(1000, self.countdown)
        elif self.t == 0:
            self.finish()

    def finish(self):
        self.lblTime.destroy()
        self.framePlayers.destroy()
        self.btnQuit.destroy()
        app.geometry("950x650+200+10")

        lblResultPlayer1 = Label(self, font=("Rokkitt", 22, "bold"), bg="#fee6cd", fg="#b05e11",
                                 text=self.numePlayer1 + " a obtinut scorul : " + str(self.rspCorect1) + " corecte, "
                                      + str(self.rspGresit1) + " gresite!")
        lblResultPlayer1.pack(pady=(100, 0))

        lblResultPlayer2 = Label(self, font=("Rokkitt", 22, "bold"), bg="#fee6cd", fg="#b05e11",
                                 text=self.numePlayer2 + " a obtinut scorul : " + str(self.rspCorect2) + " corecte, "
                                      + str(self.rspGresit2) + " gresite!")
        lblResultPlayer2.pack(pady=(50, 0))

        self.btnQuit = Button(self, compound=CENTER, height=55, image=self.imgBtnUtils, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343",
                              font=("Rokkitt", 15), bg="#fee6cd", fg="#af4343",
                              text="QUIT",
                              command=lambda: [self.abort(), app.show_frame(MainMenu), self.destroy(),
                                               self.kill()])
        self.btnQuit.bind("<Enter>", lambda event: self.btnQuit.configure(image=self.imgBtnUtilsDark))
        self.btnQuit.bind("<Leave>", lambda event: self.btnQuit.configure(image=self.imgBtnUtils))
        self.btnQuit.pack(pady=(120, 0))


app = Root()
app.mainloop()
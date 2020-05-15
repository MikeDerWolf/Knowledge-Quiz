from tkinter import *
from PIL import ImageTk, Image
import pygame
import sqlite3
import gc
import random

pygame.init()
pygame.mixer.music.load("RUDE - Eternal Youth.mp3")
pygame.mixer.music.play(loops=-1)
volumeLevels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
initialVolumeIndex = 4
pygame.mixer.music.set_volume(volumeLevels[initialVolumeIndex])


class Root(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Knowledge Quiz")
        self.geometry("950x650+200+50")
        self.iconbitmap('brainlogo.ico')
        self.resizable(0, 0)
        # Setup Frame
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.pageList = [MainMenu, Settings, GameMode, Category]

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

        self.backgroundImage = ImageTk.PhotoImage(Image.open("backgroundMainMenu.jpg"))
        self.backgroundLabel = Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.imgBtn = PhotoImage(file = "btnMenu.png")
        self.imgBtnPress = PhotoImage(file = "btnMenuDark.png")

        self.btnPlay = Button(self, compound=CENTER, text="PLAY", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="#68a302",
                              bg="#fee2cd", activebackground="#fee2cd", activeforeground="#68a302", command=lambda: controller.show_frame(GameMode))  # 7eba00
        self.btnPlay.bind("<Enter>", lambda event: self.btnPlay.configure(image = self.imgBtnPress))
        self.btnPlay.bind("<Leave>", lambda event: self.btnPlay.configure(image=self.imgBtn))
        self.btnPlay.pack(pady=(225, 10), padx=30)

        self.btnTopScore = Button(self, compound=CENTER, text="TOP SCORE", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="#6f54b8",
                                  bg="#fee2cd", activebackground="#fee2cd", activeforeground="#6f54b8", command=self.createTopScore)
        self.btnTopScore.bind("<Enter>", lambda event: self.btnTopScore.configure(image = self.imgBtnPress))
        self.btnTopScore.bind("<Leave>", lambda event: self.btnTopScore.configure(image=self.imgBtn))
        self.btnTopScore.pack(pady=10, padx=30)

        self.btnSettings = Button(self, compound=CENTER, text="SETTINGS", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="#01728f",
                                  bg="#fee1cf", activebackground="#fee1cf", activeforeground="#01728f", command=lambda: controller.show_frame(Settings))
        self.btnSettings.bind("<Enter>", lambda event: self.btnSettings.configure(image = self.imgBtnPress))
        self.btnSettings.bind("<Leave>", lambda event: self.btnSettings.configure(image = self.imgBtn))
        self.btnSettings.pack(pady=10, padx=30)

        self.btnExit = Button(self, compound=CENTER, text="EXIT", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="red",
                              bg="#fee2d4", activebackground="#fee2d4", activeforeground="red", command=self.quit)
        self.btnExit.bind("<Enter>", lambda event: self.btnExit.configure(image = self.imgBtnPress))
        self.btnExit.bind("<Leave>", lambda event: self.btnExit.configure(image = self.imgBtn))
        self.btnExit.pack(pady=10, padx=30)

    def createTopScore(self):
        frame = TopScore(app.container, app)
        app.frames[TopScore] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        app.show_frame(TopScore)



class Settings(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.imgBtn = PhotoImage(file = "btnSettings.png")
        self.imgBtnPress = PhotoImage(file="btnSettingsDark.png")
        self.imgBtnDown = PhotoImage(file="btnSettingsDown.png")
        self.imgBtnUp = PhotoImage(file="btnSettingsUp.png")
        self.imgBtnDownDark = PhotoImage(file="btnSettingsDownDark.png")
        self.imgBtnUpDark = PhotoImage(file="btnSettingsUpDark.png")
        self.imgBtnBack = PhotoImage(file="btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="btnBackDark.png")

        self.backgroundImage = ImageTk.PhotoImage(Image.open("backgroundSettings.jpg"))
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

        self.backgroundImage = ImageTk.PhotoImage(Image.open("backgroundTopScore.jpg"))
        self.backgroundLabel = Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.imgBtnBack = PhotoImage(file="btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="btnBackDark.png")

        self.scoreFrame = LabelFrame(self, bg = "#cddbfe", relief = RAISED)
        self.scoreFrame.grid(row = 0, column = 1, pady = (175,0))

        self.scroll = Scrollbar(self.scoreFrame, bg = "#cddbfe")
        self.scroll.pack(side = RIGHT, fill = Y)

        self.scoreBox = Listbox(self.scoreFrame, width = 33, height = 11, font=("Rokkitt", 15), bg = "#ffdfbe", fg = "#7d3b00",
                                yscrollcommand = self.scroll.set, selectmode = SINGLE)
        self.scoreBox.pack(side = LEFT)

        self.scroll.configure(command = self.scoreBox.yview)

        self.conn = sqlite3.connect('mdsproject2.db')
        self.c = self.conn.cursor()

        self.c.execute("SELECT * FROM top_score ORDER BY score DESC")
        self.records = self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        for i in range(len(self.records)):
            self.scoreBox.insert(END, "  " + str(i+1) + ".     " + str(self.records[i][1]) + "          " + self.records[i][0])

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



class GameMode(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.backgroundImage = ImageTk.PhotoImage(Image.open("backgroundGameMode.jpg"))
        self.backgroundLabel = Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)


        self.imgBtnBack = PhotoImage(file="btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="btnBackDark.png")
        self.imgBtnSolo = PhotoImage(file="btnSolo.png")
        self.imgBtnSoloDark = PhotoImage(file="btnSoloDark.png")
        self.imgBtnPvp = PhotoImage(file="btnPvp.png")
        self.imgBtnPvpDark = PhotoImage(file="btnPvpDark.png")
        self.imgBtnPvpSr = PhotoImage(file="btnPvpSr.png")
        self.imgBtnPvpSrDark = PhotoImage(file="btnPvpSrDark.png")

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
                              bg="#fee6cd", fg="#af4343")
        self.btnPvp.bind("<Enter>", lambda event: self.btnPvp.configure(image=self.imgBtnPvpDark))
        self.btnPvp.bind("<Leave>", lambda event: self.btnPvp.configure(image=self.imgBtnPvp))
        self.btnPvp.grid(row = 1, column = 1)

        self.btnPvpSr = Button(self, compound=CENTER, height=190, image=self.imgBtnPvpSr, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="PvP\nSpeedrun",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343")
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



class Category(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.configure(bg = "#fee6cd")

        self.imgBtnBack = PhotoImage(file="btnBack.png")
        self.imgBtnBackDark = PhotoImage(file="btnBackDark.png")
        self.imgBtnMixed = PhotoImage(file="btnMixed.png")
        self.imgBtnMixedDark = PhotoImage(file="btnMixedDark.png")
        self.imgBtnMate = PhotoImage(file="btnMate.png")
        self.imgBtnMateDark = PhotoImage(file="btnMateDark.png")
        self.imgBtnArte = PhotoImage(file="btnArte.png")
        self.imgBtnArteDark = PhotoImage(file="btnArteDark.png")
        self.imgBtnBio = PhotoImage(file="btnBio.png")
        self.imgBtnBioDark = PhotoImage(file="btnBioDark.png")
        self.imgBtnIst = PhotoImage(file="btnIst.png")
        self.imgBtnIstDark = PhotoImage(file="btnIstDark.png")
        self.imgBtnSport = PhotoImage(file="btnSport.png")
        self.imgBtnSportDark = PhotoImage(file="btnSportDark.png")
        self.imgBtnChimie = PhotoImage(file="btnChimie.png")
        self.imgBtnChimieDark = PhotoImage(file="btnChimieDark.png")
        self.imgBtnGeo = PhotoImage(file="btnGeo.png")
        self.imgBtnGeoDark = PhotoImage(file="btnGeoDark.png")
        self.imgBtnDiv = PhotoImage(file="btnDiv.png")
        self.imgBtnDivDark = PhotoImage(file="btnDivDark.png")

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
                              bg="#fee6cd", fg="#af4343")
        self.btnMate.bind("<Enter>", lambda event: self.btnMate.configure(image=self.imgBtnMateDark))
        self.btnMate.bind("<Leave>", lambda event: self.btnMate.configure(image=self.imgBtnMate))
        self.btnMate.grid(row=2, column=0, padx=(40, 86), pady=(25,25))

        self.btnArte = Button(self, compound=CENTER, height=80, image=self.imgBtnArte, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="Arte",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343")
        self.btnArte.bind("<Enter>", lambda event: self.btnArte.configure(image=self.imgBtnArteDark))
        self.btnArte.bind("<Leave>", lambda event: self.btnArte.configure(image=self.imgBtnArte))
        self.btnArte.grid(row=3, column=0, padx=(40, 86))

        self.btnBio = Button(self, compound=CENTER, height=80, image=self.imgBtnBio, border=0,
                              activebackground="#fee6cd", activeforeground="#af4343", text="Biologie",
                              font=("Rokkitt", 25, "bold"),
                              bg="#fee6cd", fg="#af4343")
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
                             bg="#fee6cd", fg="#af4343")
        self.btnSport.bind("<Enter>", lambda event: self.btnSport.configure(image=self.imgBtnSportDark))
        self.btnSport.bind("<Leave>", lambda event: self.btnSport.configure(image=self.imgBtnSport))
        self.btnSport.grid(row=3, column=1)

        self.btnChimie = Button(self, compound=CENTER, height=80, image=self.imgBtnChimie, border=0,
                             activebackground="#fee6cd", activeforeground="#af4343", text="Chimie",
                             font=("Rokkitt", 25, "bold"),
                             bg="#fee6cd", fg="#af4343")
        self.btnChimie.bind("<Enter>", lambda event: self.btnChimie.configure(image=self.imgBtnChimieDark))
        self.btnChimie.bind("<Leave>", lambda event: self.btnChimie.configure(image=self.imgBtnChimie))
        self.btnChimie.grid(row = 1, column = 2, padx=(86, 0))

        self.btnGeo = Button(self, compound=CENTER, height=80, image=self.imgBtnGeo, border=0,
                               activebackground="#fee6cd", activeforeground="#af4343", text="Geografie",
                               font=("Rokkitt", 25, "bold"),
                               bg="#fee6cd", fg="#af4343")
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

app = Root()
app.mainloop()

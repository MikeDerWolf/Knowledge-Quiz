from tkinter import *
from PIL import ImageTk, Image
import pygame
import sqlite3
import gc

pygame.init()
pygame.mixer.music.load("RUDE - Eternal Youth.mp3")
#pygame.mixer.music.play()
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
        self.pageList = [MainMenu, Settings, TopScore, GameMode]

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

        #self.lblTitle = Label(self, text="Knowledge Quiz", font=("Matura MT Script Capitals", 60), fg="#c25e09", bg="#d7f8ff")
        #self.lblTitle.pack(pady=(85, 30), padx=30)

        self.imgBtn = PhotoImage(file = "btnMenu.png")
        self.imgBtnPress = PhotoImage(file = "btnMenuDark.png")

        self.btnPlay = Button(self, compound=CENTER, text="PLAY", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="#68a302",
                              bg="#fee2cd", activebackground="#fee2cd", activeforeground="#68a302", command=lambda: controller.show_frame(GameMode))  # 7eba00
        self.btnPlay.bind("<Enter>", lambda event: self.btnPlay.configure(image = self.imgBtnPress))
        self.btnPlay.bind("<Leave>", lambda event: self.btnPlay.configure(image=self.imgBtn))
        self.btnPlay.pack(pady=(225, 10), padx=30)

        self.btnTopScore = Button(self, compound=CENTER, text="TOP SCORE", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="#6f54b8",
                                  bg="#fee2cd", activebackground="#fee2cd", activeforeground="#6f54b8", command=lambda: controller.show_frame(TopScore))
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



app = Root()
app.mainloop()

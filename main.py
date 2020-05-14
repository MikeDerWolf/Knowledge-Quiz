from tkinter import *

from PIL import ImageTk, Image
import pygame



class Root(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Knowledge Quiz")
        self.geometry("950x650+200+50")
        self.iconbitmap('brainlogo.ico')
        self.resizable(0, 0)
        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in [MainMenu]:
            frame = F(container, self)
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
                              bg="#fee2cd", activebackground="#fee2cd", activeforeground="#68a302")  # 7eba00
        self.btnPlay.bind("<Enter>", lambda event: self.btnPlay.configure(image = self.imgBtnPress))
        self.btnPlay.bind("<Leave>", lambda event: self.btnPlay.configure(image=self.imgBtn))
        self.btnPlay.pack(pady=(225, 10), padx=30)

        self.btnTopScore = Button(self, compound=CENTER, text="TOP SCORE", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="#6f54b8",
                                  bg="#fee2cd", activebackground="#fee2cd", activeforeground="#6f54b8")
        self.btnTopScore.bind("<Enter>", lambda event: self.btnTopScore.configure(image = self.imgBtnPress))
        self.btnTopScore.bind("<Leave>", lambda event: self.btnTopScore.configure(image=self.imgBtn))
        self.btnTopScore.pack(pady=10, padx=30)

        self.btnSettings = Button(self, compound=CENTER, text="SETTINGS", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="#01728f",
                                  bg="#fee1cf", activebackground="#fee1cf", activeforeground="#01728f")
        self.btnSettings.bind("<Enter>", lambda event: self.btnSettings.configure(image = self.imgBtnPress))
        self.btnSettings.bind("<Leave>", lambda event: self.btnSettings.configure(image = self.imgBtn))
        self.btnSettings.pack(pady=10, padx=30)

        self.btnExit = Button(self, compound=CENTER, text="EXIT", font=("Rokkitt", 18, "bold"), image = self.imgBtn, borderwidth=0, fg="red",
                              bg="#fee2d4", activebackground="#fee2d4", activeforeground="red", command=self.quit)
        self.btnExit.bind("<Enter>", lambda event: self.btnExit.configure(image = self.imgBtnPress))
        self.btnExit.bind("<Leave>", lambda event: self.btnExit.configure(image = self.imgBtn))
        self.btnExit.pack(pady=10, padx=30)









app = Root()
app.mainloop()

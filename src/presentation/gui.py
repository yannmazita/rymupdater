from src.application.services import RYMupdater

import tkinter as tk
from pathlib import Path
from collections.abc import Iterator


class Button(tk.Button):
    """Custom button"""

    def __init__(self, parent, text):
        tk.Button.__init__(self, parent, text=text)


class Label(tk.Label):
    """Custom label"""

    def __init__(self, parent, text):
        tk.Label.__init__(self, parent, text=text)


class SideButtonsFrame(tk.Frame):
    """Side buttons frame"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief=tk.RAISED, bd=2)
        self.__directoryBtn = Button(self, "Directory")
        self.__startBtn = Button(self, "Start")
        self.__pauseBtn = Button(self, "Pause")
        self.__stopBtn = Button(self, "Stop")

        self.__directoryBtn.grid(row=0, column=0, sticky="ew")
        self.__startBtn.grid(row=2, column=0, sticky="ew")
        self.__pauseBtn.grid(row=3, column=0, sticky="ew")
        self.__stopBtn.grid(row=4, column=0, sticky="ew")


class InformationFrame(tk.Frame):
    """Information frame"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.__directoryLbl = Label(self, text="[current directory]")
        self.__directoryLbl.grid(row=0, column=0)


class MainApplication(tk.Frame):
    """Main application frame"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.__sideButtons = SideButtonsFrame(parent)
        self.__information = InformationFrame(parent)

        self.__sideButtons.grid(row=0, column=0, sticky="ns")
        self.__information.grid(row=0, column=1, sticky="n")

        parent.rowconfigure(0, minsize=500, weight=1)
        parent.columnconfigure(1, minsize=600, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("RYMupdater")
    mainApp = MainApplication(root)
    root.mainloop()

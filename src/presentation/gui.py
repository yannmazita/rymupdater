from src.application.services import RYMupdater
import src.presentation.gui_helpers as helpers

import tkinter as tk
from tkinter import filedialog
from functools import partial
from pathlib import Path
from collections.abc import Iterator


class Button(tk.Button):
    """Custom button."""

    def __init__(self, parent, text, command):
        tk.Button.__init__(self, parent, text=text, command=command)


class Label(tk.Label):
    """Custom label."""

    def __init__(self, parent, text):
        tk.Label.__init__(self, parent, text=text)


class SideButtonsFrame(tk.Frame):
    """Side buttons frame."""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief=tk.RAISED, bd=2)
        self.__directoryBtn = Button(self, "Directory", command=partial(helpers.openFileManager, self.directoryBtn))
        self.__startBtn = Button(self, "Start", command=None)
        self.__pauseBtn = Button(self, "Pause", command=None)
        self.__stopBtn = Button(self, "Stop", command=None)

        self.__directoryBtn.grid(row=0, column=0, sticky="ew")
        self.__startBtn.grid(row=2, column=0, sticky="ew")
        self.__pauseBtn.grid(row=3, column=0, sticky="ew")
        self.__stopBtn.grid(row=4, column=0, sticky="ew")

    @property
    def directoryBtn(self):
        """Directory button"""
        return self.__directoryBtn


class InformationFrame(tk.Frame):
    """Information frame."""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.__directoryLbl = Label(self, text="[current directory]")
        self.__directoryLbl.grid(row=0, column=0)


class MainApplication(tk.Frame):
    """Main application frame."""

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

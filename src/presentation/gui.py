from src.application.services import RYMupdater

import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from collections.abc import Iterator
from typing import Self


class Button(tk.Button):
    """Custom button."""

    def __init__(self, parent, text, command):
        tk.Button.__init__(self, parent, text=text, command=command)


class Label(tk.Label):
    """Custom label."""

    def __init__(self, parent, text):
        tk.Label.__init__(self, parent, text=text)


class SideButtonsFrame(tk.Frame):
    """Side buttons frame.

    Every widget on the left size of the main window are stored in this class.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief=tk.RAISED, bd=2)
        self.__directoryBtn: Button = Button(
            self, "Directory", command=SideButtonsFrame.openFileManager
        )
        self.__startBtn: Button = Button(self, "Start", command=None)
        self.__pauseBtn: Button = Button(self, "Pause", command=None)
        self.__stopBtn: Button = Button(self, "Stop", command=None)

        self.__directoryBtn.grid(row=0, column=0, sticky="ew")
        self.__startBtn.grid(row=2, column=0, sticky="ew")
        self.__pauseBtn.grid(row=3, column=0, sticky="ew")
        self.__stopBtn.grid(row=4, column=0, sticky="ew")

    @staticmethod
    def openFileManager():
        """Opens file manager.

        This static method is called after pressing the "Directory" button.
        The file manager opens up allowing the user to chose a directory. Its path is then
        stored in an InformationFrame class attribute, an InformationFrame class method is called
        to update a label in the GUI accordingly.

        Returns:
            None.
        """
        InformationFrame.directoryPath = filedialog.askdirectory(
            initialdir="/", title="Select a directory"
        )
        InformationFrame.updateLibraryPathLabel()


class InformationFrame(tk.Frame):
    """Information frame.

    Every widget on the right side of the main window are stored in this class. Updates
    regarding scraping progress are displayed in this frame.
    """

    instance: Self | None = None
    directoryPath: str = ""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.__libraryPathLabel = Label(self, text="[No directory selected]")
        self.__libraryPathLabel.grid(row=0, column=0)
        InformationFrame.instance = self

    @property
    def libraryPathLabel(self) -> Label:
        """Library path label."""
        return self.__libraryPathLabel

    @staticmethod
    def updateLibraryPathLabel():
        """Updates library path label"""
        assert InformationFrame.instance is not None
        InformationFrame.instance.libraryPathLabel.configure(
            text=f"Library path: {InformationFrame.directoryPath}"
        )


class MainApplication(tk.Frame):
    """Main application frame."""

    instance: Self | None = None
    directoryPath: str = ""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.__sideButtons: SideButtonsFrame = SideButtonsFrame(parent)
        self.__information: InformationFrame = InformationFrame(parent)

        self.__sideButtons.grid(row=0, column=0, sticky="ns")
        self.__information.grid(row=0, column=1, sticky="n")

        parent.rowconfigure(0, minsize=500, weight=1)
        parent.columnconfigure(1, minsize=600, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("RYMupdater")
    mainApp = MainApplication(root)
    root.mainloop()

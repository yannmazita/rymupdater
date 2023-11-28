from ..services import RYMupdater

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

    def __init__(self, parent, textvariable):
        tk.Label.__init__(self, parent, textvariable=textvariable)


class SideButtonsFrame(tk.Frame):
    """Side buttons frame.

    Every widget on the left size of the main window are stored in this class.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief=tk.RAISED, bd=2)
        self.__directoryBtn: Button = Button(
            self, "Directory", command=SideButtonsFrame.openFileManager
        )
        assert InformationFrame.instance is not None
        self.__startBtn: Button = Button(
            self, "Start", command=InformationFrame.instance.updateCurrentFilePath
        )
        self.__pauseBtn: Button = Button(self, "Pause", command=None)
        self.__stopBtn: Button = Button(self, "Stop", command=None)

        self.__directoryBtn.grid(row=0, column=0, sticky="ew")
        self.__startBtn.grid(row=2, column=0, sticky="ew")
        # self.__pauseBtn.grid(row=3, column=0, sticky="ew")
        # self.__stopBtn.grid(row=4, column=0, sticky="ew")

    @staticmethod
    def openFileManager() -> None:
        """Opens file manager.

        This static method updates the tk.StringVar musicDirectoryPath in the InformationFrame
        instance.
        This allows the label using this tk.StringVar to be automatically updated.

        Returns:
            None.
        """
        assert InformationFrame.instance is not None
        InformationFrame.instance.musicDirectoryPath.set(
            filedialog.askdirectory(initialdir="/", title="Select a directory")
        )


class InformationFrame(tk.Frame):
    """Information frame.

    Every widget on the right side of the main window are stored in this class. Updates
    regarding scraping progress are displayed in this frame.
    """

    instance: Self | None = None

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.__musicDirectoryPath: tk.StringVar = tk.StringVar(
            value="[No directory selected]"
        )
        self.__currentFilePath: tk.StringVar = tk.StringVar(value="[No input file]")
        self.__musicDirectoryLabel = Label(self, textvariable=self.__musicDirectoryPath)
        self.__currentFilePathLabel = Label(self, textvariable=self.__currentFilePath)

        self.__rym: RYMupdater = RYMupdater()
        self.__filePaths: Iterator[Path] | None = None
        # don't initialize the iterator without a real path in self.__currentFilePath

        self.__musicDirectoryLabel.grid(row=0, column=0)
        self.__currentFilePathLabel.grid(row=1, column=0)
        InformationFrame.instance = self

    @property
    def musicDirectoryPath(self) -> tk.StringVar:
        """Music directory path."""
        return self.__musicDirectoryPath

    def updateCurrentFilePath(self) -> None:
        """Updates the current file path.

        This method initialize the iterator going through the music library. Initialization
        here and not in the constructor ensures the iterator doesn't start in a non-path
        (and silently stops iterating).

        Returns:
            None
        """
        if self.__filePaths is None:
            self.__filePaths = self.__rym.tagLibrary(Path(self.__musicDirectoryPath.get()))
        try:
            currentPath: Path = next(self.__filePaths)
        except StopIteration:
            self.__currentFilePath.set("done")
            return
        self.__currentFilePath.set(str(currentPath))
        self.__currentFilePathLabel.after(10, self.updateCurrentFilePath)


class Gui(tk.Frame):
    """GUI main frame."""

    instance: Self | None = None

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.__information: InformationFrame = InformationFrame(parent)
        self.__sideButtons: SideButtonsFrame = SideButtonsFrame(parent)

        self.__sideButtons.grid(row=0, column=0, sticky="ns")
        self.__information.grid(row=0, column=1, sticky="n")

        parent.rowconfigure(0, minsize=500, weight=1)
        parent.columnconfigure(1, minsize=600, weight=1)


def startGUI() -> None:
    """Starts the GUI."""
    root = tk.Tk()
    root.title("RYMupdater")
    gui = Gui(root)
    root.mainloop()

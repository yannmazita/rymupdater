from tkinter import filedialog


def openFileManager(button):
    """Opens file manager."""
    filename = filedialog.askdirectory(initialdir="/", title="Select a directory")
    button.configure(text="Directory opened: " + filename)

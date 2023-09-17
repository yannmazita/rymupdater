from src.application.services import RYMupdater

import tkinter as tk
from pathlib import Path
from collections.abc import Iterator


class MainApplication(tk.Frame):
    """Main application frame"""

    def __init__(self, parent):
        super().__init__(self, parent)


class CustomButton(tk.Button):
    """Custom button"""
    def __init__(self, master, text):
        super().__init__(self, master, text=text)

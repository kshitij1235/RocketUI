from app.Rwindows.Windows import Rwindows_
from tkinter import Label
from tkinter import PhotoImage
from customtkinter import *
from tkinter import *
from vendor.Rocket.create import *


class windowManager:

    def __init__(self) -> None:
        self.window : dict = Rwindows_
    def get_window(self , windowname):
        return self.window[windowname]
    def get_all_rwindows(self):
        return self.window

  
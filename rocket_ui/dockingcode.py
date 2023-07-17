from tkinter import *
import tkinter.simpledialog as simpledialog
from random import randint
import os

root = Tk()
root.title("Die Roller")
root.geometry("200x215")
app = Frame(root)
app.grid()

v = StringVar()
w = Label(root, textvariable= v)
w.grid()


print("Results:")


def ad4():
        x = randint(1,4)
        v.set(x)
        print(x)

def ad6():
        x = randint(1,6)
        v.set(x)
        print(x)

def ad8():
        x = randint(1,8)
        v.set(x)
        print(x)

def ad10():
        x = randint(1,10)
        v.set(x)
        print(x)

def ad12():
        x = randint(1,12)
        v.set(x)
        print(x)

def ad20():
        x = randint(1,20)
        v.set(x)
        print(x)

def ad100():
        x = randint(1,100)
        v.set(x)
        print(x)

def other():
        try:
                x = simpledialog.askinteger("Sides", "How many sides are there?")
                y = randint(1, x)
                print(y)
                v.set(y)
        except TypeError:
                cls()

def cls():
    os.system(['clear','cls'][os.name == 'nt'])


d4 = Button(app, text = "d4", command=ad4, height = 2, width = 5, fg="white", bg="blue")
d4.grid(row=0, column=0, padx=10, pady=10)

d6 = Button(app, text = "d6", command=ad6, height = 2, width = 5, fg="white", bg="blue")
d6.grid(row=0, column=1, padx=10, pady=10)

d8 = Button(app, text = "d8", command=ad8, height = 2, width = 5, fg="white", bg="blue")
d8.grid(row=0, column=2, padx=10, pady=10)

d10 = Button(app, text = "d10", command=ad10, height = 2, width = 5, fg="white", bg="blue")
d10.grid(row=1, column=0, padx=10, pady=10)

d12 = Button(app, text = "d12", command=ad12, height = 2, width = 5, fg="white", bg="blue")
d12.grid(row=1, column=1, padx=10, pady=10)

d20 = Button(app, text = "d20", command=ad20, height = 2, width = 5, fg="white", bg="blue")
d20.grid(row=1, column=2, padx=10, pady=10)

d100 = Button(app, text = "d100", command=ad100, height = 2, width = 5, fg="white", bg="blue")
d100.grid(row=2, column=0, padx=10, pady=10)

otherbutton = Button(app, text = "Other", command=other, height = 2, width = 5, fg="white", bg="blue")
otherbutton.grid(row=2, column=1, padx=10, pady=10)

clearButton = Button(app, text = "Clear", command=cls, height =2, width = 5, fg="white", bg="blue")
clearButton.grid(row=2, column=2, padx=10, pady=10)

def onKeyPress(event):
        if event.char == '7':
                ad4()
        if event.char == '8':
                ad6()
        if event.char == '9':
                ad8()
        if event.char == '4':
                ad10()
        if event.char == '5':
                ad12()
        if event.char == '6':
                ad20()
        if event.char == '1':
                ad100()
        if event.char == '2':
                other()
        if event.char == '3':
                cls()


root.bind('<KeyPress>', onKeyPress)
root.mainloop()
from tkinter import *
from tkinter.colorchooser import *


def getColor():
    color = askcolor()[0]
    print([int(s) for s in color])


def rainbow():
    print('rainbow')


class GUI:
    BUTTON_WIDTH = 50

    def __init__(self, master):
        self.master = master
        master.title("Server GUI")

        self.label = Label(master, text="Control light")
        self.label.pack()

        self.rainbow_button = Button(
            master, text="Rainbow", width=self.BUTTON_WIDTH,
            command=rainbow
        )
        self.rainbow_button.pack()

        self.color_button = Button(
            master, text='Select Color', width=self.BUTTON_WIDTH,
            command=getColor)
        self.color_button.pack()


if __name__ == "__main__":
    root = Tk()
    my_gui = GUI(root)
    root.mainloop()
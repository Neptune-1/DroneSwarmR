from tkinter import Tk, Button, Label
from tkinter.colorchooser import askcolor

from .Server import Server


class ServerGUI:
    BUTTON_WIDTH = 50

    def __init__(self, master):
        self.master = master
        self.server = Server()
        self.server.run()
        master.title("Server GUI")

        self.label = Label(master, text="Control light")
        self.label.pack()

        self.rainbow_button = Button(
            master, text="Rainbow", width=self.BUTTON_WIDTH,
            command=self.server.rainbow
        )
        self.rainbow_button.pack()

        self.fill_button = Button(
            master, text="Fill", width=self.BUTTON_WIDTH,
            command=self.server.fill
        )
        self.fill_button.pack()

        self.blink_button = Button(
            master, text="Blink", width=self.BUTTON_WIDTH,
            command=self.server.blink
        )
        self.blink_button.pack()

        self.chase_button = Button(
            master, text="Chase", width=self.BUTTON_WIDTH,
            command=self.server.chase
        )
        self.chase_button.pack()

        self.wipe_to_button = Button(
            master, text="Wipe to", width=self.BUTTON_WIDTH,
            command=self.server.wipe_to
        )
        self.wipe_to_button.pack()

        self.fade_to_button = Button(
            master, text="Fade to", width=self.BUTTON_WIDTH,
            command=self.server.fade_to
        )
        self.fade_to_button.pack()

        self.run_button = Button(
            master, text="Run", width=self.BUTTON_WIDTH,
            command=self.server.run
        )
        self.run_button.pack()

        self.color_button = Button(
            master, text="Select color", width=self.BUTTON_WIDTH,
            command=self.get_color
        )
        self.color_button.pack()

        self.quit_button = Button(
            master, text="Close socket", width=self.BUTTON_WIDTH,
            command=self.server.close
        )
        self.quit_button.pack()

    def get_color(self):
        color = askcolor()[0]
        color = map(int, color)
        self.server.set_color(color)

    def quit(self):
        self.server.close()
        self.master.quit()


if __name__ == "__main__":
    root = Tk()
    my_gui = ServerGUI(root)
    root.mainloop()

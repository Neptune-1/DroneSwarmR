from tkinter import Tk, Label, Button

from ServerForCopters.Server import Server


class ServerGUI:
    BUTTON_WIDTH = 50

    def __init__(self, master):
        self.master = master
        self.server = Server()
        self.server.run()
        master.title("Server GUI")

        self.label = Label(master, text="Можем в ГУЙ")
        self.label.pack()

        self.greet_button = Button(
            master, text="Takeoff", width=self.BUTTON_WIDTH,
            command=self.server.takeoff
        )
        self.greet_button.pack()

        self.animation_button = Button(
            master, text="Animate", width=self.BUTTON_WIDTH,
            command=self.server.start_animation
        )
        self.animation_button.pack()

        self.pause_button = Button(
            master, text="Pause", width=self.BUTTON_WIDTH,
            command=self.server.pause
        )
        self.pause_button.pack()

        self.resume_button = Button(
            master, text="Resume", width=self.BUTTON_WIDTH,
            command=self.server.resume
        )
        self.resume_button.pack()

        self.land_button = Button(
            master, text="Land", width=self.BUTTON_WIDTH,
            command=self.server.land
        )
        self.land_button.pack()

        self.close_button = Button(
            master, text="Close", width=self.BUTTON_WIDTH,
            command=self.quit
        )
        self.close_button.pack()

    def quit(self):
        self.server.close()
        self.master.quit()


if __name__ == "__main__":
    root = Tk()
    my_gui = ServerGUI(root)
    root.mainloop()

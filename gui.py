import os
import tkinter

# GUI class.
class UI:
    def __init__(self):
        self.choice_of_course = ""
        self.choice_of_action = ""

        self.root = tkinter.Tk()
        self.window = tkinter.Frame(self.root)
        self.canvas = tkinter.Canvas(self.window, height=500, width=500, bg='#A5FFF0')
        self.canvas.pack()
        #menu list
        self.option_list = ["                              auto registration                ",
                            "                   send me a mail when available                ",
                            "                   auto registration + send a mail                "]
        self.variable = tkinter.StringVar(self.root)
        self.variable.set("    what do you want to do?")
        self.opt = tkinter.OptionMenu(self.root, self.variable, *self.option_list)
        self.opt.config(width=35, font=('Helvetica', 13))
        self.opt.pack()
        self.window.pack()

        # user entry for submitting the info
        self.usr_entry = tkinter.Entry(self.window, font=40)
        self.usr_entry.place(relx=0.15, rely=0.2, relwidth=0.7, relheight=0.1)
        self.sub_button = tkinter.Button(self.window, text='enter course name', height=2, width=40,
                                         command=lambda: self.usr_input(self.usr_entry.get()))
        self.sub_button.place(relx=0.05, rely=0.4, relwidth=0.9, relheight=0.1)

        self.window.tkraise()
        self.root.mainloop()

# get the user input from the entry and set it to the inner var
    def usr_input(self, course_name):
        self.choice_of_course = course_name
        self.choice_of_action = self.variable.get()
        self.root.destroy()
# setter
    def get_usr_choice(self):
        return self.choice_of_course
# setter
    def get_usr_action(self):
        return self.choice_of_action


import os
import tkinter


class UI:
    def __init__(self):
        self.choice_of_course = ""
        self.choice_of_action = ""

        self.root = tkinter.Tk()
        self.folder_win = tkinter.Frame(self.root)
        self.canvas = tkinter.Canvas(self.folder_win, height=500, width=500, bg='#A5FFF0')
        self.canvas.pack()

        self.option_list = ["                              auto registration                ",
                            "                   send me a mail when available                ",
                            "                   auto registration + send a mail                "]
        self.variable = tkinter.StringVar(self.root)
        self.variable.set("    what do you want to do?")
        self.opt = tkinter.OptionMenu(self.root, self.variable, *self.option_list)
        self.opt.config(width=35, font=('Helvetica', 13))
        self.opt.pack()
        self.folder_win.pack()

        self.folder_entry = tkinter.Entry(self.folder_win, font=40)
        self.folder_entry.place(relx=0.15, rely=0.2, relwidth=0.7, relheight=0.1)
        self.sub_button = tkinter.Button(self.folder_win, text='enter course name', height=2, width=40,
                                         command=lambda: self.usr_input(self.folder_entry.get()))
        self.sub_button.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.1)

        self.folder_win.tkraise()
        self.root.mainloop()

    def usr_input(self, course_name):
        self.choice_of_course = course_name
        self.choice_of_action = self.variable.get()
        self.root.destroy()

    def get_usr_choice(self):
        return self.choice_of_course

    def get_usr_action(self):
        return self.choice_of_action

    # def run_GIU(self):

    # file_win = Frame(root)
    # canvas = Canvas(file_win, height=500, width=500, bg='#A5FFF0')
    # canvas.pack()

    # for frame in (folder_win, file_win):

    # folder window
    # folder_button = Button(folder_win, text='file', height=2, width=20, command=lambda: raise_frame(file_win))
    # folder_button.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)
    # file_button = Button(folder_win, relief='sunken', bg='#E2E0E0', text='folder', height=2, width=20)
    # file_button.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.1)

    # folder_lable = Label(folder_win, bg='white')
    # folder_lable.place(relx=0.05, rely=0.5, relwidth=0.7, relheight=0.5)

    # file window
    # folder_button = Button(file_win, text='file', relief='sunken', bg='#E2E0E0', height=2, width=20)
    # folder_button.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)
    # file_button = Button(file_win,  text='folder', height=2, width=20, command=lambda: raise_frame(folder_win))
    # file_button.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.1)
    # file_entry = Entry(file_win, font=40)
    # file_entry.place(relx=0.05, rely=0.2, relwidth=0.7, relheight=0.1)
    # sub_button = Button(file_win, text='enter file', height=2, width=20, command=lambda: list_dir(file_entry.get(), file_lable))
    # sub_button.place(relx=0.77, rely=0.2, relwidth=0.2, relheight=0.1)
    # file_lable = Label(file_win, bg='white')
    # file_lable.place(relx=0.05, rely=0.4, relwidth=0.7, relheight=0.5)

import tkinter
from tkinter import colorchooser

from counter import Counter


class TableWidget:

    def __init__(self, parent, rgb_bg=(255, 255, 255), rgb_table=(0, 0, 0),
                 edit=False, rows=1, cols=1, width=20, height=20):
        self.parent = parent
        self.edit = edit
        master = tkinter.Tk()
        master.title('Tabuľka')
        master.resizable(0, 0)
        master.protocol('WM_DELETE_WINDOW', self.on_close)
        x, y = parent.canvas.winfo_rootx(), parent.canvas.winfo_rooty()
        w, h = parent.canvas.winfo_width(), parent.canvas.winfo_height()
        master.geometry('%dx%d+%d+%d' % (165, 345, x + (w / 2) - 100, y + (h / 2) - 150))
        self.master = master
        self.row_count = 1
        self.col_count = 1
        self.rgb_bg = rgb_bg
        self.rgb_table = rgb_table

        # labels
        tkinter.Label(master, text='Počet riadkov: ', anchor='w').grid(row=0, column=0, rowspan=2)
        tkinter.Label(master, text='Počet stĺpcov: ', anchor='w').grid(row=2, column=0, rowspan=2)
        tkinter.Label(master, text='Šírka bunky: ', anchor='w').grid(row=4, column=0, rowspan=2)
        tkinter.Label(master, text='Výška bunky: ', anchor='w').grid(row=6, column=0, rowspan=2)

        self.counters = [Counter(self.master, 0, 1, rows, 7, 1, edit), Counter(self.master, 2, 1, cols, 10, 1, edit),
                         Counter(self.master, 4, 1, height, 100, 10, edit), Counter(self.master, 6, 1, width, 80, 10, edit)]

        tkinter.Button(master, text='Farba pozadia', command=self.choose_color_bg, width=10, height=1).\
            grid(row=8, column=0, columnspan=3)
        tkinter.Button(master, text='Farba tabuky', command=self.choose_color_table, width=10, height=1).\
            grid(row=10, column=0, columnspan=3)
        tkinter.Button(master, text='Potvrdiť', command=self.confirm, width=10, height=1).\
            grid(row=12, column=0, columnspan=3)

    def choose_color_table(self):
        self.master.lower()
        color_code = colorchooser.askcolor(title="Zvoľ farbu")
        if color_code:
            self.rgb_table = tuple(map(int, color_code[0]))
        self.master.tkraise()

    def choose_color_bg(self):
        self.master.lower()
        color_code = colorchooser.askcolor(title="Zvoľ farbu")
        if color_code:
            self.rgb_bg = tuple(map(int, color_code[0]))
        self.master.tkraise()

    def confirm(self):
        if not self.edit:
            self.parent.create_table()
        else:
            self.parent.edit_table()
        self.master.destroy()

    def on_close(self):
        self.parent.create_table(True)
        self.master.destroy()

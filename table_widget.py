import tkinter
from tkinter import colorchooser

from counter import Counter


class TableWidget:

    def __init__(self, parent, row_count=1, col_count=1):
        self.parent = parent
        master = tkinter.Tk()
        master.title('Tabuľka')
        master.resizable(0, 0)
        master.protocol('WM_DELETE_WINDOW', self.on_close)
        x, y = parent.canvas.winfo_rootx(), parent.canvas.winfo_rooty()
        w, h = parent.canvas.winfo_width(), parent.canvas.winfo_height()
        master.geometry('%dx%d+%d+%d' % (165, 345, x + (w / 2) - 100, y + (h / 2) - 150))
        self.master = master
        self.row_count = row_count
        self.col_count = col_count
        self.rgb_bg = (255, 255, 255)
        self.rgb_table = (255, 255, 255)

        # labels
        tkinter.Label(master, text='Počet riadkov: ', anchor='w').grid(row=0, column=0, rowspan=2)
        tkinter.Label(master, text='Počet stĺpcov: ', anchor='w').grid(row=2, column=0, rowspan=2)
        tkinter.Label(master, text='Šírka bunky: ', anchor='w').grid(row=4, column=0, rowspan=2)
        tkinter.Label(master, text='Výška bunky: ', anchor='w').grid(row=6, column=0, rowspan=2)

        self.counters = [Counter(self.master, 0, 1, 1, 7, 1), Counter(self.master, 2, 1, 1, 10, 1),
                         Counter(self.master, 4, 1, 20, 100, 10), Counter(self.master, 6, 1, 20, 80, 10)]

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
        # self.master.attributes('-topmost', True)

    def confirm(self):
        self.parent.create_table()
        self.master.destroy()

    def on_close(self):
        self.parent.create_table(True)
        self.master.destroy()

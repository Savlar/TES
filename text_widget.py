import random
import tkinter
from tkinter import colorchooser, font


class TextWidget:

    def __init__(self, parent):
        self.parent = parent

        master = tkinter.Tk()
        master.protocol('WM_DELETE_WINDOW', self.on_close)
        x, y = parent.canvas.winfo_rootx(), parent.canvas.winfo_rooty()
        w, h = parent.canvas.winfo_width(), parent.canvas.winfo_height()
        master.geometry('%dx%d+%d+%d' % (200, 350, x + (w / 2) - 100, y + (h / 2) - 150))
        self.master = master

        self.rgb = (0, 0, 0)

        self.default_size = tkinter.IntVar(self.master)
        self.default_size.set(12)

        self.size = tkinter.OptionMenu(self.master, self.default_size, *range(8, 30, 2))
        self.size.grid(row=1, column=0)

        self.default_font = tkinter.StringVar(self.master)
        self.default_font.set('Arial')

        fonts = [x for x in font.families()]
        self.font = tkinter.OptionMenu(self.master, self.default_font, *fonts)
        self.font.grid(row=2, column=0)

        self.entry = tkinter.Entry(master)
        self.entry.grid(row=0, column=0)
        self.text = ''

        tkinter.Button(master, text='Farba', command=self.choose_color).grid(row=8, column=0)
        tkinter.Button(master, text='Potvrdit', command=self.confirm).grid(row=10, column=0)

    def confirm(self):
        self.text = self.entry.get()
        self.parent.create_text()
        self.on_close()

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Zvol farbu")
        self.rgb = tuple(map(int, color_code[0]))
        self.master.attributes('-topmost', True)

    def on_close(self):
        self.parent.create_text(True)
        self.master.destroy()

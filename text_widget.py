import tkinter
from tkinter import colorchooser, font
from tkinter.scrolledtext import ScrolledText


class TextWidget:

    def __init__(self, parent, text='', rgb=(0, 0, 0), size=12, font='Arial'):
        self.parent = parent

        self.edit = text != ''
        self.text = text
        master = tkinter.Tk()
        master.title('Text')
        master.resizable(0, 0)
        master.protocol('WM_DELETE_WINDOW', self.on_close)
        x, y = parent.canvas.winfo_rootx(), parent.canvas.winfo_rooty()
        w, h = parent.canvas.winfo_width(), parent.canvas.winfo_height()
        master.geometry('%dx%d+%d+%d' % (200, 310, x + (w / 2) - 100, y + (h / 2) - 150))
        self.master = master

        self.rgb = rgb

        self.default_size = tkinter.IntVar(self.master)
        self.default_size.set(size)

        self.size = tkinter.OptionMenu(self.master, self.default_size, *range(8, 30, 2))
        self.size.config(width=3)
        self.size.grid(row=1, column=0)

        self.default_font = tkinter.StringVar(self.master)
        self.default_font.set(font)

        fonts = ['Arial', 'Helvetica', 'Comic Sans MS', 'Verdana', 'Consolas', 'Calibri', 'Cambria']
        self.font = tkinter.OptionMenu(self.master, self.default_font, *fonts)
        self.font.config(width=15)
        self.font.grid(row=2, column=0)

        self.entry = ScrolledText(master, width=23, height=10)
        self.entry.insert('1.0', text)
        self.entry.grid(row=0, column=0)
        self.entry.bind('<KeyRelease>', self.text_change)

        tkinter.Button(master, text='Farba', command=self.choose_color, width=5).grid(row=8, column=0)
        self.confirm_button = tkinter.Button(master, text='Potvrdiť', command=self.confirm, width=5)
        self.confirm_button.grid(row=10, column=0)
        if text == '':
            self.confirm_button['state'] = 'disabled'

    def text_change(self, e):
        self.confirm_button['state'] = 'normal' if self.entry.get('1.0', tkinter.END) != '\n' else 'disabled'

    def confirm(self):
        self.text = self.entry.get('1.0', tkinter.END)[:-1]
        if self.edit:
            self.parent.edit_text()
        else:
            self.parent.create_text()
        self.on_close()

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Zvoľ farbu")
        self.rgb = tuple(map(int, color_code[0]))
        self.master.attributes('-topmost', True)

    def on_close(self):
        self.parent.create_text(True)
        self.master.destroy()

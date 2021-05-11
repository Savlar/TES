import tkinter


class ImageSize:

    def __init__(self, parent, image_w, image_h):
        self.canvas = parent.parent.canvas
        self.parent = parent
        self.ratio = image_w / image_h
        master = tkinter.Tk()
        master.title('Veľkosť')
        master.resizable(0, 0)
        master.protocol('WM_DELETE_WINDOW', self.on_close)
        x, y = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        master.geometry('%dx%d+%d+%d' % (145, 120, x + (w / 2) - 100, y + (h / 2) - 150))
        self.master = master
        self.master.attributes('-topmost', True)
        tkinter.Label(master, text='Šírka: ').grid(row=0, column=0)
        tkinter.Label(master, text='Výška: ').grid(row=1, column=0)

        self.checkbox = tkinter.IntVar(value=1, master=master)
        button = tkinter.Checkbutton(master, text='Zachovať pomer \nstrán', variable=self.checkbox, onvalue=1, offvalue=0)
        button.grid(row=2, column=0, columnspan=2)

        tkinter.Button(master, text='Potvrdiť', command=self.confirm).grid(row=4, column=0, columnspan=2)

        self.width = tkinter.Entry(master, width=10)
        self.width.grid(row=0, column=1)
        self.width.insert(tkinter.END, image_w)
        self.width.bind('<KeyRelease>', self.changed_width)

        self.height = tkinter.Entry(master, width=10)
        self.height.grid(row=1, column=1)
        self.height.insert(tkinter.END, image_h)
        self.height.bind('<KeyRelease>', self.changed_height)

    def changed_width(self, e):
        if self.checkbox.get() == 1:
            self.height.delete(0, tkinter.END)
            if self.width.get() != '':
                self.height.insert(0, int(int(self.width.get()) / self.ratio))

    def changed_height(self, e):
        if self.checkbox.get() == 1:
            self.width.delete(0, tkinter.END)
            if self.height.get() != '':
                self.width.insert(0, int(int(self.height.get()) * self.ratio))

    def on_close(self):
        self.master.destroy()

    def confirm(self):
        self.parent.resize(self.width.get(), self.height.get())
        self.on_close()

import tkinter


class ImageSize:

    def __init__(self, parent, image_w, image_h):
        self.canvas = parent.parent.canvas
        self.parent = parent

        master = tkinter.Tk()
        master.protocol('WM_DELETE_WINDOW', self.on_close)
        x, y = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        master.geometry('%dx%d+%d+%d' % (200, 350, x + (w / 2) - 100, y + (h / 2) - 150))
        self.master = master
        self.master.attributes('-topmost', True)
        tkinter.Label(master, text='Sirka: ').grid(row=0, column=0)
        tkinter.Label(master, text='Vyska: ').grid(row=1, column=0)
        tkinter.Button(master, text='Potvrdit', command=self.confirm).grid(row=3, column=0)

        self.width = tkinter.Entry(master)
        self.width.grid(row=0, column=1)
        self.width.insert(tkinter.END, image_w)

        self.height = tkinter.Entry(master)
        self.height.grid(row=1, column=1)
        self.height.insert(tkinter.END, image_h)

    def on_close(self):
        self.master.destroy()

    def confirm(self):
        self.parent.resize(self.width.get(), self.height.get())
        self.on_close()

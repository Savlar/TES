import tkinter


class ImageSize:

    def __init__(self, parent, image_w, image_h):
        self.canvas = parent.parent.canvas
        self.parent = parent

        master = tkinter.Tk()
        master.title('Veľkosť')
        master.resizable(0, 0)
        master.protocol('WM_DELETE_WINDOW', self.on_close)
        x, y = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        master.geometry('%dx%d+%d+%d' % (140, 80, x + (w / 2) - 100, y + (h / 2) - 150))
        self.master = master
        self.master.attributes('-topmost', True)
        tkinter.Label(master, text='Šírka: ').grid(row=0, column=0)
        tkinter.Label(master, text='Výška: ').grid(row=1, column=0)
        tkinter.Button(master, text='Potvrdiť', command=self.confirm).grid(row=3, column=0, columnspan=2)

        self.width = tkinter.Entry(master, width=10)
        self.width.grid(row=0, column=1)
        self.width.insert(tkinter.END, image_w)

        self.height = tkinter.Entry(master, width=10)
        self.height.grid(row=1, column=1)
        self.height.insert(tkinter.END, image_h)

    def on_close(self):
        self.master.destroy()

    def confirm(self):
        self.parent.resize(self.width.get(), self.height.get())
        self.on_close()

import tkinter

from program import Program


if __name__ == '__main__':
    win = tkinter.Tk()
    w, h = 1080, 720
    ws, hs = win.winfo_screenwidth(), win.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    canvas = tkinter.Canvas(master=win, height=720, width=1080)
    canvas.pack()
    Program(canvas)
    win.mainloop()

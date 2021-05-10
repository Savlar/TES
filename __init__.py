import tkinter

from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from student_program import StudentProgram
from teacher_program import TeacherProgram


if __name__ == '__main__':
    win = tkinter.Tk()
    win.resizable(0, 0)
    w, h = WINDOW_WIDTH, WINDOW_HEIGHT
    ws, hs = win.winfo_screenwidth(), win.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    canvas = tkinter.Canvas(master=win, height=WINDOW_HEIGHT, width=WINDOW_WIDTH, bg='lightblue')
    canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH)
    TeacherProgram(canvas, WINDOW_WIDTH, WINDOW_HEIGHT, win)
    # StudentProgram(canvas, WINDOW_WIDTH, WINDOW_HEIGHT, win)
    win.mainloop()

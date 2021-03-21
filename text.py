import tkinter
from tkinter.font import Font


class Text:

    def __init__(self, x, y, canvas: tkinter.Canvas, text, size, color, f):
        self.font = f
        self.color = color
        self.text = text
        self.size = size
        self.x = x
        self.y = y
        self.canvas = canvas
        f = Font(family=self.font, size=self.size)
        self.obj = self.canvas.create_text(self.x, self.y, text=self.text,
                                           font=f, fill="#%02x%02x%02x" % self.color, tag='text')

    def move(self, x, y):
        bounds = self.canvas.bbox(self.obj)
        w2, h2 = abs((bounds[2] - bounds[0]) / 2), abs((bounds[3] - bounds[1]) / 2)
        if x - w2 < 100 or x + w2 > 980 or y - h2 < 75 or y + h2 > 700:
            return
        self.canvas.coords(self.obj, x, y)
        self.x = x
        self.y = y

    def delete(self):
        self.canvas.delete(self.obj)

    def serialize(self):
        return {'type': 'text', 'x': self.x, 'y': self.y, 'color': self.color, 'text': self.text, 'size': self.size, 'font': self.font}

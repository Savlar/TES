from tkinter.font import Font

from constants import COPY_OFFSET


class Text:

    def __init__(self, x, y, parent, text, size, color, f):
        self.font = f
        self.parent = parent
        self.color = color
        self.text = text
        self.size = size
        self.x = x
        self.y = y
        self.canvas = parent.canvas
        f = Font(family=self.font, size=self.size)
        self.obj = self.canvas.create_text(self.x, self.y, text=self.text,
                                           font=f, fill="#%02x%02x%02x" % self.color, tag='text')

    def move(self, x, y):
        if self.parent.student:
            return
        bounds = self.canvas.bbox(self.obj)
        w2, h2 = abs((bounds[2] - bounds[0]) / 2), abs((bounds[3] - bounds[1]) / 2)
        x1, y1, x2, y2 = self.canvas.coords(self.canvas.find_withtag('area')[0])
        if x - w2 < x1 or x + w2 > x2 or y - h2 < y1 or y + h2 > y2:
            return
        self.canvas.coords(self.obj, x, y)
        self.x = x
        self.y = y

    def __copy__(self):
        if not self.parent.student:
            text = Text(self.x + COPY_OFFSET, self.y + COPY_OFFSET, self.parent, self.text, self.size,
                        self.color, self.font)
            return text

    def delete(self):
        self.canvas.delete(self.obj)

    def serialize(self):
        return {'type': 'text', 'x': self.x, 'y': self.y, 'color': self.color,
                'text': self.text, 'size': self.size, 'font': self.font}

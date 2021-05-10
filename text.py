from tkinter.font import Font

from constants import COPY_OFFSET, AREA_X1, AREA_Y2, AREA_Y1, AREA_X2


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
                                           font=f, fill='#%02x%02x%02x' % self.color, tag='text')

    def click(self, e):
        x1, y1, x2, y2 = self.canvas.bbox(self.obj)
        return x1 <= e.x <= x2 and y1 <= e.y <= y2

    def set(self, text, size, color, font):
        self.text = text
        self.size = size
        self.color = color
        self.font = font
        self.parent.canvas.itemconfig(self.obj, text=text)
        self.parent.canvas.itemconfig(self.obj, font=Font(family=font, size=size))
        self.parent.canvas.itemconfig(self.obj, fill='#%02x%02x%02x' % color)
        x1, y1, x2, y2 = self.canvas.bbox(self.obj)
        self.x = int(((x2 - x1) // 2) + x1)
        self.y = int(((y2 - y1) // 2) + y1)
        self.canvas.coords(self.obj, self.x, self.y)

    def move(self, x, y):
        if self.parent.student:
            return
        bounds = self.canvas.bbox(self.obj)
        w2, h2 = (bounds[2] - bounds[0]) / 2, (bounds[3] - bounds[1]) / 2
        if x - w2 < AREA_X1 or x + w2 > AREA_X2 or y - h2 < AREA_Y1 or y + h2 > AREA_Y2:
            return
        self.canvas.coords(self.obj, x, y)

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

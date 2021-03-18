import tkinter


class Button:

    def __init__(self, image, x, y, canvas: tkinter.Canvas):
        self.canvas = canvas
        self._image = image
        self._coords = (x, y)
        self.obj = self.canvas.create_image(x, y, image=image)

    @property
    def coords(self):
        return self._coords

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

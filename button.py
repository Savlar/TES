class Button:

    def __init__(self, image, x, y, parent):
        self.canvas = parent.canvas
        self.parent = parent
        self.mr = parent.width - x
        self.mt = y
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

    def resize(self):
        new_x = self.parent.width - self.mr
        new_y = self.mt
        print(new_x, new_y)
        self.canvas.coords(self.obj, new_x, new_y)

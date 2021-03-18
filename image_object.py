import tkinter
from typing import Tuple

from PIL import ImageTk
from PIL.PngImagePlugin import PngImageFile

from created_object import CreatedObject


class ImageObject(CreatedObject):

    def __init__(self, x: int, y: int, c: tkinter.Canvas, img):
        self._coords: Tuple[int,int] = (x, y)
        self.canvas = c
        self.obj = None
        self.pil_img: PngImageFile = img
        self.tk_img = ImageTk.PhotoImage(img)

    def delete(self):
        self.canvas.delete(self.obj)


class CloneObject(ImageObject):

    def __init__(self, x, y, c, img):
        super(CloneObject, self).__init__(x, y, c, img)

    def delete(self):
        super(CloneObject, self).delete()


class ClickableObject(ImageObject):

    def __init__(self, x, y, c, img):
        super(ClickableObject, self).__init__(x, y, c, img)

    def delete(self):
        super(ClickableObject, self).delete()


class StaticObject(ImageObject):

    def __init__(self, x, y, c, img):
        super(StaticObject, self).__init__(x, y, c, img)
        self.obj = self.canvas.create_image(x, y, image=self.tk_img)

    def delete(self):
        super(StaticObject, self).delete()

    def serialize(self):
        coords = self.canvas.coords(self.obj)
        return {'type': 'static', 'image': self.pil_img.tobytes(), 'size': (self.pil_img.width, self.pil_img.height),
                'x': coords[0], 'y': coords[1]}


class DraggableObject(ImageObject):

    def __init__(self, x, y, c, img):
        super(DraggableObject, self).__init__(x, y, c, img)

    def delete(self):
        super(DraggableObject, self).delete()

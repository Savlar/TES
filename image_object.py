import tkinter
from typing import Tuple

from PIL import ImageTk, Image
from PIL.PngImagePlugin import PngImageFile


class ImageObject:

    def __init__(self, x: int, y: int, c: tkinter.Canvas):
        self._coords: Tuple[int,int] = (x, y)
        self.canvas = c
        self.size = None
        self.obj = None

    def delete(self):
        self.canvas.delete(self.obj)

    def move(self, x, y):
        w, h = self.size
        w2, h2 = w / 2, h / 2
        if x - w2 < 100 or x + w2 > 980 or y - h2 < 75 or y + h2 > 700:
            return
        self.canvas.coords(self.obj, x, y)

    def check_coords(self):
        w2, h2 = self.size[0] / 2, self.size[1] / 2
        if self._coords[0] - w2 < 100:
            self._coords = (100 + w2, self._coords[1])
        if self._coords[0] + w2 > 980:
            self._coords = (980 - w2, self._coords[1])
        if self._coords[1] - h2 < 75:
            self._coords = (self._coords[0], 75 + h2)
        if self._coords[1] + h2 > 700:
            self._coords = (self._coords[0], 700 - h2)
        self.canvas.coords(self.obj, *self._coords)


class CloneableObject(ImageObject):

    def __init__(self, x, y, c, img, order):
        super(CloneableObject, self).__init__(x, y, c)
        self.original = img
        self.size = (75, 75)
        self.order = order
        self.pil_img = img.resize(self.size)
        self.tk_img = ImageTk.PhotoImage(self.pil_img)
        self._coords = (50, 120 + 85 * order)
        self.obj = self.canvas.create_image(*self._coords, image=self.tk_img, tag='clone')

    def delete(self):
        super(CloneableObject, self).delete()

    def serialize(self):
        return {'type': 'cloneable', 'image': self.pil_img.tobytes(), 'size': self.size, 'order': self.order}


class ClickableObject(ImageObject):

    def __init__(self, x, y, c, imgs):
        super(ClickableObject, self).__init__(x, y, c)
        self.pil_imgs = imgs
        self.originals = imgs
        self.tk_imgs = []
        self.index = 0
        self.size = None
        self.obj = None
        self.initialize()

    def initialize(self):
        self.delete()
        self.tk_imgs = []
        self.index = 0
        self.size = self.pil_imgs[0].size
        for img in self.pil_imgs:
            self.tk_imgs.append(ImageTk.PhotoImage(img))
        self.resize(*self.size)
        self.obj = self.canvas.create_image(*self._coords, image=self.tk_imgs[0], tag='image')
        self.canvas.tag_raise(self.obj)

    def delete(self):
        super(ClickableObject, self).delete()

    def serialize(self):
        coords = self.canvas.coords(self.obj)
        img_bytes = []
        for img in self.pil_imgs:
            img_bytes.append(img.tobytes())
        return {'type': 'clickable', 'images': img_bytes, 'size': self.size,
                'x': coords[0], 'y': coords[1]}

    def clicked(self, e):
        width, height = self.pil_imgs[self.index].size
        w2, h2 = width / 2, height / 2
        x, y = self.canvas.coords(self.obj)
        if (x - w2) <= e.x <= (x + w2) and (y - h2) <= e.y <= (y + h2):
            self.index = self.index + 1 if self.index + 1 < len(self.tk_imgs) else 0
            self.canvas.itemconfig(self.obj, image=self.tk_imgs[self.index])

    def resize(self, w, h):
        if (w, h) > self.size:
            self.pil_imgs = self.originals
        for i in range(len(self.pil_imgs)):
            self.pil_imgs[i] = self.pil_imgs[i].resize((w, h), resample=Image.CUBIC)
            self.tk_imgs[i] = ImageTk.PhotoImage(self.pil_imgs[i])
        self.size = self.pil_imgs[0].size
        self.canvas.itemconfig(self.obj, image=self.tk_imgs[self.index])

    def collision(self, e, other):
        x, y = e.x, e.y
        mx, my = self.canvas.coords(self.obj)
        w, h = self.pil_imgs[self.index].size
        w2, h2 = w / 2, h / 2
        return mx - w2 <= x <= mx + w2 and my - h2 <= y <= my + h2


class StaticObject(ImageObject):

    def __init__(self, x, y, c, img):
        super(StaticObject, self).__init__(x, y, c)
        self.pil_img: PngImageFile = img
        self.original = img
        self.size = None
        self.tk_img = None
        self.obj = None
        self.initialize()

    def initialize(self):
        self.size = self.pil_img.size
        self.tk_img = ImageTk.PhotoImage(self.pil_img)
        self.obj = self.canvas.create_image(*self._coords, image=self.tk_img, tag='image')
        self.canvas.tag_raise(self.obj)

    def delete(self):
        super(StaticObject, self).delete()

    def serialize(self):
        coords = self.canvas.coords(self.obj)
        return {'type': 'static', 'image': self.pil_img.tobytes(), 'size': (self.pil_img.width, self.pil_img.height),
                'x': coords[0], 'y': coords[1]}

    def resize(self, w, h):
        if (w, h) > self.size:
            self.pil_img = self.original
        self.pil_img = self.pil_img.resize((w, h), resample=Image.CUBIC)
        self.tk_img = ImageTk.PhotoImage(self.pil_img)
        self.size = self.pil_img.size
        self.canvas.itemconfigure(self.obj, image=self.tk_img)

    def collision(self, e, other):
        x, y = e.x, e.y
        mx, my = self.canvas.coords(self.obj)
        w, h = self.pil_img.size
        w2, h2 = w / 2, h / 2
        return mx - w2 <= x <= mx + w2 and my - h2 <= y <= my + h2


class DraggableObject(ImageObject):

    def __init__(self, x, y, c, img):
        super(DraggableObject, self).__init__(x, y, c)
        self.pil_img: PngImageFile = img
        self.original = img
        self.tk_img = None
        self.size = None
        self.obj = None
        self.initialize()

    def initialize(self):
        self.size = self.pil_img.size
        self.tk_img = ImageTk.PhotoImage(self.pil_img)
        self.obj = self.canvas.create_image(*self._coords, image=self.tk_img, tag='image')
        self.canvas.tag_raise(self.obj)

    def delete(self):
        super(DraggableObject, self).delete()

    def serialize(self):
        coords = self.canvas.coords(self.obj)
        return {'type': 'draggable', 'image': self.pil_img.tobytes(), 'size': (self.pil_img.width, self.pil_img.height),
                'x': coords[0], 'y': coords[1]}

    def resize(self, w, h):
        if (w, h) > self.size:
            self.pil_img = self.original
        self.pil_img = self.pil_img.resize((w, h), resample=Image.CUBIC)
        self.tk_img = ImageTk.PhotoImage(self.pil_img)
        self.size = self.pil_img.size
        self.canvas.itemconfigure(self.obj, image=self.tk_img)

    def collision(self, e, other):
        x, y = e.x, e.y
        mx, my = self.canvas.coords(self.obj)
        w, h = self.pil_img.size
        w2, h2 = w / 2, h / 2
        return mx - w2 <= x <= mx + w2 and my - h2 <= y <= my + h2

import tkinter
from typing import Tuple

from PIL import ImageTk, Image

from constants import DRAG_SIZE


class ImageObject:

    def __init__(self, x: int, y: int, c: tkinter.Canvas, img):
        self._coords: Tuple[int,int] = (x, y)
        self.canvas = c
        self.size = None
        self.index = None
        self.obj = None
        self.pil_img = img
        self.original = []
        self.drag = []
        self.tk_img = []

    def initialize(self):
        self.size = self.pil_img[0].size
        self.original = self.pil_img[:]
        self.to_tk_image()
        self.resize(*self.size)
        self.obj = self.canvas.create_image(*self._coords, image=self.tk_img[0], tag='image')
        self.canvas.tag_raise(self.obj)
        self.check_coords()

    def to_tk_image(self):
        self.tk_img = []
        for image in self.pil_img:
            self.tk_img.append(ImageTk.PhotoImage(image))

    def delete(self):
        self.canvas.delete(self.obj)

    def move(self, x, y):
        x1, y1, x2, y2 = self.canvas.coords(self.canvas.find_withtag('area')[0])
        w, h = self.size
        w2, h2 = w / 2, h / 2
        if x - w2 < x1 or x + w2 > x2 or y - h2 < y1 or y + h2 > y2:
            return
        self.canvas.coords(self.obj, x, y)
        # self._coords = (x, y)

    def resize(self, w, h):
        self.pil_img = self.original[:]
        self.index = 0
        self.to_tk_image()
        for i in range(len(self.pil_img)):
            self.pil_img[i] = self.pil_img[i].resize((w, h), resample=Image.LANCZOS)
            self.tk_img[i] = ImageTk.PhotoImage(self.pil_img[i])
        self.size = self.pil_img[0].size
        self.canvas.itemconfig(self.obj, image=self.tk_img[self.index or 0])

    def rescale(self, pct_w, pct_h):
        # x, y = self._coords
        # self._coords = (x * pct_w, y * pct_h)
        w, h = self.size
        new_w = int(w * pct_w)
        new_h = int(h * pct_h)
        self.resize(new_w, new_h)
        self.check_coords()

    def flip(self, vertically=False):
        self.delete()
        for i in range(len(self.pil_img)):
            self.pil_img[i] = self.pil_img[i].transpose(method=Image.FLIP_TOP_BOTTOM if vertically else Image.FLIP_LEFT_RIGHT)
        self.initialize()

    def collision(self, e):
        x, y = e
        mx, my = self.canvas.coords(self.obj)
        w, h = self.pil_img[0].size
        w2, h2 = w / 2, h / 2
        return mx - w2 <= x <= mx + w2 and my - h2 <= y <= my + h2

    def check_coords(self):
        x1, y1, x2, y2 = self.canvas.coords(self.canvas.find_withtag('area')[0])
        w2, h2 = self.size[0] / 2, self.size[1] / 2
        if self._coords[0] - w2 < x1:
            self._coords = (x1 + w2, self._coords[1])
        if self._coords[0] + w2 > x2:
            self._coords = (x2 - w2, self._coords[1])
        if self._coords[1] - h2 < y1:
            self._coords = (self._coords[0], y1 + h2)
        if self._coords[1] + h2 > y2:
            self._coords = (self._coords[0], y2 - h2)
        self.canvas.coords(self.obj, *self._coords)

    def click(self, e):
        x, y = self._coords
        w2, h2 = self.size[0] / 2, self.size[1] / 2
        return x - w2 <= e.x <= x + w2 and y - h2 <= e.y <= y + h2

    def serialize(self):
        img_bytes = []
        for img in self.pil_img:
            img_bytes.append(img.tobytes())
        data = {'image': img_bytes, 'size': self.size, 'x': self._coords[0], 'y': self._coords[1]}

        return data

    def draw_drag(self, redraw=False):
        x, y = self._coords
        w2, h2 = self.size[0] / 2, self.size[1] / 2
        sizes = [(x - w2 - DRAG_SIZE, y - h2 - DRAG_SIZE, x - w2 + DRAG_SIZE, y - h2 + DRAG_SIZE),
                 (x - DRAG_SIZE, y - h2 - DRAG_SIZE, x + DRAG_SIZE, y - h2 + DRAG_SIZE),
                 (x + w2 - DRAG_SIZE, y - h2 - DRAG_SIZE, x + w2 + DRAG_SIZE, y - h2 + DRAG_SIZE),
                 (x + w2 - DRAG_SIZE, y - DRAG_SIZE, x + w2 + DRAG_SIZE, y + DRAG_SIZE),
                 (x + w2 - DRAG_SIZE, y + h2 - DRAG_SIZE, x + w2 + DRAG_SIZE, y + h2 + DRAG_SIZE),
                 (x - DRAG_SIZE, y + h2 - DRAG_SIZE, x + DRAG_SIZE, y + h2 + DRAG_SIZE),
                 (x - w2 - DRAG_SIZE, y + h2 - DRAG_SIZE, x - w2 + DRAG_SIZE, y + h2 + DRAG_SIZE),
                 (x - w2 - DRAG_SIZE, y - DRAG_SIZE, x - w2 + DRAG_SIZE, y + DRAG_SIZE)]
        for i, size in enumerate(sizes):
            if redraw:
                self.canvas.coords(self.drag[i], *size)
            else:
                self.drag.append(self.canvas.create_rectangle(*size, tag='img_drag', fill='coral1', width=2, outline='red'))

    def drag_resize(self, x, y, drag_id):
        curr_x, curr_y = self._coords
        index = self.drag.index(drag_id)
        if index == 0:
            y_diff = int((curr_y - y) - (self.size[1] // 2))
            x_diff = int((curr_x - x) - (self.size[0] // 2))
            self.resize(self.size[0] + x_diff, self.size[1] + y_diff)
            self._coords = (curr_x - (x_diff / 2), curr_y - (y_diff / 2))
        if index == 1:
            y_diff = int((curr_y - y) - (self.size[1] // 2))
            self.resize(self.size[0], self.size[1] + y_diff)
            self._coords = (curr_x, curr_y - (y_diff / 2))
        if index == 2:
            x_diff = int((x - curr_x) - (self.size[0] // 2))
            y_diff = int((curr_y - y) - (self.size[1] // 2))
            self.resize(self.size[0] + x_diff, self.size[1] + y_diff)
            self._coords = (curr_x + (x_diff / 2), curr_y - (y_diff / 2))
        if index == 3:
            x_diff = int((x - curr_x) - (self.size[0] // 2))
            self.resize(self.size[0] + x_diff, self.size[1])
            self._coords = (curr_x + (x_diff / 2), curr_y)
        if index == 4:
            x_diff = int((x - curr_x) - (self.size[0] // 2))
            y_diff = int((y - curr_y) - (self.size[1] // 2))
            self.resize(self.size[0] + x_diff, self.size[1] + y_diff)
            self._coords = (curr_x + (x_diff / 2), curr_y + (y_diff / 2))
        if index == 5:
            y_diff = int((y - curr_y) - (self.size[1] // 2))
            self.resize(self.size[0], self.size[1] + y_diff)
            self._coords = (curr_x, curr_y + (y_diff / 2))
        if index == 6:
            x_diff = int((curr_x - x) - (self.size[0] // 2))
            y_diff = int((y - curr_y) - (self.size[1] // 2))
            self.resize(self.size[0] + x_diff, self.size[1] + y_diff)
            self._coords = (curr_x - (x_diff / 2), curr_y + (y_diff / 2))
        if index == 7:
            x_diff = int((curr_x - x) - (self.size[0] // 2))
            self.resize(self.size[0] + x_diff, self.size[1])
            self._coords = (curr_x - (x_diff / 2), curr_y)
        self.draw_drag(True)
        self.check_coords()

    def delete_drag(self):
        for drag in self.drag:
            self.canvas.delete(drag)


class CloneableObject(ImageObject):

    def __init__(self, x, y, c, img, order):
        super(CloneableObject, self).__init__(x, y, c, img)
        self.size = (75, 75)
        self.order = order
        self._coords = (50, 120 + 85 * order)
        self.initialize()

    def initialize(self):
        self.order = 0
        self.original = self.pil_img.copy()
        self.to_tk_image()
        self.resize(*self.size)
        self.obj = self.canvas.create_image(*self._coords, image=self.tk_img[0], tag='clone')
        self.canvas.tag_raise(self.obj)

    def delete(self):
        super(CloneableObject, self).delete()

    def serialize(self):
        data = super(CloneableObject, self).serialize()
        data['image'] = [self.original[0].tobytes()]
        data['size'] = self.original[0].size
        data['type'] = 'cloneable'
        data['order'] = self.order
        return data


class ClickableObject(ImageObject):

    def __init__(self, x, y, c, imgs):
        super(ClickableObject, self).__init__(x, y, c, imgs)
        self.index = 0
        self.initialize()

    def initialize(self):
        self.index = 0
        self.original = self.pil_img[:]
        super(ClickableObject, self).initialize()

    def delete(self):
        super(ClickableObject, self).delete()

    def serialize(self):
        data = super(ClickableObject, self).serialize()
        data['type'] = 'clickable'
        return data

    def clicked(self, e):
        width, height = self.pil_img[self.index].size
        w2, h2 = width / 2, height / 2
        x, y = self.canvas.coords(self.obj)
        if (x - w2) <= e.x <= (x + w2) and (y - h2) <= e.y <= (y + h2):
            self.index = self.index + 1 if self.index + 1 < len(self.tk_img) else 0
            self.canvas.itemconfig(self.obj, image=self.tk_img[self.index])

    def collision(self, e):
        return super(ClickableObject, self).collision(e)


class StaticObject(ImageObject):

    def __init__(self, x, y, c, img):
        super(StaticObject, self).__init__(x, y, c, img)
        self.initialize()

    def delete(self):
        super(StaticObject, self).delete()

    def serialize(self):
        data = super(StaticObject, self).serialize()
        data['type'] = 'static'
        return data

    def resize(self, w, h):
        super(StaticObject, self).resize(w, h)

    def collision(self, e):
        return super(StaticObject, self).collision(e)


class DraggableObject(ImageObject):

    def __init__(self, x, y, c, img):
        super(DraggableObject, self).__init__(x, y, c, img)
        self.initialize()

    def delete(self):
        super(DraggableObject, self).delete()

    def serialize(self):
        data = super(DraggableObject, self).serialize()
        data['type'] = 'draggable'
        return data

    def resize(self, w, h):
        super(DraggableObject, self).resize(w, h)

    def collision(self, e):
        return super(DraggableObject, self).collision(e)

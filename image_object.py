import _tkinter
from typing import Tuple

from PIL import ImageTk, Image

from constants import DRAG_SIZE, CLONE_SIZE, COPY_OFFSET, CLONE_X, CLONE_Y, AREA_X2, AREA_X1, AREA_Y1, AREA_Y2


class ImageObject:

    def __init__(self, x: int, y: int, parent, img, visible=True):
        self._coords: Tuple[int, int] = (x, y)
        self.parent = parent
        self.canvas = parent.canvas
        self.student = self.parent.student
        self.size = None
        self.index = None
        self.obj = None
        self.deletable = True
        self.visible = visible
        self.pil_img = img
        self.offset = None
        self.original = []
        self.drag = []
        self.tk_img = []

    def initialize(self, reset=False):
        self.size = self.pil_img[0].size
        self.original = self.pil_img[:]
        self.to_tk_image()
        self.resize(*self.size)
        if not reset:
            self.obj = self.canvas.create_image(*self._coords, image=self.tk_img[0], tag='image',
                                                state='hidden' if not self.visible and self.student else 'normal')
        else:
            self.canvas.itemconfig(self.obj, image=self.tk_img[0])
        self.canvas.tag_raise(self.obj)
        self.check_image_size()
        self.check_coords()

    def check_image_size(self):
        w, h = self.pil_img[0].size
        if w > AREA_X2 - AREA_X1:
            scale = (AREA_X2 - AREA_X1) / w
            self.resize(AREA_X2 - AREA_X1, scale * h)
        w, h = self.pil_img[0].size
        if h > AREA_Y2 - AREA_Y1:
            scale = (AREA_Y2 - AREA_Y1) / h
            self.resize(scale * w, AREA_Y2 - AREA_Y1)

    def reset(self):
        self.pil_img = self.original[:]
        self.initialize(True)

    def to_tk_image(self):
        self.tk_img = []
        for image in self.pil_img:
            self.tk_img.append(ImageTk.PhotoImage(image))

    def delete(self):
        if self.deletable:
            self.delete_drag()
            self.canvas.delete(self.obj)

    def move(self, x, y):
        if not self.offset:
            self.offset = (x - self._coords[0], self._coords[1] - y)
            return
        x1, y1, x2, y2 = self.canvas.coords(self.canvas.find_withtag('area')[0])
        w, h = self.size
        w2, h2 = w / 2, h / 2
        off_x, off_y = self.offset
        if (x - off_x) - w2 < x1 or (x - off_x) + w2 > x2 or (y + off_y) - h2 < y1 or (y + off_y) + h2 > y2:
            return
        self.canvas.coords(self.obj, x - off_x, y + off_y)
        self._coords = (x - off_x, y + off_y)

    def resize(self, w, h):
        w, h = int(w), int(h)
        self.pil_img = self.original[:]
        self.index = 0
        self.to_tk_image()
        for i in range(len(self.pil_img)):
            self.pil_img[i] = self.pil_img[i].resize((w, h), resample=Image.LANCZOS)
            self.tk_img[i] = ImageTk.PhotoImage(self.pil_img[i])
        self.size = self.pil_img[0].size
        self.canvas.itemconfig(self.obj, image=self.tk_img[self.index or 0])

    def rescale(self, pct_w, pct_h, resize=True):
        w, h = self.size
        new_w = int(w * pct_w)
        new_h = int(h * pct_h)
        if resize:
            self.resize(new_w, new_h)
        w1, h1, w2, h2 = self.canvas.bbox(self.obj)
        self._coords = (pct_w * w1 + (w2 - w1) / 2, pct_h * h1 + (h2 - h1) / 2)
        self.check_coords()

    def flip(self, vertically=False):
        self.delete()
        for i in range(len(self.pil_img)):
            self.pil_img[i] = self.pil_img[i].transpose(
                method=Image.FLIP_TOP_BOTTOM if vertically else Image.FLIP_LEFT_RIGHT)
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
        for img in self.original:
            img_bytes.append((img.mode, img.tobytes()))
        data = {'image': img_bytes, 'size': self.original[0].size, 'x': self._coords[0], 'y': self._coords[1],
                'visible': self.visible}
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
                self.drag.append(self.canvas.create_rectangle(
                    *size, tag='img_drag', fill='coral1', width=2, outline='red'))
        self.canvas.tag_raise('img_drag')

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
        self.drag = []


class CloneableObject(ImageObject):

    def __init__(self, x, y, c, img, order, visible=True):
        super(CloneableObject, self).__init__(x, y, c, img, visible)
        self.order = order
        self._coords = (0, )
        self.initialize()

    def initialize(self, reset=False):
        self._coords = (CLONE_X, CLONE_Y + 78 * self.order)
        self.original = self.pil_img.copy()
        w, h = self.original[0].size
        self.size = self.original[0].size
        if w > CLONE_SIZE:
            self.size = (CLONE_SIZE, int((CLONE_SIZE / w) * h))
        if self.size[1] > CLONE_SIZE:
            self.size = (int((CLONE_SIZE / h) * w), CLONE_SIZE)
        self.to_tk_image()
        self.resize(*self.size)
        if not reset:
            self.obj = self.canvas.create_image(*self._coords, image=self.tk_img[0], tag='clone')
        else:
            self.canvas.itemconfig(self.obj, image=self.tk_img[0], tag='clone')
        self.canvas.tag_raise(self.obj)

    def delete(self):
        super(CloneableObject, self).delete()

    def serialize(self):
        data = super(CloneableObject, self).serialize()
        data['image'] = [(self.original[0].mode, self.original[0].tobytes())]
        data['size'] = self.original[0].size
        data['type'] = 'cloneable'
        data['order'] = self.order
        return data


class ClickableObject(ImageObject):

    def __init__(self, x, y, c, imgs, visible=True):
        super(ClickableObject, self).__init__(x, y, c, imgs, visible)
        self.index = 0
        self.dragging_mode = False
        self.initialize()

    def delete(self):
        super(ClickableObject, self).delete()

    def serialize(self):
        data = super(ClickableObject, self).serialize()
        data['type'] = 'clickable'
        return data

    def clicked(self, e):
        if self.dragging_mode:
            return
        self.index = self.index + 1 if self.index + 1 < len(self.tk_img) else 0
        self.canvas.itemconfig(self.obj, image=self.tk_img[self.index])

    def collision(self, e):
        return super(ClickableObject, self).collision(e)

    def move(self, x, y):
        if not self.student and self.dragging_mode:
            super(ClickableObject, self).move(x, y)

    def __copy__(self):
        x, y = self._coords
        return ClickableObject(x + COPY_OFFSET, y + COPY_OFFSET, self.parent, self.pil_img[:], self.visible)


class StaticObject(ImageObject):

    def __init__(self, x, y, c, img, visible=True):
        super(StaticObject, self).__init__(x, y, c, img, visible)
        self.initialize()

    def delete(self):
        super(StaticObject, self).delete()

    def serialize(self):
        data = super(StaticObject, self).serialize()
        data['type'] = 'static'
        return data

    def resize(self, w, h):
        if not self.student:
            super(StaticObject, self).resize(w, h)

    def collision(self, e):
        return super(StaticObject, self).collision(e)

    def move(self, x, y):
        if not self.student:
            super(StaticObject, self).move(x, y)

    def __copy__(self):
        x, y = self._coords
        return StaticObject(x + COPY_OFFSET, y + COPY_OFFSET, self.parent, self.pil_img[:], self.visible)


class DraggableObject(ImageObject):

    def __init__(self, x, y, c, img, visible=True):
        super(DraggableObject, self).__init__(x, y, c, img, visible)
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

    def __copy__(self):
        x, y = self._coords
        return DraggableObject(x + COPY_OFFSET, y + COPY_OFFSET, self.parent, self.pil_img[:], self.visible)


class StaticButton(ImageObject):

    def __init__(self, x, y, c, img, oid, visible=True):
        super(StaticButton, self).__init__(x, y, c, img, visible)
        self.oid = oid
        self.initialize()

    def delete(self):
        self.parent.delete_marker()
        try:
            self.canvas.itemconfig(self.oid, state='normal')
        except _tkinter.TclError:
            pass
        super(StaticButton, self).delete()

    def move(self, x, y):
        if not self.student:
            self.parent.delete_marker()
            super(StaticButton, self).move(x, y)

    def serialize(self):
        data = super(StaticButton, self).serialize()
        data['type'] = 'button'
        data['parent'] = self.oid
        return data

    def marker(self):
        self.parent.delete_marker()
        w, h = self.size
        x, y = self._coords
        self.parent.marker = (self.canvas.create_rectangle(
            x - w / 2, y - w / 2, x + w / 2, y + h / 2, outline='red', width=4), self.oid)


class DraggableButtonImage(ImageObject):

    def __init__(self, x, y, c, img, visible=True):
        super(DraggableButtonImage, self).__init__(x, y, c, img, visible)
        self.size = (img[0].width, img[0].height)
        self._coords = (x, y)
        self.initialize()

    def initialize(self, reset=False):
        self.original = self.pil_img.copy()
        self.to_tk_image()
        self.resize(*self.size)
        self.obj = self.canvas.create_image(*self._coords, image=self.tk_img[0], tag='button_clone')
        self.canvas.tag_raise(self.obj)

    def delete(self):
        super(DraggableButtonImage, self).delete()

    def rescale(self, pct_w, pct_h, resize=False):
        w, h = self.size
        w1, h1, w2, h2 = self.canvas.coords(self.parent.area)
        self._coords = (4 + w2 + (w / 2), self._coords[1])
        self.canvas.coords(self.obj, *self._coords)

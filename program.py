import copy
import pickle
import tkinter
from tkinter import filedialog, messagebox
from typing import Tuple
from PIL import Image
from functions import get_images, get_image
from image_object import StaticObject, ClickableObject, DraggableObject
from serialize import deserialize_images, deserialize_tables, deserialize_tools, deserialize_text, deserialize_clones, \
    deserialize_background
from table import Table


class Program:

    def __init__(self, canvas: tkinter.Canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.images = dict()
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_up)
        self.canvas.bind('<Button-1>', self.click)
        self.canvas.bind('<Configure>', self.on_resize)

        self.student = False
        self.resizing = False
        self.canvas.created_images = []
        self.background = None
        self.buttons = []
        self.created_objects = []
        self.added_tools = []
        self.created_images = []
        self.cloneable_images = []
        self.marker = None
        self.clicked_object = None
        self.dragging = None
        self.path = None
        self.action = False
        self.clicked_resizer = False
        self.serialized_data = []
        self.area = None

    def init(self):
        self.initialize_buttons()
        self.area = self.canvas.create_rectangle(100, 75, 1200, 694, width=5, outline='black', tag='area')
        self.canvas.update()

    def initialize_buttons(self):
        pass

    def moved_image(self, e, dragged_id):
        img = next(filter(lambda x: x.obj == dragged_id, self.created_images), None)
        if img:
            if not self.clicked_resizer:
                img.delete_drag()
                img.move(e.x, e.y)
                self.remove_from_table(img)
            self.dragging = None
            return True
        return False

    def moved_tool(self, e, dragged_id):
        tool = next(filter(lambda x: x.obj == dragged_id, self.added_tools), None)
        if tool:
            if not (self.clicked_resizer and abs(tool._coords[0] - e.x) < 5 and abs(tool._coords[1] - e.y) < 5):
                tool.move(e.x, e.y)
            return True
        return False

    def moved_table(self, e, dragged_id):
        for obj in self.created_objects:
            if isinstance(obj, Table) and obj.drag == dragged_id:
                obj.move_table(e.x, e.y)
                return True
        return False

    def resize_image(self, e, dragged_id):
        for image in self.created_images:
            if dragged_id in image.drag:
                self.dragging = dragged_id
                image.drag_resize(e.x, e.y, dragged_id)

    def drag(self, e):
        curr: Tuple = self.canvas.find_withtag('current')
        if len(curr) == 0:
            return
        dragged_id = self.canvas.find_withtag('current')[0]
        if self.background and dragged_id == self.background.obj:
            return
        self.dragging = dragged_id
        self.canvas.tag_raise(dragged_id)
        if dragged_id in self.canvas.find_withtag('clone'):
            self.create_clone(dragged_id, e)
            return
        coords = self.canvas.coords(dragged_id)
        if len(coords) == 2 and dragged_id > len(self.buttons):
            if self.moved_image(e, dragged_id):
                return
            if self.moved_tool(e, dragged_id):
                return
            for x in self.created_objects:
                if x.obj == dragged_id:
                    x.move(e.x, e.y)
        else:
            if self.moved_table(e, dragged_id):
                return
            self.resize_image(e, dragged_id)

    def on_resize(self, e):
        if not self.resizing:
            self.resizing = True
            wscale = e.width / self.width
            hscale = e.height / self.height
            self.width = e.width
            self.height = e.height
            self.canvas.config(width=self.width, height=self.height)
            h = ((self.width - 180) / 16) * 9
            # self.canvas.scale('all', 0, 0, wscale, hscale)
            self.canvas.coords(self.area, 100, 75, self.width - 80, h + 75)
            for image in self.created_images:
                image.rescale(wscale, hscale)

            # for i in self.buttons:
            #     i.resize()
            self.resizing = False

    def click(self, e):
        if self.canvas.find_withtag('current') and \
                self.canvas.find_withtag('current')[0] in self.canvas.find_withtag('img_drag'):
            return
        x1, y1, x2, y2 = self.canvas.coords(self.canvas.find_withtag('area')[0])
        if x1 <= e.x <= x2 and y1 <= e.y <= y2:
            self.clicked_canvas(e)

    def mouse_up(self, e):
        if self.action:
            self.action = False
            self.delete_marker()
            self.clicked_resizer = False
        if self.dragging:
            if self.canvas.type(self.dragging) == 'image':
                self.set_image_coords(self.find_dragged_object(), (e.x, e.y))
                self.remove_from_table()
                self.add_to_table()
                self.dragging = None
        else:
            for x in self.created_images:
                self.add_to_table(x)

    @staticmethod
    def create_image_dict(path, image_list):
        img = {}
        for item in image_list:
            img[item] = (Image.open(f'{path}{item}.png'), tkinter.PhotoImage(file=f'{path}{item}.png'))
        return img

    def new_exercise(self):
        if self.serialized_data != self.get_serialized_data():
            self.ask_save()
        self.delete_all()

    def load_exercise(self):
        if self.serialized_data != self.get_serialized_data():
            self.ask_save()
        path = filedialog.askopenfilename(
            filetypes=[('Rozpracovane riesenie', '*.pickle')], defaultextension='*.pickle', initialdir='./exercises')
        if not path:
            return
        self.path = path[path.rindex('/') + 1:]
        with open(path, 'rb') as read:
            serialized = pickle.load(read)
        self.delete_all()
        self.serialized_data = serialized
        self.deserialize()

    def deserialize(self):
        # this MUST be first, no idea why
        self.added_tools = deserialize_tools(self, self.student)

        self.created_objects = deserialize_tables(self)
        self.created_images = deserialize_images(self, self.student)
        for image in self.created_images:
            self.add_to_table(image)
        self.created_objects.extend(deserialize_text(self))
        self.cloneable_images = deserialize_clones(self)
        self.background = deserialize_background(self)
        self.lower_bg()

    def save_exercise(self):
        filename = filedialog.asksaveasfile(
            'wb', filetypes=[('Rozpracovane riesenie', '*.pickle')], defaultextension='*.pickle',
            initialdir='./exercises', initialfile=self.path)
        if filename is not None and not isinstance(filename, tuple):
            self.serialized_data = self.get_serialized_data()
            self.path = filename.name[:filename.name.rindex('/')]
            pickle.dump(self.serialized_data, filename)

    def mark(self):
        self.delete_marker()
        x, y = self.canvas.coords(self.clicked_object)
        w, h = 28, 24
        if self.clicked_object > 11:
            w, h = 28, 28
        self.marker = \
            (self.canvas.create_rectangle(x - w, y - h, x + w, y + h, outline='red', width=5), self.clicked_object)

    def delete_marker(self):
        if self.marker:
            self.canvas.delete(self.marker[0])
            self.marker = None

    # TODO rewrite
    def clicked_canvas(self, e):
        if self.marker:
            types = {12: self.image_resizer, 13: self.flip_horizontally, 14: self.flip_vertically, 15: self.copy,
                     16: self.delete}
            self.action = True
            # noinspection PyArgumentList
            types[self.marker[1]](e)
            if len(self.created_images):
                self.created_images[-1].check_coords()
            return
        curr = self.canvas.find_withtag('current')
        if curr:
            for tool in self.added_tools:
                if tool.obj == curr[0]:
                    if tool.oid in [12, 13, 14, 15, 16]:
                        tool.marker()
                        self.clicked_resizer = True
                        return
        for item in reversed(self.created_images):
            item.delete_drag()
            if isinstance(item, ClickableObject):
                if item.click(e):
                    item.clicked(e)
                    return
        self.clicked_resizer = False

    def copy(self, e):
        for image in reversed(self.created_images):
            if image.click(e):
                self.created_images.append(copy.copy(image))
                return
        for obj in reversed(self.created_objects):
            if obj.click(e):
                self.created_objects.append(copy.copy(obj))

    def delete(self, e):
        for image in reversed(self.created_images):
            if image.click(e) and image.deletable:
                image.delete()
                self.remove_from_table(image)
                self.created_images.remove(image)
                return

    def add_to_table(self, obj=None):
        if obj is not None:
            dragged_image = obj
        else:
            dragged_image = self.find_dragged_object()
        if not dragged_image:
            return
        for item in self.created_objects:
            if isinstance(item, Table):
                item.add_object(dragged_image)

    def remove_from_table(self, object_id=None):
        dragged_image = self.find_dragged_object() if not object_id else object_id
        for item in self.created_objects:
            if isinstance(item, Table):
                item.remove_object(dragged_image)

    def find_dragged_object(self):
        for item in self.created_images:
            if item.obj == self.dragging:
                return item

    def snap_to_table(self):
        for obj in self.created_images:
            self.add_to_table(obj)

    def set_image_coords(self, img, coords):
        for obj in self.created_images:
            if img == obj:
                img.move(*coords)
        # if not self.in_collision(coords, img):
        #     for obj in self.created_images:
        #         if img == obj:
        #             img._coords = coords
        # else:
        #     self.canvas.coords(img.obj, *img._coords)

    def in_collision(self, coords, obj):
        for img in self.created_images:
            if obj != img and img.collision(coords):
                return True
        return False

    def delete_all(self):
        for obj in self.cloneable_images + self.added_tools + self.created_objects + self.created_images:
            obj.delete()
        self.cloneable_images = self.added_tools = self.created_objects = self.created_images = []
        if self.background:
            self.background.delete()
        self.background = None
        self.serialized_data = []

    def create_static_object(self, e):
        image = get_image()
        if not image:
            return
        self.created_images.append(StaticObject(e.x, e.y, self, [image]))
        self.add_to_table(self.created_images[-1])

    def create_moveable_object(self, e):
        image = get_image()
        if not image:
            return
        self.created_images.append(DraggableObject(e.x, e.y, self, [image]))
        self.add_to_table(self.created_images[-1])

    def create_clickable_object(self, e):
        images = get_images()
        if len(images) == 0:
            return
        self.created_images.append(ClickableObject(e.x, e.y, self, images))
        self.add_to_table(self.created_images[-1])

    def lower_bg(self):
        self.canvas.tag_lower('bg')

    def create_clone(self, oid, e):
        for img in self.cloneable_images:
            if img.obj == oid:
                self.created_images.append(DraggableObject(e.x, e.y, self, img.original.copy()))
                self.created_images[-1].check_coords()
                self.dragging = self.created_images[-1].obj
                self.canvas.itemconfig(oid, tag='clone')
                self.canvas.itemconfig(self.dragging, tag='current')

    def get_image_by_id(self, id_):
        if self.background and self.background.obj == id_:
            return self.background
        for image in reversed(self.created_images + self.cloneable_images + self.added_tools):
            if image.obj == id_:
                return image
        return

    def get_text_by_id(self, id_):
        for item in self.created_objects:
            if item.obj == id_:
                return item
        return

    def get_serialized_data(self):
        serialized = []
        for obj in self.created_objects + self.created_images + self.cloneable_images + self.added_tools:
            serialized.append(obj.serialize())
        if self.background:
            serialized.append(self.background.serialize())
        return serialized

    def ask_save(self):
        if messagebox.askyesno(title='Alert', message='Chces ulozit zadanie?'):
            self.save_exercise()

    def flip_vertically(self, e):
        for image in reversed(self.created_images):
            if image.click(e):
                image.flip(True)
                return

    def flip_horizontally(self, e):
        for image in reversed(self.created_images):
            if image.click(e):
                image.flip()
                return

    def image_resizer(self, e):
        for image in reversed(self.created_images):
            if image.click(e):
                image.draw_drag()
                return

import pickle
import tkinter
from tkinter import filedialog, messagebox
from typing import Tuple
from PIL import Image

from background import Background
from button import DraggableButton
from functions import get_images, get_image
from image_object import StaticObject, ClickableObject, DraggableObject, CloneableObject
from table import Table
from text import Text


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
        self.serialized_data = []
        self.area = None
        self.table_widget = None
        self.text_widget = None

    def init(self):
        self.initialize_buttons()
        self.area = self.canvas.create_rectangle(100, 75, 1000, 700, width=5, outline='black', tag='area')
        self.canvas.update()

    def initialize_buttons(self):
        pass

    def drag(self, e):
        curr: Tuple = self.canvas.find_withtag('current')
        if len(curr) == 0:
            return
        dragged_id = self.canvas.find_withtag('current')[0]

        if dragged_id in self.canvas.find_withtag('clone'):
            self.create_clone(dragged_id, e)
            return
        coords = self.canvas.coords(dragged_id)
        if len(coords) == 2 and dragged_id > len(self.buttons):
            for img in self.created_images + self.added_tools:
                if img.obj == dragged_id:
                    img.delete_drag()
                    img.move(e.x, e.y)
            for x in self.created_objects:
                if x.obj == dragged_id:
                    x.move(e.x, e.y)
            self.dragging = dragged_id
        else:
            for obj in self.created_objects:
                if isinstance(obj, Table) and obj.drag == dragged_id:
                    obj.move_table(e.x, e.y)
                    return
            for image in self.created_images:
                if dragged_id in image.drag:
                    self.dragging = dragged_id
                    image.drag_resize(e.x, e.y, dragged_id)

    def on_resize(self, e):
        if not self.resizing:
            self.resizing = True
            wscale = e.width / self.width
            hscale = e.height / self.height
            self.width = e.width
            self.height = e.height
            self.canvas.config(width=self.width, height=self.height)
            # self.canvas.coords(self.area, 100, 75, self.width - 80, self.height - 20)
            # for image in self.created_images:
            #     image.rescale(wscale, hscale)
            self.canvas.scale('all', 0, 0, wscale, hscale)

            # for i in self.buttons:
            #     i.resize()
            # print(self.canvas.coords(self.canvas.find_withtag('area')[0]))

            # map(lambda x: x.resize, self.buttons)
            self.resizing = False

    def click(self, e):
        if self.canvas.find_withtag('current') and self.canvas.find_withtag('current')[0] in self.canvas.find_withtag('img_drag'):
            return
        x1, y1, x2, y2 = self.canvas.coords(self.canvas.find_withtag('area')[0])
        if x1 <= e.x <= x2 and y1 <= e.y <= y2:
            self.clicked_canvas(e)

    def mouse_up(self, e):
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

    # TODO rewrite
    def load_exercise(self):
        if self.serialized_data != self.get_serialized_data():
            self.ask_save()
        path = filedialog.askopenfilename(filetypes=[('Rozpracovane riesenie',
                                                   '*.pickle')], defaultextension='*.pickle', initialdir='./exercises')
        if not path:
            return
        self.path = path[path.rindex('/') + 1:]
        with open(path, 'rb') as read:
            serialized = pickle.load(read)
        self.delete_all()
        self.serialized_data = serialized
        for obj in serialized:
            if obj['type'] == 'table':
                table = Table(self, obj['data'], obj['x'], obj['y'], obj['color'])
                table.draw_table()
                self.created_objects.append(table)
        def read(data, size):
            images = []
            for item in data:
                mode, img = item
                images.append(Image.frombytes(mode, size, img))
            return images

        for obj in serialized:
            if obj['type'] == 'text':
                self.created_objects.append(Text(obj['x'], obj['y'], self, obj['text'], obj['size'], obj['color'], obj['font']))
            if obj['type'] == 'cloneable':
                self.cloneable_images.append(
                    CloneableObject(0, 0, self, read(obj['image'], obj['size']), obj['order']))
            if obj['type'] == 'background':
                self.background = Background(read(obj['image'], obj['size']), self)
                self.lower_bg()
            if obj['type'] == 'static':
                self.created_images.append(
                    StaticObject(obj['x'], obj['y'], self, read(obj['image'], obj['size'])))
                self.add_to_table(self.created_images[-1])
            if obj['type'] == 'clickable':

                self.created_images.append(ClickableObject(obj['x'], obj['y'], self, read(obj['image'], obj['size'])))
                self.add_to_table(self.created_images[-1])
            if obj['type'] == 'draggable':
                self.created_images.append(
                    DraggableObject(obj['x'], obj['y'], self, read(obj['image'], obj['size'])))
                self.add_to_table(self.created_images[-1])

    def save_exercise(self):
        filename = filedialog.asksaveasfile('wb', filetypes=[('Rozpracovane riesenie', '*.pickle')],
                                            defaultextension='*.pickle', initialdir='./exercises', initialfile=self.path)
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
            if self.marker[1] == self.clicked_object:
                self.clicked_object = None
            self.marker = None

    def clicked_canvas(self, e):
        if self.marker:
            types = {5: self.create_clickable_object, 6: self.create_moveable_object, 7: self.create_cloneable_object,
                     8: self.create_static_object, 12: self.image_resizer, 13: self.flip_horizontally, 14: self.flip_vertically}
            types[self.marker[1]](e)
            self.delete_marker()
            if len(self.created_images):
                self.created_images[-1].check_coords()
            return
        for item in self.created_images:
            item.delete_drag()
            if isinstance(item, ClickableObject):
                item.clicked(e)
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

    def remove_from_table(self):
        dragged_image = self.find_dragged_object()
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
        # if not self.in_collision(coords, img):
        if True:
            for obj in self.created_images:
                if img == obj:
                    img._coords = coords
        else:
            self.canvas.coords(img.obj, *img._coords)

    def in_collision(self, coords, obj):
        for img in self.created_images:
            if obj != img and img.collision(coords):
                return True
        return False

    def delete_all(self):
        for obj in self.cloneable_images:
            obj.delete()
        self.cloneable_images = []
        for obj in self.created_objects:
            obj.delete()
        self.created_objects = []
        for obj in self.created_images:
            obj.delete()
        self.created_images = []
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
        for image in self.created_images + self.cloneable_images + self.added_tools:
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
        for obj in self.created_objects:
            serialized.append(obj.serialize())
        for img in self.created_images:
            serialized.append(img.serialize())
        for img in self.cloneable_images:
            serialized.append(img.serialize())
        if self.background:
            serialized.append(self.background.serialize())
        return serialized

    def ask_save(self):
        if messagebox.askyesno(title='Alert', message='Chces ulozit zadanie?'):
            self.save_exercise()

    def flip_vertically(self, e):
        for image in self.created_images:
            if image.click(e):
                image.flip(True)

    def flip_horizontally(self, e):
        for image in self.created_images:
            if image.click(e):
                image.flip()

    def image_resizer(self, e):
        for image in self.created_images:
            if image.click(e):
                image.draw_drag()

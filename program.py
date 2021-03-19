import pickle
import tkinter
from tkinter import filedialog
from typing import Tuple
from PIL import Image

from button import Button
from image_object import StaticObject, ImageObject
from table import Table
from table_widget import TableWidget


class Program:

    def __init__(self, canvas: tkinter.Canvas):
        self.canvas = canvas
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_up)
        self.canvas.bind('<Button-1>', self.click)
        self.canvas.images = self.images = \
            self.create_image_dict('textures/', ['new_task', 'save', 'save_final', 'load', 'clickable',
                                                 'moveable', 'clone', 'static', 'table', 'text', 'background'])
        self.canvas.created_images = []
        self.buttons = []
        self.created_objects = []
        self.marker = None
        self.clicked_object = None
        self.dragging = None
        self.initialize_buttons()
        self.canvas.create_rectangle(100, 75, 980, 700, width=5, outline='black')
        self.table_widget = None
        self.canvas.update()

    def drag(self, e):
        curr: Tuple = self.canvas.find_withtag('current')
        if len(curr) == 0:
            return
        dragged_id = self.canvas.find_withtag('current')[0]
        coords = self.canvas.coords(dragged_id)
        if len(coords) == 2 and dragged_id > len(self.buttons):
            self.dragging = dragged_id
            self.canvas.coords(dragged_id, (e.x, e.y))
        else:
            for obj in self.created_objects:
                if isinstance(obj, Table) and obj.drag == dragged_id:
                    obj.move_table(e.x, e.y)
                    return

    def click(self, e):
        if 0 <= e.x <= 50 and 0 <= e.y <= 50:
            for obj in self.created_objects:
                obj.delete()
            self.created_objects = []
        if 100 <= e.x <= 980 and 75 <= e.y <= 700:
            self.clicked_canvas(e)
            return
        btn_ids = {2: self.save_exercise, 4: self.load_exercise, 5: self.mark, 6: self.mark,
                   7: self.mark, 8: self.mark, 9: self.create_table_widget}
        curr = self.canvas.find_withtag('current')
        if not len(curr):
            return
        self.clicked_object = curr[0]
        btn_ids[self.clicked_object]()

    def mouse_up(self, e):
        if self.dragging and self.canvas.type(self.dragging) == 'image':
            self.remove_from_table()
            self.add_to_table()
            self.dragging = None
        else:
            for x in self.created_objects:
                if not isinstance(x, Table):
                    self.add_to_table(x)

    @staticmethod
    def create_image_dict(path, image_list):
        img = {}
        for item in image_list:
            img[item] = tkinter.PhotoImage(file=f'{path}{item}.png')
        return img

    def initialize_buttons(self):
        x = 20
        y = 30
        for key in self.images:
            self.buttons.append(Button(self.images[key], x, y, self.canvas))
            x += 50
            if key == 'load':
                x += 150
            if key == 'static':
                x += 100
        self.canvas.update()

    def create_table_widget(self):
        if not self.table_widget:
            self.table_widget = TableWidget(self)

    def create_table(self):
        data = []
        for counter in self.table_widget.counters:
            data.append(counter.value)
        new_table = Table(self.canvas, data, 200, 200)
        new_table.draw_table()
        self.created_objects.append(new_table)
        self.table_widget = None

    def load_exercise(self):
        path = filedialog.askopenfilename(filetypes=[('Rozpracovane riesenie',
                                                   '*.pickle')], defaultextension='*.pickle', initialdir='./exercises')
        with open(path, 'rb') as read:
            serialized = pickle.load(read)
        for obj in serialized:
            if obj['type'] == 'table':
                table = Table(self.canvas, obj['data'], obj['x'], obj['y'])
                table.draw_table()
                self.created_objects.append(table)
        for obj in serialized:
            if obj['type'] == 'static':
                self.created_objects.append(
                    StaticObject(obj['x'], obj['y'], self.canvas, Image.frombytes('RGB', obj['size'], obj['image'])))
                self.add_to_table(self.created_objects[-1])

    def save_exercise(self):
        filename = filedialog.asksaveasfile('wb', filetypes=[('Rozpracovane riesenie',
                                                          '*.pickle')], defaultextension='*.pickle', initialdir='./exercises')

        serialized_objects = []
        for obj in self.created_objects:
            serialized_objects.append(obj.serialize())
        if filename is not None and not isinstance(filename, tuple):
            pickle.dump(serialized_objects, filename)

    def mark(self):
        self.delete_marker()
        x, y = self.canvas.coords(self.clicked_object)
        self.marker = \
            (self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, outline='red'), self.clicked_object)

    def delete_marker(self):
        if self.marker:
            self.canvas.delete(self.marker[0])
            if self.marker[1] == self.clicked_object:
                self.clicked_object = None
            self.marker = None

    def clicked_canvas(self, e):
        if self.marker:
            types = {5: self.create_clickable_object, 8: self.create_static_object}
            types[self.marker[1]](e)

            self.delete_marker()

    def create_static_object(self, e):
        filename = filedialog.askopenfilename(title='Vyber obrazok', initialdir='./textures',
                                              filetypes=[('Obrazky', '*.png')])
        img = Image.open(filename)
        self.created_objects.append(StaticObject(e.x, e.y, self.canvas, img))

    def create_clickable_object(self, e):
        filenames = filedialog.askopenfilenames(title='Vyber obrazok', initialdir='./textures',
                                                filetypes=[('Obrazky', '*.png')])
        print(filenames)

    def add_to_table(self, obj=None):
        if obj is not None:
            dragged_image = obj
        else:
            dragged_image = self.find_dragged_object()
        for item in self.created_objects:
            if isinstance(item, Table):
                item.add_object(dragged_image)

    def remove_from_table(self):
        dragged_image = self.find_dragged_object()
        for item in self.created_objects:
            if isinstance(item, Table):
                item.remove_object(dragged_image)

    def find_dragged_object(self):
        for item in self.created_objects:
            if item.obj == self.dragging:
                return item

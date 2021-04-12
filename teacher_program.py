import time
import tkinter

from background import Background
from button import DraggableButton, Button
from functions import get_image
from image_menu import ImageMenu
from image_object import CloneableObject, StaticButton
from program import Program
from table import Table
from table_menu import TableMenu
from table_widget import TableWidget
from text import Text
from text_menu import TextMenu
from text_widget import TextWidget


class TeacherProgram(Program):

    def __init__(self, canvas: tkinter.Canvas, width, height):
        super(TeacherProgram, self).__init__(canvas, width, height)
        self.student = False
        self.canvas.bind('<Button-3>', self.right_click)
        self.canvas.images = self.images = \
            self.create_image_dict('textures/', ['new_task', 'save', 'save_final', 'load', 'clickable',
                                                 'moveable', 'clone', 'static', 'table', 'text', 'background',
                                                 'enlarge', 'flip_horizontal', 'flip_vertical', 'copy', 'bin'])
        self.menu = None
        self.table_widget = None
        self.text_widget = None
        self.coords = None
        self.init()

    # TODO rewrite
    def right_click(self, e):
        try:
            clicked = self.canvas.find_withtag('current')[0]
        except IndexError:
            return
        if clicked < 17:
            return
        for item in reversed(self.created_objects):
            if isinstance(item, Table) and clicked == item.drag:
                self.menu = TableMenu(self, item)
                self.menu.menu.tk_popup(e.x_root, e.y_root)
                return
        if clicked in self.canvas.find_withtag('text'):
            self.menu = TextMenu(self, self.get_text_by_id(clicked))
            self.menu.menu.tk_popup(e.x_root, e.y_root)
            return
        if clicked not in self.canvas.find_withtag('image'):
            if self.canvas.type(clicked) == 'image':
                self.canvas.itemconfig(clicked, tag='image')
            else:
                return
        image = self.get_image_by_id(clicked)
        self.menu = ImageMenu(self, image, image in self.cloneable_images or (
                    self.background and clicked == self.background.obj))
        self.menu.menu.tk_popup(e.x_root, e.y_root)

    def create_background(self):
        image = get_image()
        if not image:
            return
        self.background = Background([image], self)
        self.lower_bg()

    def click(self, e):
        super(TeacherProgram, self).click(e)
        btn_ids = {1: self.new_exercise, 2: self.save_exercise, 4: self.load_exercise, 5: self.mark, 6: self.mark,
                   7: self.create_cloneable_object, 8: self.mark, 9: self.mark,
                   10: self.mark, 11: self.create_background}
        curr = self.canvas.find_withtag('current')
        if not len(curr) or curr[0] > 11:
            return
        self.clicked_object = curr[0]
        btn_ids[self.clicked_object]()

    def create_table_widget(self, e):
        if not self.table_widget:
            self.coords = (e.x, e.y)
            self.table_widget = TableWidget(self)

    def create_text_widget(self, e):
        if not self.text_widget:
            self.coords = (e.x, e.y)
            self.text_widget = TextWidget(self)

    def create_cloneable_object(self):
        image = get_image()
        if not image:
            return
        self.cloneable_images.append(CloneableObject(0, 0, self, [image], len(self.cloneable_images)))

    def create_text(self, empty=False):
        if empty:
            self.text_widget = None
            return
        text = Text(*self.coords, self, self.text_widget.text, self.text_widget.default_size.get(),
                    self.text_widget.rgb, self.text_widget.default_font.get())
        self.created_objects.append(text)
        self.text_widget = None

    def create_table(self, empty=False):
        if empty:
            self.table_widget = None
            return
        data = []
        for counter in self.table_widget.counters:
            data.append(counter.value)
        new_table = Table(self, data, *self.coords, self.table_widget.rgb)
        new_table.draw_table()
        self.created_objects.append(new_table)
        self.table_widget = None
        self.snap_to_table()

    def initialize_buttons(self):
        x = 30
        y = 33
        for key in list(self.images.keys())[:-5]:
            self.buttons.append(Button(self.images[key][1], x, y, self, left_pct=x/self.width))
            x += 60
            if key == 'load':
                x += 300
            if key == 'static':
                x += 200
        x = 1240
        y = 100
        for key in list(self.images.keys())[-5:]:
            self.buttons.append(DraggableButton(self.images[key][0], x, y, self))
            y += 70

    def create_button_clone(self, oid, e):
        for button in self.buttons:
            if isinstance(button, DraggableButton) and button.image.obj == oid:
                self.canvas.itemconfig(oid, state='hidden')
                self.added_tools.append(StaticButton(e.x, e.y, self, button.image.original.copy(), oid))
                self.added_tools[-1].check_coords()
                self.dragging = self.added_tools[-1].obj
                self.canvas.itemconfig(oid, tag='button_clone')
                self.canvas.itemconfig(self.dragging, tag='current')

    def drag(self, e):
        super(TeacherProgram, self).drag(e)
        curr = self.canvas.find_withtag('current')
        if len(curr) == 0:
            return
        dragged_id = self.canvas.find_withtag('current')[0]
        if dragged_id in self.canvas.find_withtag('button_clone'):
            self.create_button_clone(dragged_id, e)

    def clicked_canvas(self, e):
        if self.marker and self.marker[1] < 11:
            types = {5: self.create_clickable_object, 6: self.create_moveable_object, 7: self.create_cloneable_object,
                     8: self.create_static_object, 9: self.create_table_widget, 10: self.create_text_widget}
            # noinspection PyArgumentList
            types[self.marker[1]](e)
            if len(self.created_images):
                self.created_images[-1].check_coords()
            time.sleep(0.1)
            self.delete_marker()
            return
        super(TeacherProgram, self).clicked_canvas(e)

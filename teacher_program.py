import time
import tkinter

from tkinter import messagebox
from background import Background
from button import DraggableButton, Button
from constants import CREATE_NEW_EXERCISE, SAVE_EXERCISE_TEACHER, LOAD_EXERCISE_TEACHER, CREATE_CLONE, \
    CREATE_BACKGROUND, BUTTONS_TOP_X, BUTTONS_TOP_Y, BUTTONS_TOP_SPACING, CLICKABLE_OBJECT, DRAGGABLE_OBJECT, \
    STATIC_OBJECT, TABLE_OBJECT, TEXT_OBJECT, TOOL_X, TOOL_Y
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

    def __init__(self, canvas: tkinter.Canvas, width, height, win):
        super(TeacherProgram, self).__init__(canvas, width, height)
        win.wm_title('eÚlohy')
        self.student = False
        self.canvas.bind('<Button-3>', self.right_click)
        self.canvas.images = self.images = \
            self.create_image_dict('textures/', ['new_task', 'save', 'load', 'clickable',
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
        btn_ids = {CREATE_NEW_EXERCISE: self.new_exercise, SAVE_EXERCISE_TEACHER: self.save_exercise,
                   LOAD_EXERCISE_TEACHER: self.load_exercise, CLICKABLE_OBJECT: self.mark, DRAGGABLE_OBJECT: self.mark,
                   CREATE_CLONE: self.create_cloneable_object, STATIC_OBJECT: self.mark, TABLE_OBJECT: self.mark,
                   TEXT_OBJECT: self.mark, CREATE_BACKGROUND: self.create_background}
        curr = self.canvas.find_withtag('current')
        if not len(curr) or curr[0] > CREATE_BACKGROUND:
            return
        self.clicked_object = curr[0]
        if self.clicked_object in [CREATE_NEW_EXERCISE, SAVE_EXERCISE_TEACHER, LOAD_EXERCISE_TEACHER,
                                   CREATE_CLONE, CREATE_BACKGROUND]:
            self.delete_marker()
        btn_ids[self.clicked_object]()

    def create_table_widget(self, e):
        if not self.table_widget:
            self.coords = (e.x, e.y)
            self.table_widget = TableWidget(self)

    def create_text_widget(self, e):
        if not self.text_widget:
            self.coords = (e.x, e.y)
            self.text_widget = TextWidget(self)

    def remove_image(self, image):
        if image == self.background:
            image.delete()
            self.background = None
            return
        if image in self.cloneable_images:
            self.cloneable_images.pop(self.cloneable_images.index(image))
            self.move_clones(image.order)
            image.delete()
        elif image in self.added_tools:
            self.added_tools.pop(self.added_tools.index(image))
        super(TeacherProgram, self).remove_image(image)
        
    def move_clones(self, i):
        for clone in self.cloneable_images:
            if clone.order > i:
                clone.order -= 1
                clone.delete()
                clone.initialize()

    def create_cloneable_object(self):
        for image in self.cloneable_images:
            if image.order > 6:
                messagebox.showwarning(title='Klony', message='Bol vytvorený maximálny počet klonovacích objektov')
                return
        image = get_image()
        if not image:
            return
        self.cloneable_images.append(CloneableObject(0, 0, self, [image], len(self.cloneable_images)))

    def edit_text(self):
        text = self.menu.text
        text.set(self.text_widget.text, self.text_widget.default_size.get(), self.text_widget.rgb,
                 self.text_widget.default_font.get())

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
        new_table = Table(self, data, *self.coords, self.table_widget.rgb_bg, self.table_widget.rgb_table)
        new_table.draw_table()
        self.created_objects.append(new_table)
        self.table_widget = None
        self.snap_to_table()

    def edit_table(self):
        table = self.menu.table
        table.set(self.table_widget.rgb_bg, self.table_widget.rgb_table)

    def initialize_buttons(self):
        x = BUTTONS_TOP_X
        y = BUTTONS_TOP_Y
        separators = []
        for key in list(self.images.keys())[:-5]:
            self.buttons.append(Button(self.images[key][1], x, y, self, left_pct=x/self.width))
            if key == 'load':
                separators.append(x + (BUTTONS_TOP_SPACING / 2))
                x += 7
            if key == 'static':
                separators.append(x + (BUTTONS_TOP_SPACING / 2))
                x += 7
            x += BUTTONS_TOP_SPACING
        x = TOOL_X
        y = TOOL_Y
        for key in list(self.images.keys())[-5:]:
            self.buttons.append(DraggableButton(self.images[key][0], x, y, self))
            y += 70
        self.draw_separators(separators)

    def draw_separators(self, sep):
        for separator in sep:
            self.canvas.create_rectangle(separator, BUTTONS_TOP_Y - 35, separator + 5, BUTTONS_TOP_Y + 35,
                                         outline='blue', fill='blue', tag='separator')

    def create_button_clone(self, oid, e):
        for button in self.buttons:
            if isinstance(button, DraggableButton) and button.image.obj == oid:
                self.canvas.itemconfig(oid, state='hidden')
                self.added_tools.append(StaticButton(e.x, e.y, self, button.image.original.copy(), oid))
                self.added_tools[-1].offset = (0, 0)
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
        if self.marker and self.marker[1] < CREATE_BACKGROUND:
            types = {CLICKABLE_OBJECT: self.create_clickable_object, DRAGGABLE_OBJECT: self.create_moveable_object,
                     CREATE_CLONE: self.create_cloneable_object, STATIC_OBJECT: self.create_static_object,
                     TABLE_OBJECT: self.create_table_widget, TEXT_OBJECT: self.create_text_widget}
            # noinspection PyArgumentList
            types[self.marker[1]](e)
            if len(self.created_images):
                self.created_images[-1].check_coords()
            time.sleep(0.1)
            self.delete_marker()
            return
        super(TeacherProgram, self).clicked_canvas(e)

    def image_resizer(self, e):
        for image in reversed(self.created_images):
            if image.click(e):
                image.draw_drag()
                return

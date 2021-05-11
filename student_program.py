import tkinter

from button import Button
from constants import BUTTONS_TOP_Y, BUTTONS_TOP_X, BUTTONS_TOP_SPACING, SAVE_EXERCISE_STUDENT, LOAD_EXERCISE_STUDENT
from image_object import ClickableObject, StaticObject
from program import Program


class StudentProgram(Program):

    def __init__(self, canvas: tkinter.Canvas, width, height, win):
        super(StudentProgram, self).__init__(canvas, width, height)
        win.wm_title('eZošit')
        self.student = True
        self.canvas.images = self.images = \
            self.create_image_dict('textures/', ['save', 'load'])
        self.init()

    def initialize_buttons(self):
        x = BUTTONS_TOP_X
        y = BUTTONS_TOP_Y
        for key in list(self.images.keys()):
            self.buttons.append(Button(self.images[key][1], x, y, self, left_pct=x / self.width))
            x += BUTTONS_TOP_SPACING

    def click(self, e):
        super(StudentProgram, self).click(e)
        btn_ids = {SAVE_EXERCISE_STUDENT: self.save_exercise, LOAD_EXERCISE_STUDENT: self.load_exercise}
        curr = self.canvas.find_withtag('current')
        if not len(curr) or curr[0] > LOAD_EXERCISE_STUDENT:
            return
        self.clicked_object = curr[0]
        btn_ids[self.clicked_object]()

    def save_exercise(self):
        super(StudentProgram, self).save_exercise()

    def load_exercise(self):
        super(StudentProgram, self).load_exercise()
        for image in self.created_images:
            image.deletable = False

    def ask_save(self):
        super(StudentProgram, self).ask_save()

    def image_resizer(self, e):
        for image in reversed(self.created_images):
            if not isinstance(image, ClickableObject) and not isinstance(image, StaticObject) and image.click(e):
                image.draw_drag()
                return

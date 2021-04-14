import tkinter

from button import Button
from program import Program


class StudentProgram(Program):

    def __init__(self, canvas: tkinter.Canvas, width, height):
        super(StudentProgram, self).__init__(canvas, width, height)
        self.student = True
        self.canvas.images = self.images = \
            self.create_image_dict('textures/', ['save', 'load'])
        self.init()

    def initialize_buttons(self):
        x = 30
        y = 33
        for key in list(self.images.keys()):
            self.buttons.append(Button(self.images[key][1], x, y, self, left_pct=x / self.width))
            x += 60

    def click(self, e):
        super(StudentProgram, self).click(e)
        btn_ids = {1: self.save_exercise, 2: self.load_exercise}
        curr = self.canvas.find_withtag('current')
        if not len(curr) or curr[0] > 2:
            return
        self.clicked_object = curr[0]
        btn_ids[self.clicked_object]()

    def save_exercise(self):
        pass

    def load_exercise(self):
        super(StudentProgram, self).load_exercise()
        for image in self.created_images:
            image.deletable = False

    def ask_save(self):
        return False

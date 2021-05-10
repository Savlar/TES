from tkinter import Menu

from functions import get_images, get_image
from image_object import ClickableObject, StaticButton
from image_size import ImageSize


class ImageMenu:

    def __init__(self, parent, image, bg=False):
        self.parent = parent
        self.image = image
        self.menu = Menu(self.parent.canvas, tearoff=0)
        if isinstance(self.image, ClickableObject):
            label = 'Zapnúť ťahací mód' if not self.image.dragging_mode else 'Vypnut tahaci mod'
            self.menu.add_command(label=label, command=self.change_mode)
        self.menu.add_command(label='Zmeň obrázok', command=self.change_image)
        if not bg:
            self.menu.add_command(label='Zmeň veľkosť', command=self.change_size)
            label = 'Skryť obrázok pre žiaka' if self.image.visible else 'Zobraziť obrázok pre žiaka'
            self.menu.add_command(label=label, command=self.change_visibility)
        self.menu.add_command(label='Vymaž', command=self.remove)

    def remove(self):
        if self.parent.ask_delete():
            self.parent.remove_image(self.image)

    def change_mode(self):
        self.image.dragging_mode = not self.image.dragging_mode

    def change_visibility(self):
        self.image.visible = not self.image.visible

    def delete(self):
        self.parent.remove_image(self.image)

    def change_image(self):
        if isinstance(self.image, StaticButton):
            file = get_image()
            if not file:
                return
            self.image.original = [file]
            self.image.reset()
            return
        if isinstance(self.image, ClickableObject):
            files = get_images()
            if not files:
                return
            self.image.original = files
            self.image.initialize(True)
        else:
            file = get_image()
            if not file:
                return
            self.image.pil_img = [file]
            self.image.initialize(True)
        self.parent.add_to_table(self.image)

    def change_size(self):
        ImageSize(self, *self.image.size)

    def resize(self, w, h):
        try:
            self.image.resize(int(w), int(h))
        except ValueError:
            pass

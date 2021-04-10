from tkinter import Menu

from functions import get_images, get_image
from image_object import ClickableObject
from image_size import ImageSize
from table import Table


class ImageMenu:

    def __init__(self, parent, image, bg=False):
        self.parent = parent
        self.image = image
        self.menu = Menu(self.parent.canvas, tearoff=0)
        self.menu.add_command(label='Zmen obrazok', command=self.change_image)
        if not bg:
            self.menu.add_command(label='Zmen velkost', command=self.change_size)
        self.menu.add_command(label='Vymaz', command=self.remove)

    def delete(self):
        self.image.delete()
        for table in self.parent.created_objects:
            if isinstance(table, Table):
                table.remove_object(self.image)

    def remove(self):
        self.delete()
        if self.image == self.parent.background:
            self.parent.background = None
            return
        if self.image in self.parent.cloneable_images:
            self.parent.cloneable_images.pop(self.parent.cloneable_images.index(self.image))
        elif self.image in self.parent.added_tools:
            self.parent.added_tools.pop(self.parent.added_tools.index(self.image))
        else:
            self.parent.created_images.pop(self.parent.created_images.index(self.image))

    def change_image(self):
        if isinstance(self.image, ClickableObject):
            files = get_images()
            if not files:
                return
            self.delete()
            self.image.pil_img = files
            self.image.initialize()
        else:
            file = get_image()
            if not file:
                return
            self.delete()
            self.image.pil_img = [file]
            self.image.initialize()
        self.parent.add_to_table(self.image)

    def change_size(self):
        ImageSize(self, *self.image.size)

    def resize(self, w, h):
        try:
            self.image.resize(int(w), int(h))
        except ValueError:
            pass

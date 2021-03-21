from tkinter import Menu

from image_object import ClickableObject


class ImageMenu:

    def __init__(self, parent, image):
        self.parent = parent
        self.image = image
        self.menu = Menu(self.parent.canvas, tearoff=0)
        self.menu.add_command(label='Zmen obrazok', command=self.change_image)
        self.menu.add_command(label='Vymaz', command=self.remove)

    def delete(self):
        self.image.delete()
        for table in self.parent.created_objects:
            table.remove_object(self.image)

    def remove(self):
        self.delete()
        i = 0
        for item in self.parent.created_images:
            if item == self.image:
                break
            i += 1
        self.parent.created_images.pop(i)

    def change_image(self):
        if isinstance(self.image, ClickableObject):
            files = self.parent.get_images()
            if not files:
                return
            self.delete()
            self.image.pil_imgs = files
            self.image.initialize()
        else:
            file = self.parent.get_image()
            if not file:
                return
            self.delete()
            self.image.pil_img = file
            self.image.initialize()
        self.parent.add_to_table(self.image)

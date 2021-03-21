from tkinter import Menu


class TextMenu:

    def __init__(self, parent, text):
        self.parent = parent
        self.text = text
        self.menu = Menu(self.parent.canvas, tearoff=0)
        self.menu.add_command(label='Vymaz', command=self.delete)

    def delete(self):
        self.text.delete()
        i = 0
        for item in self.parent.created_objects:
            if item == self.text:
                break
            i += 1
        self.parent.created_objects.pop(i)

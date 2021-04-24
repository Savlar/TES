from tkinter import Menu


class TextMenu:

    def __init__(self, parent, text):
        self.p = parent
        self.text = text
        self.menu = Menu(self.p.canvas, tearoff=0)
        self.menu.add_command(label='Vymaz', command=self.delete)

    def delete(self):
        if self.p.ask_delete():
            self.text.delete()
            self.p.created_objects.pop(self.p.created_objects.index(self.text))

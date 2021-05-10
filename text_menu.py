import copy
from tkinter import Menu


class TextMenu:

    def __init__(self, parent, text):
        self.p = parent
        self.text = text
        self.menu = Menu(self.p.canvas, tearoff=0)
        self.menu.add_command(label='Duplikuj', command=self.copy)
        self.menu.add_command(label='Vymaž', command=self.delete)

    def copy(self):
        self.p.created_objects.append(copy.copy(self.text))

    def delete(self):
        if self.p.ask_delete():
            self.text.delete()
            self.p.created_objects.pop(self.p.created_objects.index(self.text))

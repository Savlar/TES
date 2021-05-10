import copy
from tkinter import Menu


class TableMenu:

    def __init__(self, parent, table):
        self.p = parent
        self.table = table
        self.menu = Menu(self.p.canvas, tearoff=0)
        self.menu.add_command(label='Duplikuj', command=self.copy)
        self.menu.add_command(label='Vymaž', command=self.delete)

    def copy(self):
        self.p.created_objects.append(copy.copy(self.table))

    def delete(self):
        if self.p.ask_delete():
            self.table.delete(self.p.created_images)
            self.p.created_objects.pop(self.p.created_objects.index(self.table))

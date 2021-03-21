from tkinter import Menu


class TableMenu:

    def __init__(self, parent, table):
        self.p = parent
        self.table = table
        self.menu = Menu(self.p.canvas, tearoff=0)
        self.menu.add_command(label='Vymaz', command=self.delete)

    def delete(self):
        self.table.delete(self.p.created_images)
        self.p.created_objects.pop(self.p.created_objects.index(self.table))

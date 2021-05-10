import copy
from tkinter import Menu

from table_widget import TableWidget


class TableMenu:

    def __init__(self, parent, table):
        self.p = parent
        self.table = table
        self.menu = Menu(self.p.canvas, tearoff=0)
        self.menu.add_command(label='Duplikuj', command=self.copy)
        self.menu.add_command(label='Editovať', command=self.edit)
        self.menu.add_command(label='Vymaž', command=self.delete)

    def edit(self):
        self.p.table_widget = TableWidget(self.p, self.table.color_bg, self.table.color_table, True,
                                          self.table.rows, self.table.cols, self.table.width, self.table.height)

    def copy(self):
        self.p.created_objects.append(copy.copy(self.table))

    def delete(self):
        if self.p.ask_delete():
            self.table.delete(self.p.created_images)
            self.p.created_objects.pop(self.p.created_objects.index(self.table))

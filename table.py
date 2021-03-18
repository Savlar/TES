import tkinter

from created_object import CreatedObject


class Table(CreatedObject):

    def __init__(self, parent: tkinter.Canvas, data, x, y):
        self.parent = parent
        self.x = x
        self.y = y
        self.drag = None
        self.data = data
        self.rows, self.cols, self.width, self.height = data[0], data[1], data[2], data[3]
        self.table_objects = [[] for _ in range(self.rows)]

    def draw_table(self):
        y = self.y
        for i in range(self.rows):
            x = self.x
            for j in range(self.cols):
                cell = self.parent.create_rectangle(x, y, x + self.width, y + self.height, outline='black')
                self.table_objects[i].append(cell)
                x += self.width
            if i == 0:
                self.drag = self.parent.create_oval(x - 5, y - 10, x + 10, y + 5, fill='red', outline='red')
            y += self.height

    def move_table(self, x, y):
        coords = self.parent.coords(self.drag)
        width2 = (coords[2] - coords[0]) / 2
        height2 = (coords[3] - coords[1]) / 2
        diff_x = -((coords[0] + width2) - x)
        diff_y = -((coords[1] + height2) - y)
        if (x + diff_x) - self.width * self.cols < 100 or x + width2 > 980 or y + height2 < 75 or \
                (y + diff_y) + self.height * self.rows > 700:
            return
        self.parent.coords(self.drag, (x - width2, y - height2, x + width2, y + height2))

        for row in self.table_objects:
            for obj in row:
                cell_coords = self.parent.coords(obj)
                self.parent.coords(obj, cell_coords[0] + diff_x, cell_coords[1] + diff_y, cell_coords[2] + diff_x,
                                   cell_coords[3] + diff_y)

    def delete(self):
        self.parent.delete(self.drag)
        for row in self.table_objects:
            for obj in row:
                self.parent.delete(obj)

    def serialize(self):
        coords = self.parent.coords(self.table_objects[0][0])
        return {'type': 'table', 'data': self.data, 'x': coords[0], 'y': coords[1]}

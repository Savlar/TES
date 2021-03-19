import tkinter


class Table:

    def __init__(self, parent: tkinter.Canvas, data, x, y):
        self.parent = parent
        self.obj = None
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
        self.x += diff_x
        self.y += diff_y
        self.parent.coords(self.drag, (x - width2, y - height2, x + width2, y + height2))

        for row in self.table_objects:
            for obj in row:
                if type(obj) != int:
                    ix, iy = self.parent.coords(obj.obj)
                    self.parent.coords(obj.obj, ix + diff_x, iy + diff_y)
                else:
                    cell_coords = self.parent.coords(obj)
                    self.parent.coords(obj, cell_coords[0] + diff_x, cell_coords[1] + diff_y, cell_coords[2] + diff_x,
                                       cell_coords[3] + diff_y)

    def delete(self):
        self.parent.delete(self.drag)
        for row in self.table_objects:
            for obj in row:
                if type(obj) != int:
                    obj.delete()
                else:
                    self.parent.delete(obj)

    def serialize(self):
        return {'type': 'table', 'data': self.data, 'x': self.x, 'y': self.y}

    def add_object(self, img):
        obj = img.obj
        x, y = self.parent.coords(obj)
        if self.x <= x <= self.x + self.cols * self.width and self.y <= y <= self.y + self.y * self.rows:
            ix = int((y - self.y) // self.height)
            iy = int((x - self.x) // self.width)
            if self.table_objects[ix][iy] == img:
                return
            self.put_in_middle(ix, iy, obj)
            if type(self.table_objects[ix][iy]) != int:
                self.parent.delete(self.table_objects[ix][iy].obj)
            else:
                self.parent.delete(self.table_objects[ix][iy])
            self.table_objects[ix][iy] = img
            self.resize_image(img)

    def remove_object(self, img):
        for i in range(len(self.table_objects)):
            for j in range(len(self.table_objects[i])):
                if self.table_objects[i][j] == img:
                    self.table_objects[i][j] = None
                    cell = self.parent.create_rectangle(j * self.width + self.x, i * self.height + self.y,
                                                        (j + 1) * self.width + self.x, (i + 1) * self.height + self.y,
                                                        outline='black')
                    self.table_objects[i][j] = cell
                    return

    def put_in_middle(self, ix, iy, obj):
        x, y = (self.x + (self.width * iy) + (self.width / 2)), (self.y + (self.height * ix) + (self.height / 2))
        self.parent.coords(obj, x, y)

    def resize_image(self, img):
        img.resize(self.width, self.height)

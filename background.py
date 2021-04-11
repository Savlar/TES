from PIL import ImageTk


class Background:

    def __init__(self, img, parent):
        self.parent = parent
        self.canvas = parent.canvas
        self.pil_img = img[:]
        self.tk_img = None
        self.obj = None
        self.initialize()

    def initialize(self):
        self.tk_img = [ImageTk.PhotoImage(self.pil_img[0])]
        x1, y1, x2, y2 = self.canvas.coords(self.canvas.find_withtag('area')[0])
        self.obj = self.canvas.create_image((x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1, image=self.tk_img[0], tag='bg')
        self.canvas.tag_lower('bg')

    def delete(self):
        self.canvas.delete(self.obj)

    def serialize(self):
        return {'type': 'background', 'size': self.pil_img[0].size,
                'image': [(self.pil_img[0].mode, self.pil_img[0].tobytes())]}

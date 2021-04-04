from PIL import ImageTk


class Background:

    def __init__(self, img, canvas):
        self.canvas = canvas
        self.size = img[0].size
        self.pil_img = img
        self.tk_img = None
        self.obj = None
        self.initialize()

    def initialize(self):
        self.pil_img = [self.pil_img[0].resize(self.size)]
        self.tk_img = [ImageTk.PhotoImage(self.pil_img[0])]
        x1, y1, x2, y2 = self.canvas.coords(self.canvas.find_withtag('area')[0])
        self.obj = self.canvas.create_image((x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1, image=self.tk_img[0], tag='bg')
        self.canvas.tag_lower('bg')

    def delete(self):
        self.canvas.delete(self.obj)

    def serialize(self):
        return {'type': 'background', 'size': (880, 625), 'image': [self.pil_img[0].tobytes()]}

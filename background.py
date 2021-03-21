from PIL import ImageTk


class Background:

    def __init__(self, img, canvas):
        self.canvas = canvas
        self.size = (880, 625)
        self.pil_img = img
        self.tk_img = None
        self.obj = None
        self.initialize()

    def initialize(self):
        self.pil_img = self.pil_img.resize(self.size)
        self.tk_img = ImageTk.PhotoImage(self.pil_img)
        self.obj = self.canvas.create_image(540, 387.5, image=self.tk_img, tag='bg')

    def delete(self):
        self.canvas.delete(self.obj)

    def serialize(self):
        return {'type': 'background', 'size': (880, 625), 'image': self.pil_img.tobytes()}

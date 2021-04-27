from PIL import ImageTk, Image

from constants import AREA_X1, AREA_X2, AREA_Y1, AREA_Y2


class Background:

    def __init__(self, img, parent):
        self.parent = parent
        self.canvas = parent.canvas
        self.size = img[0].size
        self.pil_img = img[:]
        self.original = self.pil_img[:]
        self.tk_img = None
        self.obj = None
        self._coords = ((AREA_X2 - AREA_X1) / 2 + AREA_X1, (AREA_Y2 - AREA_Y1) / 2 + AREA_Y1)
        self.initialize()

    def initialize(self):
        self.tk_img = [ImageTk.PhotoImage(self.pil_img[0])]
        self.obj = self.canvas.create_image(*self._coords, image=self.tk_img[0], tag='bg')

    def resize(self, w, h):
        w, h = int(w), int(h)
        self.pil_img = self.original[:]
        self.tk_img = [ImageTk.PhotoImage(self.pil_img[0])]
        self.pil_img[0] = self.pil_img[0].resize((w, h), resample=Image.LANCZOS)
        self.size = self.pil_img[0].size
        self.canvas.itemconfig(self.obj, image=self.tk_img[0])
        self.canvas.coords(self.obj, self._coords)

    def rescale(self, pct_w, pct_h):
        w, h = self.size
        new_w = int(w * pct_w)
        new_h = int(h * pct_h)
        h = ((self.parent.width - 180) / 16) * 9
        self._coords =  (AREA_X1 + (self.parent.width - 80) / 2, AREA_Y1 + (h / 2))
        self.resize(new_w, new_h)

    def delete(self):
        self.canvas.delete(self.obj)

    def serialize(self):
        return {'type': 'background', 'size': self.pil_img[0].size,
                'image': [(self.pil_img[0].mode, self.pil_img[0].tobytes())]}

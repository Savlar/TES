from tkinter import filedialog

from PIL import Image


def get_image():
    filename = filedialog.askopenfilename(title='Vyber obrazok', initialdir='./images',
                                          filetypes=[('Obrazky', '*.jpg')])
    if not filename:
        return
    return Image.open(filename)


def get_images():
    filenames = filedialog.askopenfilenames(title='Vyber obrazok', initialdir='./images',
                                filetypes=[('Obrazky', '*.jpg')])
    if not filenames:
        return
    imgs = []
    for file in filenames:
        imgs.append(Image.open(file))
    return imgs

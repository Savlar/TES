from PIL import Image

from background import Background
from image_object import StaticObject, DraggableObject, ClickableObject, StaticButton, CloneableObject
from table import Table
from text import Text


def read(data, size):
    images = []
    for item in data:
        mode, img = item
        images.append(Image.frombytes(mode, size, img))
    return images


def deserialize_tables(parent):
    tables = []
    for obj in list(filter(lambda x: x['type'] == 'table', parent.serialized_data)):
        table = Table(parent, obj['data'], obj['x'], obj['y'], obj['color'])
        table.draw_table()
        tables.append(table)
    return tables


def deserialize_tools(parent):
    tools = []
    for obj in list(filter(lambda x: x['type'] == 'button', parent.serialized_data)):
        tools.append(
            StaticButton(obj['x'], obj['y'], parent, read(obj['image'], obj['size']), obj['parent'], obj['visible']))
        parent.canvas.itemconfig(obj['parent'], state='hidden')
    return tools


def deserialize_text(parent):
    text = []
    for obj in list(filter(lambda x: x['type'] == 'text', parent.serialized_data)):
        text.append(Text(obj['x'], obj['y'], parent, obj['text'], obj['size'], obj['color'], obj['font']))
    return text


def deserialize_background(parent):
    for obj in list(filter(lambda x: x['type'] == 'background', parent.serialized_data)):
        return Background(read(obj['image'], obj['size']), parent)


def deserialize_clones(parent):
    clones = []
    for obj in list(filter(lambda x: x['type'] == 'cloneable', parent.serialized_data)):
        clones.append(CloneableObject(0, 0, parent, read(obj['image'], obj['size']), obj['order'], obj['visible']))
    return clones


def deserialize_images(parent, student):
    images = []
    for obj in parent.serialized_data:
        if not obj['visible'] and student:
            continue
        if obj['type'] == 'static':
            images.append(StaticObject(obj['x'], obj['y'], parent, read(obj['image'], obj['size']), obj['visible']))
        elif obj['type'] == 'clickable':
            images.append(ClickableObject(obj['x'], obj['y'], parent, read(obj['image'], obj['size']), obj['visible']))
        elif obj['type'] == 'draggable':
            images.append(DraggableObject(obj['x'], obj['y'], parent, read(obj['image'], obj['size']), obj['visible']))
    return images

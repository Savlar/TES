import tkinter


class Counter:

    def __init__(self, parent, row, col, min_, max_, step):
        self.parent = parent
        self.value = min_
        self.min_ = min_
        self.max_ = max_
        self.step = step

        self.label = tkinter.Label(parent, text=str(self.value))
        self.label.grid(row=row, column=col, rowspan=2)
        self.btn_up = tkinter.Button(parent, text='+', command=self.increment, width=1, height=1)
        self.btn_up.grid(row=row, column=col + 1)
        self.btn_down = tkinter.Button(parent, text='-', command=self.decrement, width=1, height=1)
        self.btn_down['state'] = 'disabled'
        self.btn_down.grid(row=row + 1, column=col + 1)

    def increment(self):
        self.value += self.step
        self.btn_up['state'] = 'normal' if self.value < self.max_ else 'disabled'
        self.btn_down['state'] = 'normal'
        self.label.config(text=str(self.value))

    def decrement(self):
        self.value -= self.step
        self.btn_down['state'] = 'disabled' if self.value == self.min_ else 'normal'
        self.btn_up['state'] = 'normal'
        self.label.config(text=str(self.value))

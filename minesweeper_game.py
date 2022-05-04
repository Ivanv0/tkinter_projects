from tkinter import Tk, Frame, Label, Button
from random import shuffle

rows = 10
columns = 10
mines_count = 5

cell_size = 3
font = 'Times 20'
c_font = 'Times 40'


class Cell(Button):
    def __init__(self, _x, _y, **kwargs):
        super(Cell, self).__init__(**kwargs, command=self.click)
        self.x = _x
        self.y = _y
        self.number = None
        self.neighbours = []
        self.is_mine = False

    def click(self):
        self.configure(state='disabled')
        if self.is_mine:
            self.configure(text='*', background='red')
            click_all_cells()
            counter_label.configure(text='GAME OVER')

        else:
            if self.number != 0:
                self.configure(text=f'{self.number}')
            else:
                for i in self.neighbours:
                    if i['state'] != 'disabled':
                        i.click()
            self.configure(background='grey85')
        win_check()

    def r_click(self):
        global counter

        if self['state'] == 'normal':
            self.configure(state='disabled', text='\u274C')
            counter -= 1
            counter_label.configure(text=f'{counter}')
        elif self['text'] == '\u274C':
            self.configure(state='normal', text='')
            counter += 1
            counter_label.configure(text=f'{counter}')
        elif self.number != None:
            if self.number == len(tuple(filter(lambda s: s['text'] == '\u274C', self.neighbours))):
                for i in tuple(filter(lambda s: s['state'] == 'normal', self.neighbours)):
                    if i['state'] == 'normal':
                        i.click()
            elif self.number == len(n := tuple(filter(
                    lambda s: s['state'] == 'normal' or s['text'] == '\u274C', self.neighbours))):
                for i in tuple(filter(lambda s: s['state'] == 'normal', n)):
                    i.r_click()
        win_check()

    def __str__(self):
        return f'Cell {self.x}-{self.y}'
    def __repr__(self):
        return f'Cell {self.x}-{self.y}'

def click_all_cells():
    for i in range(rows):
        for j in range(columns):
            if cells[i][j]['state'] == 'normal':
                cells[i][j].click()

def win_check():
    if len(mines) == len(tuple(filter(lambda s: s['text'] == '\u274C', mines))):
        click_all_cells()
        counter_label.configure(text='YOU WIN')

root = Tk()

counter = mines_count
counter_label = Label(root, text=f'{counter}', font=c_font)
counter_label.pack()

game_field = Frame(root)
game_field.pack(padx=5, pady=5)

cells = []
for i in range(rows):
    temp = []
    for j in range(columns):
        btn = Cell(i, j, master=game_field, font=font, width=cell_size, height=cell_size//2,
                   borderwidth=1, relief='raise', disabledforeground='black')
        btn.grid(row=i, column=j)
        temp.append(btn)
    cells.append(temp)
del temp
for i in range(rows):
    cells[i] = tuple(cells[i])
cells = tuple(cells)

temp = list(range(rows*columns))
shuffle(temp)
mines = []
for i in temp[:mines_count]:
    x = i // rows
    y = i % columns
    cells[x][y].is_mine = True
    mines.append(cells[x][y])
del temp, x, y
mines = tuple(mines)

for i in range(rows):
    for j in range(columns):
        btn = cells[i][j]
        if not btn.is_mine:
            if i == 0:
                btn.neighbours.append(cells[1][j])
                if j != 0:
                    btn.neighbours.append(cells[0][j - 1])
                    btn.neighbours.append(cells[1][j - 1])
                if j != columns - 1:
                    btn.neighbours.append(cells[0][j + 1])
                    btn.neighbours.append(cells[1][j + 1])
            elif i == rows - 1:
                btn.neighbours.append(cells[rows-2][j])
                if j != 0:
                    btn.neighbours.append(cells[i][j - 1])
                    btn.neighbours.append(cells[i - 1][j - 1])
                if j != columns - 1:
                    btn.neighbours.append(cells[i][j + 1])
                    btn.neighbours.append(cells[i - 1][j + 1])
            else:
                btn.neighbours.append(cells[i - 1][j])
                btn.neighbours.append(cells[i + 1][j])
                if j != 0:
                    btn.neighbours.append(cells[i - 1][j - 1])
                    btn.neighbours.append(cells[i][j - 1])
                    btn.neighbours.append(cells[i + 1][j - 1])
                if j != columns - 1:
                    btn.neighbours.append(cells[i - 1][j + 1])
                    btn.neighbours.append(cells[i][j + 1])
                    btn.neighbours.append(cells[i + 1][j + 1])
            btn.number = len(tuple(filter(lambda x: x.is_mine, btn.neighbours)))
        btn.bind('<Button-3>', lambda e: e.widget.r_click())

root.bind('<Escape>', lambda e: root.destroy())
root.mainloop()

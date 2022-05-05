from tkinter import Tk, Frame, Label, Button
from random import shuffle

rows = 10
columns = 10
mines_count = (rows * columns) // 5

font = ('Times', 20)
c_font = ('Times', 40)


class Cell(Button):
    def __init__(self, order_number, x, y, **kwargs):
        super(Cell, self).__init__(**kwargs, command=self.click)
        self.bind('<Button-3>', lambda e: e.widget.r_click())

        self.x = x
        self.y = y
        self.num = order_number
        self.neighbours = ()

        self.number = None
        self.is_mine = False

    def reset(self):
        self.number = None
        self.is_mine = False
        self.configure(text='', state='normal', background='#f0f0f0')

    def get_neighbours(self):
        _temp = []
        if self.x == 0:
            _temp.append(cells[1][self.y])
            if self.y != 0:
                _temp.append(cells[0][self.y - 1])
                _temp.append(cells[1][self.y - 1])
            if self.y != columns - 1:
                _temp.append(cells[0][self.y + 1])
                _temp.append(cells[1][self.y + 1])
        elif self.x == rows - 1:
            _temp.append(cells[rows - 2][self.y])
            if self.y != 0:
                _temp.append(cells[self.x][self.y - 1])
                _temp.append(cells[self.x - 1][self.y - 1])
            if self.y != columns - 1:
                _temp.append(cells[self.x][self.y + 1])
                _temp.append(cells[self.x - 1][self.y + 1])
        else:
            _temp.append(cells[self.x - 1][self.y])
            _temp.append(cells[self.x + 1][self.y])
            if self.y != 0:
                _temp.append(cells[self.x - 1][self.y - 1])
                _temp.append(cells[self.x][self.y - 1])
                _temp.append(cells[self.x + 1][self.y - 1])
            if self.y != columns - 1:
                _temp.append(cells[self.x - 1][self.y + 1])
                _temp.append(cells[self.x][self.y + 1])
                _temp.append(cells[self.x + 1][self.y + 1])
        self.neighbours = tuple(_temp)

    def get_number(self):
        if not self.is_mine:
            self.number = len(tuple(filter(lambda n: n.is_mine, self.neighbours)))
        else:
            self.number = None

    def click(self):
        global game

        if game:
            self.configure(state='disabled')
            if self.is_mine:
                
                self.configure(text='*', background='red')
                
                click_all_cells()
                counter_label.configure(text='GAME OVER')
                game = False

            else:
                if self.number != 0:
                    self.configure(text=f'{self.number}')
                else:
                    for neighbour in self.neighbours:
                        if neighbour['state'] != 'disabled':
                            neighbour.click()
                self.configure(background='grey85')

    def r_click(self):
        global counter

        if game:
            if self['state'] == 'normal':
                if counter > 0:
                    self.configure(state='disabled', text='\u274C')
                    counter -= 1
                    counter_label.configure(text=f'{counter}')
                    win_check()
            elif self['text'] == '\u274C':
                self.configure(state='normal', text='')
                counter += 1
                counter_label.configure(text=f'{counter}')
            elif not self.is_mine:
                if self.number == len(tuple(filter(lambda s: s['text'] == '\u274C', self.neighbours))):
                    for neighbour in tuple(filter(lambda s: s['state'] == 'normal', self.neighbours)):
                        if neighbour['state'] == 'normal':
                            neighbour.click()
                elif self.number == len(n := tuple(filter(
                        lambda s: s['state'] == 'normal' or s['text'] == '\u274C', self.neighbours))):
                    for neighbour in tuple(filter(lambda s: s['state'] == 'normal', n)):
                        neighbour.r_click()


def click_all_cells():
    for row in cells:
        for cell in row:
            if cell['state'] == 'normal':
                cell.click()


def win_check():
    global game

    if len(mines) == len(tuple(filter(lambda s: s['text'] == '\u274C', mines))):
        click_all_cells()
        counter_label.configure(text='YOU WIN')
        game = False


root = Tk()
root.title('Minesweeper')
root.geometry('+0+0')
root.resizable(False, False)

counter = mines_count
counter_label = Label(root, text=f'{counter}', font=c_font)
counter_label.pack()

game_field = Frame(root)
game_field.pack(padx=5, pady=5)

cells = []
mines = []

for i in range(rows):
    temp = []
    for j in range(columns):
        _cell = Cell(i * rows + j, x=i, y=j, master=game_field, font=font, width=3,
                     borderwidth=1, relief='raise', disabledforeground='black')
        _cell.grid(row=i, column=j)
        temp.append(_cell)
    cells.append(temp)
del i, j, temp

for _row in cells:
    for _cell in _row:
        _cell.get_neighbours()
del _row, _cell


def replay():
    global counter, mines, game
    counter = mines_count
    counter_label.configure(text=f'{counter}')

    m = list(range(rows * columns))
    shuffle(m)
    m = sorted(m[:mines_count])

    mines = []

    for row in cells:
        for cell in row:
            cell.reset()

            if cell.num in m:
                cell.is_mine = True
                mines.append(cell)

    for row in cells:
        for cell in row:
            cell.get_number()
    game = True


game = False
replay()
counter_label.bind('<Button-1>', lambda e: replay())
root.bind('<Escape>', lambda e: root.destroy())
root.mainloop()

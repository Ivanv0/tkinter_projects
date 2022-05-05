from tkinter import Tk, Frame, Label, Button
from random import shuffle

rows = 10
columns = 10
mines_count = (rows * columns) // 5

cell_size = 3
font = 'Times 15'
c_font = 'Times 40'


class Cell(Button):
    def __init__(self, num, **kwargs):
        super(Cell, self).__init__(**kwargs, command=self.click)
        self.num = num
        self.number = None
        self.neighbours = []
        self.is_mine = False

    def click(self):
        self.configure(state='disabled')
        if self.is_mine:
            self.configure(text='*', background='red')
            if counter_label['text'] != 'GAME OVER':
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

    def r_click(self):
        global counter

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
        elif self.number != None:
            if self.number == len(tuple(filter(lambda s: s['text'] == '\u274C', self.neighbours))):
                for i in tuple(filter(lambda s: s['state'] == 'normal', self.neighbours)):
                    if i['state'] == 'normal':
                        i.click()
            elif self.number == len(n := tuple(filter(
                    lambda s: s['state'] == 'normal' or s['text'] == '\u274C', self.neighbours))):
                for i in tuple(filter(lambda s: s['state'] == 'normal', n)):
                    i.r_click()


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
root.geometry('+0+0')

counter = mines_count
counter_label = Label(root, text=f'{counter}', font=c_font)
counter_label.pack()

game_field = Frame(root)
game_field.pack(padx=5, pady=5)

cells = []
mines = []

m = list(range(rows*columns))
shuffle(m)
m = m[:mines_count]
for i in range(rows):
    temp = []
    for j in range(columns):
        btn = Cell(i*rows+j, master=game_field, font=font, width=cell_size, height=cell_size//2,
                   borderwidth=1, relief='raise', disabledforeground='black')
        btn.grid(row=i, column=j)
        temp.append(btn)
        if btn.num in m:
            btn.is_mine = True
            mines.append(btn)
    cells.append(temp)
del temp, m



for i in range(rows):
    for j in range(columns):
        btn = cells[i][j]
        btn.bind('<Button-3>', lambda e: e.widget.r_click())
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
            btn.neighbours = tuple(btn.neighbours)
        if not btn.is_mine:
            btn.number = len(tuple(filter(lambda x: x.is_mine, btn.neighbours)))

def replay():
    global counter, mines
    counter = mines_count
    counter_label.configure(text=f'{counter}')

    m = list(range(rows * columns))
    shuffle(m)
    m = sorted(m[:mines_count])

    mines = []

    for row in cells:
        for cell in row:
            cell.configure(text='', state='normal', background='#f0f0f0')

            if cell.num in m:
                cell.is_mine = True
                cell.number = None
                mines.append(cell)
            else:
                cell.is_mine = False

    for row in range(rows):
        for column in range(columns):
            cell = cells[row][column]
            if not cell.is_mine:
                cell.number = len(tuple(filter(lambda x: x.is_mine, cell.neighbours)))


counter_label.bind('<Button-1>', lambda e: replay())
root.bind('<Escape>', lambda e: root.destroy())
root.mainloop()

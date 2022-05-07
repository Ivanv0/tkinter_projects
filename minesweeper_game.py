from tkinter import Tk, Frame, Label, Button, PhotoImage
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
root.iconphoto(False, PhotoImage(data='''
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACW9GRnMAAAAAAAAAAADaKrbOAAAACXBIWXMAAAsSAAALEgHS3X78AAAAJXRFWHRTb2Z0d2FyZQBBZG9iZSBQaG90b3Nob3
AgQ0MgKFdpbmRvd3MpsBW66wAAAER0RVh0SVBUQzpPcmlnaW5hbERvY3VtZW50SUQAeG1wLmRpZDo0ODk1OTI0MC02MzllLTU5NDEtOWZjYy01ZmJiZDcwMDhiZGEU/EHvAAAAOHRFWHRJ
UFRDOkRvY3VtZW50SUQAeG1wLmRpZDo3QTA1MEFBMzFCQUUxMUU4ODg3MEFGOEFFOTY3QkJFMigqjq8AAAA4dEVYdElQVEM6SW5zdGFuY2VJRAB4bXAuaWlkOjdBMDUwQUEyMUJBRTExRT
g4ODcwQUY4QUU5NjdCQkUyMLPeFAAAAD10RVh0c3RSZWY6aW5zdGFuY2VJRAB4bXAuaWlkOjBkN2NkOWQyLTAwOTEtNjc0OC05OTZiLTVhMDRkMzE3YzVjZshYssYAAAA5dEVYdHN0UmVm
OmRvY3VtZW50SUQAeG1wLmRpZDo3RkU0RTc1MjFCQTcxMUU4QTk5Mjk1RjQ4MzJFMTM2QQKuv38AAAtVSURBVFgJBcEJlJbVecDx/3Pv+37b7MPMyACDOMiOwACKlKixbsElKaeJ2Wpzgt
blBK0magxHPabaY62hxkCNSapGTaoecSmosVYxURHZzSg4CA6Ms7DM/n3zre9779PfTwAAgPpXr/rGaOexkxQqBQxgEIwN8ICKAVEAAEDxoqCCeDAACE5ABDT2KDGBsUTeYcRQlUowp6WZ
b/3v6w3AGIAAAIzf81O95/m3ueHyLtpPrcbHE2TjmE/tu8RWMQZQEK8YBYMh7zxqhHTKEKtiBOrqE9RXweG+Mh1mFUey+5lXezZhZBnKHOW5j2u55cJVNGzYJAAC1Ofuu2v05y+8zY2X9f
JBz0l+sOElGP0CvANJAQZcDBgwAmqgRtn4n9tw1nHrTedByYIkees3D7P1XWXjb2+HRARBCFEE1VVsvf9mWk9r4s1dU7j9ggtIP/RIg/zPN9bonz8/ynUXD/DRl6dY++uXcJ0fYW0E3kAI
xGVYNovCrkNkggSUS7zxcTd/1O+yZ9tz3LmomrVXtCGBQrIRlp2B374b4xOAAa94azDTZ7P1npuY0tLIq++1csHsM5AHlq7QK1ccprN/hGse30Lc+R4WD3jEBlBR7nlqK+8czPDb25azcH
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
'''))

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

from tkinter import Tk, Canvas, Label, PhotoImage
from random import randrange

def rgb(r, g, b):
    return '#%02x%02x%02x' % (r,g,b)

speed = 300  # время между кадрами
canvas_width = 600  # общая длина
canvas_height = 500  # общая высота
cell_size = 50  # размер клетки
cells_num = (canvas_width // cell_size) * (canvas_height // cell_size)
snake_length = 3  # начальная длина змейки

# цвета
main_win = rgb(40,44,52)  # фон
canvas_bg = rgb(33,37,43)  # игровое поле
font_color = rgb(205,151,98)  # цвет для текста
snake_head_color = rgb(39,42,115)  # голова змейки
snake_head_frame_color = rgb(39,52,127)  # обводка головы змейки
snake_head_line_color = rgb(208,153,85)  # линия на голове змейки
snake_body_color = rgb(111,188,120)  # тело змеи
snake_body_frame_color = rgb(41, 100, 99)  # обводка для тела змейки
snake_body_line_color = rgb(39,42,71)  # линия на теле змейки
food_color = rgb(224,108,117)  # еда
food_frame_color = rgb(112,45,51)  # обводка еды

class Snake:
    def __init__(self):
        self.coords = [(0, 0)] * snake_length
        self.squares = []
        self.line_s = [0] * (snake_length - 1)
        self.line_f = [0] * (snake_length - 1)
        for x, y in self.coords:
            square = canvas.create_rectangle((x + 1, y + 1), (x + cell_size - 1, y + cell_size - 1),
                                             fill=snake_body_color)
            self.squares.insert(0, square)


class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.oval = 0
        self.place()
        self.stay = True

    def place(self):
        if score < cells_num:
            while (self.x, self.y) in snake.coords:
                self.x = randrange(0, canvas_width // cell_size) * cell_size
                self.y = randrange(0, canvas_height // cell_size) * cell_size
            self.oval = canvas.create_oval((self.x + 2, self.y + 2), (self.x + cell_size - 2, self.y + cell_size - 2),
                                           fill=food_color, outline=food_frame_color)
        else:
            self.stay = False

    def replace(self):
        canvas.delete(self.oval)
        self.place()


def move():
    global snake, food, direction, game

    x, y = snake.coords[0]

    if direction == 'right':
        x += cell_size
    elif direction == 'left':
        x -= cell_size
    elif direction == 'up':
        y -= cell_size
    elif direction == 'down':
        y += cell_size

    global score, game
    if check_collision(x, y):
        game = False
        if score == cells_num:
            text = '\U0001F40D YOU WIN \U0001F40D'
        else:
            text = '\U0001F330 GAME OVER \U0001F330'
        canvas.create_text((canvas_width // 2, canvas_height // 2),
                           text=text, font='Times 50', fill=font_color)
        canvas.create_text((canvas_width // 2, canvas_height // 2 + 50), text='Press R to restart',
                           font='Times 20', fill=font_color)
        del snake
        del food
    else:
        snake.coords.insert(0, (x, y))
        square = canvas.create_rectangle((x + 1, y + 1), (x + cell_size - 1, y + cell_size - 1),
                                         fill=snake_head_color, outline=snake_head_frame_color)
        snake.squares.insert(0, square)
        new_line(x, y)

        canvas.itemconfig(snake.line_s[1], fill=snake_body_line_color)
        canvas.itemconfig(snake.squares[1], fill=snake_body_color,
                          outline=snake_body_frame_color)

        if x == food.x and y == food.y:
            score += 1
            label_score.configure(text=f'{score}')
            food.replace()
        else:
            del snake.coords[-1]
            canvas.delete(snake.line_s.pop())
            canvas.delete(snake.line_f.pop())
            canvas.delete(snake.squares.pop())

        canvas.update()
        root.after(speed, move)


def new_line(x, y):
    center_x = x + cell_size / 2
    center_y = y + cell_size / 2
    center = (center_x, center_y)

    if direction == 'right':
        snake.line_s.insert(0, canvas.create_line((x, center_y),
                                                  center, fill=snake_head_line_color))
        snake.line_f.insert(0, canvas.create_line((center_x - cell_size, center_y),
                                                  (x, center_y), fill=snake_body_line_color))
    elif direction == 'left':
        snake.line_s.insert(0, canvas.create_line((x + cell_size, center_y),
                                                  center, fill=snake_head_line_color))
        snake.line_f.insert(0, canvas.create_line((center_x + cell_size, center_y),
                                                  (x + cell_size, center_y), fill=snake_body_line_color))
    elif direction == 'up':
        snake.line_s.insert(0, canvas.create_line((center_x, y + cell_size),
                                                  center, fill=snake_head_line_color))
        snake.line_f.insert(0, canvas.create_line((center_x, center_y + cell_size),
                                                  (center_x, y + cell_size), fill=snake_body_line_color))
    elif direction == 'down':
        snake.line_s.insert(0, canvas.create_line((center_x, y),
                                                  center, fill=snake_head_line_color))
        snake.line_f.insert(0, canvas.create_line((center_x, center_y - cell_size),
                                                  (center_x, y), fill=snake_body_line_color))


def change_direction(event):
    if game:
        global direction
        new = direction
        if event.keycode == 87:
            new = 'up'
        elif event.keycode == 65:
            new = 'left'
        elif event.keycode == 83:
            new = 'down'
        elif event.keycode == 68:
            new = 'right'

        if new != direction:
            if new != wrong_direction():
                direction = new


def wrong_direction():
    head = snake.coords[0]
    body = snake.coords[1]

    if head[0] > body[0]:
        return 'left'
    elif body[0] > head[0]:
        return 'right'
    elif head[1] < body[1]:
        return 'down'
    elif head[1] > body[1]:
        return 'up'


def check_collision(x, y):
    if x < 0 or x >= canvas_width:
        return True
    if y < 0 or y >= canvas_height:
        return True
    if (x, y) in snake.coords[1:-1]:
        return True
    if not food.stay:
        return True
    return False


root = Tk()
root.geometry('+0+0')
root.resizable(False, False)
root['bg'] = main_win
root.title('Snake')
root.iconphoto(False, PhotoImage(data='''iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAz
fHTVMAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAlvRkZzAAAAAAAAAAAA2iq2zgAAAAlwSFlzAAALEgAACxIB0t1+/
AAAABR0RVh0b2lpbzpDb2xvclNwYWNlAHNSR0JeLUu7AAACp0lEQVQ4EQXBy2scdQAA4O83Mzv7StokJjFJq2k0YtpK7UWhFUUEhYKoUBFRDz2JoCDUgwhe
9D8o4sGTF28eKogHD0ILtuLB0ldKWzA2bTE1SdPd7m72NZnx+wAAAAAAnnhufNdHAAAAAAAAAPGh2fr3J5fmrmIBACAGAAAAqJRK75z48Pmvp96dmXZhsGe
l8fBHAIgAAAAAxicr++9vPggbqwML09X9AAARAAAAQKPRv1Qv1SUjwZ1b65cAABIAAACAbndweRgyNoqilbgCAJAAnpmpVt/LQrHbkDzO7eSRkShSSs300y
DK+mGjtdMEAEhijp18+8jpsaXRtLm2WVSisfy/W5vRWL1WtFods68/GY2ObofOmbXmjYftnwAAwqtLC1df+ezpg+lKt5hsVoo8SYpKqRq283aRqIbmsFlsL
W9dPvXH1U8e9LLzAADJ9OLYUxP1UHz3zV9nL7TbnwIAIEeWAkuABu5BeG1hz/m3Pt935OHNSvHgWiscPXogv3ju7zC/b8q/Ww21alWRDnXuDUwv1oqbq80w
M7urOPfb8q+nb9x+P77daF04nDx6vLI7q5nOnfnlinSm5Mr1f/Tjodvr69bWG1qjmevX7pk4PBJG9w7C3mcnFuOV7fkAmDhQG33j8anyeL/TFUWJTpappmX
9wVA1iXTzXDVBNSKPThz/4oVDF3++206gUoqOlculNwc75Vq3nxT1XfUg7xRxXA9FqSsLFXna0xskRZbnYe/kI3uGyVC802snY2n65ccfvPjVgZfHQ+Pmhs
Z6Od++vxVG0vmiW7RDaadiqFeU41qI076Jg4+FbG4nrC2v5nd+v/tteGlx/s99c9GEjEEWm5qt6LUolUMx6IcQx4UiKel1+2ojZY2NLf3t0Nxa2fzhbKd16
n/+Wg2SIRb0qQAAAABJRU5ErkJggg=='''))

score = snake_length
label_score = Label(text=f'{score}', font='Times 30', background=main_win, foreground=font_color)
label_score.pack()

canvas = Canvas(width=canvas_width, height=canvas_height, bg=canvas_bg, highlightbackground='grey')
canvas.pack(padx=10, pady=10)

canvas.create_text((canvas_width / 2, canvas_height / 2), text='Press R to launch', font='Times 50', fill=font_color)

game = False


def launch(event):
    global snake, food, direction, score, game

    canvas.delete('all')

    score = snake_length
    label_score.configure(text=f'{score}')
    direction = 'right'
    snake = Snake()
    food = Food()
    game = True
    move()


root.bind('<r>', launch)
root.bind('<Key>', change_direction)
root.bind('<Escape>', lambda e: root.destroy())

root.mainloop()

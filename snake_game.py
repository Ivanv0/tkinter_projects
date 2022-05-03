from tkinter import Tk, Canvas, Label
from random import randrange

speed = 300  # время между кадрами
canvas_width = 600  # общая длина
canvas_height = 500  # общая высота
cell_size = 50  # размер клетки
cells_num = (canvas_width // cell_size) * (canvas_height // cell_size)
snake_length = 3  # начальная длина змейки

# цвета
canvas_bg = 'linen'  # игровое поле
snake_head_color = 'lime green'  # голова змейки
snake_head_frame_color = 'cyan'  # обводка головы змейки
snake_head_line_color = 'red'  # линия на голове змейки
snake_body_color = 'lawn green'  # тело змеи
snake_body_frame_color = 'pale green'  # обводка для тела змейки
snake_body_line_color = 'black'  # линия на теле змейки
food_color = 'tomato'  # еда
food_frame_color = 'coral'  # обводка еды


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
        if score != cells_num:
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
            text = 'YOU WIN'
        else:
            text = 'GAME OVER'
        canvas.create_text((canvas_width // 2, canvas_height // 2),
                           text=text, font='Times 50')
        canvas.create_text((canvas_width // 2, canvas_height // 2 + 50), text='Press R to restart', font='Times 20')
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

score = snake_length
label_score = Label(text=f'{score}', font='Times 30')
label_score.pack()

canvas = Canvas(width=canvas_width, height=canvas_height, bg=canvas_bg)
canvas.pack()

canvas.create_text((canvas_width / 2, canvas_height / 2), text='Press R to launch', font='Times 50')

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

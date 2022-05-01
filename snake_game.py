from tkinter import Tk, Canvas, Label
from random import randrange

speed = 200
canvas_width = 600
canvas_height = 500
cell_size = 25
snake_length = 3

canvas_bg = 'linen'
snake_head_color = 'lime green'
snake_head_frame_color = 'cyan'
snake_body_color = 'lawn green'
snake_body_frame_color = 'pale green'
food_color = 'tomato'
food_frame_color = 'coral'

class Snake:
    def __init__(self):
        self.coords = [(0,0)] * snake_length
        self.squares = []
        for x, y in self.coords:
            square = canvas.create_rectangle((x+1, y+1),
                (x+cell_size-1, y+cell_size-1), fill=snake_body_color)
            self.squares.insert(0, square)

class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.oval = 0
        self.place()

    def place(self):
        while (self.x, self.y) in snake.coords:
            self.x = randrange(0, canvas_width // cell_size) * cell_size
            self.y = randrange(0, canvas_height // cell_size) * cell_size
        self.oval = canvas.create_oval((self.x+2, self.y+2), (self.x+cell_size-2, self.y+cell_size-2),
            fill=food_color, outline=food_frame_color)

    def replace(self):
        canvas.delete(self.oval)
        self.place()

def move():
    x, y = snake.coords[0]

    if direction == 'right':
        x += cell_size
    elif direction == 'left':
        x -= cell_size
    elif direction == 'up':
        y -= cell_size
    elif direction == 'down':
        y += cell_size

    if check_collision(x, y):
        canvas.create_text((canvas_width//2, canvas_height//2),
            text='GAME OVER', font='Times 50')
    else:
        snake.coords.insert(0, (x, y))
        square = canvas.create_rectangle((x+1, y+1), (x+cell_size-1, y+cell_size-1),
            fill=snake_head_color, outline=snake_head_frame_color)
        snake.squares.insert(0, square)

        canvas.itemconfig(snake.squares[1], fill=snake_body_color,
            outline= snake_body_frame_color)

        if x == food.x and y == food.y:
            global score

            food.replace()
            score += 1
            label_score.configure(text=f'{score}')
        else:
            del snake.coords[-1]
            canvas.delete(snake.squares.pop())

        root.after(speed, move)

def change_direction(new):
    global direction

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
    if (x, y) in snake.coords[1:]:
        return True

root = Tk()
root.geometry('+0+0')
root.resizable(False, False)

score = 3
label_score = Label(text=f'{score}', font='Times 30')
label_score.pack()

canvas = Canvas(width=canvas_width, height=canvas_height, bg=canvas_bg)
canvas.pack()

direction = 'right'
snake = Snake()
food = Food()

root.bind('<Up>', lambda event: change_direction('up'))
root.bind('<Down>', lambda event: change_direction('down'))
root.bind('<Right>', lambda event: change_direction('right'))
root.bind('<Left>', lambda event: change_direction('left'))

move()

root.bind('<Escape>', lambda e: root.destroy())
root.mainloop()
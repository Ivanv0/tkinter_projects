from tkinter import Tk,  Canvas
from math import pi, sin, cos

def end_xy(line_length, angle):
	x = center_x + line_length * cos(angle)
	y = center_y + line_length * sin(angle)
	return (x,y)

def text():
	start = -round(pi/3, 5)
	finish = round(start + 2*pi, 5)
	step = round(pi/30, 5)
	line_start = (canv.winfo_width() - 4) // 2 - 10
	line_end = (canv.winfo_width() - 4) // 2 -5
	i = 0
	h = 1
	while start < finish:
		if i % 5:
			canv.create_line(end_xy(line_start, start), end_xy(line_end, start))
		else:
			canv.create_line(end_xy(0, start), end_xy(line_end, start), fill='grey70')
			canv.create_line(end_xy(line_start-2, start), end_xy(line_end, start), width=3)
			canv.create_text(end_xy(line_start - 10, start), text=f'{h}')
			h += 1
		i += 1
		start += step

root = Tk()

# высота и ширина холста могут быть разными
# это будет выгдядеть странно, но это работает
height = 400
width = 400
upd_time = 5 # время в миллисекундах используемое для анимации

canv = Canvas(root, height=height+10, width=width+10)
canv.pack()
canv.update()

center_x = (canv.winfo_width() - 4) // 2
center_y = (canv.winfo_height() - 4) // 2

text()
canv.create_oval((center_x-2, center_y-2), (center_x+2, center_y+2), fill='black')
canv.create_oval((5,5), (width+5, height+5))

angle_of_big = - round(pi, 5) / 2
len_of_big = (canv.winfo_width() - 4) // 2 - 20

angle_of_small = - round(pi, 5) / 2
len_of_small = (canv.winfo_width() - 4) // 5

angle_step = round(pi / 180, 5)
step = 0

def stop(event):
	global anim 
	anim = False

def speed(event):
	global upd_time
	if event.char == '=':
		if upd_time < 5:
			upd_time += 1
		else:
			upd_time += 5
	if event.char == '-':
		if upd_time > 0:
			if upd_time <= 5:
				upd_time -= 1
			else:
				upd_time -= 5
	print(upd_time)

anim = True
root.bind('<Escape>', stop)
root.bind('<Key>', speed)

big = canv.create_line((center_x, center_y), end_xy(len_of_big, angle_of_big))
small = canv.create_line((center_x, center_y), end_xy(len_of_small, angle_of_small))

while anim:
	root.after(upd_time)
	step += 1
		
	if step == 12:
		step = 0

		canv.delete(small)
		angle_of_small += angle_step
		small = canv.create_line((center_x, center_y), end_xy(len_of_small, angle_of_small))		
	
	canv.delete(big)
	angle_of_big += angle_step
	big = canv.create_line((center_x, center_y), end_xy(len_of_big, angle_of_big))
	
	canv.update()

root.bind('<Escape>', lambda e: root.destroy())
root.mainloop()
# при закрытии выдаёт ошибку связанную с прерыванием

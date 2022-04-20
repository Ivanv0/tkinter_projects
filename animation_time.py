from tkinter import Tk,  Canvas
from time import localtime
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
			canv.create_text(end_xy(line_start - 20, start), text=f'{h}', font=20)
			h += 1
		i += 1
		start += step

def get_time():
	current = localtime()
	return current.tm_sec, current.tm_min, current.tm_hour

root = Tk()

# высота и ширина холста могут быть разными
# это будет выгдядеть странно, но это работает
height = 400
width = 400
upd_time = 1000 # время в миллисекундах используемое для анимации

canv = Canvas(root, height=height+10, width=width+10)
canv.pack()
canv.update()

center_x = (canv.winfo_width() - 4) // 2
center_y = (canv.winfo_height() - 4) // 2
center = (center_x, center_y)

text()
canv.create_oval((center_x-2, center_y-2), (center_x+2, center_y+2), fill='black')
canv.create_oval((5,5), (width+5, height+5))

len_of_h = (canv.winfo_width() - 4) // 6
len_of_m = (canv.winfo_width() - 4) // 3 + 20
len_of_s = (canv.winfo_width() - 4) // 2 - 20

angle_of_h = 0
angle_of_m = 0
angle_of_s = 0

angle_step = round(pi / 30, 5)
h_step = angle_step * 5
zero = - round(pi / 2, 5)

def stop(event):
	global anim 
	anim = False

anim = True
root.bind('<Escape>', stop)

hour = canv.create_line(center, end_xy(len_of_h, angle_of_h))
minut = canv.create_line(center, end_xy(len_of_m, angle_of_m))
second = canv.create_line(center, end_xy(len_of_s, angle_of_s))

while anim:
	time = get_time()
	print(time)

	canv.delete(second)
	angle_of_s = zero + (time[0] * angle_step) 
	second = canv.create_line(center, end_xy(len_of_s, angle_of_s), width=2)		
	
	canv.delete(minut)
	angle_of_m = zero + (time[1] * angle_step) + (time[0] * angle_step)/60
	minut = canv.create_line(center, end_xy(len_of_m, angle_of_m), width=2)
	
	canv.delete(hour)
	angle_of_h = zero + (time[2] * h_step) + (time[1] * angle_step) / 12
	hour = canv.create_line(center, end_xy(len_of_h, angle_of_h), width=2)

	canv.update()
	root.after(upd_time)

root.bind('<Escape>', lambda e: root.destroy())
root.mainloop()
# при закрытии выдаёт ошибку связанную с прерыванием

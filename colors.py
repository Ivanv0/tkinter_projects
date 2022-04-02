from tkinter import Tk, Canvas, PhotoImage, Frame, Label, Button, Entry
from tkinter import messagebox  as mb

def rgb(r, g, b):
	def dop(s):
		if s > 255:
			s %= 256
		if s < 0:
			s = 255 - (-s % 256)
		s = hex(s)[2:]
		if len(s) == 1: s = '0' + s
		return s
	return '#' + dop(r) + dop(g) + dop(b)

am = lambda x, y: (x + y) // 2
gm = lambda x, y: int((x * y)**0.5)

def get_color(event):
	try:
		c = img.get(event.x, event.y)
		color.configure(bg=rgb(c[0],c[1],c[2]))
		c = tuple(map(str, c))
		num.configure(text=c[0]+'-'+c[1]+'-'+c[2])
	except:
		pass

def get_text(w):
	if n := w.get() :
		return n
	else:
		return '0'

def reprint():
	try:
		r = get_text(r_entry)
		g = get_text(g_entry)
		b = get_text(b_entry)
		i, j = 0, 0
		while (i != 256) and (j != 256):
			if i < j:
				y = j
				for x in range(i, 256):
					img.put(rgb(eval(r), eval(g), eval(b)), (x,y))
				i += 1
			else:
				x = i
				for y in range(j, 256):
					img.put(rgb(eval(r), eval(g), eval(b)), (x,y))
				j += 1
			canv.update()
		out.configure(text='Done')
	except Exception as e:
		out.configure(text=f'{e}')

def get_help():
	message = '''For reprint, you can use x, y,
ordinary numbers and python expressions
you can also use two functions sra and srg
am - the algebraic mean
am(a, b) = (a + b) / 2
gm - is the geometric mean
gm(a, b) = √(a * b)
Use integer values to make everything work
Both functions also return integer values
You can use negative values for the inverse gradient
Use the English keyboard layout to enter values'''
	mb.showinfo('HELP', message)

def prw(event):
	out.configure(text='Wait')

h = 256
w = 256

root = Tk()

up_frame = Frame()
up_frame.pack()

canv = Canvas(up_frame, height=h, width=w)
canv.pack(side='left')

frame = Frame(up_frame, height=h, width=w)
frame.pack(side='right')

num = Label(frame, text='255-255-255', font=('TimesNew_Roman', 30))
color = Canvas(frame,height=150,width=250, bg='white')
num.pack()
color.pack()

img = PhotoImage(width=w, height=h)
canv.create_image((w/2, h/2), image=img, state='normal')

down_frame = Frame()
down_frame.pack()

width = 8
Label(down_frame, text='R=', font=('TimesNew_Roman', 15)).pack(side='left')
r_entry = Entry(down_frame, width=width, font=('TimesNew_Roman', 15))
r_entry.pack(side='left')
Label(down_frame, text='G =', font=('TimesNew_Roman', 15)).pack(side='left')
g_entry = Entry(down_frame, width=width, font=('TimesNew_Roman', 15))
g_entry.pack(side='left')
Label(down_frame, text='B =', font=('TimesNew_Roman', 15)).pack(side='left')
b_entry = Entry(down_frame, width=width, font=('TimesNew_Roman', 15))
b_entry.pack(side='left')

repr_button = Button(down_frame, width=width, text='reprint', font=('TimesNew_Roman', 14), command=reprint)
repr_button.pack(side='left')

out = Label(root, text='Wait', font=('TimesNew_Roman', 20))
out.pack()

Button(text='     HELP     ', font=('TimesNew_Roman', 15), command=get_help).pack()

root.update()
for x in range(256):
	for y in range(256):
		img.put(rgb(x,y,gm(x,y)), (x,y))
out['text'] = '|------------------|'

canv.bind('<Motion>', get_color)
repr_button.bind('<Button-1>', prw)
root.mainloop()
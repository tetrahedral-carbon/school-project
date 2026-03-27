# base for ticket booking system

from tkinter import *

root = Tk()
root.geometry("1200x900")

Label(root, text = "welcome to bus ticket booking center", font = ("Arial", 25, "bold")).grid(row = 0, column = 1)

# seat selection-deselection changes
num = 0     # no. of seats selected

def select(seatnum):
    seat_btn = seat_dict[seatnum]
    seat_btn.config(bg = "green", command = lambda n=seatnum: deselect(n))
    global cost_counter
    global num
    num += 1
    cost_counter.config(text = f"{num} seat(s) selected --> total cost = ₹{num*500}")


def deselect(seatnum):
    seat_btn = seat_dict[seatnum]
    seat_btn.config(bg = "#F0F0F0", command = lambda n=seatnum: select(n))
    global cost_counter
    global num
    num -= 1
    cost_counter.config(text = f"{num} seat(s) selected --> total cost = ₹{num*500}")


# creating seats
seat_dict = {}
# first row
for i in range(1, 4):
    seatnum = i
    seat_btn = Button(root, text = f"L{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select(n), padx = 30)
    seat_btn.grid(row = 1, column = i-1)
    seat_dict[i] = seat_btn

# second row
for i in range(4, 7):
    seatnum = i
    seat_btn = Button(root, text = f"L{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select(n), padx = 30)
    seat_btn.grid(row = 2, column = i-4)
    seat_dict[i] = seat_btn

# third row
for i in range(7, 10):
    seatnum = i
    seat_btn = Button(root, text = f"L{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select(n), padx = 30)
    seat_btn.grid(row = 3, column = i-7)
    seat_dict[i] = seat_btn

# fourth row
for i in range(10, 13):
    seatnum = i
    seat_btn = Button(root, text = f"L{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select(n), padx = 22)
    seat_btn.grid(row = 4, column = i-10)
    seat_dict[i] = seat_btn

# cost counter
cost_counter = Label(root, text = f"{num} seat(s) selected --> total cost = ₹{num*500}", font = ("Arial", 20))
cost_counter.grid(row = 5, column = 1)

root.mainloop()
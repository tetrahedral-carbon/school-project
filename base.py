# base for ticket booking system

# gui modules
from tkinter import *
from tkinter import ttk
import ttkbootstrap as ttk

# welcome page
root = Tk()
root.geometry("1920x1080")
root.title("BlueBus Booking Platform")

wlcm_lbl = Label(root, text = "Welcome To Bus Ticket Booking Center", font = ("Arial", 25, "bold"))
wlcm_lbl.grid(row = 0, column = 0, columnspan = 2)

# seat selection-deselection changes
num_low = num_up = 0     # no. of seats selected

# LOWER BERTH
def select_low(seatnum):
    seat_btn = seat_dict_low[seatnum]
    seat_btn.config(bg = "green", command = lambda n=seatnum: deselect_low(n))
    global cost_counter, num_low, num_up

    num_low += 1
    num = num_low + num_up
    cost = num_low*500 + num_up*400
    cost_counter.config(text = f"{num} seat(s) selected --> total cost = ₹{cost}")

def deselect_low(seatnum):
    seat_btn = seat_dict_low[seatnum]
    seat_btn.config(bg = "white", command = lambda n=seatnum: select_low(n))
    global cost_counter, num_low, num_up

    num_low -= 1
    num = num_low + num_up
    cost = num_low*500 + num_up*400
    cost_counter.config(text = f"{num} seat(s) selected --> total cost = ₹{cost}")

# UPPER BERTH
def select_up(seatnum):
    seat_btn = seat_dict_up[seatnum]
    seat_btn.config(bg = "green", command = lambda n=seatnum: deselect_up(n))
    global cost_counter, num_low, num_up

    num_up += 1
    num = num_low + num_up
    cost = num_low*500 + num_up*400
    cost_counter.config(text = f"{num} seat(s) selected --> total cost = ₹{cost}")

def deselect_up(seatnum):
    seat_btn = seat_dict_up[seatnum]
    seat_btn.config(bg = "white", command = lambda n=seatnum: select_up(n))
    global cost_counter, num_low, num_up

    num_up -= 1
    num = num_low + num_up
    cost = num_low*500 + num_up*400
    cost_counter.config(text = f"{num} seat(s) selected --> total cost = ₹{cost}")



# creating frame for lower berth
lower_frame = LabelFrame(root, text = "", padx = 100, pady = 100) 
lower_frame.grid(row = 1, column = 0)

Label(lower_frame, text = "                             ").grid(row = 0, column = 1)
Label(lower_frame, text = "\nLower Berth", font = ("Arial", 20)).grid(row = 6, column = 1)

# creating seats - lower berth
seat_dict_low = {}
# first row
for i in range(1, 4):
    seatnum = i
    seat_btn = Button(lower_frame, text = f"L{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select_low(n), padx = 34, bg = "white")
    if i == 1:
        seat_btn.grid(row = 1, column = i-1)
        seat_dict_low[i] = seat_btn
    else:
        seat_btn.grid(row = 1, column = i)
        seat_dict_low[i] = seat_btn

# second row
for i in range(4, 7):
    seatnum = i
    seat_btn = Button(lower_frame, text = f"L{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select_low(n), padx = 34, bg = "white")
    if i == 4:
        seat_btn.grid(row = 2, column = i-4)
        seat_dict_low[i] = seat_btn
    else:
        seat_btn.grid(row = 2, column = i-3)
        seat_dict_low[i] = seat_btn

# third row
for i in range(7, 10):
    seatnum = i
    seat_btn = Button(lower_frame, text = f"L{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select_low(n), padx = 34, bg = "white")
    if i == 7:
        seat_btn.grid(row = 3, column = i-7)
        seat_dict_low[i] = seat_btn
    else:
        seat_btn.grid(row = 3, column = i-6)
        seat_dict_low[i] = seat_btn

# fourth row
for i in range(10, 13):
    seatnum = i
    seat_btn = Button(lower_frame, text = f"L{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select_low(n), padx = 23, bg = "white")
    if i == 10:
        seat_btn.grid(row = 4, column = i-10)
        seat_dict_low[i] = seat_btn
    else:
        seat_btn.grid(row = 4, column = i-9)
        seat_dict_low[i] = seat_btn

# fifth row
for i in range(13, 16):
    seatnum = i
    seat_btn = Button(lower_frame, text = f"L{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select_low(n), padx = 23, bg = "white")
    if i == 13:
        seat_btn.grid(row = 5, column = i-13)
        seat_dict_low[i] = seat_btn
    else:
        seat_btn.grid(row = 5, column = i-12)
        seat_dict_low[i] = seat_btn




# creating frame for upper berth
upper_frame = LabelFrame(root, text = "", padx = 100, pady = 100) 
upper_frame.grid(row = 1, column = 1)

Label(upper_frame, text = "                             ").grid(row = 0, column = 1)
Label(upper_frame, text = "\nUpper Berth", font = ("Arial", 20)).grid(row = 6, column = 1)

# creating seats - upper berth
seat_dict_up = {}
# first row
for i in range(1, 4):
    seatnum = i
    seat_btn = Button(upper_frame, text = f"U{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select_up(n), padx = 34, bg = "white")
    if i == 1:
        seat_btn.grid(row = 1, column = i-1)
        seat_dict_up[i] = seat_btn
    else:
        seat_btn.grid(row = 1, column = i)
        seat_dict_up[i] = seat_btn

# second row
for i in range(4, 7):
    seatnum = i
    seat_btn = Button(upper_frame, text = f"U{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select_up(n), padx = 34, bg = "white")
    if i == 4:
        seat_btn.grid(row = 2, column = i-4)
        seat_dict_up[i] = seat_btn
    else:
        seat_btn.grid(row = 2, column = i-3)
        seat_dict_up[i] = seat_btn

# third row
for i in range(7, 10):
    seatnum = i
    seat_btn = Button(upper_frame, text = f"U{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select_up(n), padx = 34, bg = "white")
    if i == 7:
        seat_btn.grid(row = 3, column = i-7)
        seat_dict_up[i] = seat_btn
    else:
        seat_btn.grid(row = 3, column = i-6)
        seat_dict_up[i] = seat_btn

# fourth row
for i in range(10, 13):
    seatnum = i
    seat_btn = Button(upper_frame, text = f"U{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select_up(n), padx = 23, bg = "white")
    if i == 10:
        seat_btn.grid(row = 4, column = i-10)
        seat_dict_up[i] = seat_btn
    else:
        seat_btn.grid(row = 4, column = i-9)
        seat_dict_up[i] = seat_btn

# fifth row
for i in range(13, 16):
    seatnum = i
    seat_btn = Button(upper_frame, text = f"U{seatnum}", font = ("Arial", 20, "normal"), command = lambda n=seatnum: select_up(n), padx = 23, bg = "white")
    if i == 13:
        seat_btn.grid(row = 5, column = i-13)
        seat_dict_up[i] = seat_btn
    else:
        seat_btn.grid(row = 5, column = i-12)
        seat_dict_up[i] = seat_btn



# cost counter
cost_counter = Label(root, text = f"0 seat(s) selected --> total cost = ₹0", font = ("Arial", 20))
cost_counter.grid(row = 2, column = 0)

Label(root, text = "").grid(row = 3, column = 0)


# after selection booking
def book():
    global num_up, num_low
    upper_frame.grid_forget()
    lower_frame.grid_forget()
    book_btn.grid_forget()
    wlcm_lbl.grid_forget()
    cost_counter.grid_forget()
    
    ticket_cost = num_low*500 + num_up*400
    total_cost = ticket_cost*1.18

    Label(root, text = f"{num_up+num_low} seats booked", font = ("Calibri", 25)).grid(row = 0, column = 0)

    Label(root, text = f"{num_up} Upper Berth Seat(s)", font = ("Calibri", 25)).grid(row = 1, column = 0)
    Label(root, text = f"{num_low} Lower Berth Seat(s)", font = ("Calibri", 25)).grid(row = 1, column = 1)
    
    # price breakdown
    Label(root, text = "\nPrice Breakdown:", font = ("Calibri", 25)).grid(row = 2, column = 0)
    Label(root, text = f"Ticket Price   : ₹{ticket_cost:.2f}", font = ("Calibri", 25)).grid(row = 3, column = 0)
    Label(root, text = f"Taxes (18% GST): ₹{ticket_cost*0.18:.2f}", font = ("Calibri", 25)).grid(row = 4, column = 0)
    Label(root, text = f"Total Price    : ₹{total_cost:.2f}", font = ("Calibri", 25)).grid(row = 5, column = 0)


    Label(root, text = "\nThank You For Chossing BlueBus, India\'s best bus service", font = ("Calibri", 25), pady = 30).grid(row = 6, column = 0, columnspan = 2)
    

book_btn = Button(root, text = "Click To Book", font = ("Arial", 15), command = book, bg = "#3FA6BF", fg = "white")
book_btn.grid(row = 4, column = 0)


# main window loop
root.mainloop()

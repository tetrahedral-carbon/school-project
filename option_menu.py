# testing area
from tkinter import *

root = Tk()
root.title("dropdown menus")
root.geometry("900x600")

# creating windows for different routes
def route1():
    route1_win = Toplevel()
    route1_win.geometry("1500x800")
    route1_win.title("Bengaluru to Chennai")

def route2():
    route2_win = Toplevel()
    route2_win.geometry("1500x800")
    route2_win.title("Chennai to Hyderabad")

def route3():
    route3_win = Toplevel()
    route3_win.geometry("1500x800")
    route3_win.title("Hyderabad to Bengaluru")


# selecting routes
route_opt = ["Bengaluru to Chennai", "Chennai to Hyderabad", "Hyderabad to Bengaluru"]      # list of routes

route_click = StringVar()
route_click.set(route_opt[0])       # default route

route_menu = OptionMenu(root, route_click, *route_opt)
route_menu.pack()

route_menu.config(font = ("Arial", 20))

def route_select():
    if route_click.get() == route_opt[0]:
        route1()
    elif route_click.get() == route_opt[1]:
        route2()
    else:
        route3()

route_btn = Button(root, text = "click to select route", font = ("Arial", 15), command = route_select)
route_btn.pack()

root.mainloop()
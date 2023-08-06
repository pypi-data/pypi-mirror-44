try:
    from tkinter import *
except ImportError:
    from Tkinter import *

import os
import sys
from search.search import get_highlighted, search, get_engine

def search_gui_highlighted():
    text = " ".join(get_highlighted())
    engine = get_engine('google')

    master = Tk()
    master.wm_attributes('-type', 'splash')

    v = StringVar()
    e = Entry(master, textvariable=v, width=len(text) + 100)
    v.set(text)
    e.pack()
    e.icursor(len(text))

    def callback(event):
        query = v.get().split()
        search(engine, query)
        close(event)

    def close(event):
        master.destroy()
        sys.exit()

    e.bind("<Return>", callback)
    e.bind("<Escape>", close)
    if os.getenv('SR_CLOSE_LOSS_FOCUS', 'yes') == 'yes':
        master.bind("<FocusOut>", close)

    e.focus()
    mainloop()


def search_gui():
    engine = get_engine('google')

    master = Tk()
    master.wm_attributes('-type', 'splash')

    v = StringVar()
    e = Entry(master, textvariable=v, width=100)
    e.pack()

    def callback(event):
        query = v.get().split()
        search(engine, query)
        close(event)

    def close(event):
        master.destroy()
        sys.exit()

    e.bind("<Return>", callback)
    e.bind("<Escape>", close)
    if os.getenv('SR_CLOSE_LOSS_FOCUS', 'yes') == 'yes':
        master.bind("<FocusOut>", close)

    e.focus()
    mainloop()


if __name__ == "__main__":
    search_gui()

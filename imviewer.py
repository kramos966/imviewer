#!/usr/env/python3
import gui.top
import tkinter as tk
__author__ = "kramos966"
__email__  = "kramos966@outlook.com"

root = tk.Tk()
root.title("imviewer")
prog = gui.top.MainWindow(root, (640, 480))
root.mainloop()

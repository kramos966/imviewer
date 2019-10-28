import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk
import os
import sys

class MainWindow:
    def __init__(self, master, res):
        self.res = res
        self.master = master
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.cwd = os.getcwd()
        # Binding exit
        self.master.bind("q", self.quit)

        # Set geometry
        #self.master.geometry("{:d}x{:d}".format(*res))
        
        ## Show folder contents
        self.l1 = ttk.Label(text="Current files")
        self.l1.grid(row=0, column=0, sticky=tk.W+tk.S)
        # Listbox + scrollbar
        self.scroll = ttk.Scrollbar(self.master)
        self.scroll.grid(row=1, column=1, 
                rowspan=2, sticky=tk.N+tk.S)
        self.listbox = tk.Listbox(master)
        self.listbox.bind("<<ListboxSelect>>", self.handle_update)
        self.listbox.config(yscrollcommand=self.scroll.set)
        self.fill_box()
        self.listbox.grid(row=1, column=0, 
                rowspan=2, sticky=tk.N+tk.S)
        

        # Image frame
        self.imframe = ImFrame(self.master, self.res)
        self.imframe.grid(row=0, column=2, rowspan=3)
        self.imframe.grid_propagate(False)  # Ignora si hi ha res dins
        
    def fill_box(self):
        # DELETE previous entries
        self.listbox.delete(0, tk.END)
        # Get all file names in current folder
        fnames = os.listdir()
        fnames.sort()
        # Check if image
        imnames = []
        for fname in fnames:
            if fname.endswith("png") or fname.endswith("jpg") or\
                    fname.endswith("bmp") or fname.endswith("tiff"):
                imnames.append(fname)

        # Get subfolders
        subfold = list(filter(os.path.isdir, os.listdir(self.cwd)))
        subfold.sort()
        # Fill box with folders
        self.listbox.insert(tk.END, "../")
        for sub in subfold:
            self.listbox.insert(tk.END, "{:s}/".format(sub))
        # Fill with imnames
        for imname in imnames:
            self.listbox.insert(tk.END, imname)

    def handle_update(self, event):
        current_item = self.listbox.get(self.listbox.curselection())

        # Directory detection, change directory
        if current_item.endswith("/"):
            os.chdir(current_item[:-1])
            self.cwd = os.getcwd()
            self.fill_box()
        # Else, update the detected image
        else:
            self.imframe.update(current_item)

    def quit(self, event):
        self.master.destroy()
        sys.exit(0)

class ImFrame(ttk.Frame):
    """Frame onto which the image is shown."""
    def __init__(self, master, res, imname=None):
        ttk.Frame.__init__(self, master, width=res[0], height=res[1])
        self.master = master
        self.w = res[0]
        self.h = res[1]
        self.imtk = None
        self.imPIL= None

        # Label, actual location where the image is shown
        self.imlabel = ttk.Label(self)
        if imname:
            self.update(imname)
        self.imlabel.grid()
    
    def update(self, imname):
        image_PIL = Image.open(imname)
        w, h = image_PIL.size
        # If it does not fit, resize
        if (w > self.w) or (h > self.h):
            scale = min(self.w/w, self.h/h)
            new_size = (int(scale * w), int(scale * h))
            image_PIL = image_PIL.resize(new_size)
        # Convert to a tkinter image
        self.imPIL = image_PIL
        self.imtk = ImageTk.PhotoImage(self.imPIL)
        self.imlabel["image"] = self.imtk

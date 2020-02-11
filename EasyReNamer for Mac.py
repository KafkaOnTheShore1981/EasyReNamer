# -*-coding:utf-8-*-
"""This is a free tool which easily adds sequence numbers to names of files
in a selected folder, just by clicking your mouse few times.

Here is the usage:
1. Press the 'Click me' button.
2. Select a folder in the pop-up window.
3. Click 'Choose' to execute the operation or 'Cancel' to give it up.
4. 'Undo' button is used to remove sequence numbers.
5. Press 'Check' to make sure the operation has been completed successfully.

Note that operations on hidden files or sub-folders are neglected.
"""
import os
import sys
import re
import threading
import tkinter as tk
from tkinter import filedialog


class EasyReNamer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EasyReNamer V3.0")
        self.n = 0
        label_info = tk.Label(self, text="Please select a folder:")
        label_info.pack()
        panel = tk.Frame()
        self.btn_rename = tk.Button(panel, text="Click Me", width=10,
                                    highlightbackground='orange',
                                    command=threading.Thread(target=self.rename).start)
        self.btn_rename.grid(row=0, column=0, padx=30)
        self.btn_undo = tk.Button(panel, text="Undo", width=10,
                                  highlightbackground="grey",
                                  command=self.undo)
        self.btn_undo.grid(row=0, column=1, padx=30)
        btn_check = tk.Button(panel, text="Check", width=10,
                              highlightbackground='darkblue', fg='white',
                              command=self.check)
        btn_check.grid(row=0, column=2, padx=30)
        panel.pack()
        self.label_show = tk.Label(self)
        self.label_show.pack()

    def widget_position(self, width, height):
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        x = (self.width - width) / 2
        y = (self.height - height) / 2
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.grid()

    def get_items_list(self):
        try:
            self.folder_path = filedialog.askdirectory(title='EasyReNamer')
            self.items_list = os.listdir(self.folder_path)
        except OSError:
            print("Opening failed")
            sys.exit()

    def rename(self):
        self.get_items_list()
        self.btn_rename.config(state='disabled')
        for item in self.items_list.copy():
            item_path = self.folder_path + os.sep + item
            if os.path.isdir(item_path) or item.startswith('.') or \
                    item.startswith('~$'):
                continue
            else:
                new_item_path = self.folder_path + os.sep + '(' + \
                                str(self.n + 1) + ')' + item
                os.rename(item_path, new_item_path)
                self.n += 1
                self.label_show.config(text="{} file(s) renamed".format(self.n))
        self.label_show.config(text="{} file(s) completed successfully".format(self.n))

    def undo(self):
        self.get_items_list()
        for item in self.items_list.copy():
            item_path = self.folder_path + os.sep + item
            if os.path.isdir(item_path) or item.startswith('.') or \
                    item.startswith('~$'):
                continue
            else:
                new_item_path = self.folder_path + os.sep + \
                                re.sub('\(\d*\)', '', item)
                os.rename(item_path, new_item_path)
        self.label_show.config(text='Undo Finished!')

    def check(self):
        filedialog.askopenfilename()


if __name__ == "__main__":
    root = EasyReNamer()
    root.widget_position(500, 70)
    root.mainloop()

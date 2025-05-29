# Here the TreeView class but with scrols y,x
# It will be frame and table in it
import tkinter as tk
from tkinter import ttk

#كلاس الجدول
class Table:
    def __init__(self, master, width=150, height=100, columns=[], data=[]):
        self.frame = tk.Frame(master, width=width, height=height,  background="#436165")
        self.frame.grid_propagate(False)
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        self.x_scroll = tk.Scrollbar(self.frame, orient="horizontal")
        self.y_scroll = tk.Scrollbar(self.frame, orient="vertical")

        
        self.table = ttk.Treeview(self.frame, columns=columns, show="headings",
                                  xscrollcommand=self.x_scroll,
                                  yscrollcommand=self.y_scroll) #ربط السكرول العمودي
        
        self.x_scroll.config(command=self.table.xview)
        self.y_scroll.config(command=self.table.yview)

        #عرض الجدول 
        self.table.grid(row=0, column=0, sticky="nsew")
        self.x_scroll.grid(row=1,column=0, sticky="ew")
        self.y_scroll.grid(row=0, column=1, rowspan=2, sticky="ns")
        
        #اعداد الاعمده
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col,
                               width=200 if col is not columns[0] else 50, anchor="center")
        #اضافة البيانات للجدول
        for row in data:
            self.table.insert("",tk.END, values=row)
  
    def get_table(self):
        return self.frame

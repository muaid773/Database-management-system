import tkinter.ttk as tk
import tkinter as Tkk
from tkinter import Toplevel as tpl
from tkinter import messagebox as ms
from login import LogIn as lg
from table import Table
from database import Dbase

class HomePage(Tkk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.config(background="#436165")
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")
    def start(self, values):
        #البيانات اللازمة لتشغيل الواحهة
        self.db_path = values[0]
        self.table_name = values[1]
        self.table_select = []
        #الاتصال بقاعدة البيانات
        self.con = Dbase(self.db_path)
        self.con.connect()
        #تحضير الجدول
        self.table = Table(self, 560, 300,
                           self.con.get_columns(self.table_name),
                           self.con.get_data(self.table_name))

        
        head = Tkk.Frame(self, bg="#81DBFF",  width=720, height=5, pady=5)

        self.tools_frame = Tkk.Frame(self, bg="#777CEB", pady=5, height=5, width=720)

        edits_frame_left = Tkk.Frame(self, bg="#5C6C6E", height=300, width=180)

        edits_frame_right = Tkk.Frame(self, bg="#5C6C6E", height=300, width=180)

        self.table_frame = self.table.get_table()

        self.table.table.bind("<<TreeviewSelect>>", self.person)
        
        head.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.tools_frame.grid(row=1, column=0, columnspan=3, sticky="ew")
        edits_frame_left.grid(row=2, column=0, sticky="ns")
        self.table_frame.grid(row=2, column=1, sticky="nsew")
        edits_frame_right.grid(row=2, column=2, sticky="ns")
        
        #tools
        Tkk.Label(head, text="واجهة التحكم", bg="#81DBFF", height=2, font="Arial 10 bold").pack()
        self.insert_btn = tk.Button(self.tools_frame, text="اضافة", command=self.insert)
        self.insert_btn.grid(row=0, column=0, padx=2)
        self.edit_btn = tk.Button(self.tools_frame, text="تعديل", command=self.edit)
        self.edit_btn.grid(row=0, column=1, padx=2)
        self.delete_btn = tk.Button(self.tools_frame, text="حذف", command=self.delete)
        self.delete_btn.grid(row=0, column=2, padx=2)
        self.next_btn = tk.Button(self.tools_frame, text="عودة", command=lambda: self.controller.show_frame('LogIn'))
        self.next_btn.grid(row=0, column=3, padx=2)

        #About
        tk.Label(self, text="اعداد المبرمج: مؤيد علي عبد الله حوات", font="Times 10 bold", background="#313137", foreground="#FFFFFF", anchor='center').grid(row=3, column=0, columnspan=3, sticky="ew")


    def person(self, event):
        for select_person in self.table.table.selection():
            item = self.table.table.item(select_person)
            self.table_select = item["values"]
            print("selected> ",self.table_select)

    def insert(self):
        self.win_insert = tpl(self, background="#6896A5")
        self.win_insert.title("ادخال البيانات")
        self.win_insert.geometry("650x280+100+80")
        self.columns_in = self.con.get_columns_without_id(self.table_name)

        insert_btn = tk.Button(self.win_insert, text="اضافة البيانات", command=self.insert_add)
        insert_btn.grid(row=0, column=0, columnspan=6, pady=5)
        self.insert_entrys = []
        x, y = 1, -1
        for col in self.columns_in:
            y += 1
            Tkk.Label(self.win_insert, text=col, width=5, bg="#6896A5").grid(row=x, column=y)
            entry = tk.Entry(self.win_insert, width=15)
            y += 1
            entry.grid(row=x, column=y, padx=10, pady=2)
            self.insert_entrys.append(entry)
            
            if y == 5:
                x += 1
                y = -1
    def insert_add(self):
        data = []
        columns = self.columns_in
        # جلب جميعالاعمدة في الجدول بشكل خاص
        for entry in self.insert_entrys:
            value = entry.get()
            data.append(value)
        self.con.inser(self.table_name, columns, data)
        for entry in self.insert_entrys:
            entry.delete(0, Tkk.END)
        self.win_insert.destroy()
        self.controller.show_frame_values("HomePage", [self.db_path, self.table_name])
        ms.showinfo("نجحت الاضافة", "تمت اضافة البيانات بنجاح.")

    def edit(self):
        if  self.table_select != []:
            self.win_edit = tpl(self, background="#6896A5")
            self.win_edit.title("تعديل ابيانات")
            self.win_edit.geometry("600x280+100+80")           
            #جلب العمود المحدد 
            edit_btn = tk.Button(self.win_edit, text="تعديل", command=self.edit_seve)
            edit_btn.grid(row=0, column=0, columnspan=6, pady=10)
            self.edit_entrys = []
            x, y = 1, 0
            for col in self.table_select:
                Tkk.Label(self.win_edit, text=col, width=15, bg="#6896A5").grid(row=x, column=y)
                entry = tk.Entry(self.win_edit, width=15)
                entry.insert(0, col)
                entry.grid(row=x, column=y, padx=10, pady=2)
                self.edit_entrys.append(entry)
                y += 1
                if y == 6:
                    x += 1
            self.edit_entrys[0].config(state="readonly")
        else:
            ms.showerror("خطاء في التعديل", "يرجى تحديد صف ثم المحاولة مجددا")
    def edit_seve(self):
        id = int(self.table_select[0])
        #جمع المعلموات الجديدة
        new_data = []
        for d in self.edit_entrys:
            if d is not self.edit_entrys[0]:
                new_data.append(d.get())
        self.con.edit(self.table_name, id, new_data)
        self.win_edit.destroy()
        self.controller.show_frame_values("HomePage", [self.db_path, self.table_name])
        ms.showinfo("نجاح التعديل", "تم تعديل البيانات بنجاح")

    def delete(self):
        if  self.table_select != []:
            if ms.askyesno('التاكد','هل انت متاكد من الحذف'):
                row_id = self.table_select[0]
                self.con.delete(self.table_name, row_id)
                self.controller.show_frame_values("HomePage", [self.db_path, self.table_name])
        else:
            ms.showerror("خطتء في الحذف", "يرجى تحديد صف والمحاولة مجددا")

import tkinter.ttk as tk
import tkinter as Tkk
from tkinter import filedialog as Fdg
from tkinter import simpledialog as smdlg
from tkinter import messagebox as ms
from tkinter import Toplevel as tpl
from database import Dbase

class LogIn(Tkk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid(row=0, column=0, sticky="snew")
        self.config(background="#436165")

        head = Tkk.Frame(self, bg="#DCF30C")
        head.pack(fill="x")

        Tkk.Label(head, text="نظام ادارة قواعد البيانات", height=2, bg="#DCF30C", font="Times 20 bold").pack()
        open_db = Tkk.Button(self, text="فتح قاعدة بيانات", bg="#11D342", width=100, command=self.opendb)
        open_db.pack(pady=5)

        create_db = Tkk.Button(self, text="انشاء قاعدة بيانات", bg="#11D342", width=100, command=self.creat_db)
        create_db.pack(pady=5)


    def opendb(self):
        self.db_path = Fdg.askopenfilename(title="فتح قاعدة بيانات")
        if self.db_path:
            self.show_tables()

    def show_tables(self):
        if hasattr(self, 'tables_frame'):
            self.tables_frame.destroy()
            
        self.tables_frame = Tkk.Frame(self, bg="#036164")
        self.tables_frame.pack(side="top")
        Tkk.Label(self.tables_frame, text=f"الجداول في \n | {self.db_path} |", bg="#072C72", fg="#FFFFFF").pack(fill="x")
        cr_tb_btn = tk.Button(self.tables_frame, text="انشاء جدول", command=self.cr_column_tp)
        cr_tb_btn.pack()
        buttons_list = []
        #connect
        self.con = Dbase(self.db_path)
        self.con.connect()
        tables = self.con.get_tables()
        for btn in tables:
            button = Tkk.Button(self.tables_frame, text=f" {btn} ",bg="#74704C", command=lambda b=btn: self.controller.show_frame_values("HomePage",
                                    [self.db_path, b]))
            
            button.pack()
            buttons_list.append(button)

    def tables_frame_clear(self):
        pass

    def creat_db(self):
        cr_db_fr = tpl(self, background="#6896A5")
        cr_db_fr.geometry("300x300")
        cr_db_fr.title("قاعدة بيانات جديدة")

        tk.Label(cr_db_fr, text="انشاء قاعدة بيانات",background="#072C72",foreground="#FFFFFF", font="Times 20 bold").pack(fill="x")
        def save():
            pth = Fdg.askdirectory(title="حغظ في")
            DBget = db_name.get() if db_name.get().endswith(".db") else db_name.get()+".db"
            self.db_path = pth+"/"+ DBget
            if pth and DBget:    
                self.con = Dbase(self.db_path)
                self.con.connect()
                cr_db_fr.destroy()
                ms.showinfo("نجاح","تم انشاء قاعدة البيانات بنجاح ")
        cr_db_btn = tk.Button(cr_db_fr, text="انشاء", command=save)
        cr_db_btn.pack(pady=10)

        tk.Label(cr_db_fr, text="ادخل تسمية لقاعدة البيانات", font="courier", background="#6896A5").pack()
        db_name = tk.Entry(cr_db_fr)
        db_name.pack(padx=10, pady=5)
    def cr_column_tp(self):
        self.table_name = smdlg.askstring("اسم الجدول", "يرجى ادخال تسمية للجدول")
        if self.table_name is not None:
            self.column_fr = tpl(self, background="#6896A5")
            self.column_fr.title("انشاءالاعمدة")
            self.column_fr.geometry("600x300")
            self.cols_li_en = []
            self.y = 0
            self.x = 1
            self.n = 1
            def column():
                column_name = tk.Entry(self.column_fr, width=20,)
                self.y += 1
                tk.Label(self.column_fr, text=f"C{self.n}").grid(row=self.x, column=self.y)
                self.y += 1
                column_name.grid(row=self.x, column=self.y, padx=5, pady=5)
                self.cols_li_en.append(column_name)
                self.n += 1
                if self.y == 6:
                    self.x += 1
                    self.y = 0
            cr_column = tk.Button(self.column_fr, text="عمود", command=column)
            cr_column.grid(row=0, column=0, columnspan=5, pady=5)

            cr_table = tk.Button(self.column_fr, text="انشاء", command=self.create_table)
            cr_table.grid(row=1, column=7, rowspan=self.x, sticky="ns")

    def create_table(self):
        columns = {}
        for col in self.cols_li_en:
            columns[col.get()] = "TEXT"
        if columns != {}:
            self.con.create_table(self.table_name, columns)
            self.controller.show_frame("LogIn")
            self.show_tables()
            self.column_fr.destroy()
            ms.showinfo("نجاح", "تم انشاء الجدول بنجاح")
        else:
            ms.showwarning("لا اعمدة", "لايوجد اعمدة\nيرجى اضافة عمو او اكثر")








        

        

import tkinter as tk
from controllers import Controller
import os
import sys
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مدير قواعد البيانات")
        self.geometry("850x400")
        self.iconbitmap(self.resource_path("data\icon.ico"))
        self.config(background="#436165")
        self.resizable(False, False)
        
        self.controller = Controller(self)   # إدارة النوافذ
        self.controller.show_frame("LogIn")
    def resource_path(self, relative_path):
        """يعيد المسار الصحيح للملف سواء أثناء التطوير أو بعد التحويل لـ exe"""
        if hasattr(sys, '_MEIPASS'):
          return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

from home import HomePage
from login import LogIn 

class Controller:
    def __init__(self, root):
        self.root = root
        self.frames = {}

        for F in (LogIn, HomePage):
            page_name = F.__name__
            frame = F(self.root, self)
            self.frames[page_name] = frame
            
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() # رفع النافذة للأمام
    
    def show_frame_values(self, page_name, values):
        frame = self.frames[page_name]
        frame.start(values)
        frame.tkraise()
from time import sleep
from typing import Text
from PIL import Image, ImageGrab
import tkinter
import ctypes

class CTkPrScrn:
    def __init__(self):
        self.__start_x, self.__start_y = 0, 0
        self.__scale = 1

        self.__win = tkinter.Tk()
        self.__win.attributes("-alpha", 0.5)  # 设置窗口半透明
        self.__win.attributes("-fullscreen", True)  # 设置全屏
        self.__win.attributes("-topmost", True)  # 设置窗口在最上层

        self.__width, self.__height = self.__win.winfo_screenwidth(), self.__win.winfo_screenheight()

        # 创建画布
        self.__canvas = tkinter.Canvas(self.__win, width=self.__width, height=self.__height, bg="gray")

        self.__win.bind('<Button-1>', self.xFunc1)  # 绑定鼠标左键点击事件
        self.__win.bind('<ButtonRelease-1>', self.xFunc1)  # 绑定鼠标左键点击释放事件
        self.__win.bind('<B1-Motion>', self.xFunc2)  # 绑定鼠标左键点击移动事件
        self.__win.bind('<Escape>', lambda e: self.__win.destroy())  # 绑定Esc按键退出事件

        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        dc = user32.GetDC(None)
        widthScale = gdi32.GetDeviceCaps(dc, 8)  # 分辨率缩放后的宽度
        heightScale = gdi32.GetDeviceCaps(dc, 10)  # 分辨率缩放后的高度
        width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
        height = gdi32.GetDeviceCaps(dc, 117)  # 原始分辨率的高度
        self.__scale = width / widthScale
        #print(self.__width, self.__height, widthScale, heightScale, width, height, self.__scale)

        self.__win.mainloop()  # 窗口持久化

    def xFunc1(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={g_scale * event.x}, y={g_scale * event.y}")
        if event.state == 8:  # 鼠标左键按下
            self.__start_x, self.__start_y = event.x, event.y
        elif event.state == 264:  # 鼠标左键释放
            if event.x == self.__start_x or event.y == self.__start_y:
                return
        
            box={
                'start_x': self.__scale * self.__start_x,
                'start_y': self.__scale * self.__start_y,
                'end_x': self.__scale * event.x,
                'end_y': self.__scale * event.y
            }
            

            self.__win.update()
            sleep(0.5)
            self.__win.destroy()

    def xFunc2(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={self.__scale * event.x}, y={self.__scale * event.y}")
        if event.x == self.__start_x or event.y == self.__start_y:
            return
        self.__canvas.delete("prscrn")
        self.__canvas.create_rectangle(self.__start_x, self.__start_y, event.x, event.y,
                                       fill='white', outline='red', tag="prscrn")
        # 包装画布
        self.__canvas.pack()

if __name__ == '__main__':
    prScrn = CTkPrScrn()

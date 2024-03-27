from tkinter import Tk, Label, Button, filedialog, PhotoImage
from PIL import Image, ImageTk
import os
import subprocess

class ImageMixer:
    def __init__(self, window):
        self.window = window  # 初始化窗口
        window.title("图片合成器")  # 设置窗口标题

        # 设置窗口大小
        window.geometry('500x500')

        self.label = Label(window, text="请选择图片")  # 创建标签
        self.label.grid(row=0, column=0, columnspan=2)  # 设置标签位置

        self.select_img_button = Button(window, text="选择普通图片", command=self.select_img)  # 创建选择图片按钮
        self.select_img_button.grid(row=1, column=0)  # 设置按钮位置

        self.select_barcode_button = Button(window, text="选择二维码图片", command=self.select_barcode)  # 创建选择二维码图片按钮
        self.select_barcode_button.grid(row=2, column=0)  # 设置按钮位置

        self.mix_button = Button(window, text="合成图片", command=self.mix_images)  # 创建合成图片按钮
        self.mix_button.grid(row=3, column=0)  # 设置按钮位置

        self.img_putong_path = None  # 初始化普通图片路径
        self.img_barcode_path = None  # 初始化二维码图片路径

        self.img_putong_label = Label(window)  # 创建普通图片标签
        self.img_putong_label.grid(row=1, column=1)  # 设置标签位置

        self.img_barcode_label = Label(window)  # 创建二维码图片标签
        self.img_barcode_label.grid(row=2, column=1)  # 设置标签位置

        self.img_mix_label = Label(window)  # 创建合成图片标签
        self.img_mix_label.grid(row=3, column=1)  # 设置标签位置

        self.img_mix_text_label = Label(window, text="")  # 创建合成图片文本标签
        self.img_mix_text_label.grid(row=4, column=1)  # 设置标签位置

    def select_img(self):
        self.img_putong_path = filedialog.askopenfilename()  # 打开文件对话框选择普通图片
        self.show_img(self.img_putong_path, self.img_putong_label)  # 显示选择的普通图片

    def select_barcode(self):
        self.img_barcode_path = filedialog.askopenfilename()  # 打开文件对话框选择二维码图片
        self.show_img(self.img_barcode_path, self.img_barcode_label)  # 显示选择的二维码图片

    def show_img(self, img_path, img_label):
        img = Image.open(img_path)  # 打开图片
        img.thumbnail((100, 100))  # 缩小图片
        img_tk = ImageTk.PhotoImage(img)  # 创建PhotoImage对象
        img_label.config(image=img_tk)  # 设置标签图片
        img_label.image = img_tk  # 保存图片引用

    def mix_images(self):
        if not os.path.exists(self.img_putong_path) or not os.path.exists(self.img_barcode_path):  # 检查图片路径是否存在
            print("文件不存在")
            return

        img_putong = Image.open(self.img_putong_path)  # 打开普通图片
        img_barcode = Image.open(self.img_barcode_path)  # 打开二维码图片

        img_mix = Image.new('RGBA', img_putong.size)  # 创建新的RGBA图片

        for w in range(img_mix.width):
            for h in range(img_mix.height):
                pxl_putong = img_putong.getpixel((w, h))  # 获取普通图片像素
                pxl_barcode = img_barcode.getpixel((w, h))  # 获取二维码图片像素

                if pxl_barcode[0] > 200:
                    img_mix.putpixel((w, h), pxl_putong)  # 设置新图片像素
                else:
                    alpha = 150
                    r = int((pxl_putong[0] - (255 - alpha)) / alpha * 255)
                    g = int((pxl_putong[1] - (255 - alpha)) / alpha * 255)
                    b = int((pxl_putong[2] - (255 - alpha)) / alpha * 255)

                    r = max(0, min(255, r))
                    g = max(0, min(255, g))
                    b = max(0, min(255, b))

                    img_mix.putpixel((w, h), (r, g, b, alpha))  # 设置新图片像素

        img_mix.save("./合成图片.png")  # 保存新图片

        output_path = os.path.abspath("./合成图片.png")  # 获取新图片绝对路径

        self.show_img(output_path, self.img_mix_label)  # 显示新图片
        self.img_mix_label.bind("<Button-1>", lambda e: subprocess.run('explorer /select,"{}"'.format(output_path)))  # 绑定点击事件打开新图片位置
        self.img_mix_text_label.config(text="点击打开图片位置")  # 设置新图片文本标签

if __name__ == "__main__":
    root = Tk()  # 创建Tk对象
    gui = ImageMixer(root)  # 创建ImageMixer对象
    root.mainloop()  # 开始主循环

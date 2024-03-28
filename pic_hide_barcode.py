from tkinter import Tk, Label, Entry, Button, filedialog, PhotoImage
from PIL import Image, ImageTk
import os

# 选择图片的函数
def select_image(entry, label):
    # 打开文件对话框，选择图片文件
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    # 清空输入框，并将选择的文件路径插入输入框
    entry.delete(0, 'end')
    entry.insert(0, filename)

    # 打开并显示图片
    img = Image.open(filename)
    img.thumbnail((100, 100))  # 缩小图片
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo  # 保存引用，防止被垃圾回收

# 创建图片的函数
def create_image():
    # 获取输入框中的文件路径
    imgPutong_path = entry1.get()
    imgBarcode_path = entry2.get()

    # 打开图片文件
    imgPutong = Image.open(imgPutong_path)
    imgBarcode = Image.open(imgBarcode_path)

    # 创建新图片，使用RGBA模式，方便稍后保存为png。新图的分辨率和普通图相同。
    imgMix = Image.new("RGBA", (imgPutong.width, imgPutong.height) )

    # 填充新图片上的每一个像素
    for w in range(imgMix.width):
        for h in range(imgMix.height):
            pxlPutong = imgPutong.getpixel( (w,h) )
            pxlBarcode = imgBarcode.getpixel( (w,h) )

            # 如果二维码图片的像素值大于200，则使用普通图片的像素
            if pxlBarcode[0] > 200: 
                imgMix.putpixel( (w, h), (pxlPutong[0], pxlPutong[1], pxlPutong[2], 255) )
            else:
                # 否则，使用二维码图片的像素，并设置透明度为150
                alpha = 150
                imgMix.putpixel( (w, h), (int( ( pxlPutong[0]- (255-alpha) ) / alpha * 255),
                                          int( ( pxlPutong[1]- (255-alpha) ) / alpha * 255),
                                          int( ( pxlPutong[2]- (255-alpha) ) / alpha * 255),
                                          alpha) )

    # 保存新图片
    imgMix.save("./合成图片.png")

    # 获取当前工作目录，并拼接出新图片的完整路径
    cwd = os.getcwd()
    img_path = os.path.join(cwd, "合成图片.png")

    print("生成完毕，图片位置：", img_path)
    print("快去群里浪吧")

    # 显示合成的图片
    img = Image.open(img_path)
    img.thumbnail((100, 100))  # 缩小图片
    photo = ImageTk.PhotoImage(img)
    img_label.config(image=photo)
    img_label.image = photo  # 保存引用，防止被垃圾回收

    # 点击图片打开图片位置
    img_label.bind("<Button-1>", lambda e: os.startfile(os.path.dirname(os.path.realpath(img_path))))

    # 显示"点击打开图片"的标签
    text_label.config(text="点击打开图片")

# 创建Tk窗口
root = Tk()

# 创建并显示标签和输入框
label1 = Label(root, text="请选择普通图片：")
label1.pack()

entry1 = Entry(root)
entry1.pack()

button1 = Button(root, text="选择图片")
button1.pack()

img_label1 = Label(root)
img_label1.pack()

# 设置按钮的点击事件
button1.config(command=lambda: select_image(entry1, img_label1))

label2 = Label(root, text="请选择二维码图片：")
label2.pack()

entry2 = Entry(root)
entry2.pack()

button2 = Button(root, text="选择图片")
button2.pack()

img_label2 = Label(root)
img_label2.pack()

button2.config(command=lambda: select_image(entry2, img_label2))

# 创建并显示生成图片的按钮
button = Button(root, text="生成图片", command=create_image)
button.pack()

# 创建并显示图片标签
img_label = Label(root)
img_label.pack()

# 创建并显示文本标签
text_label = Label(root)
text_label.pack()

# 启动Tk的消息循环
root.mainloop()
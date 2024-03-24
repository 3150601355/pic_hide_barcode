from PIL import Image   # 若提示No module named 'PIL'，则：pip install Pillow

# 打开两张素材图片，其中二维码背景为白色。
# 注意：为了代码简洁，这两张图的分辨率必需要是相同的。
imgPutong = Image.open("普通图片.jpg")          
imgBarcode = Image.open("二维码.jpg")   

# 创建新图片，使用RGBA模式，方便稍后保存为png。新图的分辨率和普通图相同。
imgMix = Image.new("RGBA", (imgPutong.width, imgPutong.height) )

# 填充新图片上的每一个像素
for w in range(imgMix.width):
    for h in range(imgMix.height):
        pxlPutong = imgPutong.getpixel( (w,h) )
        pxlBarcode = imgBarcode.getpixel( (w,h) )

        if pxlBarcode[0] > 200: 
            # 如果二维码上的这个像素为白色，直接复制imgXg对应位置的像素值到imgResult，透明度设为255（不透明）
            imgMix.putpixel( (w, h), (pxlPutong[0], pxlPutong[1], pxlPutong[2], 255) )
        else:
            # 如果二维码上的这个像素为黑色，根据视频中的公式计算出新的rgb值。
            alpha = 150 # 透明度：255 * 60% ≈ 150 （半透明）
            imgMix.putpixel( (w, h), (int( ( pxlPutong[0]- (255-alpha) ) / alpha * 255),
                                      int( ( pxlPutong[1]- (255-alpha) ) / alpha * 255),
                                      int( ( pxlPutong[2]- (255-alpha) ) / alpha * 255),
                                      alpha) )
# 保存图片
imgMix.save("./合成图片.png")
print("生成完毕，快去群里浪吧")



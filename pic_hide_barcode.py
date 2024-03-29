from PIL import Image   # 若提示No module named 'PIL'，则：pip install Pillow
import qrcode
import argparse


def Normal_input(imgPutongPath = "./普通图片.jpg", imgBarcodePath="./二维码.jpg", imgOutputPath = "./合成图片.png"):
    # 打开两张素材图片，其中二维码背景为白色。
    # 注意：为了代码简洁，这两张图的分辨率必需要是相同的。
    imgPutong = Image.open("普通图片.jpg")
    imgBarcode = Image.open("二维码.jpg")

    imgBarcode = imgBarcode.convert("RGBA")

    print(imgPutong)

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




def find_max_subarray(arr, x, y, mode):
    m = len(arr)
    n = len(arr[0])

    # 构建辅助数组用于保存每个位置（i，j）处的子矩阵的和
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 计算辅助数组中每个位置的值
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1] - dp[i - 1][j - 1] + arr[i - 1][j - 1]

    max_sum = float('-inf')
    max_subarray_top_left = None

    if mode == 0:
        # 寻找具有最大总和的子矩阵的左上角值的索引
        for i in range(x, m + 1):
            for j in range(y, n + 1):
                subarray_sum = dp[i][j] - dp[i - x][j] - dp[i][j - y] + dp[i - x][j - y]
                if subarray_sum > max_sum:
                    max_sum = subarray_sum
                    max_subarray_top_left = (i - x, j - y)
    elif mode == 1:
        # 寻找具有最大总和的子矩阵的左上角值的索引
        for i in range(x, m + 1):
            for j in range(y, n + 1):
                subarray_sum = dp[i][j] - dp[i - x][j] - dp[i][j - y] + dp[i - x][j - y]
                if subarray_sum >= max_sum:
                    max_sum = subarray_sum
                    max_subarray_top_left = (i - x, j - y)

    return max_subarray_top_left


def detect_lightest_region(imgPutong, imgBarcode, mode):
    # Initialize variables to store the maximum count of light pixels and the corresponding position
    max_light_count = 0
    lightest_position = None
    THRESHOLD = 180
    arr = [[0 for i in range(imgPutong.width)] for j in range(imgPutong.height)]

    # Iterate over each pixel position in the dimension of imgBarcode
    for w in range(imgPutong.width):
        for h in range(imgPutong.height):
            # Get the pixel value at the corresponding position in imgPutong
            pxlPutong = imgPutong.getpixel((w, h))

            # Check if the pixel is light (white-ish)
            if sum(pxlPutong[:3]) > THRESHOLD * 3:  # Assuming white-ish if the sum of RGB values is greater than 600
                # Increment the count of light pixels
                arr[h][w] = 1


    return find_max_subarray(arr, imgBarcode.width, imgBarcode.height, mode)


def Link_input(link, imgPutongPath = "./普通图片.jpg", imgBarcodePath="./二维码.jpg", anchor_y=None, anchor_x=None, imgOutputPath = "./合成图片.png", mode = 0):
    # 打开两张素材图片，其中二维码背景为白色。
    # 注意：为了代码简洁，这两张图的分辨率必需要是相同的。
    imgPutong = Image.open("普通图片.jpg")
    if imgPutong.height >= 1000:
        qrcode.make(link, box_size=10, border=0).save("二维码.jpg")
    else:
        qrcode.make(link, box_size=5, border=0).save("二维码.jpg")
    imgBarcode = Image.open("二维码.jpg")

    imgBarcode = imgBarcode.convert("RGBA")

    if anchor_x is None or anchor_y is None:
        anchor_y, anchor_x = detect_lightest_region(imgPutong, imgBarcode, mode)

    print(anchor_x, anchor_y)

    print(imgPutong)

    # 创建新图片，使用RGBA模式，方便稍后保存为png。新图的分辨率和普通图相同。
    imgMix = Image.new("RGBA", (imgPutong.width, imgPutong.height) )

    # 填充新图片上的每一个像素
    for w in range(imgMix.width):
        for h in range(imgMix.height):
            pxlPutong = imgPutong.getpixel((w, h))
            if anchor_x <= w < anchor_x + imgBarcode.width and anchor_y <= h < anchor_y + imgBarcode.height:
                pxlBarcode = imgBarcode.getpixel( (w-anchor_x,h-anchor_y) )

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
            else:
                imgMix.putpixel((w, h), (pxlPutong[0], pxlPutong[1], pxlPutong[2], 255))

    # 保存图片
    imgMix.save("./合成图片.png")
    print("生成完毕，快去群里浪吧")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers and comments.')
    parser.add_argument('--link', '-l', type=str, help='Your link')
    parser.add_argument('--imgPutongPath', '-pin', type=str, help='Path of the base picture ex) ./普通图片.jpg')
    parser.add_argument('--imgBarcodePath', '-qrin', type=str, help='Path of the QR code. ex) ./二维码.jpg')
    parser.add_argument('--imgOutputPath', '-pout', type=str, help='Path of the output picture (must end in .png)')
    parser.add_argument('--anchor_x', '-x', type=int, help='QR code anchor position of width')
    parser.add_argument('--anchor_y', '-y', type=int, help='QR code anchor position of height')
    parser.add_argument('--mode', '-mode', type=int, help='QR code position mode, 0 for first position, 1 for last position')

    args = parser.parse_args()

    # Create a dictionary to hold the arguments
    filtered_args = {k: v for k, v in vars(args).items() if v is not None}
    print(filtered_args)

    if 'link' in filtered_args:
        # Handle the case when Link is None
        Link_input(**filtered_args)
    else:
        # Call your function with the filtered arguments
        Normal_input(**filtered_args)

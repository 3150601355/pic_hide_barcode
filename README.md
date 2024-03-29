# pic_hide_barcode
## From original author:

hide barcode in a picture. 在一张普通图片里隐藏二维码，可以被微信识别。这个代码谁都可以用，唯独有一个人不给用，抖X上有个叫“大神开发”的营销号，先后盗了我十几个原创视频，我从未见过如此厚颜无耻之人！

## What is new in this fork:

- Enables the creation of such pictures starting from a base picture and a link, instead of a QR code needed
- Supports more command-line input parameters, including:
  - Input picture path
  - Input QR code path
  - Output picture path
  - link (Only when using link)
  - anchor_x: the x position of your QR code on the picture (Only when using link)
  - anchor_y: the y position of your QR code on the picture (Only when using link)
  - mode: alternative modes in positioning the QR code (Only when using link)

Here are quotes discussing different input methods:

### Quotes about Input Methods:

1. **Using QR code path directly:**  
   ```--imgBarcodePath "path/to/QRcode.jpg"``` or ```-qrin "path/to/QRcode.jpg"```  
   "By providing the path to your QR code image directly, you can seamlessly integrate it into your base picture."

2. **Using a link to generate QR code:**  
   ```--link "your-link-here"``` or ```-l "your-link-here"```  
   "With the ability to generate a QR code from a provided link, you can dynamically incorporate relevant URLs into your images."

3. **Fine-tuning position and mode:**  
   ```--anchor_x x_value``` or ```-x x_value```  
   ```--anchor_y y_value``` or ```-y y_value```  
   ```--mode mode_value``` or ```-mode mode_value```  
   "Adjusting the anchor position and mode allows for precise placement and alignment of the QR code within your image."



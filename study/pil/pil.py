from PIL import Image, ImageFilter


im = Image.open('dpv8lj.jpg')
w, h = im.size
print('Original image size: %sx%s' % (w, h))
# im.thumbnail((w//2, h//2))  # 调整图片大小
# print('Resize image to: %sx%s' % (w//2, h//2))
# im.save('resize.jpg', 'jpeg')

im2 = im.filter(ImageFilter.BLUR)  # 添加滤镜模糊
im2.save('blur.jpg', 'jpeg')

from typing import final
from PIL import Image
from wand import font
from wand.image import Image as WandImage
from wand.font import Font
import json
from amzqr import amzqr
import os


config = json.load(open('config.json'))
font_fix = int(config["font_fix"])
square_color = tuple(config["square_color"])
data = config["data"]
font = config["font"]
bottom_logo_name = config["bottom_logo_name"]
middle_logo_name = config["middle_logo_name"]
qr_file_name = config["qr_name"]


with WandImage() as img:
    img.background_color = 'white'
    img.font = Font(font, 60)  
    img.read(filename='label: SCAN HERE                                                                               SCAN HERE                                                 SCAN HERE                                                ')
    img.virtual_pixel = 'white'
    # 360 degree arc, rotated -90 degrees
    img.distort('arc', (360,-91))
    img.save(filename='text.png')   
    img.format = 'png'



version, level, qr_name = amzqr.run(
    data,
    version=1,
    level='H',
    picture=None,
    colorized=False,
    contrast=1.0,
    brightness=1.0,
    save_name='temp.png',
    save_dir=os.getcwd()
)
qr_img = Image.open(qr_name)
sx, sy = qr_img.size
d = 36   #dopnt dare change this value
qr_img = qr_img.crop((d,d, sx-d, sy-d))
sx, sy = qr_img.size


copy_region = qr_img.crop( ( int(sx/4)*2, 0, int(sy/4)*3, sy ) )
csx, csy = copy_region.size


version, level, qr_name = amzqr.run(
    data,
    version=1,
    level='H',
    picture=middle_logo_name,
    colorized=False,
    contrast=1.0,
    brightness=1.0,
    save_name='temp.png',
    save_dir=os.getcwd()
)
qr_img = Image.open(qr_name)
sx, sy = qr_img.size
qr_img = qr_img.crop((d,d, sx-d, sy-d))
sx, sy = qr_img.size



big_qr_img = Image.new('RGB', (sx*3, sy*3), (255,255,255))
crop_region_w = big_qr_img.size[0] / 6
for ix in range(12):
    for iy in range(3):
        big_qr_img.paste(copy_region, (csx*ix,csy*iy))
big_qr_img.paste(qr_img, (csx*4,csy*1))
big_qr_img = big_qr_img.crop(  ( crop_region_w, crop_region_w, crop_region_w*5, crop_region_w*5 ) )



template = Image.open('template_final.png').resize(big_qr_img.size)
mask = Image.open('template_mask.png')\
    .resize(big_qr_img.size)\
    .convert('L')

final_img = Image.composite(template, big_qr_img, mask)



white = Image.open('white.png')
white = white.resize(final_img.size)
text_color = white.copy()
mask = white.copy()
font_fix = int(final_img.size[0] / font_fix)
mask.paste( Image.open('text.png')\
    .resize( (white.size[0]-font_fix, white.size[1]-font_fix) ), (int(font_fix/2),int(font_fix/2)-5) )
mask = mask.resize(final_img.size)\
    .convert('L')
final_img = Image.composite(final_img, white, mask)



logo = Image.open(bottom_logo_name)
size = (  int(final_img.size[0]/4), int(final_img.size[1]/4) )
logo.thumbnail(size, Image.ANTIALIAS)
final_img.paste( logo, \
    (int(final_img.size[0]/2) - int(logo.size[0]/2), int(final_img.size[1]/8)*7 - int(logo.size[1]/2) ), \
    logo )


final_img.save(qr_file_name)
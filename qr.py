import qrcode
from PIL import Image
from qrcode.image import styledpil
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask, SquareGradiantColorMask
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
divider = config["divider"]
print(config)

with WandImage() as img:
    img.background_color = 'white'
    img.font = Font(font, 60)  
    img.read(filename='label: SCAN HERE                                                                         SCAN HERE                                                     SCAN HERE                                                    ')
    img.virtual_pixel = 'white'
    # 360 degree arc, rotated -90 degrees
    img.distort('arc', (360,-86))
    img.save(filename='text.png')
    img.format = 'png'

# qr = qrcode.QRCode(
#     version=2,
#     error_correction=qrcode.constants.ERROR_CORRECT_M,
#     box_size=20,
#     border=0,
# )
# qr.add_data(data)

version, level, qr_name = amzqr.run(
    data,
    version=1,
    level='H',
    picture=None,
    colorized=False,
    contrast=1.0,
    brightness=1.0,
    save_name='qr.png',
    save_dir=os.getcwd()
)
img_3 = Image.open('qr.png')
sx, sy = img_3.size
d = divider
img_3 = img_3.crop((sx/d, sy/d, sx-(sx/d), sy-(sy/d)))
# img_3 = qr.make_image(fill_color=square_color)
# img_3 = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
sx, sy = img_3.size

copy_region = img_3.crop( ( int(sx/4)*2, 0, int(sy/4)*3, sy ) )
csx, csy = copy_region.size

version, level, qr_name = amzqr.run(
    data,
    version=1,
    level='H',
    picture="starbucks_middle.png",
    colorized=False,
    contrast=1.0,
    brightness=1.0,
    save_name='qr.png',
    save_dir=os.getcwd()
)
img_3 = Image.open('qr.png')
sx, sy = img_3.size
img_3 = img_3.crop((sx/d, sy/d, sx-(sx/d), sy-(sy/d)))
sx, sy = img_3.size

# img_3 = qr.make_image(embedded_image=Image.open("logo_middle.png"), color_mask=SquareGradiantColorMask(square_color), image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())

new_im = Image.new('RGB', (sx*3, sy*3), (255,255,255))
for ix in range(12):
    for iy in range(3):
        new_im.paste(copy_region, (csx*ix,csy*iy))
new_im.paste(img_3, (csx*4,csy*1))
x = new_im.size[0] / 6
new_im = new_im.crop(  ( x, x, x*5, x*5 ) )


template = Image.open('template_final.png')
template = template.resize(new_im.size)
mask = Image.open('template_mask.png')
mask = mask.resize(new_im.size)
mask = mask.convert('L')
new_im = Image.composite(template, new_im, mask)

white = Image.open('white.png')
white = white.resize(new_im.size)
text_color = white.copy()
mask = white.copy()
mask.paste( Image.open('text.png').resize( (white.size[0]-font_fix, white.size[1]-font_fix) ), (int(font_fix/2),int(font_fix/2)) )
mask = mask.resize(new_im.size)
mask = mask.convert('L')
text_color.save("gg.png")
new_im = Image.composite(new_im, white, mask)

logo = Image.open('logo.png')
size = (  int(new_im.size[0]/4), int(new_im.size[1]/4) )
logo.thumbnail(size, Image.ANTIALIAS)
new_im.paste( logo, (int(new_im.size[0]/2) - int(logo.size[0]/2), int(new_im.size[1]/8)*7 - int(logo.size[1]/2) ), logo )

# logo = Image.open('logo_middle.png').convert('L')
# size = (  int(new_im.size[0]/4), int(new_im.size[1]/4) )
# logo.thumbnail(size, Image.ANTIALIAS)
# new_im.paste( logo, (int(new_im.size[0]/2) - int(logo.size[0]/2), int(new_im.size[1]/2) - int(logo.size[1]/2) ), logo )


new_im.save("demo.png")

img_3.paste(  copy_region, (sx, 0) , copy_region  )
img_3.save("qr3.png")
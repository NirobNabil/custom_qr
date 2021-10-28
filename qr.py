import qrcode
from PIL import Image
from qrcode.image import styledpil
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=20,
    border=0,
)
qr.add_data('lots lots lots of data')

img_3 = qr.make_image(fill_color="orange", image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
img_3 = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
sx, sy = img_3.size

copy_region = img_3.crop( ( int(sx/4)*2, 0, int(sy/4)*3, sy ) )
csx, csy = copy_region.size

img_3 = qr.make_image(image_factory=StyledPilImage, embeded_image_path="logo.png", module_drawer=RoundedModuleDrawer())

new_im = Image.new('RGB', (sx*3, sy*3), (255,255,255))
for ix in range(12):
    for iy in range(3):
        new_im.paste(copy_region, (csx*ix,csy*iy))
new_im.paste(img_3, (csx*4,csy*1))
x = new_im.size[0] / 6
new_im = new_im.crop(  ( x, x, x*5, x*5 ) )

template = Image.open('template.png')
template = template.resize(new_im.size)
mask = Image.open('template_mask.png')
mask = mask.resize(new_im.size)
mask = mask.convert('L')

new_im = Image.composite(template, new_im, mask)
new_im.save("temp.png")

img_3.paste(  copy_region, (sx, 0) , copy_region  )
img_3.save("qr3.png")
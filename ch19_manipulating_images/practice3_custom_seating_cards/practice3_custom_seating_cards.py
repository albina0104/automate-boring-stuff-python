# Custom Seating Cards
# Creates custom invitations from a list of guests in a plaintext file -
# generates an image file with the guest name and a flowery decoration.

import os
from PIL import Image, ImageDraw, ImageFont

with open('guests.txt') as file:
    guests_list = file.read().splitlines()

flowery_decoration_img = Image.open('flowery_decoration.png')
img_width, img_height = flowery_decoration_img.size
font_size = 22
fonts_folder = '/usr/share/fonts/truetype/ubuntu'
ubuntu_font = ImageFont.truetype(os.path.join(fonts_folder, 'Ubuntu-B.ttf'), font_size)

os.makedirs('seating_cards', exist_ok=True)

for guest in guests_list:
    img = flowery_decoration_img.copy()
    draw = ImageDraw.Draw(img)
    text_width = draw.textlength(guest, font=ubuntu_font)
    text_height = font_size
    x_coord = int((img_width - text_width) / 2)
    y_coord = int((img_height - text_height) / 2)
    draw.text((x_coord, y_coord), guest, fill='PaleVioletRed', font=ubuntu_font)
    draw.rectangle((0,0, img_width, img_height), fill=None, outline='black', width=10)
    img.save(os.path.join('seating_cards', f'{guest}.png'))

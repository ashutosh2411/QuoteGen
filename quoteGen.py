""" 
 Author; Ashutosh Upadhye @ashutosh2411
"""
import PIL
import csv
import textwrap
import pandas as pd
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

df=pd.read_csv('quotes.csv', sep='\t',header=None)
lines, authors = df.values[1:,1], df.values[1:,0]

for idx, val in enumerate(lines):
    # echo each quote and author
    print(idx, val)
    # create main quote value depending on number of lines in the quote. 
    nLines = len(val.split('\n'))
    if nLines > 1 and nLines < 5:
    	para = val.split('\n')
    else:
	    para = textwrap.wrap(val, width=40)
    # set image dimensions
    MAX_W, MAX_H = 1920, 1280
    imageFile = "template.png"
    im = Image.open(imageFile).convert('RGBA')
    # resize the image
    im = im.resize((1920, 1280), Image.ANTIALIAS)
    # create new layer for adding opacity 
    poly = Image.new('RGBA', (1920,1280))
    
    # paste in the layer on top of the image im
    im.paste(poly,mask=poly)
    # command to start merging layers 
    draw = ImageDraw.Draw(im)
    # setting up fonts
    font = ImageFont.truetype("fonts/BLKCHCRY.TTF",80)
    authorfont = ImageFont.truetype("fonts/BLKCHCRY.TTF",60)
    linkfont = ImageFont.truetype("fonts/BLKCHCRY.TTF",24)
    # setting up padding and positioning for quote text
    current_h, pad = 300, 50
    # for loop breaking up each quote into lines not exceeding the width of the image dimensions  
    for line in para:
        line = line.replace("\xe2\x80\x9c",'"').replace("\xe2\x80\x99","'").replace("\xe2\x80\x9d",'"')
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font, fill=(0,0,0,255))
        current_h += h + pad
    # setting up padding and positioning for author text
    current_h2, pad2 = 900, 80
    currentauthor = authors[idx]
    w, h = draw.textsize(currentauthor, font=authorfont)
    draw.text(((MAX_W - w) / 2, (current_h + 100)), currentauthor, font=authorfont, fill=(0,0,0,255))
    current_h2 += h + pad2
    # setting up padding and positining for optional text
    current_h3, pad3 = 1200, 30
    sitelink = "Akshar, Literary Arts Society, IIT Palakkad"
    w, h = draw.textsize(sitelink, font=linkfont)
    draw.text(((MAX_W - w) / 2, current_h3), sitelink, font=linkfont,fill=(0,0,0,255))
    current_h3 += h + pad3
    
    # loading optional logo and converting to RGBA for transparency support
    logo = Image.open('logo.png').convert('RGBA')
    logo = logo.resize((100, (100*1280)/1920), Image.ANTIALIAS)
    logo_w, logo_h = logo.size
    im.paste(logo, (0,1280-logo_h), logo)
    # saving the image to our chosen location
    im.save("out/image_%d.png" %idx)

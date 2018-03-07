#!/usr/local/bin/python
# -*- coding: utf-8 -*-
##
 #  @filename   :   main.cpp
 #  @brief      :   2.7inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     August 16 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd2in7
import Image
import ImageFont
import ImageDraw
import time
import requests
import requests_cache
import sys  
import urllib, json

reload(sys)  
sys.setdefaultencoding('utf-8')

def main():

        display_Charts()
        wait=60
        refresh_time=225
        start_time=time.time()+refresh_time

        while True:
            print('restart  : current time ' + str(time.time()/60) + ' started time ' +str(start_time/60))
   
            if (time.time()-start_time)>0:
                start_time=time.time()+refresh_time # rest refresh time
                display_Charts()

            time.sleep(wait)


def display_Charts():
    epd = epd2in7.EPD()
    epd.init()
    #epd.rotate(3) # Rotate the Display by 270 degree 
    from coinmarketcap import Market
    coinmarketcap = Market()
    CurrencyData=coinmarketcap.ticker(start=0, limit=5, convert='EUR')
    LINEHEIGHT=20
    price=0
    currency_symbol='€'

    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), 255)    # 255: clear the image with white
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 12)
    font_table_title = ImageFont.truetype('fonts/Grand9KPixel.ttf', 10)
    font_titles = ImageFont.truetype('fonts/slkscr.ttf', 16)
    font_num = ImageFont.truetype('fonts/PixelSplitter-Bold.ttf', 14)
    font_date = ImageFont.truetype('fonts/PixelSplitter-Bold.ttf',12)

    draw.rectangle((0, 0, 264, 28), fill = 0);
    draw.rectangle((0, 160, 264, 176), fill = 0);
    draw.rectangle((0, 28, 264, 50), fill = 0);
    draw.text((2, 8)," Cryptocurrency Market ",  font = font_titles,  fill = 255)
    draw.text((5, 32), "NAME          PRICE                           CHANGE(24h)",font =font_table_title,  fill = 255)
    for item in CurrencyData:
        #price=round(float(),4)
        draw.text((5,40+LINEHEIGHT),item['symbol'],font =font_titles,fill = 0)
        draw.text((60,40+LINEHEIGHT),"€"+item['price_eur'],font =font_num,fill = 0)
        draw.text((200,40+LINEHEIGHT),item['percent_change_24h']+"%",font =font_num,fill = 0)
        LINEHEIGHT+=20
    
    draw.text((0,160),str(" UPDATED ON:"+time.strftime("%c")),font =font_date,fill = 255)

    epd.display_frame(epd.get_frame_buffer(image))

if __name__ == '__main__':
    main()

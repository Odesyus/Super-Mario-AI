from PIL import Image, ImageChops
import os

def BlokMapping(input, height, width, Blocks):
    Txt = open('./Maps/LevelMap.txt','w')
    im = Image.open(input) #Resmin alınması
    k = 0
    x = 0
    Samples = []
    for sample in Blocks: 
        Samples.append(Image.open(sample)) #Örnek resimlerin "resim" olarak diziye alınması
    imgwidth, imgheight = im.size
    for i in range(0,imgheight, height):
        for j in range(0,imgwidth, width):
            box = (j, i, j+width, i+height) #Büyük resmi küçük parçalara ayırma
            a = im.crop(box)
            """a.save(os.path.join('./Test',"IMG-%s.png" % k))
            k += 1"""
            for Samp in Samples: 
                test = ImageChops.difference(a,Samp) 
                if test.getbbox() == None:
                    if Samp == Samples[0]:
                        x = 2 
                    elif Samp == Samples[1]:
                        x = 3
                    elif Samp == Samples[2]:
                        x = 4
                    elif Samp == Samples[3]:
                        x = 5
                    else:
                        x = 1
            if x == 1 or x == 2 or x == 3 or x == 4 or x == 5 :
                Txt.write(str(x))
                x = 0
            else:
                Txt.write("0")
Blocks = ['./Maps/Block (1).png','./Maps/Block (2).png','./Maps/Block (3).png','./Maps/Block (4).png','./Maps/Block (5).png',
'./Maps/Block (6).png','./Maps/Block (7).png','./Maps/Block (8).png','./Maps/Block (9).png','./Maps/Block (10).png'] #Örnek resimler
BlokMapping('./Maps/BG.png', 32, 32, Blocks)



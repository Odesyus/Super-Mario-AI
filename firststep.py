import pygame
import numpy as np
import random
import os

pygame.init()

font = pygame.font.Font('Sprites\Super Mario Bros.ttf', 20)
loop1 = True
Blocks = []
ListMario = []
DeadMario = []
ListGumba = []
framerate = 30
maxsize_x = 1536
maxsize_y = 416 
acc = 0.3
maxacc = 5
gravacc = 0.5
scroll = 0
screenx = [maxsize_x, 0]
x = 0
Generation = 0
Evolution = 0
Highscore = 0
MaxHighScore = []
MaxHighScore.insert(0, 0)
NextGeneration = []
loop = []
Mode = False
timer = 0

testD = input("\n\n\nPrograma hosgeldiniz... \n"
"Evet maalesef ki zamanin yetismemesinden dolayi bu kismini konsoldan yapmak zorunda kaldim. (uzgunum...)\n"
"Simdi asil meseleye gelelim bu program ne ise yariyor \n"
"En kisa aciklamasiyla ekranda bir cok Mario nun kendi kendine oynadigi bir Super Mario Bros. \n"
"Sizin belirlediginiz sayida Mario belirledigiz ve yine sizin belirlediginiz sayida ekranda gelerek bolumu bitirmeye calisiyor\n"
"Misal 20 Marioluk bir deney yapmak istiyorsunuz isterseniz ekranda tek seferde 4 Mario ile 5 defada da yapabilirsiniz\n"
"isterseniz 20 Marioyu tek seferde sizin bilgisayarinizin gucune bagli\n\n"
"----------------------------------------------------------------------------------------\n\n"
"Simdi ilk soru bilgisayariniz ne kadar guclu yani tek seferde kac Mario ekranda olsun ?   ")

while True:
    try:
        D = int(testD)
        os.system('cls' if os.name=='nt' else 'clear')
        break
    except:
        testD = input("\n\nLutfen sayi giriniz...")

testM = input('Peki tek nesilde kac Mario olsun ?   ')

while True:
    try:
        M = int(testM)
        os.system('cls' if os.name=='nt' else 'clear')
        break
    except:
        testM = input("Lutfen sayi giriniz...")

T = input('Son soru Yapay zeka olsun mu \n \n Evet ? Hayir?   ') 

while True:
    try:
        if T == 'Evet' or T == 'evet':
            Mode = False
        elif T == 'Hayir' or T == 'hayir':
            Mode = True
        os.system('cls' if os.name=='nt' else 'clear')
        break
    except:
        T = input('Lutfen Evet veya Hayir giriniz...')

MaxM = M

win = pygame.display.set_mode((maxsize_x, maxsize_y))

pygame.display.set_caption('First Step')

clock = pygame.time.Clock()

#Projenin en onemli kisimlarindan biri olan YAPAY ZEKA kismi tum Mariolarin sahip oldugu beyinleri 
class Brain(object): 
    def __init__(self, value1, value2, value3, weight1, weight2):
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        self.weight1 = weight1
        self.weight2 = weight2
    # Bunu tam olarak aciklamasini bilmiyorum ama yaptigim arastirmalarda yapay zeka icin en mukemmel fonksiyon olarak kabul ediliyor
    # Ben de bunu kullanayim dedim amam benim icin de islemin bu kismi buyu gibi geliyor
    def sigmoid(self, x, deriv = False): 
        if deriv == True:              
            return x * (1-x)
        return 1 / (1 + np.exp(-x))
    # Burda en kisa haliyle Marionun aldigi degerler ve basta aldigi genler (agirliklar) sigmoid fonksiyonuna sokulup sonunda 2 deger elde ediliyor
    def predict(self): 
        self.Data = np.array([self.value1, self.value2, self.value3])# bu 2 degerden birisi Mario nun ilerleyip ilerlemiyecegini 
        self.layer1 = self.sigmoid(np.dot(self.Data, self.weight1))# digeri de ziplayip ziplamiyacagini belirliyor
        self.layer2 = self.sigmoid(np.dot(self.layer1, self.weight2))
        return self.layer2

# Iste asil kahramanimiz Mario en ici en karsik olan class ama cok bariz olan seyler harici herseyi acikladim
class Mario (object):
    def __init__(self, x, y, width, height, weight1, weight2, color):
        self.offset = 5
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.RAcc = 0
        self.LAcc = 0
        self.MaxJump = 6
        self.Coll = {'Up': False, 'Down': False, 'Left': False, 'Right': False}
        self.Gravity = self.MaxJump
        self.Falling = False
        self.canJump = True
        self.IsJumping = False 
        self.onBlock = True #Mario nun zeminde olup olmadigini kontol eden degisken
        self.Slide = 'None' #Donuslerde yavaslarken ki sprite icin yaptigim degisken
        self.WalkCount = 0 #Sprite dongusunu olusturmak icin her adimda arttirdigim bir degisken
        self.RightLeft = True #Mario nun hangi yone baktigini belirlemek icin kullandigim degisken
        self.MarioStand = True #Mario haraket edip etmedigini belirlemek icin kullandigim degisken
        self.Mhitbox = (round(self.x), round(self.y), self.width, self.height) #Mario nun kendi hitboxu
        self.Phitbox = (round(self.x), round(self.y+72), 32, 1) #Mario nun Blockda oldugunu kontrol etmek icin hitbox
        self.color = color # Her Marionun kendine ozel olmasini istedim bu yuzden kullanici taminli olmayan tamamen rastegele bir renk degsikeni yaptim oyundaki Mario nun etrafindaki kutusarin renklerini belirlemek icin
        self.weight1 = weight1 # iste bunlar Marionun genleri ilk nesil icin rastgele veriyorum degerleri ama sonraki nesillerde 
        self.weight2 = weight2
        self.value1 = 0 # Bunlar da dis cevreden aldigi degerler ilk deger en yakinindaki blok ile Mario arasindaki uzaklik icin
        self.value2 = 0.1 # 2.si en yakindaki Gumba ile arasindaki mesafe icin 
        self.value3 = 0.1 # 3.su en yakindaki bosluk ile Mario arasindaki uzaklik icin degerler
        self.Brain = Brain(self.value1, self.value2, self.value3, self.weight1, self.weight2)
        self.afktime = 0 # Ilk nesil Mariolar genelde baslangic noktasinda duruyorlar veya bi yere takiliyorlar bu deger ne kadar zaman takildiklarini belirlemek icin
        self.time = 0 # Mariolar daha hizli gitsin diye zaman ekledim en sonda Marionun toplam skorundan cikariyorum
        self.score = 0  # Bu da yine yapay zeka icin onemli olan fitness degeri aslinda Mario nun ne kadar "saglikli" oldugunu belirlemek icib
        self.NBHeight = 0 # Value 2 yi bulmak icin gereken ara deger

    def Update(self):
        # Value degerleri her saniye degistigi icin her saniye tekrar tekrar atamam lazim
        self.Brain.value1 = self.value1
        self.Brain.value2 = self.value2
        self.Brain.value3 = self.value3
    # Bu da tum classlarda olan Sprite fonksiyonu isminden de anlasildigi gibi spritelari ekrana yazdiriyor
    # Arada bazi farkli fonksiyonlar da koydum her karede calismasi gereken bazi fonksiyonlar var hepsi ayri ayri olmasin diye buraya koydum
    def Sprites(self, win):
        # Eger bir Mario bir zaman (3 saniye) hareketsiz kalirsa veya haraket edemezse afktime artiyor ve Mario oluyor
        if self.RAcc >= 4:
            self.afktime = 0 
        else:
            self.afktime += 1
        self.score += int(self.RAcc*50) # Sag gittigi surece skoru artiyor
        if self.IsJumping: # cok ziplayan Mariolari cezalandirmak icin skorlarini azaltiyorum
            self.score -= 5 * self.afktime
        self.time += 1
        # Bu spritelarin hepsini ana sprite paketinden tek tek kesip sonrasinda 
        # Goruntusunu bozmadan upscale etmek zorunda kaldim cok eglenceli degildi:(
        WalkRightSp = pygame.image.load('Sprites\WalkRightSp1.png'), pygame.image.load('Sprites\WalkRightSp2.png'), pygame.image.load('Sprites\WalkRightSp3.png')
        WalkLeftSp = pygame.image.load('Sprites\WalkLeftSp1.png'), pygame.image.load('Sprites\WalkLeftSp2.png'), pygame.image.load('Sprites\WalkLeftSp3.png')
        MarioStandR = pygame.image.load('Sprites\MarioStandR.png')
        MarioStandL = pygame.image.load('Sprites\MarioStandL.png')
        MarioJumpSp = pygame.image.load('Sprites\MarioJumpRight.png'), pygame.image.load('Sprites\MarioJumpLeft.png')
        MarioSlide = pygame.image.load('Sprites\MarioSlideR.png'), pygame.image.load('Sprites\MarioSlideL.png') 
        
        # Yavas yavas daha karmasik yerlere geliyoruz burasi spritelarin hangi sirayla hangi sekilde 
        if self.WalkCount + 1 >= 12: #Yuruyus sprite dongusunu saglamak icin yaptigim kucuk bir degisken 
            self.WalkCount = 0
        if (self.IsJumping or self.Falling) and not self.onBlock:
            if self.RightLeft:
                win.blit(MarioJumpSp[0], (round(self.x), round(self.y)))
            else:
                win.blit(MarioJumpSp[1], (round(self.x), round(self.y)))
        else:
            if self.MarioStand:
                if self.RightLeft:
                    win.blit(MarioStandR, (round(self.x), round(self.y)))
                else:
                    win.blit(MarioStandL, (round(self.x), round(self.y)))
            else:
                if self.Slide == 'Right':
                    win.blit(MarioSlide[0], (round(self.x), round(self.y)))
                elif self.Slide == 'Left':
                        win.blit(MarioSlide[1], (round(self.x), round(self.y)))
                else:
                    if self.RightLeft:
                        win.blit(WalkRightSp [self.WalkCount//4], (round(self.x), round(self.y)))
                        self.WalkCount += 1
                    else:
                        win.blit(WalkLeftSp [self.WalkCount//4], (round(self.x), round(self.y)))
                        self.WalkCount += 1

        self.Mhitbox = (round(self.x), round(self.y), self.width, self.height)
        self.Phitbox = (round(self.x), round(self.y+64), 32, 1)
        '''pygame.draw.rect(win, self.color, pygame.Rect(round(self.x), round(self.y+(self.height/2)), 512, 4), 2)'''
        pygame.draw.rect(win, self.color, self.Mhitbox, 4)
    def Rect(self):
        return pygame.Rect(self.Phitbox)
    def MRect(self):
        return pygame.Rect(self.Mhitbox)

# Bu da kucuk mantar kafali canavarimiz Gumba Mario dan cok fazla farkli ozelligi yok aslinda
class Gumba (object):
    def __init__(self, x, y, width, height, begin, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.begin = begin
        self.end = end
        self.path = [self.end, self.begin] 
        self.WalkCount = 0
        self.vel = 2
        self.death = False
        self.hitbox = (self.x, self.y, self.width, self.height)

    def Rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)
        
    def draw(self, win):

        GumbaSprite = pygame.image.load('Sprites\GumbaSprite1.png'), pygame.image.load('Sprites\GumbaSprite2.png')

        self.move()
        if not self.death:
            if self.WalkCount + 1 >= 8:
                self.WalkCount = 0    
            win.blit(GumbaSprite[self.WalkCount//4], (round(self.x), round(self.y)))
            self.WalkCount += 1
            self.hitbox = (round(self.x), self.y, 32, 32)
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.WalkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.WalkCount = 0
        if self.death:
            self.x = 0
            self.y = 0

# Burda farkli olarak bloktype degiskeni var o da adi ustunde ne tur blok oldugunu tutuyor
class Block (object):
    def __init__(self, x, y, width, height, blocktype):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.blocktype = blocktype
        self.rect = self.x, self.y, self.width, self.height
    def draw (self, win, timer):
        self.rect = self.x, self.y, self.width, self.height
        # pygame.draw.rect(win, (255,255,255), self.rect, 1)
        if self.blocktype == 2 or self.blocktype == 3 or self.blocktype == 4:
            BlockSprite = pygame.image.load('Sprites\BlockSprite1.png')
            win.blit(BlockSprite, (round(self.x), round(self.y)))
        elif self.blocktype == 5:
            BlockSprite = pygame.image.load('Sprites\BlockSprite2.png'), pygame.image.load('Sprites\BlockSprite2 - 2.png'), pygame.image.load('Sprites\BlockSprite2 - 3.png'), pygame.image.load('Sprites\BlockSprite2 - 2.png'), pygame.image.load('Sprites\BlockSprite2.png')
            win.blit(BlockSprite[timer//5], (round(self.x), round(self.y)))
        elif self.blocktype == 6:
            BlockSprite = pygame.image.load('Sprites\BlockSprite3.png')
            win.blit(BlockSprite, (round(self.x), round(self.y)))
        else:
            pass
    def Rect(self):
        self.rect = round(self.x), round(self.y), self.width, self.height
        return pygame.Rect(self.rect)

# Mariolarin olusturulma fonksiyonu evet bir suru random degisken aliyor iste isin guzel kismi da bu bazen bu random degiskenler sayesinde tek seferde oyunu bitiredebiliyor 
if M < D: # Sacma sacma yerinde ziplayadabiliyor
    for i in range(0, M):
        ListMario.append(Mario(5, 320, 32, 64, np.random.uniform(-1, 1, (3, 7)), np.random.uniform(-1, 1, (7, 2)), ((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))))
    Generation += 1
    M = 0
else:
    for i in range(0, D):
        ListMario.append(Mario(5, 320, 32, 64, np.random.uniform(-1, 1, (3, 7)), np.random.uniform(-1, 1, (7, 2)), ((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))))
    Generation += 1
    M -= D

# Koda ile ilgili en guru duymadigim yer burasi her halde cok gereksiz kalabalik ama Gumbalar da ilk olarak burda ekrana geliyor
ListGumba.append(Gumba(850, 352, 32, 32, maxsize_x, 0))
ListGumba.append(Gumba(1350, 352, 32, 32, maxsize_x, 0))
ListGumba.append(Gumba(3132, 352, 32, 32, maxsize_x, 0))
ListGumba.append(Gumba(5380, 352, 32, 32, maxsize_x, 0))
ListGumba.append(Gumba(5640, 352, 32, 32, maxsize_x, 0))

# Maps klasorundeki .txt belgesini cekmek icin fonksiyonum
def ArrayCon():
    string = open ('Maps\LevelMap.txt', 'r').read()
    array = [] 
    array[:0] = string 
    lenarr = len(array)
    arr = np.array(array)
    newarr = arr.reshape(int(maxsize_y/32), int(lenarr/int(maxsize_y/32)))
    return newarr

# Bu da ayri bir program ile aldigim level mapindeki blok verileri blok nesnelerine donusturen fonksiyon 
for i in range(0, maxsize_y, 32):
    for j in range(0, 6784, 32):
        temp = ArrayCon()[(int(i/32)), (int(j/32))]
        if temp == '1':
            Blocks.append(Block((j), i, 32, 32, 1))
        elif temp == '2':
            Blocks.append(Block((j), i, 32, 32, 2))
        elif temp == '3':
            Blocks.append(Block((j), i, 32, 32, 3))
        elif temp == '4':
            Blocks.append(Block((j), i, 32, 32, 4))
        elif temp == '5':
            Blocks.append(Block((j), i, 32, 32, 5))
        else:
            pass

# Geriye gidip de haritadan dusmemek icin yaptigim Duvar
Blocks.append(Block(-10, 0, 15, 416, 50))

# Ekranin ustundeki yazi icin fonksiyon
def text_objects(font):
    textSurface = font.render(str(Generation)+'.Jenerasyon '+str(Evolution)+'. Evrim Kalan Mario: '+str(M + len(ListMario))+' Suanki En Yuksek Skor '+str(Highscore)+' Bu Neslin En Yusek Skoru '+str(MaxHighScore[Evolution]), True, (0,0,0),(255,255,255))
    return textSurface, textSurface.get_rect()

# Ekrandaki tum Mariolar oldugunde tum ayarlari sifirlayan ve yeni Jenerasyonu hazirlayan fonksiyon
def restart(ListMario, M, Generation, D):
    Blocks = []
    ListGumba = []
    if M < D:
        for i in range(0, M):
            ListMario.append(Mario(5, 320, 32, 64, np.random.uniform(-1, 1, (3, 7)), np.random.uniform(-1, 1, (7, 2)), ((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))))
        Generation += 1
        M = 0
    else:
        for j in range(0, D):
            ListMario.append(Mario(5, 320, 32, 64, np.random.uniform(-1, 1, (3, 7)), np.random.uniform(-1, 1, (7, 2)), ((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))))
        Generation += 1
        M -= D
    for Marios in ListMario:
        Marios.afktime = 0
        Marios.score = 0
    for i in range(0, maxsize_y, 32):
        for j in range(0, 6784, 32):
            temp = ArrayCon()[(int(i/32)), (int(j/32))]
            if temp == '1':
                Blocks.append(Block((j), i, 32, 32, 1))
            elif temp == '2':
                Blocks.append(Block((j), i, 32, 32, 2))
            elif temp == '3':
                Blocks.append(Block((j), i, 32, 32, 3))
            elif temp == '4':
                Blocks.append(Block((j), i, 32, 32, 4))
            elif temp == '5':
                Blocks.append(Block((j), i, 32, 32, 5))
            else:
                pass

    ListGumba.append(Gumba(850, 352, 32, 32, maxsize_x, 0))
    ListGumba.append(Gumba(1350, 352, 32, 32, maxsize_x, 0))
    
    
    ListGumba.append(Gumba(3132, 352, 32, 32, maxsize_x, 0))
    ListGumba.append(Gumba(5380, 352, 32, 32, maxsize_x, 0))
    ListGumba.append(Gumba(5640, 352, 32, 32, maxsize_x, 0))
    return M, Generation, Blocks, ListGumba

# simdi en oneli kisma geldik crossbreed veya crossover fonkiyonu bunu bolum bolum aciklayacagim
def crossbreed(DeadMario, MaxM):
    # Bu kisim olu Mariolari degerlendirdigim kisim basta hepsini skoruna gore kucuktan buyuge dogru siraliyorum 
    # Sonra bu listenin en iyi kismini yeni nesil uretmek icin aliyorum 
    DeadMario = sorted(DeadMario, key = lambda DeadMario: DeadMario.score)
    NextGen = []
    last_best = int((MaxM-1)*0.80)
    Bests = DeadMario[last_best:]
    for Mem in NextGen:
        Mem.x = 5 
        Mem.y = 320
        Mem.score = 0
        Mem.time = 0
        Mem.afktime = 0
    DeadMario.clear()
    # Burada da yeni nesil uretme basliyor kullancini belirledigi sayiya ulasana kadar yeni nesiller uretilmeye devam ediyor
    while True:
        if len(NextGen) < MaxM:
            # Daha deminki aldigimiz en iyi nesilden en en iyisini ve rasgele bi tanesini seciyoruz ve bunun genlerini aliyoruz
            member1 = Bests[len(Bests) - 1]
            member2 = random.choice(Bests)

            member1_weight1 = member1.weight1
            member1_weight2 = member1.weight2

            member2_weight1 = member2.weight1
            member2_weight2 = member2.weight2

            newmember_weight1 = []
            newmember_weight2 = []
            newmember_color = (0, 0, 0)
            color1 = (0, 0, 0)
            color2 = (0, 0, 0)
            newcolor = (0, 0, 0)
            # Sonra bu genleri rastgele olarak dagtiyoruz ve kucuk bir mutasyon ihtimali olmasini da unutmuyoruz
            for a, b in zip(member1_weight1, member2_weight1):
                for c, d in zip(a, b):
                    prob = random.random()
                    if prob < 0.40:
                        color1 = member1.color
                        newmember_weight1.append(c)
                    elif prob < 0.80:
                        color1 = member2.color
                        newmember_weight1.append(d)
                    else:
                        color1 = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                        newmember_weight1.append(np.random.uniform(1, -1))

            for i, j in zip(member1_weight2, member2_weight2):
                for k, l in zip(i, j):
                    prob = random.random()
                    if prob < 0.40:
                        color2 = member1.color
                        newmember_weight2.append(k)
                    elif prob < 0.80:
                        color2 = member2.color
                        newmember_weight2.append(l)
                    else:
                        color2 = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                        newmember_weight2.append(np.random.uniform(1, -1))
            
            newmember_weight1 = np.array(newmember_weight1).reshape(3, 7)
            newmember_weight2 = np.array(newmember_weight2).reshape(7, 2)
            newcolor = (((color1[0]+color2[0])/2), ((color1[1]+color2[1])/2), ((color1[0]+color2[2])/2))
            # Yeni olusacak bireyin kutusunun rengi ata nesillerden gelmesini sagliyorum ayni zamanda
            NextGen.append(Mario(5, 320, 32, 64, newmember_weight1, newmember_weight2, newcolor))
        else:
            break
        # Son olarak yeni nesili test icin tekrardan ana donguye atiyorum
    return NextGen, DeadMario

# Mario her ilerlediginde ekranin sola gitmesi gerek bu fonksiyon da onu sagliyor iste
def BlockUpdate(Mario, Blocks, Gumba, scroll):
    for Mario in Mario:
        Mario.x -= scroll
    for Block in Blocks:
        Block.x -= scroll
    for Gumba in Gumba:
        Gumba.x -= scroll
        Gumba.path[1] += scroll
        Gumba.path[0] -= scroll

# Evet en karisik fonksiyona geldik en basit aciklamasiyla Marionun bir sonraki konumunda erkranda bloklarla 
# Nasil etkilesime girdigini inceleyen fonksiyon ve bunun disinda Mario.value degerlerini de aldigi fonksiyon
# suan hala cok fazla hata var bu fonksiyonda ama en "calisabilir" hali bu simdilik
def BlockCollide(Mario, Blocks, ListGumba, screenx):
    for Mario in Mario:
        temp = {0:False, 1:True, 2:False, 3:False, 4:False, 5:False, 6:1500, 7:416, 8:-1}
        for Block in Blocks:
            if screenx[1] < Block.x <= screenx[0]:
                temp[0] = Mario.Rect().colliderect(Block.Rect()) or temp[0]
                for Gumba in ListGumba:
                    if screenx[1] < Gumba.x <= screenx[0]:
                        if  Gumba.Rect().colliderect(Block.Rect()):
                            if Block.x < Gumba.x:
                                Gumba.path[0] = Block.x + 32
                            elif Block.x > Gumba.x:
                                Gumba.path[1] = Block.x - 32
                        if pygame.Rect(round(Mario.x), round(Mario.y+(Mario.height/2)), 512, 4).colliderect(Gumba.Rect()):
                            Mario.value2 = Gumba.x - Mario.x
                if Mario.x-64 < Block.x < Mario.x+96:
                    temp[2] = pygame.Rect(round(Mario.x + Mario.RAcc), round(Mario.y), Mario.width, Mario.height).colliderect(Block.Rect()) or temp[2]
                    temp[3] = pygame.Rect(round(Mario.x - Mario.LAcc), round(Mario.y), Mario.width, Mario.height).colliderect(Block.Rect()) or temp[3]
                    temp[4] = pygame.Rect(round(Mario.x), round(Mario.y + Mario.Gravity ** 2), Mario.width, Mario.height).colliderect(Block.Rect()) or temp[4]
                    if Mario.IsJumping and (Mario.x < Block.x < Mario.x + Mario.width or Mario.x < Block.x + Block.width < Mario.x + Mario.width):
                        temp[5] = pygame.Rect(round(Mario.x), round(Mario.y - Mario.Gravity ** 2), Mario.width, Mario.height).colliderect(Block.Rect()) or temp[5]
                    if pygame.Rect(round(Mario.x), round(Mario.y+Mario.height), 512, 4).colliderect(Block.Rect()):
                        if Block.x < temp[6]:
                            temp[6] = Block.x - Mario.x
                            Mario.value1 = temp[6]
                        while temp[1] == True:
                            for Block in Blocks:
                                if Block.y == 384:
                                    if temp[8] + 32 == Block.x:
                                        temp[8] = Block.x
                                    else:
                                        Mario.value3 = temp[8] - Mario.x
                                        temp[1] = False
                                    if pygame.Rect(round(Mario.x), 384, 32, 32).colliderect(Block.Rect()):
                                        temp[8] = Block.x
                    if Mario.Falling:
                        if pygame.Rect(round(Mario.x), round(Mario.y + (Mario.Gravity ** 2)), Mario.width, Mario.height).colliderect(Block.Rect()):
                            Mario.y = Block.y - Mario.height
                            
                    if Mario.IsJumping:
                        if pygame.Rect(round(Mario.x), round(Mario.y - Mario.Gravity ** 2), Mario.width, Mario.height).colliderect(Block.Rect()):
                            Mario.y = Block.y + Block.height
                            if Block.blocktype == 5:
                                Block.blocktype = 6
                            elif Block.blocktype == 2 or Block.blocktype == 3 or Block.blocktype == 4:
                                Blocks.remove(Block)
        if temp[0]:
            Mario.onBlock = True
            Mario.Gravity = Mario.MaxJump
        else:
            Mario.onBlock = False
        if temp[2]:
            Mario.Coll['Right'] = True
        else:
            Mario.Coll['Right'] = False
        if temp[3]:
            Mario.Coll['Left'] = True
        else:
            Mario.Coll['Left'] = False
        if temp[4]:
            Mario.Coll['Down'] = True
        else:
            Mario.Coll['Down'] = False
        if temp[5]:
            Mario.Coll['Up'] = True
        else:
            Mario.Coll['Up'] = False

# Bu haraket fonksiyonu her halde mukemmele en yakin yazdigim fonksiyon aslinda cok bir sey yok Marioyu belli arakliklarla isinliyor en kisa haliyle
def Moving (Mario, keys, massacc, acc, Blocks): 
    for Mario in Mario:# Mode degiskeni burda devreye giriyor iste hangi oyun modunda bulundugumuzu anlamai icin
        if (keys[pygame.K_d] and Mode) or ((float(Mario.Brain.predict()[0]) < float(0.5) and not Mode) ):
            if not keys[pygame.K_a]:
                if (Mario.LAcc > 0): #En sevdigim kisimlardan birisi normal Mario oyununda oldugu gibi Mario direk durmuyor basta biraz ayagi kayiyor sonra durup diger tarafa haraket ediyor
                    Mario.LAcc -= acc
                    if Mario.Coll['Left']:
                        Mario.x += 2
                        Mario.LAcc = 0
                    else:
                        Mario.x -= Mario.LAcc 
                        Mario.Slide = 'Right'
                else:
                    Mario.Slide = 'None'
                    Mario.RightLeft = True
                    Mario.MarioStand = False
                    if Mario.x < (maxsize_x-(Mario.width+Mario.RAcc)):
                        if Mario.Coll['Right']:
                            Mario.x -= 2
                            Mario.RAcc = 0
                        else:
                            Mario.x += Mario.RAcc
                            if(Mario.RAcc < maxacc):
                                Mario.RAcc += acc

        elif keys[pygame.K_a]:
            if not keys[pygame.K_d]:
                if (Mario.RAcc > 0):
                    Mario.RAcc -= acc
                    if Mario.Coll['Right']:
                        Mario.x -= 2
                        Mario.RAcc = 0
                    else:
                        Mario.x += Mario.RAcc
                        Mario.Slide = 'Left'
                else:
                    Mario.Slide = 'None'
                    Mario.RightLeft = False
                    Mario.MarioStand = False
                    if Mario.Coll['Left']:
                        Mario.x += 2
                        Mario.LAcc = 0
                    else:
                        Mario.x -= Mario.LAcc 
                        if(Mario.LAcc  < maxacc):
                            Mario.LAcc += acc

            
        elif keys[pygame.K_a] & keys[pygame.K_d]:
            Mario.MarioStand = True
            Mario.LAcc = 0
            Mario.RAcc = 0
        else:
            Mario.MarioStand = True
            Mario.WalkCount = 0
            Mario.LAcc = 0
            Mario.RAcc = 0

# Mantikta Moving ile ayni bu sefer y kordinati ama ele alinmasi gereken daha fazla degisken var biraz daha karisik o yuzden
def Jumping(Mario, keys, Blocks):
    for Mario in Mario: 
        if keys[pygame.K_SPACE] and Mode or (float(Mario.Brain.predict()[1]) > float(0.68) and not Mode ):
            if Mario.onBlock:
                Mario.onBlock = False
                Mario.Gravity = 6
                Mario.IsJumping = True
        if Mario.IsJumping:
            if Mario.Gravity > 0:
                if Mario.Coll['Up']:
                    Mario.Gravity = 0
                else:
                    Mario.y -= Mario.Gravity ** 2
                    Mario.IsJumping = True
                    Mario.Gravity -= gravacc
            if Mario.Gravity == 0:
                Mario.canJump = False
                Mario.IsJumping = False
                Mario.onBlock = False

# Tam anlamiyla Jummping fonksiyonun tersi 
def Gravity(Mario, Blocks):
    for Mario in Mario:
        if Mario.onBlock:
            Mario.Gravity = 0
            Mario.Falling = False
        else: # Eger yoksa Mario ya yer cekimi uygula
            if Mario.IsJumping == False:
                Mario.Falling = True
                if Mario.Gravity == Mario.MaxJump:
                    Mario.Gravity = 6
                if Mario.Coll['Down'] and Mario.Falling:
                    Mario.Gravity = 0
                else:
                    if not Mario.Gravity == Mario.MaxJump:
                        Mario.Gravity += gravacc
                    Mario.y += Mario.Gravity ** 2

# Mario nun "saldiri" fonksiyonu eger Mario dusuyorsa x konumu Gumba ile ayni ise ve Mario ile dikdortgenleri birlesiyorsa Gumba oluyor Mario 1000 skor aliyor degilse Mario oluyor # 
# Aslinda aklimda daha cok dusman yapmak vardi ama sonra vazgectim
def Smash (Marios, ListEnemies, DeadMario):
    for Mario in Marios:
        for Enemies in ListEnemies:
            if Mario.MRect().colliderect(Enemies.Rect()):
                if Mario.Falling:
                    Enemies.death = True
                    Mario.IsJumping = True
                    Mario.Gravity = 3
                    Mario.Smash = True
                    Mario.score += 1000
                else:
                    DeadMario.append(Mario)
                    Marios.remove(Mario)

# Ekran cizimlerinin yapildigi fonksiyon
def redraw(Mario, x, ListGumba, screenx):
    BgSp = pygame.image.load('Sprites\BG.png')
    TextSurf, TextRect = text_objects(font)
    TextRect.center = (int(maxsize_x/2), 25)
    win.blit(BgSp, (int(x), 0))
    if not Mode:
        win.blit(TextSurf, TextRect)
    for Mario in ListMario:
        Mario.Sprites(win)
        Mario.Update()
    for Gumba in ListGumba:
        if screenx[1] < Gumba.x <= screenx[0]:
            Gumba.draw(win)
    for Block in Blocks:
        if screenx[1] < Block.x <= screenx[0]:
            Block.draw(win,timer)
    pygame.display.update()

# Bu daha cok kendm icin olan bi fonksiyondu suan ara isler icin kullaniyorum 
def debug(key, M, D):
    A = []
    A = sorted(D, key = lambda D: D.score, reverse = True)
    if len(A) != 0:
        return A[0].score

# Burada da ana dongumuz var olan olaylara gore fonksiyonlari cagriyor
while loop1:
    timer += 1
    if timer + 1 >= 15:
        timer = 0
    for Marios in ListMario:
        if Marios.y > 420 or Marios.afktime > 100:
            Marios.score -= int(Marios.time)
            DeadMario.append(Marios)
            ListMario.remove(Marios)
    if len(ListMario) == 0:
        Blocks.clear()
        ListGumba.clear()
        Blocks = []
        ListGumba = []
        M, Generation, Blocks, ListGumba = restart(ListMario, M, Generation, D)
        temp = 0
        x = 0

    if len(ListMario) == 0 and M == 0:
        Generation = 0
        NextGeneration, DeadMario = crossbreed(DeadMario, MaxM)
        M = MaxM
        Evolution += 1
        if M < D:
            for i in range(0, M):
                ListMario.append(NextGeneration[i])
            Generation += 1
            M = 0
        else:
            for i in range(0, D):
                ListMario.append(NextGeneration[M-1])
                M -= 1
            Generation += 1
    
    MarioM = []
    MarioM = sorted(ListMario, key = lambda ListMario: ListMario.x, reverse = True)
    Highscore = MarioM[0].score
    if len(MarioM) > 0:
        if MarioM[0].x >= maxsize_x/2:
            scroll += (MarioM[0].x - maxsize_x/2 - scroll)
        else:
            scroll = 0
    x -= scroll

    keys = pygame.key.get_pressed()

    BlockUpdate(ListMario, Blocks, ListGumba, scroll)

    BlockCollide(ListMario, Blocks, ListGumba, screenx)
    
    Moving(ListMario, keys, maxacc, acc, Blocks)
    
    Jumping (ListMario, keys, Blocks)

    Gravity(ListMario, Blocks)

    Smash(ListMario, ListGumba, DeadMario)

    redraw(ListMario, x, ListGumba, screenx)

    clock.tick(framerate)

    MaxHighScore.insert(Evolution, debug(keys, ListMario, DeadMario))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop1 = False
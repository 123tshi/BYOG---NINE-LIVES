import pygame
import sys
import time
import random

winwidth = 1200
winheight = 670
white = (255, 255, 255)
black = (0, 0, 0)
purple = (188, 188, 246)
blue = (153, 230, 255)
pillwidth = 7
pillheight = 25
yellow=(255, 255, 153)
pink = (255, 204, 242)
#blue = (0, 0, 255)
swidth = 26
sheight = 20
TIMER = 0


class Text():

    def __init__(self, size, text, x, y, color, font):
        self.font = pygame.font.SysFont(font, size)
        self.title = self.font.render(text, 1, color)
        self.pos = self.title.get_rect()
        self.pos.centerx = x
        self.pos.centery = y


    def blit(self, screen):
        screen.blit(self.title, self.pos)

    def update(self, newtext):
        self.title = self.font.render(newtext, 1, self.color)


class ScoreText(pygame.sprite.Sprite):

    def __init__(self, size, color, position, font):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.position = position
        self.font = pygame.font.SysFont(font, size)
        self.text = "SCORE: 0"
        self.image = self.font.render(str(self.text), 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.position[0]-self.rect.width/2, self.position[1])

    def update(self, cat):
        self.text = "SCORE: " + str(cat.score)
        self.image = self.font.render(str(self.text), 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.position[0]-self.rect.width/2, self.position[1])


class Game():

    def __init__(self, intro, play, ending, ticks):
        self.intro = intro
        self.play = play
        self.ending = ending
        self.beg_time = ticks
        self.winner = 0

    def blinks(self):
        self.cur_time = pygame.time.get_ticks()
        if (self.cur_time - self.beg_time) % 1000 < 500:
            return True
        else:
            return False


class Cat(pygame.sprite.Sprite):

    def __init__(self, x, y, swidth, sheight):
        pygame.sprite.Sprite.__init__(self)
        self.speed = [5, 5]
        self.width = swidth
        self.height = sheight
        self.image = pygame.image.load("cat1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (swidth, sheight))
        self.rect = self.image.get_rect()
        self.rect.width = self.width
        self.rect.height = self.height
        self.rect = self.rect.move(x, y)
        self.beg_time = pygame.time.get_ticks()
        self.start_time = 0
        self.lifecount = 9
        self.oncount = 0
        self.score = 0

    def update(self, counter, eatgroup, eatcount, onepscreen, poisongroup):
        cur_time = pygame.time.get_ticks()
        if counter != 0:
            self.image = pygame.image.load("cat2.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect.width = self.image.get_rect().width
            self.rect.height = self.image.get_rect().height
            if (cur_time - self.beg_time) % 1000 >= 500:
                cur_time += 500

        else:
            if (cur_time - self.beg_time) % 1000 < 500:
                self.image = pygame.image.load("cat1.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
                self.rect.width = self.image.get_rect().width
                self.rect.height = self.image.get_rect().height

            else:
                self.image = pygame.image.load("cat2.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
                self.rect.width = self.image.get_rect().width
                self.rect.height = self.image.get_rect().height


        collisions = pygame.sprite.spritecollide(self, eatgroup, True)
        for key in collisions:
            self.score += 1
            eatcount -= 1

        collisions2 = pygame.sprite.spritecollide(self, poisongroup, True)
        for key in collisions2:
            self.lifecount -= 1
            self.oncount = 0


    def check(self):
        cur_time = pygame.time.get_ticks()
        if (cur_time - self.start_time) > 400:
            self.back()

    def back(self):
        self.rect.y = 520
        self.image = pygame.image.load("cat2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height


    def jump(self):
        self.start_time = pygame.time.get_ticks()
        self.image = pygame.image.load("cat1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height
        self.rect.y = 420
        self.rect.move(self.rect.x, self.rect.y)


class Eat(pygame.sprite.Sprite):

    def __init__(self, x, y, swidth, sheight):
        pygame.sprite.Sprite.__init__(self)
        self.speed = [5, 5]
        self.width = swidth
        self.height = sheight
        self.image = pygame.image.load("yumbird.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (swidth, sheight))
        self.rect = self.image.get_rect()
        self.rect.width = self.width
        self.rect.height = self.height
        self.rect = self.rect.move(x, y)
        self.beg_time = pygame.time.get_ticks()
        self.counter = 0

    def update(self, eatcount):
        self.counter = 0
        if self.counter == 0:
            self.speed = random.randrange(8, 15)
            self.counter += 1
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()
            eatcount -= 1


class Poison(pygame.sprite.Sprite):

    def __init__(self, x, y, swidth, sheight):
        pygame.sprite.Sprite.__init__(self)
        self.width = swidth
        self.height = sheight
        self.image = pygame.image.load("badbird.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (swidth, sheight))
        self.rect = self.image.get_rect()
        self.rect.width = self.width
        self.rect.height = self.height
        self.rect = self.rect.move(x, y)
        self.beg_time = pygame.time.get_ticks()
        self.counter = 0

    def update(self, poisoncount, onepscreen1):
        if self.counter == 0:
            if poisoncount % 2 == 0:
                self.speed = random.randrange(16, 18)
            else:
                self.speed = random.randrange(8, 15)
            self.counter += 1
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()


class Lives(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.image.load("catlife.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.height = self.height
        self.rect = self.rect.move(x, y)


def main():
    start = True
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    counter = 0
    while start:
        fps = 60

        game = Game(True, True, True, pygame.time.get_ticks())

        pygame.display.set_caption("NINE LIVES")
        screen = pygame.display.set_mode((winwidth, winheight), pygame.SRCALPHA)

        bg = pygame.image.load("jumpbg.jpg").convert()
        bg = pygame.transform.scale(bg, (winwidth, winheight))

        playbg = pygame.image.load("sky5.png").convert()
        playbg = pygame.transform.scale(playbg, (winwidth, winheight))

        playbg2 = pygame.image.load("sky6.png").convert()
        playbg2 = pygame.transform.scale(playbg2, (winwidth, winheight))

        trees = pygame.image.load("trees.tif").convert()
        trees = pygame.transform.scale(trees, (winwidth, 90))

        title = Text(130, "NINE", screen.get_rect().centerx + 285, screen.get_rect().centery, black,
                     "estrangelonisibinoutline")
        subtitle = Text(30, "-CLICK ANYWHERE TO START-", screen.get_rect().centerx + 285, screen.get_rect().centery + 60,
                        black, "dincondensed")

        print(pygame.font.get_fonts())

        onepscreen1 = 0
        eatgroup = pygame.sprite.Group()
        poisongroup = pygame.sprite.Group()

        eatcount = 0
        maxeatcount = 1000

        poisoncount = 0
        maxpoisoncount = 1000

        cat = Cat(80, 520, 284, 119)

        catgroup = pygame.sprite.Group()
        catgroup.add(cat)

        TIMER = 0

        lifegroup = pygame.sprite.Group()
        lifecount = 9

        score = ScoreText(40, white, (winwidth - 150, 10), "estrangelonisibinoutline")
        scoregroup = pygame.sprite.Group()
        scoregroup.add(score)
        while game.intro:

            screen.blit(bg, (0, 0))
            title.blit(screen)

            if game.blinks():
                subtitle.blit(screen)

            # Checks if window exit button pressed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif pygame.key.get_pressed() == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    subtitle.blit(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    game.intro = False

            clock.tick(fps)

            pygame.display.flip()

        while game.play:
            if game.blinks():
                screen.blit(playbg, (0, 0))
            else:
                screen.blit(playbg2, (0, 0))
            catgroup.draw(screen)
            eatgroup.draw(screen)
            lifegroup.draw(screen)
            poisongroup.draw(screen)
            scoregroup.draw(screen)
            if counter != 0:
                cat.check()
                if cat.rect.y == 520:
                    counter = 0

            if lifecount != cat.lifecount:
                for life in lifegroup:
                    life.kill()
                lifecount = cat.lifecount

            for i in range(cat.lifecount):
                if cat.oncount == 0:
                    life = Lives(winwidth - 70 - 70*i, 50, 60, 60)
                    lifegroup.add(life)
            cat.oncount += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif pygame.key.get_pressed() == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if counter == 0:
                            cat.jump()
                            counter += 1

            freq = random.randrange(40, 45)
            if eatcount < maxeatcount and TIMER % freq == 0:
                ycoor = random.randrange(380, 580)
                bfly = Eat(winwidth, ycoor, 95, 88)
                eatgroup.add(bfly)
                eatcount += 1

            if poisoncount % 2 == 0:
                freq2 = 161
            else:
                freq2 = 213
            if poisoncount < maxpoisoncount and TIMER % freq2 == 0:
                if onepscreen1 <= 1:
                    if poisoncount % 2 == 0:
                        ycoor2 = random.randrange(380, 420)
                    else:
                        ycoor2 = random.randrange(560, 580)
                    pfly = Poison(winwidth, ycoor2, 95, 88)
                    #onepscreen += 1
                    poisongroup.add(pfly)
                    poisoncount += 1

            TIMER += 1
            #poisonous butterflies
            #clouds going across screen like butterflie
            onepscreen = poisongroup.update(poisoncount, onepscreen1)
            eatgroup.update(eatcount)
            scoregroup.update(cat)
            catgroup.update(counter, eatgroup, eatcount, onepscreen, poisongroup)
            print(cat.lifecount)
            if cat.lifecount == 0:
                time.sleep(1)
                game.play = False
            clock.tick(fps)
            pygame.display.flip()

        while game.ending:
            screen.blit(bg, (0, 0))
            fps = 60
            # Print background
            endtext = "YOU LOSE"
            endtext = Text(80, endtext, screen.get_rect().centerx + 275, screen.get_rect().centery, black, "estrangelonisibinoutline")
            endtext.blit(screen)
            endtext2 = "YOUR SCORE: " + str(cat.score)
            endtext2 = Text(30, endtext2, screen.get_rect().centerx + 275, screen.get_rect().centery + 60, black, "estrangelonisibinoutline")
            endtext2.blit(screen)


            endsubtitle = Text(30, "-CLICK ANYWHERE TO CONTINUE-", screen.get_rect().centerx + 275,
                            screen.get_rect().centery + 100, black, "dincondensed")

            if game.blinks():
                endsubtitle.blit(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    endsubtitle.blit(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    game.ending = False
                    game.intro = True
                    game.play = True

            clock.tick(fps)

            pygame.display.flip()

if __name__ == '__main__':
    main()

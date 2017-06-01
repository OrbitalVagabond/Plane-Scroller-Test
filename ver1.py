import pygame, os, sys, math, leveldat

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Force static position of screen

# Constants
WHITE = (255, 255, 255)
LIGHT_GREY = (120, 120, 120)
GREEN = (0, 255, 0)


WIN_W = 16*32
WIN_H = 700

SHIP_WIDTH = WIN_W / 15
SHIP_HEIGHT = WIN_H / 15

TIMER = 0

class Copter1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0,0,40,40)
        self.default_speed = 7
        self.image = pygame.Surface((self.rect.width,self.rect.height))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, ship, chirality):
        pygame.sprite.Sprite.__init__(self)
        self.side = chirality
        x, y = self.set_pos(ship)
        self.initial_y = y
        self.rect = pygame.Rect(x, y, 5, 5)
        self.rect.centerx = x
        self.speed = 15
        self.image = pygame.Surface((5,5)).convert()

    def set_pos(self, ship):
        x = ship.centerx
        if self.side == 0:
            x += 5
        elif self.side == 1:
            x -= 5
        y = ship.y - 5
        return x, y

    def update(self, camera):
        self.rect.y -= self.speed
        if self.rect.y < camera.state.y:
            self.kill()

class CameraEntity(pygame.sprite.Sprite):
    def __init__(self, maprect):
        pygame.sprite.Sprite.__init__(self)
        self.maprect = maprect
        self.rect = pygame.Rect(maprect.width/2,maprect.height - WIN_H/2,20,20)
        self.image = pygame.Surface((self.rect.width,self.rect.height))
        self.speed = 1
        self.moving = True
    def update(self):
        if self.rect.y < WIN_H/2:
            self.moving = False
        if self.moving == True:
            self.rect.y -= self.speed

class Camera(object):
    def __init__(self, total_width, total_height):
        self.state = pygame.Rect(0, 0, total_width, total_height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, camera_entity_rect, ship_rect):
        #self.state = pygame.Rect(-target_rect.x + WIN_W/2, -target_rect.y + WIN_H/2,
        # self.state.width, self.state.height)
        x = self.ship_camera(ship_rect)
        y = self.level_camera(camera_entity_rect)

        self.state = pygame.Rect(x, y, self.state.width, self.state.height)

    def ship_camera(self, ship_rect):

        x = -ship_rect.centerx + WIN_W / 2
        # Stop scrolling at left edge
        if x > 0:
            x = 0

        # Stop scrolling at the right edge
        elif x < -(self.state.width - WIN_W):
            x = -(self.state.width - WIN_W)

        return x

    def level_camera(self, camera_entity_rect):
        y = -camera_entity_rect.y + WIN_H / 2
        # Stop scrolling at top
        if y > 0:
            y = 0

        # Stop scrolling at the bottom
        elif y < -(self.state.height - WIN_H):
            y = -(self.state.height - WIN_H)

        return y




class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        #self.image.convert()
        self.image.fill(LIGHT_GREY)
        self.rect = pygame.Rect(x, y, 32, 32)


class Ship(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        self.side_speed = 5
        self.top_speed = 4
        self.image = pygame.Surface((SHIP_WIDTH, SHIP_HEIGHT)).convert()
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = container.centerx
        self.rect.y = container.bottom - self.rect.height * 3
        self.container = container
        self.diagup_speed = round(self.top_speed / math.sqrt(2))
        self.diagside_speed = round(self.side_speed / math.sqrt(2))


    def update(self,moving,camera_rect,bullet_group):
        global TIMER
        up = False
        down = False
        right = False
        left = False
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            up = True
        if key[pygame.K_s]:
            down = True
        if key[pygame.K_a]:
            left = True
        if key[pygame.K_d]:
            right = True
        if key[pygame.K_SPACE]:

            if TIMER % 10 == 0:
                p = Bullet(self.rect,0)
                p1 = Bullet(self.rect,1)
                bullet_group.add(p,p1)

        if down and not up:
            if right and not left:
                self.rect.y += self.diagup_speed
                self.rect.x += self.diagside_speed
                print self.diagside_speed
                print self.diagup_speed
            elif left and not right:
                self.rect.y += self.diagup_speed
                self.rect.x -= self.diagside_speed
                print self.diagside_speed
                print self.diagup_speed
            else:
                self.rect.y += self.top_speed

        elif up and not down:
            if right and not left:
                self.rect.y -= self.diagup_speed
                self.rect.x += self.diagside_speed
            elif left and not right:
                self.rect.y -= self.diagup_speed
                self.rect.x -= self.diagside_speed
            else:
                self.rect.y -= self.top_speed

        elif right and not left:
            self.rect.x += self.side_speed

        elif left and not right:
            self.rect.x -= self.side_speed


        if moving == True:
            self.rect.y -= 1

        if self.rect.y < camera_rect.y - WIN_H/2:
            self.rect.y = camera_rect.y - WIN_H/2
        elif self.rect.y > camera_rect.y + WIN_H/2 - SHIP_HEIGHT:
            self.rect.y = camera_rect.y + WIN_H/2 - SHIP_HEIGHT




        self.rect.clamp_ip(self.container)










def main():
    pygame.init()
    # Create Game Variables
    global TIMER
    fps = 60
    clock = pygame.time.Clock()
    play = True
    pygame.display.set_caption('Raiden 2 Clone')
    screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)


    # Create Groups
    platform_group = pygame.sprite.Group()
    ship_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    # Load Level
    levelclass = leveldat.Mapdat()
    level=levelclass.map

    # Build Level
    x = y = meta_x = 0
    sample_row = True
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platform_group.add(p)

            if sample_row:
                meta_x += 32

            x += 32
        y += 32
        sample_row = False
        x = 0

    # Use level data to create container
    container = pygame.Rect(0, 0, meta_x, y)

    # Camera

    total_width = len(level[0]) * 32
    total_height = len(level) * 32
    camera = Camera(total_width, total_height)
    total_rect = pygame.rect.Rect(0, 0, total_width, total_height)

    # Create Game Objects
    camera_entity = CameraEntity(total_rect)
    DACHOPPA = Ship(container)
    ship_group.add(DACHOPPA)
    platform_group.add(camera_entity)






    # Gameplay

    while play:
        TIMER += 1
        # Checks if window exit button pressed
        #pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Update
        platform_group.update()
        ship_group.update(camera_entity.moving,camera_entity.rect,bullet_group)
        camera.update(camera_entity.rect, DACHOPPA.rect)
        bullet_group.update(camera)
        screen.fill(WHITE)


        # Draw Everything
        #platform_group.draw(screen)
        #screen.blit(DACHOPPA.image,DACHOPPA.rect)
        for p in platform_group:
            screen.blit(p.image, camera.apply(p))
        for s in ship_group:
            screen.blit(s.image, camera.apply(s))
        for b in bullet_group:
            screen.blit(b.image, camera.apply(b))

        # Limits frames per iteration of while loop
        clock.tick(fps)

        # Writes to main surface
        pygame.display.flip()


if __name__ == "__main__":
    main()
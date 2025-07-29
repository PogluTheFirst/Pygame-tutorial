# Platformer

#! This uses pygame-ce instead of pygame
#! Always read the documentation at pyga.me/docs
#! The comments are written by me, hopefully the work well enough

#& New Things in this project:
#* 1. Platformer Logic:
    #~ 1.1. Player Movement:
        #& The player directly controls left/right movement
        #& Up/Down movement is controlled by gravity and jumping
        #& We just need to make direction.y increasingly large and set it to a negative value when the player jumps
        #& Including dt with the fall speed requires a bit more math, so we'll limit the framerate to 60 FPS

#* 2. More organized imports:
    #& Some minor change is the state management for the player
    #& Also, we will keep the imports more centralized:
    #& There will be one method that imports everything

#*3. Better timers:
    #& Games heavily rely on timers:
    #& for this game
    #& The player has a cooldown, we spawn a bee every x seconds
    #& We keep a fire sprite animation for a bit, Enemies will die 0.2 seconds after being shot
    #& Ideally, we have a reusable timer class that can:
    #& 1. Easily be called anywhere
    #& 2. Can call on function on timeout
    #& 3. Shout be repeatable

from settings import * 
from sprites import *
from support import *
from groups import AllSprites
from Timer import Timer
from random import randint

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        #* groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        #* Load game
        self.load_assets()
        self.setup()

        #* Timer
        self.bee_timer = Timer(500, func = self.create_bee, repeat = True, autostart = True)

    def create_bee(self):
        Bee(self.bee_frames, 
            pos = ((self.level_width + WINDOW_WIDTH), randint(0, self.level_height)),
            groups =  (self.all_sprites, self.enemy_sprites),
            speed = randint(300, 500))

    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet(self.bullet_surf, (x, pos[1]), direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.fire_surf, pos, self.all_sprites, self.player)
        self.audio['shoot'].set_volume(0.05)
        self.audio['shoot'].play()

    def load_assets(self):
        #* Graphics
        self.player_frames = import_folder('images', 'player')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')

        #* Sounds
        self.audio = audio_importer('audio')
        # self.audio['impact'].play()

    def setup(self):
        tmx_map = load_pygame(join('data', 'maps', 'world.tmx'))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE
        
        for x, y, image in tmx_map.get_layer_by_name('Main').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)
            if obj.name == 'Worm':
                Worm(self.worm_frames, pygame.FRect(obj.x, obj.y, obj.width, obj.height), (self.all_sprites, self.enemy_sprites))

    def collision(self):
        #* bullets -> enemies
        for bullet in self.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collision:
                self.audio['impact'].set_volume(0.05)
                self.audio['impact'].play()
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.destroy()
        
        #* player -> enemies
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            #* update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()

            #* draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 
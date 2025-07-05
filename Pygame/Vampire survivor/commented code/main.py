# Vampire survivor game

#! pip install pygame-ce
#! This tutorial uses pygame-ce (pygame community edition)
#! Always check official documentation (pyga.me/docs) 
#! For best comment/documentation reading experience use colorful comments (not better comments) extension in vscode

#! Documentation
#& This project will be much closer to an actual game
#* A couple of key concepts to cover:
    #& Collisions
    #& Camera
    #& Creating levels in an editor
    #& Proper animation control

#& First of all we have to setup the basics
#& There are four folders within the project folder (ignore the fact that there is commented and uncommented code folder from me)
#& There is an audio folder
#& There is data and images folder aswell
#& inside images are all required images as well as animation frames
#& The data folder has graphics, maps and tilesets

#* 1. Collisions:
    #& Rect can only check overlaps
    #& For actual collisions we need to use the collision info and update the player position
    #~ Problem: On which side will colliison happen
    #& so we first have to get the collision side
    #^ 1.1. Getting the collision side:
        #& Seperate the dimensions:
        #& We move and check collisions on the horizontal and vertical axis individually
        #& We only check the axis
        #& That way, we only need to know if the player is left or right of the obstacle
        #& If there is an overlap and the player is moving right than the collison must be on the left side (assuming obstacle dosen't move)
        #~ Problems with this approach
        #& While this is easy to implement it only works if a single object is moving
        #& For example in the game, the player only collides with tress, rocks and hill but not with the enemies
        #& For collisions between 2 moving objects we need some more logic

#* 2. Creating levels:
    #& When creating a proper level we need an editor
    #& A way to place images and see the result right away
    #& A really good choice is Tiled, a free tile editor available at mapeditor.org
    #& For the video, he only covers how to import tile maps, not how to create them
    #& If you need to know, then watch bro's video about Tiled
    #& Once module imported and map imported into game
    #& We want to access all of the individual layers on the map
    #& There are types of layers in Tiled like object layer and tile layer

#* 3. Camera:
    #& We currently can only see thing on the display surface and not anything else
    #& There is a limitation that the display surface cannot be changed
    #& It always starts at 0, 0 and continues to display dimensions
    #& To create a camera we need to change where elements are drawn
    #^ Really important:
    #& The position of a sprite (or rather the rect) does not change
    #& We only draw it in a different position 
    #& This is important to make keep the collision logic
    #~ 3.1. How to draw stuff in a different position
        #& We will customize the sprite group drawing logic
        #& Group.draw is simply a for loop that blits sprites on a surface
    #~ 3.2. Y sorting
        #& If there are overlaps between sprites you want to make sure that the right sprite is on top
        #& You get that effect by soritng the sprites by the  centery position

#* 4. Animation control
    #& And we keep doing the same ( import images and update self.image )
    #& But we need to add statement management
    #& For example: if the player moves right then play the "right" animation frames
    #& Also stop the animation with the when the player stops

#* 5. Adding the murican gun
    #& The gun is another sprite that rotates around the player
    #& The only difficlt part is to get the angle:
    #& We want the angle between the player and the mouse
    #& But you need to be careful: The mouse pos is always on the coords of the display surface
    #& But the player dosen't directly link to the display surface coordinates anymore due to the camera
    #& You either need to account for the camera offset or use the fact the player is always the center
    #& We use the second cuz it is stupid not to

#* 6. Enemies
    #& We need a timer that trigger twice per second
    #& When it triggers it creates an instance of the enemy
    #& It walks toward the player and can collide with objects
    #& It always plays a walking animation (need animations for that)


#* Imports
#& No need to import pygame as it has already been imported in settings.py
from random import randint, choice
from pytmx.util_pygame import load_pygame #? The library used for tmx files and map creation with pygame
from player import Player
from settings import *
from sprites import *
from groups import *

#* Using a class for creating pygame window
class Game:
    def __init__(self):
        #* Basic setup
        pygame.init() #? initalize
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #? Dimensions
        pygame.display.set_caption('Survivor') #? Title
        self.clock = pygame.time.Clock() #? Clock object
        self.running = True

        #* Group
        self.all_sprites =AllSprites() #? sprite group
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        #* Gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100 #? in milliseconds

        #* Enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 350)
        self.spawn_positions = []

        #* Setup
        self.load_images()
        self.setup() #? Tile map setup

        #* Audio
        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.2)
        self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.impact_sound.set_volume(0.5)

        #* Sprites
        #& as groups as seperated by comma and not withing parenthesis with each other the actions are seperate
        #& The player resides in all_sprites but has access to all sprites
        #& But the object are in both groups
        #* Example sprite creation Group used here is commented out in sprites.py
        # for i in range(6):
        #     x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
        #     w, h = randint(60, 100), randint(50, 100)
        #     CollisionSprite((x, y), (w, h), (self.all_sprites, self.collision_sprites))

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()

        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx')) #?Loading tilemap
        #& Ordering of creation of stuff matters

        for x, y, image in map.get_layer_by_name('Ground').tiles(): #? .tiles() shows pygame that this is a bottom tile layer
            Sprite((x * TILESIZE, y * TILESIZE), image, self.all_sprites) #? We have to multiply x and y with tile size (size of a single tile)
            #& You can set the tilesize when creating a map

        for obj in map.get_layer_by_name('Objects'): #? Gets a layer Objects layer from the map here
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites)) #? Creation of objects

            # #* Data from the layer
            # print(obj.x) 
            # print(obj.y)
            # print(obj.image)

        for obj in map.get_layer_by_name('Collisions'): #? Invisible rects layer
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites) 
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot: #? left button
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self): #? running the game
        while self.running:
            #* dt
            dt = self.clock.tick() / 1000 #? dt in milliseconds

            #* event loop
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)
                    
            #* update
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()

            #* draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update() #? updating every frame

        pygame.quit() #? ending

if __name__ == "__main__":
    game = Game()
    game.run()

#* For no reason at all
# ⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⠛⠋⠉⠈⠉⠉⠉⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢿⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⡏⣀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⠀
# ⣿⣿⣿⢏⣴⣿⣷⠀⠀⠀⠀⠀⢾⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⠀
# ⣿⣿⣟⣾⣿⡟⠁⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣷⢢⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀
# ⣿⣿⣿⣿⣟⠀⡴⠄⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⣿⠀
# ⣿⣿⣿⠟⠻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠶⢴⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⣿⠀
# ⣿⣁⡀⠀⠀⢰⢠⣦⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⡄⠀⣴⣶⣿⡄⣿⠀
# ⣿⡋⠀⠀⠀⠎⢸⣿⡆⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⠗⢘⣿⣟⠛⠿⣼⠀
# ⣿⣿⠋⢀⡌⢰⣿⡿⢿⡀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣧⢀⣼⠀
# ⣿⣿⣷⢻⠄⠘⠛⠋⠛⠃⠀⠀⠀⠀⠀⢿⣧⠈⠉⠙⠛⠋⠀⠀⠀⣿⣿⣿⣿⣿⠀
# ⣿⣿⣧⠀⠈⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠟⠀⠀⠀⠀⢀⢃⠀⠀⢸⣿⣿⣿⣿⠀
# ⣿⣿⡿⠀⠴⢗⣠⣤⣴⡶⠶⠖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡸⠀⣿⣿⣿⣿⠀
# ⣿⣿⣿⡀⢠⣾⣿⠏⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠉⠀⣿⣿⣿⣿⠀
# ⣿⣿⣿⣧⠈⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⡄⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⣿⣦⣄⣀⣀⣀⣀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠙⣿⣿⡟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠁⠀⠀⠹⣿⠃⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⢐⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
# ⣿⣿⣿⣿⠿⠛⠉⠉⠁⠀⢻⣿⡇⠀⠀⠀⠀⠀⠀⢀⠈⣿⣿⡿⠉⠛⠛⠛⠉⠉⠀
# ⣿⡿⠋⠁⠀⠀⢀⣀⣠⡴⣸⣿⣇⡄⠀⠀⠀⠀⢀⡿⠄⠙⠛⠀⣀⣠⣤⣤⠄⠀⠀

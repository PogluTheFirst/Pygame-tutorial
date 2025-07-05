from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'down', 0 #? Default
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha() 
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        #* Movement
        self.direction = pygame.Vector2() #? 0, 0 by default
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_images(self):
        #& for this dictionary it is like {player state: [frames of player]}
        #& names of keys have to match the folder names
        self.frames = {'left': [],
                       'right': [],
                       'up': [],
                       'down': []
                       }
        
        #& Walk from os takes a path and basically performs os.listdir() on everything inside including subfolders
        #& os.walk return stuff like this [path, subfolder, everything inside folder]
        # print(list(walk(join('images', 'player'))))
        for state in self.frames.keys(): #? Basically adding all the surfs to the list in the dictionaries
            for folder_path, sub_folders, file_names in walk(join('images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key = lambda name: name.split('.')[0]): #? sorting files shold be done
                        #& The lambda function gets the number of the png from the folder
                        full_path = join(folder_path, file_name) #? getting the full path of the file
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

        # print(self.frames)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        # self.rect.center += self.direction * self.speed * dt
        self.hitbox_rect.x += self.direction.x * self.speed * dt #? Seperatng both axis for collision 
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left #? moves player left if touching sprite from right
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right #? moves player right if touching sprite from left
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top #? moves player up if bottom of sprite touching
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom #? moves player down if top of sprite touching

    def animate(self, dt):
        #* get state (changing the state)
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        

        #* animate
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0 #? animation speed
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
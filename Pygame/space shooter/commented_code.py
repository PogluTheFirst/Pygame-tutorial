# Spaceship game

#! pip install pygame-ce
#! This tutorial uses pygame-ce (pygame community edition)
#! Always check official documentation (pyga.me/docs) 
#! For best comment/documentation reading experience use colorful comments (not better comments) extension in vscode

#! Documentation
#* 1. Pygame has two important concepts
#& Surfaces and Rectangles:
    #^ 1. Surfaces:
        #& Surfaces can be Images like imported png or text
        #& They can also serve as a window (Display surface)
        #& Two types of surfaces
        #~ 1.1.1 Display surface:
            #& The canvas that everything will be drawn on
            #& You can only have one at a time
        #~ 1.1.2 Regular Surface:
            #& It is an image of some kind
            #& You can have any but they are only visible when attached to the display surface
        #~ 1.1.3 Placing surfaces sucks:
            #& Since we always place the topleft it requites math to place it in a precise spot
            #& Sometimes we just want to place the center or the right side of a surface
        #~ 1.1.4 Placing surfaces via rects:
            #& Rects can help place a surface more elegantly
            #& They also do collisions and they can be drawn
            #& surface.get_frect(point = pos)
        #~ 1.1.5 Other:
            #& Other than that, they (display surfaces and regular surfaces) share some attributes and methods. 
            #& for example, you can fill both with a color via surface.fill(color)
    #^ 2. Rectangles:
        #& Wraps around a surface and can position it
        #& Also Does collisions, can be drawn
        #~ 1.2.1 Placing Rects:
            #& Rects are just rectangles with a size and position
            #& They also have lots of points:
            #& Tuples with an x and y position like (midbottom, topleft, topright, center, bottomleft, etc.)
            #& you can place a rect by using these points so you are not confined to just topleft
            #& X or y positions (left, top, right, bottom, centerx, centery, etc.)
            #& There is also width, height and size
            #& Each point can be measured and changed
            #& The points say relative to each other: Moving one means you move all
        #~ 1.2.2 Types of Rects:
            #& There are two types of rects:
            #? 1.2.2.1 Rects:
                #& They store data as integers
                #& They are not as useful cuz they are not as precise as frects
                #& They are basically here for backwards compatibility with pygame
            #? 1.2.2.2 Frects:
                #& Frects are exclusive to pygame-ce
                #& Frects store data as floating point values
                #& They are better as they are more precise
                #& They are more common to see in projects nowadays
        #~ 1.2.3 Creating Rects:
                #& You can create a rect from scratch
                #& pygame.Rect(pos, size)
                #& pygame.FRect(pos, size)

                #& Or you can create it from a surface (rect will have same size as surface)
                #& surface.get_rect(point = pos)
                #& surface.get_frect(point = pos)

#* 2. Drawing Graphics
#& Pygame can display graphics in 2 ways:
#& Show an image or text via a surface & and draw pixels
#^ 2.1 Show an image/text(surface):
    #& A surface in pygame is usually an image (png, jpg), a plain area or rendered text
    #& In pygame drawing order matters, things drawn after are drawn on top

    #& How to Create:
    #& plain surface: pygame.Surface((width, height))
    #& imported surface: pygame.image.load(path)
    #& text surface: font.render(text, AntiAlias, Color)

    #& To place: display_surface.blit(surf_name, (topleft position on window or a rect))
    #~ 2.1.1 Important when importing:
        #& The file can become a problem depending on the code editor
        #& vscode starts a relative path from the main directory
        #& Sublime starts from the python file

        #& Depending on the os you might need a different slash in the file path
        #& Images/player.png or images\player.png, This should be dynamic

        #& When importing an image, you want to convert it to a format pygame can work more easily with
        #& if the image has no transparent pixels: .convert()
        #& if the image has transparent pixels: .convert_alpha()
        #& This will make your game run much faster
    #~ 2.1.2 Join method from os.path:
        #& Takes in file path like this join('folder', 'file')
        #& Joins them using a slash that is appropriate for your os
    #~ 2.1.3 Creating text:
        #& You first need to create a font object:
        #& pygame.font.Font(font, style, size)
        #& This font is rendered and you get a surface
    #~ 2.1.4 Drawing things:
        #& pygame.draw has lots of draw methods
        #& You could draw rectangles, circles, lines etc.
    #~ 2.1.5 Colors in pygame:
        #& You can define colors in 3 ways with pygame
        #& inbuilt color names ('red', 'green')
        #& Hex codes ('#000000', '#FFFFFF')
        #& RGB tuples: (red, green, blue) where red green or blue is any value from 0 to 255
 
#* 3. Update
#& Literally Just a loop (usually a while True loop)
#& On every iteration we get input, update elements & draw a frame
#^ 3.1 Event Loop:
    #& Checks event [keyboard, mouse and controller input, timers]
    #& Also includes pressing x to close the game

#* 4. Movement:
#& General Idea
#& In the most basic sense, moving stuff is easy: you simply blit a surface in a different pos on every frame
#& You can do that via a (x, y) tuple or a rect
#^ 4.1 Frame rate:
    #& Higher framerate make objects move faster and smoother, slower framerate is makes them slower and more jankier
    #& Faster is not always better as things may end up moving to fast 
    #& We can use the clock object to set a framerate regardless of the pc it is running on
    #& It is still better to use delta time than setting a constant frame rate
    #~ 4.1.1 Framerate independence:
        #& Depending on the computer your game could run at very different framerates
        #& Since we update the position on every new frame we get faster movement on faster computers
        #& Table to understand
        #& _____________________________________________________________________________________
        #& | Movement(pixel / Frame)  | Frames / second      | Actual Movement(pixel / second) |
        #& | 10                       | 30                   | 10 * 30 = 300                   |
        #& | 10                       | 60                   | 10 * 60 = 600                   |
        #& | 10                       | 120                  | 10 * 120 = 1200                 |
        #& --------------------------------------------------------------------------------------
        #& We can fix this using delta time
#^ 4.2 Refinement:
    #& Vectors are an excellent way to store a direction
    #& Including delta time makes the movement framerate dependent
    #~ 4.2.1 Vectors:
        #& Basically a list with 2 values: x and y
        #& Pygame has 2d and 3d vectors
        #& You can read and change the values
        #& Vector(x =1, y = 5)
        #&
    #~ 4.2.2 Vector math:
        #& Multiplying a vector multiplies all individual elements of that vector
        #& Vector(4, 2) * 2 = vector(8, 4)
        #& This also applies to adding vectors
        #& vector(4, 2) + vector(1, 5) = vector(5, 7)
        #& You can add a vector to the tuple position of a rectangle
        #& rect.center + vector(1, 5)
    #~ 4.2.3 Delta time:
        #& The time it takes you computer to render the current frame e.g.
        #& 60 frames / sec -> 1 sec / 60 = 0.017
        #& Table with delta time
        #& _____________________________________________________________________________________________________________________________________
        #& | Movement(pixel / Frame) | Frames / second | Actual Movement(pixel / second) | Delta time     | Dt adjusted movement (pixel / sec)|
        #& | 10                      | 30              | 10 * 30 = 300                   | 1 / 30 = 0.33  | 10 * 30 * 0.33 = 10               |
        #& | 10                      | 60              | 10 * 60 = 600                   | 1 / 60 = 0.017 | 10 * 60 * 0.017 = 10              |
        #& | 10                      | 120             | 10 * 120 = 1200                 | 1 / 120 = 0.008| 10 * 120 * 0.008 = 10             |
        #& -------------------------------------------------------------------------------------------------------------------------------------
        #& As you can see the Delta time adjusted movemtn is much more accurate than actual movment
        #& Delta time implementation: rect.center += direction * speed * dt
#^ 4.3. Input:
    #& There are a couple ways of taking input
    #~ 4.3.1. Event loop:
        #& We've already used it to close the game
        #& It can also get keyboard and mouse input but you can only have one event loop
    #~ 4.3.2. pygame.key and pygame.mouse:
        #& Can also get keyboard and mouse input
        #& But can be called anywhere in the code, super useful when creating classes
    #~ 4.3.3. Best way to get input?:
        #& I generally use pygame.key and pygame.mouse for input
        #& It's much easier to integrate with classes (you can call it anywhere in the code)
        #& It can check buttons continously (event loop input only checks the action of a button being pressed, NOT if a button is pressed)
    #~ 4.3.4. Normalizing Vectors:
        #& When pressing two buttons like up and left at the same time the object will travel faster than normally 
        #& Here is a diagram of what happens and why it is faster
        #&                  ^
        #&   424 speed    /  |
        #&   faster  ->  /   |
        #&              /    | -> 300 speed
        #&             /     |
        #&            /      |
        #&           ---------> 
        #&              |-> 300 speed
        #& Faster because of how vector addition works
        #& The magnitude should always be the same for x and y so that these values are balanced
        #& By using the normalize function on a vector it makes it so that
        #&                  ^
        #&   300 speed       |
        #&                   |
        #&              /    | -> 300 speed
        #&             /     |
        #&            /      |
        #&           ---------> 
        #& Normalizing makes it so that the hypotenuse of this vector gets shrunk down to x and y

#* 5. Sprites:
    #& We should be using classes rather than creating every object on screen by making a seperate one
    #& The code is starting to become messy
    #& For the player, we have a surface a rect, code for movement and for firing
    #& And it is still not doing very much, this needs to be better organized
    #& Sprites are the best way to use classes in pygame
    #^ 5.1 Using sprites and sprite definition:
        #& It's an inbuild pygame class that always contains a surface and a rect
        #& We create a custom class inherits from pygame.sprite.Sprite
        #& For this class we need to set
        #& self.image = surface
        #& self.rect = rect
    #^ 5.2 Displaying a sprite:
        #! Bad (but possible) approach:
        #! surface.blit(sprite.image, sprite.rect)
        #& Good approach:
        #& Use a pygame group
    #^ 5.3 Sprite Groups:
        #& Most games have dozens, if not thousands of sprites
        #& pygame is expecting that and sprite groups are designed around that
        #& group.draw(surface) -> draws all sprites on surface
        #& group.update(args) -> calls update with arg on every sprite
        #& You can loop over sprites and use them in other methods as well, making it easy to sort them into logical groups

#* 6. Time:
    #& We want to use time in 2 ways:
    #& 1. Spawn a meteor every x seconds
    #& 2. Have a cooldown for laser
    #&Those need different approaches
    #& The meteors need a timer that times out in an interval
    #& The laser needs a timer that runs for a short amount of time
    #^ 6.1 Interval timer:
        #& A timer that triggers every x seconds
        #& You first need to create an event and then set a timer with that event 
        #& You can then capture the event in the event loop this is builtin to pygame
    #^ 6.2 Custom timer:
        #& Pygame lets you capture the time since the start of the game
        #& You can use that to create a custom timer
        #& Get a starting point and then measure the time passed since that point

#* 7. Collisions:
    #& There are two types of collisions:
    #^ 7.1 rect collisions:
        #& Rectangles can check collisions with:
        #& A single point 
        #& Another rect
        #& A list of rects
        #& For example: 
        #& Rect1.colliderect(Rect2) Checks collision with another rect
    #^ 7.2 Sprite Collisions:
        #& Checks for collisions between a single sprite and sprites in a group
        #& pygame.sprite.spritecollide(sprite, sprite group, doKill, collided = None) example
    #^ 7.3 Collision limitation:
        #& Pygame collisions only check overlaps
        #& Proper collision behaviour need to be implemented seperately

#* 8. Additional topics:
    #^ 8.1 Using a mask:
        #& An object that checks which pixels of a surfaces are visible
        #& Invisible pixels -> Black     Visible Pixels -> White, makes the image black and white
        #& You can use that for two purposes
        #& Pixel perfect collisions
        #& Creating silhouettes (making the player flash, or adding an outline)
        #& Using a mask is very hardware intensive
    #^ 8.2 Transforming surfaces:
        #& pygame.transform can change surfaces
        #& Options: Scale, flip, rotate, blur, grayscale, invert
        #& Transforming a surface reduces quality
        #& For example if you rotate a surface once, you lose a bit of quality (not enough for anyone to notice)
        #& But if you rotate a surface 1000 times per second then the quality decay will be very noticeable
    #^ 8.3 Animated explosion:
        #& First, we import the explosion images
        #& Then we create an explosion class
        #& Whenever a laser hits a meteor we create an instance of the class
        #& It plays an animation then disappears
    #^ 8.4 Sounds
        #& You first need to create a Sound objet
        #& pygame.mixer.Sound(file path)
        #& The resulting sound file can play, stop, rewind, set_volume etc.

#! End of my documentation (I don't know if it's good or not)((hopefully good))

#! Code
import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite): #? Inheritance
    def __init__(self, groups): #? groups is the sprite group you want to attach it to
        #* setup
        super().__init__(groups) #? You should know what this does, also give the group to the super dunder init method
        # self.original_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
        # self.image = self.original_surf
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        #* Cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 300 #? In milliseconds

        #* Mask
        self.mask = pygame.mask.from_surface(self.image) #? Adds mask to surface
        # mask_surf = mask.to_surface() #? Turns mask into a surface
        # mask_surf.set_colorkey((0, 0, 0)) #? Makes all pixels of one color invisible
        # self.image = mask_surf #? turns image into mask
        #& Even without doing this by passing the pygame.sprite.mask_collide creates another mask by itself

        #& transform test
        # self.image = pygame.transform.rotate(self.image, 90) #? args = image, degrees of rotation
        # self.image = pygame.transform.scale2x(self.image) #? Scales image by 2
        # self.image = pygame.transform.grayscale(self.image)
        # self.rotation = 10

    def laser_timer(self):
        if not self.can_shoot: #? if player can't shoot
            current_time = pygame.time.get_ticks() #? Gets amount of time since timer is called to start in milliseconds
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        #* Player movement
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        #* Laser firing
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

        #* Continous rotation
        # self.rotation += 20 * dt
        # self.image = pygame.transform.rotate(self.image, self.rotation) #? Crashes game after some time
        #& To avoid crash, rotate the surface only once
        # self.image = pygame.transform.rotate(self.original_surf, self.rotation)
        # self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1) #? Rotates and zooms at the same time
        #& This will make sure quality of image better

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        #* Setup
        super().__init__(groups)
        self.image = surf #? Optimizing cuz only importing star surf once rather than 20 times
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))) #? don need the for loop here
        #& We dont need it cuz sprites are created before the game rather than the while loop

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt #? Centery because we are adjusting only one point of rect
        if self.rect.bottom < 0:
            self.kill() #? Destroys the sprite

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1) #? random.uniform gets floating number
        self.speed = randint(400, 500)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center) #? Removes some wobbly behaviour of meteor

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_frect(center = pos)
        explosion_sound.play()

    def update(self, dt):
        self.frames_index += 20 * dt #? Basically animation speed
        if self.frames_index < len(self.frames): #? if animation has finished
            self.image = self.frames[int(self.frames_index) % len(self.frames)] #? Try to understand
        else:
            self.kill()

def collisions():
    global running
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask) #? applies mask to rect
    if collision_sprites:  #? DoKill is False here
        # print(collision_sprites[0])
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, '#F1F1F1') #? only takes string as text
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, '#F1F1F1', text_rect.inflate(20, 10).move(0, -8), 5, 10) #? rect.inflate increases the size of the rect
    #& .move and .inflate args = (x, y)

#* General setup
pygame.init() #? Initializes pygame
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #? Setting the screen as a variable
pygame.display.set_caption('Spaceship Game') #? Changes title of window
running = True
clock = pygame.time.Clock() #? Clock object Can control the frame rate

#* Plain Surface
# surf = pygame.Surface((100, 200)) #? making a surface
# surf.fill('green')
# x = 100

#* Importing images
#~ Player
# player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
# player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
# # player_rect = player_surf.get_frect(bottomright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10)) #? Placing from another point
# player_direction = pygame.math.Vector2() #? Empty vector = 0, 0
# player_speed = 300

#~ Star
# star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
# star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))for i in range(20)] #? Creating this cuz without it star pos changes every frame

#~ Meteor
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
# meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

#~ Laser
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
# laser_rect = laser_surf.get_frect(bottomleft = (20 , WINDOW_HEIGHT - 20))
 
#~ Font
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40) #? You can have a default font by writing None for font arg
# text_surf = font.render('text', True, '#F1F1F1')

#~ Import Frames
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

#~ Sound
laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav')) #? creating a sound object
laser_sound.set_volume(0.2  ) #? Args floating value between 0 and 1

explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sound.set_volume(0.2)
# explosion_sound.play(loops = -1) #?-1 makes it loop infinitely

#~ Sprites
all_sprites = pygame.sprite.Group() #? Creating a sprite group
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites) #? Creating an instance of the player class

#* Custom events -> meteor event
meteor_event = pygame.event.custom_type() #? creating a custom event
pygame.time.set_timer(meteor_event, 300) #? args = the timer to turn to event, time in milliseconds

#~ Plain rect
# plain_rect = pygame.FRect(left, top, width , height) #? We ain't doin this

while running: #? Mainloop
    # clock.tick(60) #? changes the framerate
    # print(clock.get_fps())
    dt = clock.tick() / 1000 #? Returns the delta time as seconds

    #* Event loop
    for event in pygame.event.get(): #? pygame.event.get() Gets all inputs
        if event.type == pygame.QUIT: #? Checks if game is closed
            running = False
        #^ Event loop input (beta way)
        # if event.type == pygame.KEYDOWN: #? If any key is being pressed
        #     print(event.key) #? Returns pressed key
        #     print(event.key == pygame.K_1) #? Number 1 on keyboard
        # if event.type == pygame.KEYDOWN and event.key == pygame.K:
        #     print(1)
        # if event.type == pygame.MOUSEMOTION: #? for mouse
        #     print(event.pos) #? returns mouse position on window
        #     player_rect.center = event.pos #? You should understand what this does
        if event.type == meteor_event: #? checks if it should spawn a meteor
            meteorx, meteory = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (meteorx, meteory) ,(all_sprites, meteor_sprites)) #? You can add sprite to multiple sprite groups like this

    #* Input (sigma chad way)
    #^ Mouse
    # print(pygame.mouse.get_pos())
    # print(pygame.mouse.get_pressed()) #? Returns a tuple with three boolean values (LeftClick, ScrollClick, RightClick)
    # print(pygame.mouse.get_pressed()[0]) #? To get single value use indexing e.g. LeftClick here
    # print(pygame.mouse.get_rel()) #? Check if mouse is moving and how fast it is moving
    #^ Keyboard
    # print(pygame.key.get_pressed()) #? Returns a large boolean tuple containing every key on the keyboard
    # keys = pygame.key.get_pressed() #? A good way to use it is indexing
    # # if keys[pygame.K_1]: #? you can use these values for indexing
    # #     print(1) 
    # # if keys[pygame.K_RIGHT]: #? right arrow key
    # #     player_direction.x = 1 #? Changes x value of vector
    # # else:
    # #     player_direction.x = 0
    # player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) #? Moves the same way as above if statement with left movement
    # #& This works cuz pygame.K_RIGHT/LEFT returns TRUE or FALSE, 0 or 1 so if you press right, the statement becomes 1-0=1 and left 0-1=-1
    # #& however in doing this order matters 
    # player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) #? For top bottom movement
    # # print((player_direction * player_speed).magnitude) #? This value returns the length of the vector
    # player_direction = player_direction.normalize() if player_direction else player_direction #? Normalizes the vector if direction is 1
    # player_rect.center += player_direction * player_speed * dt #? Actually moving player

    # recent_keys = pygame.key.get_just_pressed() #? Only returns true on the first click not while holding
    # if recent_keys[pygame.K_SPACE]:
    #     print('fire laser')
    #* update
    all_sprites.update(dt) #? Passing delta time as an arg
    collisions()
    # collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)
    # if collision_sprites:  #? DoKill is False here
    #     # print(collision_sprites[0])
    #     egg = False

    # for laser in laser_sprites:
    #     collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
    #     if collided_sprites:
    #         laser.kill()

    #* Draw the game
    display_surface.fill('#3a2e3f') #? Fills screen with color
    # x += 0.1 #? Moving the surface
    # display_surface.blit(surf, (x, 150)) #? placing
    # for pos in star_positions:
    #     display_surface.blit(star_surf, pos)
    # display_surface.blit(player_surf, (100, 50)) #? Placing with topleft (boring way)
    # player_rect.left += 1 #? Moving to the right by using only one point
    # print(player_rect.right)
    # display_surface.blit(meteor_surf, meteor_rect) #? meteor
    # display_surface.blit(laser_surf, laser_rect) #? laser
    #* Player movement
    # player_rect.x += player_direction * 0.4
    # if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
    #     player_direction *= -1
    # if player_rect.bottom >= WINDOW_HEIGHT or player_rect.top <= 0:
    #     player_direction.y *= -1
    # if player_rect.right >= WINDOW_WIDTH or player_rect.left <= 0:
    #     player_direction.x *= -1

    # player_rect.center += player_direction * player_speed * dt #? Delta time movement
    # display_surface.blit(player_surf, plain_rect)
    # display_surface.blit(player_surf, player_rect) #? Placing with rect (Chad way)
    all_sprites.draw(display_surface)
    display_score()

    #& Test collsions
    # print(player.rect.collidepoint((100, 200))) #? Checks if rect is colliding with any point e.g. (100, 200)
    # print(player.rect.collidepoint(pygame.mouse.get_pos())) #? Checks if rect is colliding mouse
    # print(player.rect.colliderect(meteor.rect)) #? If player collides with meteor

    #& Test Draw
    # pygame.draw.line(display_surface, 'red', (0, 0), (500, 600), 10) #? args (surface, color, start_point, end_point, line_width)
    # pygame.draw.aaline(display_surface, 'red', (0, 0), pygame.mouse.get_pos()) #? args (surface, color, start_point, end_point)
    # pygame.draw.rect(display_surface, 'red', player.rect, 10, 10) #? args = (surface, color, rect, border_width, border_radius)
    # pygame.draw.ellipse(display_surface, 'red', player.rect) #? args = (surface, color, rect, border_width, border_radius)
    #& For more args check the documentation

    pygame.display.update()

pygame.quit() #? Oppoite of pygame.init()
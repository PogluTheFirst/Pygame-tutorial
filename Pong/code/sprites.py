from settings import *
from random import choice, uniform

class Paddle(pygame.sprite.Sprite):
    #* All this stuff was moved from Player to Paddle parent class to use inheritance
    def __init__(self, groups):
        super().__init__(groups)

        #* Image
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0, 0), SIZE['paddle']), 0, 4) #? pygame-ce docs (read them fool)
        # self.image.fill(COLORS['paddle'])

        #* Shadow surf
        self.shadow_surf = self.image.copy()
        pygame.draw.rect(self.shadow_surf, COLORS['paddle shadow'], pygame.FRect((0, 0), SIZE['paddle']), 0, 4)

        #* Rect and movement
        self.rect = self.image.get_frect(center = (POS['player']))
        self.old_rect = self.rect.copy()
        self.direction = 0 #? since player moves only up and down, no need for vector

    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)

class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)
        self.speed = SPEED['player']

    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_s]) - int(keys[pygame.K_w]) 

class Opponent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.speed = SPEED['opponent']
        self.rect.center = POS['opponent'] #? updates the original rect rather than rewriting all the code
        self.ball = ball

    def get_direction(self):
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score

        #* Image
        self.image = pygame.Surface((SIZE['ball']), pygame.SRCALPHA) #? SRCALPHA makes surf invisible
        self.ball_pos = (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2) #? Ball is drawn on top of image
        pygame.draw.circle(self.image, COLORS['ball'], self.ball_pos, self.ball_pos[0])
        # self.image.fill(COLORS['ball'])

        #* Shadow surf
        self.shadow_surf = self.image.copy()
        pygame.draw.circle(self.shadow_surf, COLORS['ball shadow'], self.ball_pos, self.ball_pos[0])

        #* Rect and movement
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.old_rect = self.rect.copy() #? new rect with same pos and size
        self.direction = pygame.Vector2(choice((-1, 1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.speed = SPEED['ball']
        self.speed_modifier = 0

        #* Timer
        self.start_time = pygame.time.get_ticks()
        self.duration = 1000

    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt * self.speed_modifier
        self.collision('horizontal')
        self.rect.centery += self.direction.y * self.speed * dt * self.speed_modifier
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect): #? overlap check
                if direction == 'horizontal':
                    if self.rect.right > sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.x *= -1

    def wall_collison(self):
        #* Top and bottom
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        # #* Left and right (gonna be commented out later)
        # if self.rect.left <= 0:
        #     self.rect.left = 0
        #     self.direction.x *= -1
        # if self.rect.right >= WINDOW_WIDTH:
        #     self.rect.right = WINDOW_WIDTH
        #     self.direction.x *= -1  
        #* Left right collision with score
        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            self.update_score('player' if self.rect.x < WINDOW_WIDTH / 2 else 'opponent')
            self.reset()

    def reset(self):
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.direction = pygame.Vector2(choice((-1, 1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.start_time = pygame.time.get_ticks()

    def timer(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            self.speed_modifier = 1
        else:
            self.speed_modifier = 0

    def update(self, dt):
        self.old_rect = self.rect.copy() #? storing pos of rectangle and updating it every frame
        self.timer()
        self.move(dt)
        self.wall_collison()
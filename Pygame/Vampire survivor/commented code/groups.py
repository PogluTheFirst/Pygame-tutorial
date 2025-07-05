from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2() #? Add this with drawing logic to offset rects and make a camera

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')] #? Checks for ground attribute 
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        for layer in [ground_sprites, object_sprites]: #? Order is important
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery): #? sorted for y sorting
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
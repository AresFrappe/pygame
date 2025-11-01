from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target):
        self.offset.x = -(target[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target[1] - WINDOW_HEIGHT / 2)
        for sprite in self:
            self.display.blit(sprite.image, sprite.rect.topleft + self.offset)
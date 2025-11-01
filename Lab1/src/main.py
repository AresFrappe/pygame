from settings import *
from player import Player, Npc
from sprites import Sprite
from pytmx.util_pygame import load_pygame
from groups import AllSprites


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Simulation")
        self.clock = pygame.time.Clock()

        self.all_sprites = AllSprites()
        self.collide_sprites = pygame.sprite.Group()

        self.setup()

        self.running = True

    def setup(self):
        map = load_pygame(join('assets', 'data', 'map', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collide_sprites))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collide_sprites)
            if obj.name == 'NPC':
                self.npc = Npc((obj.x, obj.y), self.all_sprites, self.collide_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.screen.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
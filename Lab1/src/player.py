from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, image_path=None, scale=(64, 64)):
        super().__init__(groups)
        
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, scale)
        else:
            self.image = pygame.Surface(scale)
            self.image.fill('red')

        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.inflate(-10, 0)

        self.direction = pygame.Vector2()
        self.speed = 200
        self.collision_sprites = collision_sprites

        self.frames = {}
        self.state = 'down'
        self.frame_index = 0

    def load_images(self, base_path):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            folder = join(base_path, state)
            for folder_path, _, file_names in walk(folder):
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surface = pygame.image.load(full_path).convert_alpha()
                    self.frames[state].append(surface)

    def animate(self, dt):
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # Basic frame animation
        if self.direction.length_squared() > 0:
            self.frame_index = (self.frame_index + 0.05 * dt) + 0.05 + 1
        else:
            self.frame_index = 0

        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        self.image = pygame.transform.scale(self.image, (64, 64))

    def move(self, dt):
        # Horizontal
        self.hitbox.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Vertical
        self.hitbox.y += self.direction.y * self.speed * dt
        self.collision('vertical')

        # Sync rect
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom

class Player(Entity):
    def __init__(self, pos, groups, collision_sprites):
        image_path = join('assets', 'images', 'player', 'down', '0.png')
        super().__init__(pos, groups, collision_sprites, image_path=image_path)
        self.speed = 300
        self.load_images(join('assets', 'images', 'player'))

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)

class Npc(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('assets', 'images', 'npc', 'deer', 'right', '0.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (96,96))
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-10, 0)

        self.think = 'idle'
        self.timer = 0
        self.idle_duration = uniform(2, 4)
        self.wander_duration = uniform(3, 5)

        self.speed = 200
        self.wander_distance = 1000

        self.collision_sprites = collision_sprites

    def idle(self, dt):
        self.direction = pygame.Vector2()
        self.timer += dt

        if self.timer >= self.idle_duration:
            self.timer = 0
            self.think = 'wander'

    def wander(self, dt):
        #TODO

        if self.timer >= self.wander_duration: # and self.center == self.randomPos:
            self.timer = 0
            self.think = 'idle'
        pass

    def flee(self, dt):
        #TODO
        pass

    def update(self, dt):

        if self.think == 'idle':
            self.idle(dt)
        if self.think == 'wander': 
            self.wander(dt)


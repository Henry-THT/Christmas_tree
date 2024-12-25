import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Merry Christmas!!!")

background_color = (0, 0, 50)
screen.fill(background_color)

colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (128, 0, 128)]

def draw_tree_crown():
    pygame.draw.polygon(screen, (34, 139, 34), [(400, 100), (300, 250), (500, 250)])
    pygame.draw.polygon(screen, (34, 139, 34), [(400, 200), (250, 350), (550, 350)])
    pygame.draw.polygon(screen, (34, 139, 34), [(400, 300), (200, 450), (600, 450)])

def draw_tree_trunk():
    pygame.draw.rect(screen, (139, 69, 19), (370, 450, 60, 100))

def generate_spiral_lights():
    lights = []
    layers = 6
    lights_per_layer = [7, 9, 11, 13, 15, 13]


    for layer in range(layers):
        base_y = 150 + layer * 50
        layer_width = 200 + layer * 100
        num_lights = lights_per_layer[layer]
        for i in range(num_lights):
            angle = i * (360 / num_lights)
            x = 400 + int((layer_width / 2) * 0.5 * math.cos(math.radians(angle)))
            y = base_y + int(25 * math.sin(math.radians(angle)))

            if math.sin(math.radians(angle)) < 0 :
                continue

            depth = base_y - y
            lights.append((x, y, random.choice(colors), depth))
    return lights



def draw_lights(lights):
        lights.sort(key=lambda light: light[3], reverse=True)
        for x, y, color, _ in lights:
            brightness = random.randint(100, 255)
            dynamic_color = (color[0] * brightness // 255, color[1] * brightness // 255, color[2] * brightness // 255)
            pygame.draw.circle(screen, color, (x, y), 5)

def update_lights(lights):
    for i in range(len(lights)):
        x, y, color, depth = lights[i]
        new_color = random.choice(colors)
        lights[i] = (x, y, new_color, depth)

lights = generate_spiral_lights()

class Snowflake:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

    def fall(self):
        self.y += self.speed
        if self.y > 600:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, 800)
            self.size = random.randint(3, 4)
            self.speed = random.randint(5, 10)


    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.size)

snowflakes = [Snowflake(random.randint(0, WIDTH), random.randint(-50, HEIGHT), random.randint(3, 4), random.randint(5, 10)) for _ in range(100)]


def draw_snowflakes():
    for snowflake in snowflakes:
        snowflake.fall()
        snowflake.draw()

def draw_tree_top_star():
    center = (400, 80)
    star_color = (255, 255, random.randint(100, 255))
    pygame.draw.circle(screen, star_color, center, 10)
    for radius in range(15, 50, 5):
        alpha = random.randint(20, 50)
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 150, alpha), center, radius)
        screen.blit(surface, (0, 0))

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT // 2)
        self.size = random.randint(2, 4)
        self.brightness = random.randint(100, 255)
        self.fade = random.choice([-1, 1])

    def twinkle(self):
        self.brightness += self.fade * random.randint(1, 3)
        if self.brightness > 255:
            self.brightness = 255
            self.fade *= -1
        elif self.brightness < 100:
            self.brightness = 100
            self.fade *= -1


    def draw(self):
        star_surface = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        center = (self.size * 2, self.size * 2)
        points = []
        for i in range(10):
            angle = math.pi / 5 * i
            radius = self.size * 2 if i % 2 == 0 else self.size
            x = center[0] + math.cos(angle) * radius
            y = center[1] + math.sin(angle) * radius
            points.append((x, y))
        pygame.draw.polygon(star_surface, (255, 255, 255), points)
        #pygame.draw.circle(star_surface, (255, 255, 255, self.brightness), (self.size, self.size), self.size)
        star_surface.set_alpha(self.brightness)
        screen.blit(star_surface, (self.x - self.size * 2, self.y - self.size * 2))


stars = [Star() for _ in range(50)]

def draw_stars():
    for star in stars:
        star.twinkle()
        star.draw()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    draw_stars()
    draw_tree_top_star()
    draw_tree_crown()
    draw_tree_trunk()
    draw_lights(lights)
    update_lights(lights)
    draw_snowflakes()

    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(144)
    pygame.time.delay(200)

pygame.quit()

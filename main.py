import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPACESHIP_SPEED = 5
BULLET_SPEED = 8
ALIEN_SPEED = 2
ALIEN_FIRE_RATE = 0.02

# Nuevas dimensiones de las imágenes
ALIEN_WIDTH = 64
ALIEN_HEIGHT = 64
SPACESHIP_WIDTH = 64
SPACESHIP_HEIGHT = 64

# Configuración de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Caza de Aliens")

# Cargar imágenes y ajustarlas a las nuevas dimensiones
spaceship_img = pygame.transform.scale(pygame.image.load("sprites/spaceship.png"), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
alien_img = pygame.transform.scale(pygame.image.load("sprites/alien.png"), (ALIEN_WIDTH, ALIEN_HEIGHT))

# Inicializar sonidos
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")

# Clase para la nave espacial
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speedx = 0  # Agregar velocidad horizontal

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -SPACESHIP_SPEED
        elif keys[pygame.K_RIGHT]:
            self.speedx = SPACESHIP_SPEED
        else:
            self.speedx = 0

        # Actualizar posición en función de la velocidad
        self.rect.x += self.speedx

        # Limitar la nave espacial a la pantalla
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

# Clase para los alienígenas
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = alien_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speedy = random.randint(1, ALIEN_SPEED)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -50)
            self.speedy = random.randint(1, ALIEN_SPEED)

# Clase para las balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))  # Tamaño de la bala
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= BULLET_SPEED

# Función para mostrar un mensaje en la pantalla
def show_message(message, font_size, x, y):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)

# Función para el menú principal
def main_menu():
    running = True
    start_game = False  # Variable para confirmar que se inicie el juego

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game = True  # Marcar para iniciar el juego
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        show_message("Caza de Aliens", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        show_message("Presiona Enter para Jugar", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        show_message("Presiona Esc para Salir", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        pygame.display.update()

        if start_game:  # Si se marcó para iniciar el juego, salir del bucle del menú
            break

    return "play"  # Retorna "play" para indicar que el juego debe comenzar

# Función principal del juego
def main():
    pygame.mixer.music.load("sounds/background_music.mp3")
    pygame.mixer.music.play(-1)  # Repetir la música de fondo

    clock = pygame.time.Clock()
    score = 0

    spaceship = Spaceship()
    aliens = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Agregar la nave espacial al grupo de todos los sprites
    all_sprites.add(spaceship)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game_state = main_menu()

        if game_state == "play":
            # Crear la nave espacial y el grupo de sprites fuera del bucle
            spaceship = Spaceship()
            aliens = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            bullets = pygame.sprite.Group()

            # Agregar la nave espacial al grupo de todos los sprites
            all_sprites.add(spaceship)

            for _ in range(10):
                alien = Alien()
                aliens.add(alien)
                all_sprites.add(alien)

            game_over = False

            while not game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            bullet = Bullet(spaceship.rect.centerx, spaceship.rect.top)
                            all_sprites.add(bullet)
                            bullets.add(bullet)
                            shoot_sound.play()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    spaceship.speedx = -SPACESHIP_SPEED
                elif keys[pygame.K_RIGHT]:
                    spaceship.speedx = SPACESHIP_SPEED
                else:
                    spaceship.speedx = 0

                spaceship.rect.x += spaceship.speedx

                all_sprites.update()

                # Detectar colisiones entre balas y alienígenas
                hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
                for hit in hits:
                    explosion_sound.play()
                    score += 1
                    alien = Alien()
                    aliens.add(alien)
                    all_sprites.add(alien)

                # Detectar colisiones entre la nave espacial y los alienígenas
                hits = pygame.sprite.spritecollide(spaceship, aliens, False)
                if hits:
                    game_over = True

                screen.fill(BLACK)
                all_sprites.draw(screen)
                show_message(f"Score: {score}", 24, 70, 10)
                pygame.display.flip()
                clock.tick(60)

            game_state = "menu"

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

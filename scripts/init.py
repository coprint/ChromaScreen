import pygame

logo_path = "/home/noya/init.png"

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
logo = pygame.image.load(logo_path)
logo = pygame.transform.scale(logo, screen.get_size())
screen.blit(logo, (0, 0))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
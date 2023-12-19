import pygame


def blit_rotate_center(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rect.topleft)


def draw_car(screen, player_car, images, camera_offset):
    for img, pos in images:
        screen.blit(img, (pos[0] - camera_offset.x, pos[1] - camera_offset.y))

    player_car.draw(screen, camera_offset)
    pygame.display.update()


def move_player(player, keys: any):
    moved = False

    if keys[pygame.K_LEFT]:
        player.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player.move_forward()

    if keys[pygame.K_DOWN]:
        moved = True
        player.move_backward()

    if not moved:
        player.reduce_speed()


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_text_center(window, font, text):
    render = font.render(text, 1, (0, 0, 0))
    window.blit(render, (window.get_width()/2 - render.get_width() /2, window.get_height()/2 - render.get_height()/2))

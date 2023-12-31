import time
import pygame
import numpy as np

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (0, 120, 120)
COLOR_ALIVE_NEXT = (255, 255, 255)

SIZE = 5
WIDTH = 180
HEIGHT = 100




def draw_text(text, font, text_color, x, y, screen):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def main():
    pygame.init()

    font_size = 18
    text_font = pygame.font.SysFont("Mono", font_size)
    text_x = 100
    text_y = 502

    screen = pygame.display.set_mode((WIDTH * SIZE, HEIGHT * 1.2 * SIZE))

    draw_text("mouse click - spawn alive cells", text_font, COLOR_ALIVE_NEXT, text_x, text_y, screen)
    draw_text("space - pause/unpause", text_font, COLOR_ALIVE_NEXT, text_x, text_y + font_size, screen)
    draw_text("r - random cells", text_font, COLOR_ALIVE_NEXT, text_x, text_y + (2 * font_size), screen)
    draw_text("c - clear", text_font, COLOR_ALIVE_NEXT, text_x, text_y + (3 * font_size), screen)

    cells = np.zeros((HEIGHT, WIDTH))
    # screen.fill(COLOR_GRID)
    update(screen, cells, SIZE)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, SIZE)
                    pygame.display.update()
                if event.key == pygame.K_r:
                    random = np.random.randint(2, size=(HEIGHT, WIDTH))
                    cells = random
                    update(screen, cells, SIZE)
                    pygame.display.update()
                if event.key == pygame.K_c:
                    cells = np.zeros((HEIGHT, WIDTH))
                    update(screen, cells, SIZE)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // SIZE, pos[0] // SIZE] = 1
                update(screen, cells, SIZE)
                pygame.display.update()

        # screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, SIZE, with_progress=True)
            pygame.display.update()

        time.sleep(0.005)


if __name__ == '__main__':
    main()

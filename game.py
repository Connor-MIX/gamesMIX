import pygame
import random
import time

pygame.init()  # Обязательная инициализация Pygame

# Полный экран
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

pygame.display.set_caption("Click the circles!")  # Название окна

# Цвета
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# Остальные константы
version = "v_0.0.5"
radius = 50
time_limit = 1 # Это время, за которое нужно успеть нажать на круг

# Различные шрифты
font24 = pygame.font.SysFont("Times New Roman", 24)
font24_italic = pygame.font.SysFont("Times New Roman", 24, italic=True)

font48 = pygame.font.SysFont("Times New Roman", 48)
font48_bold = pygame.font.SysFont("Times New Roman", 48, bold=True)

font60 = pygame.font.SysFont("Times New Roman", 60)

font72_osuMIX = pygame.font.SysFont("Times New Roman", 72, bold=True, italic=True)


def start():
    screen.fill(BLACK)  # Весь экран в чёрный

    osuMIX_text = font72_osuMIX.render("Click the circles!", True, WHITE) # Текст, сглаживание, цвет
    osuMIX_rect = osuMIX_text.get_rect(center=(width // 2, height // 2 - 100)) # Местоположение кнопки
    screen.blit(osuMIX_text, osuMIX_rect) # Отображение

    # Это уже кнопка, но пока суть та же
    start_button = font60.render("Start", True, WHITE)
    start_rect = start_button.get_rect(center=(width // 2, height // 2))
    screen.blit(start_button, start_rect)

    quit_button = font48.render("Quit", True, WHITE)
    quit_rect = quit_button.get_rect(center=(width // 2, height // 2 + 60))
    screen.blit(quit_button, quit_rect)

    version_button = font24.render(version, True, WHITE)
    version_rect = version_button.get_rect(bottomright=(width - 10, height - 40))  # Правый нижний угол, но чуть повыше
    screen.blit(version_button, version_rect)

    author_text = font24_italic.render("by ConnorMIX", True, WHITE)  # Курсивный текст
    author_rect = author_text.get_rect(bottomright=(width - 10, height - 10))  # Правый нижний угол
    screen.blit(author_text, author_rect)

    pygame.display.flip()  # Рендер короче

    return start_rect, quit_rect

def circle(combo):
    while True: # Бесконечный цикл, который будет продолжаться до тех пор, пока не будет найдено подходящее положение для круга
        # Рандом координаты в диапозоне от a до b (a, b). За счёт "... - radius" круги не будут выходить за экран
        x = random.randint(radius, width - radius)
        y = random.randint(radius, height - radius)
        
        # Определяем область комбо в геймплее
        combo_text = font48.render(f"Combo: {combo}", True, WHITE)
        combo_rect = combo_text.get_rect(bottomleft=(10, height - 10))
        
        # Проверяем, попадает ли круг в область Combo
        circle_rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        if not combo_rect.colliderect(circle_rect):
            return (x, y)

def gg(combo):
    # Функция Game Over короче (а победить в моей игре нельзя, хахаха)
    screen.fill(BLACK)

    osuMIX_text = font72_osuMIX.render("Click the circles!", True, WHITE)
    osuMIX_rect = osuMIX_text.get_rect(center=(width // 2, height // 2 - 150))
    screen.blit(osuMIX_text, osuMIX_rect)

    gg_text = font48_bold.render(f"Game Over! Combo: {combo}", True, WHITE)  # По шрифту 48-го размера рендерим текст, как раньше
    gg_rect = gg_text.get_rect(center=(width // 2, height // 2 - 40))
    screen.blit(gg_text, gg_rect)

    restart_button = font48.render("Restart", True, WHITE)
    restart_rect = restart_button.get_rect(center=(width // 2, height // 2 + 20))
    screen.blit(restart_button, restart_rect)

    quit_button = font48.render("Quit", True, WHITE)
    quit_rect = quit_button.get_rect(center=(width // 2, height // 2 + 70))
    screen.blit(quit_button, quit_rect)

    # Тут чисто всё работает также, что и в функции start
    version_text = font24.render(version, True, WHITE)
    version_rect = version_text.get_rect(bottomright=(width - 10, height - 40))
    screen.blit(version_text, version_rect)

    author_text = font24_italic.render("by ConnorMIX", True, WHITE)
    author_rect = author_text.get_rect(bottomright=(width - 10, height - 10))
    screen.blit(author_text, author_rect)

    pygame.display.flip()

    return restart_rect, quit_rect

# Начинаем суету
running = True
show_start = True

while running:
    if show_start: # Если show_start = True
        start_rect, quit_rect = start() # Наши кнопки из функции start
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Если игрок нажал на Quit, то...
                running = False # ...весь running оффается и игра закрывается.
            if event.type == pygame.MOUSEBUTTONDOWN: # Снова "повтор", но мы смотрим, куда именно нажал игрок
                mouse_x, mouse_y = event.pos # Узнаём корды курсора во время нажатия
                if start_rect.collidepoint(mouse_x, mouse_y): # Если курсор находится в области Start, то...
                    show_start = False # ...функция start закрывается и переходим к геймплею.
                elif quit_rect.collidepoint(mouse_x, mouse_y): # Если же курсор находится в области Quit, то соответственно...
                    running = False # ...выход из игры.

    else: # А это наш основной геймплей в else)
        combo = 0 # Константа отсутсвия комбо
        game_over = False
        current_circle_pos = circle(combo) # Координаты текущего круга
        current_circle_color = WHITE # Цвет текущего круга
        next_circle_pos = circle(combo) # Координаты следующего круга

        while not game_over: # "Пока game_over != True", игра будет продолжаться
            screen.fill(BLACK)

            # Создаём сразу 2 круга разных цветов: белый - текущий, серый - следующий круг
            pygame.draw.circle(screen, current_circle_color, current_circle_pos, radius, 8)
            pygame.draw.circle(screen, GRAY, next_circle_pos, radius, 8)

            start_time = time.time() # Используем библиотеку времени
            clicked = False # Следим, было ли нажатие на круг

            while time.time() - start_time < time_limit: # Цикл будет выполняться, пока не истечет 1 секунда (time_limit)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        game_over = True
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        distance_current = ((mouse_x - current_circle_pos[0]) ** 2 + (mouse_y - current_circle_pos[1]) ** 2) ** 0.5 # Теорема Пифагора
                        
                        if distance_current < radius: # Короче, если попал по кругу:
                            combo += 1 # +1 к комбо
                            clicked = True
                            current_circle_pos = next_circle_pos # Текущий круг становится следующим...
                            current_circle_color = WHITE # ...и перекрашивается с серого в белый.
                            next_circle_pos = circle(combo) # И создаём новый серый круг
                            break
                        else: # Если не попал по кругу:
                            game_over = True # Game Over)
                            break

                if game_over: # Если game_over выше = True, то...
                    break # ...выходим из цикла.

                combo_text = font48.render(f"Combo: {combo}", True, WHITE) # Показываем комбо в геймплее
                combo_rect = combo_text.get_rect(bottomleft=(10, height - 10)) # Правый нижний угол
                screen.blit(combo_text, combo_rect)
                pygame.display.flip()

                if clicked: # Если clicked = True, то...
                    break # ...выходим из цикла.

            if not clicked: # Если не нажал, то...
                restart_rect, quit_rect = gg(combo) # Вызываем функцию game over
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            game_over = True
                            break
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x, mouse_y = event.pos

                            # Если игрок нажал на Restart после проигрыша, то всё по новой крч)
                            if restart_rect.collidepoint(mouse_x, mouse_y):
                                game_over = False
                                combo = 0
                                current_circle_pos = circle(combo)
                                next_circle_pos = circle(combo)
                                current_circle_color = WHITE
                                break
                            if quit_rect.collidepoint(mouse_x, mouse_y):
                                running = False
                                game_over = True
                                break
                    else:
                        continue 
                    break 
            if game_over:
                break 

pygame.quit() # Выходим из игры
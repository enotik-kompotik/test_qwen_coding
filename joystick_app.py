import pygame
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

# Настройки точки
dot_radius = 15
dot_pos = [WIDTH // 2, HEIGHT // 3]
dot_speed = 5

# Настройки джойстика
joystick_center = [WIDTH // 2, HEIGHT * 2 // 3]
joystick_max_radius = 80
joystick_stick_radius = 30
joystick_pos = [joystick_center[0], joystick_center[1]]

# Состояние клавиш
keys = {
    'W': False,
    'A': False,
    'S': False,
    'D': False
}

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Управление точкой: Джойстик + WASD")
clock = pygame.time.Clock()

def draw_dot():
    """Рисует красную точку"""
    pygame.draw.circle(screen, RED, (int(dot_pos[0]), int(dot_pos[1])), dot_radius)

def draw_joystick():
    """Рисует джойстик"""
    # Внешний круг (база)
    pygame.draw.circle(screen, GRAY, joystick_center, joystick_max_radius, 3)
    # Внутренний круг (стик)
    pygame.draw.circle(screen, DARK_GRAY, (int(joystick_pos[0]), int(joystick_pos[1])), joystick_stick_radius)

def update_dot_position():
    """Обновляет позицию точки на основе ввода"""
    dx, dy = 0, 0
    
    # Управление через WASD
    if keys['W']:
        dy -= dot_speed
    if keys['S']:
        dy += dot_speed
    if keys['A']:
        dx -= dot_speed
    if keys['D']:
        dx += dot_speed
    
    # Управление через джойстик
    joy_dx = joystick_pos[0] - joystick_center[0]
    joy_dy = joystick_pos[1] - joystick_center[1]
    joy_distance = math.sqrt(joy_dx**2 + joy_dy**2)
    
    if joy_distance > 0:
        # Нормализуем и масштабируем скорость джойстика
        joy_speed = min(joy_distance / joystick_max_radius, 1.0) * dot_speed
        dx += (joy_dx / joy_distance) * joy_speed
        dy += (joy_dy / joy_distance) * joy_speed
    
    # Обновляем позицию
    dot_pos[0] += dx
    dot_pos[1] += dy
    
    # Ограничиваем точку пределами экрана
    dot_pos[0] = max(dot_radius, min(WIDTH - dot_radius, dot_pos[0]))
    dot_pos[1] = max(dot_radius, min(HEIGHT - dot_radius - 150, dot_pos[1]))  # Оставляем место для джойстика

def handle_joystick_input(mouse_pos):
    """Обрабатывает движение джойстика"""
    dx = mouse_pos[0] - joystick_center[0]
    dy = mouse_pos[1] - joystick_center[1]
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance <= joystick_max_radius:
        joystick_pos[0] = mouse_pos[0]
        joystick_pos[1] = mouse_pos[1]
    else:
        angle = math.atan2(dy, dx)
        joystick_pos[0] = joystick_center[0] + math.cos(angle) * joystick_max_radius
        joystick_pos[1] = joystick_center[1] + math.sin(angle) * joystick_max_radius

def reset_joystick():
    """Возвращает джойстик в центральное положение"""
    joystick_pos[0] = joystick_center[0]
    joystick_pos[1] = joystick_center[1]

# Основной цикл
running = True
joystick_active = False

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Обработка нажатий клавиш
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys['W'] = True
            elif event.key == pygame.K_a:
                keys['A'] = True
            elif event.key == pygame.K_s:
                keys['S'] = True
            elif event.key == pygame.K_d:
                keys['D'] = True
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys['W'] = False
            elif event.key == pygame.K_a:
                keys['A'] = False
            elif event.key == pygame.K_s:
                keys['S'] = False
            elif event.key == pygame.K_d:
                keys['D'] = False
        
        # Обработка мыши для джойстика
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            dx = mouse_pos[0] - joystick_center[0]
            dy = mouse_pos[1] - joystick_center[1]
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance <= joystick_max_radius + joystick_stick_radius:
                joystick_active = True
                handle_joystick_input(mouse_pos)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            joystick_active = False
            reset_joystick()
        
        elif event.type == pygame.MOUSEMOTION:
            if joystick_active:
                handle_joystick_input(event.pos)
    
    # Обновление позиции точки
    update_dot_position()
    
    # Отрисовка
    screen.fill(WHITE)
    draw_dot()
    draw_joystick()
    
    # Подсказка
    font = pygame.font.Font(None, 24)
    text = font.render("Управление: WASD или джойстик ниже", True, BLACK)
    screen.blit(text, (10, 10))
    
    pygame.display.flip()

pygame.quit()

from random import randint, choice
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Константа для всех возможных ячеек
ALL_CELLS = {(x * GRID_SIZE, y * GRID_SIZE) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

class GameObject:
    """Базовый класс для объектов в игре."""
    
    def __init__(self, position=(0, 0)):
        """Инициализирует объект."""
        self.position = position
        self.body_color = (0, 0, 0)

    def draw(self):
        """Метод для отрисовки объекта."""
        pass

class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, snake_positions):
        """Задает цвет яблока и устанавливает его начальную позицию."""
        super().__init__(self.randomize_position(snake_positions))
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_positions):
        """Устанавливает случайное положение яблока на игровом поле, избегая змейки."""
        occupied_cells = set(snake_positions)  # Занятые позиции
        free_cells = ALL_CELLS - occupied_cells  # Свободные позиции
        self.position = choice(tuple(free_cells))  # Выбор случайной свободной позиции
        return self.position

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        start_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(start_position)
        self.body_color = SNAKE_COLOR
        self.length = 1  # Начальная длина змейки
        self.positions = [start_position]  # Начальная позиция
        self.direction = RIGHT  # Начальное направление
        self.next_direction = None  # Следующее направление
        self.high_score = 1  # Рекордный размер змейки

        # Словарь для управления направлениями
        self.direction_map = {
            (pygame.K_UP, RIGHT): UP,
            (pygame.K_DOWN, RIGHT): DOWN,
            (pygame.K_LEFT, RIGHT): LEFT,
            (pygame.K_RIGHT, RIGHT): RIGHT,
            (pygame.K_UP, LEFT): UP,
            (pygame.K_DOWN, LEFT): DOWN,
            (pygame.K_LEFT, UP): LEFT,
            (pygame.K_RIGHT, UP): RIGHT,
            (pygame.K_UP, DOWN): UP,
            (pygame.K_DOWN, UP): DOWN,
            (pygame.K_LEFT, DOWN): LEFT,
            (pygame.K_RIGHT, DOWN): RIGHT,
            (pygame.K_UP, DOWN): UP,
            (pygame.K_DOWN, UP): DOWN,
            (pygame.K_LEFT, RIGHT): LEFT,
            (pygame.K_RIGHT, LEFT): RIGHT,
        }

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку."""
        x, y = self.get_head_position()
        new_position = (
            (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Проверка на столкновение с собой только если длина змейки больше 2
        if len(self.positions) > 2 and new_position in self.positions[2:]:
            self.reset()
            return

        # Добавляем новую позицию головы
        self.positions.insert(0, new_position)

        # Если длина змейки больше, чем 1, удаляем последний сегмент
        if len(self.positions) > self.length:
            self.positions.pop()  # Удаляем последний сегмент, если длина не увеличилась

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT  # Изменяем на фиксированное направление
        self.next_direction = None

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def handle_keys(self):
        """Обрабатывает действия пользователя."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Обработка нажатия Esc
                    pygame.quit()
                    raise SystemExit
                
                # Извлечение нового направления из словаря
                new_direction = self.direction_map.get((event.key, self.direction), self.direction)
                if new_direction != self.direction:
                    self.next_direction = new_direction

def main():
    """Основная функция для запуска игры."""
    pygame.display.set_caption("Змейка — Рекордный размер: 1")
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Обработка событий и обновление направления
        snake.handle_keys()
        snake.update_direction()
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Увеличиваем длину змейки
            apple.randomize_position(snake.positions)  # Устанавливаем позицию яблока
            # Обновляем рекордный размер и заголовок окна
            if snake.length > snake.high_score:
                snake.high_score = snake.length
                pygame.display.set_caption(f"Змейка — Рекордный размер: {snake.high_score}")

        # Отрисовка объектов
        snake.draw()
        apple.draw()

        # Обновление дисплея
        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    main()

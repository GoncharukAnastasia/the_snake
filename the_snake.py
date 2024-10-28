from random import randint
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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
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

    def __init__(self):
        """Задает цвет яблока и устанавливает его начальную позицию."""
        super().__init__(self.randomize_position())
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )
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

        # Проверка на столкновение с собой
        if new_position in self.positions[2:]:
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


def handle_keys(snake):
    """Обрабатывает действия пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция для запуска игры."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Обработка событий и обновление направления
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Увеличиваем длину змейки
            apple.randomize_position()

        # Отрисовка объектов
        snake.draw()
        apple.draw()

        # Обновление дисплея
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    main()

import sys
import random
import pygame

# Initialize Pygame
pygame.init()

# Define constants
CELL_SIZE = 40
GRID_SIZE = 10
MINE_COUNT = 10
SCREEN_SIZE = CELL_SIZE * GRID_SIZE
FONT = pygame.font.Font(None, 30)

# Timer and score
start_time = pygame.time.get_ticks()
score = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Cell colors
COLORS = {
    1: BLUE,
    2: GREEN,
    3: RED,
    4: pygame.Color("darkblue"),
    5: pygame.Color("darkred"),
    6: pygame.Color("turquoise"),
    7: BLACK,
    8: GREY,
}

# Create a window
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Minesweeper")


def generate_board(size, mine_count):
    # Generate a board filled with zeroes
    board = [[0 for _ in range(size)] for _ in range(size)]

    # Place mines randomly
    mines = 0
    while mines < mine_count:
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        if board[y][x] == 0:
            board[y][x] = -1
            mines += 1

    # Calculate numbers for non-mine cells
    for y in range(size):
        for x in range(size):
            if board[y][x] == -1:
                continue

            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size and board[ny][nx] == -1:
                        board[y][x] += 1

    return board


def draw_board(board, revealed, flagged):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE,
                                    CELL_SIZE)
            pygame.draw.rect(screen, GREY, cell_rect, 3)

            if revealed[y][x]:
                if board[y][x] == -1:
                    pygame.draw.circle(screen, BLACK, cell_rect.center, CELL_SIZE // 4)
                elif board[y][x] > 0:
                    text_surface = FONT.render(str(board[y][x]), True,
                                               COLORS[board[y][x]])
                    screen.blit(text_surface,
                                text_surface.get_rect(center=cell_rect.center))
            elif flagged[y][x]:
                pygame.draw.polygon(screen, RED, (
                    (cell_rect.left + CELL_SIZE // 2, cell_rect.top + CELL_SIZE // 4),
                    (cell_rect.right - CELL_SIZE // 4,
                     cell_rect.bottom - CELL_SIZE // 4),
                    (cell_rect.left + CELL_SIZE // 4, cell_rect.bottom - CELL_SIZE // 4),
                ))


def draw_timer_and_score(score):
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = FONT.render(f"Time: {elapsed_time}s", True, BLACK)
    score_text = FONT.render(f"Score: {score}", True, BLACK)

    screen.blit(timer_text, (5, 5))
    screen.blit(score_text, (SCREEN_SIZE - 100, 5))


def reveal_cell(board, revealed, x, y):
    revealed[y][x] = True
    if board[y][x] == 0:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and not revealed[ny][nx]:
                    reveal_cell(board, revealed, nx, ny)


def calculate_score(board, flagged):
    correct_flags = 0
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] == -1 and flagged[y][x]:
                correct_flags += 1
    return correct_flags


def game_loop(board):
    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    flagged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False

    while not game_over:
        screen.fill(WHITE)
        draw_board(board, revealed, flagged)
        score = calculate_score(board, flagged)
        draw_timer_and_score(score)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                    if not flagged[grid_y][grid_x]:
                        if board[grid_y][grid_x] == -1:
                            revealed = [[True for _ in range(GRID_SIZE)]
                                        for _ in range(GRID_SIZE)]
                        else:
                            reveal_cell(board, revealed, grid_x, grid_y)
                elif event.button == 3:  # Right click
                    x, y = event.pos
                    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                    flagged[grid_y][grid_x] = not flagged[grid_y][grid_x]

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    board = generate_board(GRID_SIZE, MINE_COUNT)
    game_loop(board)

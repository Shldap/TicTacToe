import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 400
HEIGHT = 400
LINE_WIDTH = 6
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE

# Colors
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
PLAYER_X_COLOR = (255, 0, 0)
PLAYER_O_COLOR = (0, 0, 255)

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Game state
board = [['', '', ''],
         ['', '', ''],
         ['', '', '']]
current_player = 'X'
game_over = False
winner = None
player_name = {'X': 'Player 1', 'O': 'Player 2'}
single_player_mode = False

# Function to draw the game board
def draw_board():
    window.fill(BG_COLOR)
    pygame.draw.line(window, LINE_COLOR, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(window, LINE_COLOR, (0, 2 * CELL_SIZE), (WIDTH, 2 * CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(window, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(window, LINE_COLOR, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, HEIGHT), LINE_WIDTH)

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            if board[row][col] == 'X':
                pygame.draw.line(window, PLAYER_X_COLOR, (x - 50, y - 50), (x + 50, y + 50), LINE_WIDTH)
                pygame.draw.line(window, PLAYER_X_COLOR, (x + 50, y - 50), (x - 50, y + 50), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(window, PLAYER_O_COLOR, (x, y), 50, LINE_WIDTH)

    pygame.display.update()

# Function to handle a player's move
def make_move(row, col):
    global current_player, game_over, winner

    if board[row][col] == '':
        board[row][col] = current_player

        if check_win(current_player):
            game_over = True
            winner = current_player
        elif check_draw():
            game_over = True
            winner = 'Draw'
        else:
            current_player = 'O' if current_player == 'X' else 'X'

# Function to check if a player has won
def check_win(player):
    # Check rows
    for row in range(BOARD_SIZE):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True

    # Check columns
    for col in range(BOARD_SIZE):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False

# Function to check if the game is a draw
def check_draw():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == '':
                return False
    return True

# Function to reset the game
def reset_game():
    global board, current_player, game_over, winner
    board = [['', '', ''],
             ['', '', ''],
             ['', '', '']]
    current_player = 'X'
    game_over = False
    winner = None
    draw_board()

# Function to perform the AI's move (in single-player mode)
def ai_move():
    available_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == '':
                available_moves.append((row, col))
    
    if available_moves:
        row, col = random.choice(available_moves)
        make_move(row, col)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = event.pos
            clickedrow = mouse_y // CELL_SIZE
            clicked_col = mouse_x // CELL_SIZE
            make_move(clicked_row, clicked_col)
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()

    draw_board()

    if game_over:
        font = pygame.font.Font(None, 40)
        if winner == 'Draw':
            text = font.render("It's a Draw!", True, LINE_COLOR)
        else:
            text = font.render(f"{player_name[winner]} wins!", True, LINE_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(text, text_rect)
        restart_text = font.render("Press 'R' to restart", True, LINE_COLOR)
        restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        window.blit(restart_text, restart_text_rect)
    elif single_player_mode and current_player == 'O':
        ai_move()

    pygame.display.update()

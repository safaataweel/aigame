import subprocess
import time

import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH = 700
HEIGHT = 700
window_size = (700, 700)

# Define line widths and board dimensions
LINE_WIDTH = 5
WIN_LINE_WIDTH = 15
BOARD_ROWS = 8
BOARD_COLS = 8

# Define square size and width
SQUARE_SIZE = 70
SQUARE_WIDTH = 20

# Define space between squares
SPACE = 20
fps = 60
fpsClock = pygame.time.Clock()
# Define custom colors for the chessboard squares
light_square_color = (250, 223, 181)
dark_square_color = (139, 62, 47)

# Define the font and text colors
font_size = 32
BG_COLOR = (250, 200, 250)
LINE_COLOR = (23, 145, 135)
SQUARE_COLOR = (255, 255, 255)  # White color for square
SQUARE_COLOR1 = (0, 0, 0)  # Black color for square
TEXT_COLOR = (255, 0, 0)  # Red color for winner text

# Set the font and create the game window
font = pygame.font.Font(None, font_size)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Magnatic Cave')
screen.fill(BG_COLOR)

# Create the game board as a 2D numpy array
board = np.zeros((BOARD_ROWS, BOARD_COLS))
objects = []
# Define colors for players
player_colors = {
    1: (255, 255, 255),  # White color for player 1
    2: (0, 0, 0)  # Black color for player 2
}


# create a button
class Button():
    def __init__(self, x, y, width, height, buttonText='return to menu', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ff7778',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = pygame.font.Font(None, font_size).render(buttonText, True, (20, 20, 20))
        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.onclickFunction()
            else:
                self.buttonSurface.fill(self.fillColors['hover'])
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def open_app():
    subprocess.Popen(["python", "first.py"])


button_width = 100
button_height = 80
button_x = (WIDTH - button_width) // 2
button_y = HEIGHT - button_height - 5

button = Button(button_x, button_y, button_width, button_height, 'Menu', open_app)


def draw_lines():
    # Draw the chessboard
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            # Calculate the position and size of each square
            square_rect = pygame.Rect(col * SQUARE_SIZE + SQUARE_WIDTH, row * SQUARE_SIZE + SQUARE_WIDTH,
                                      SQUARE_SIZE, SQUARE_SIZE)
            # Alternate the color of the squares
            square_color = light_square_color if (row + col) % 2 == 0 else dark_square_color
            # Draw the square on the screen
            pygame.draw.rect(screen, square_color, square_rect)

    # Draw row numbers on the left side
    for row in range(BOARD_ROWS):
        # Create a text surface for each row number
        text = font.render(str(BOARD_ROWS - row), True, TEXT_COLOR)
        # Calculate the position of the text on the left side
        text_rect = text.get_rect(center=(int(SQUARE_WIDTH / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)))
        # Draw the text on the screen
        screen.blit(text, text_rect)

    # Draw column characters on the top side
    for col in range(BOARD_COLS):
        # Create a text surface for each column character
        text = font.render(chr(65 + col), True, TEXT_COLOR)
        # Calculate the position of the text on the top side
        text_rect = text.get_rect(center=(int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(SQUARE_WIDTH / 2)))
        # Draw the text on the screen
        screen.blit(text, text_rect)

    # Draw row numbers on the right side
    for row in range(BOARD_ROWS):
        # Create a text surface for each row number
        text = font.render(str(BOARD_ROWS - row), True, TEXT_COLOR)
        # Calculate the position of the text on the right side
        text_rect = text.get_rect(center=(int(WIDTH - SQUARE_WIDTH / 0.2), int(row * SQUARE_SIZE + SQUARE_SIZE / 1)))
        # Draw the text on the screen
        screen.blit(text, text_rect)

    # Draw column characters on the bottom side
    for col in range(BOARD_COLS):
        # Create a text surface for each column character
        text = font.render(chr(65 + col), True, TEXT_COLOR)
        # Calculate the position of the text on the bottom side with a slight vertical adjustment
        text_rect = text.get_rect(center=(int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                                          int(HEIGHT - SQUARE_WIDTH / 0.2)))  # Adjust the vertical position as desired
        # Draw the text on the screen
        screen.blit(text, text_rect)


def draw_figures():
    # Draw the player figures on the board
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                # Draw a white figure for player 1
                pygame.draw.rect(screen, SQUARE_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE,
                                  SQUARE_SIZE - 2 * SPACE, SQUARE_SIZE - 2 * SPACE), SQUARE_WIDTH)
            elif board[row][col] == 2:
                # Draw a black figure for player 2
                pygame.draw.rect(screen, SQUARE_COLOR1,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE,
                                  SQUARE_SIZE - 2 * SPACE, SQUARE_SIZE - 2 * SPACE), SQUARE_WIDTH)


def is_legal_move(row, col):
    # Check if the move is legal
    if col == 0 or col == BOARD_COLS - 1:
        # Brick is stacked directly on the left or right wall
        return True
    elif col > 0 and board[row][col - 1] != 0:
        # Brick is stacked to the left of another brick
        return True
    elif col < BOARD_COLS - 1 and board[row][col + 1] != 0:
        # Brick is stacked to the right of another brick
        return True
    else:
        return False


def mark_square(row, col, player):
    # Mark a square on the board with the player's number
    board[row][col] = player


def available_square(row, col):
    if 0 <= row < 8 and 0 <= col < 8:
        return board[row][col] == 0
    return False


def is_board_full():
    # Check if the board is full (all squares are marked by players)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True


# Check for a win condition for the specified player
def check_win(player):
    # Check horizontal lines iterates over each row and checks five columns If all the five squares in a row, starting from the current column, are marked with the same player's value, it means that player has won
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and \
                    board[row][col + 3] == player and board[row][col + 4] == player:
                return True

    # Check vertical lines
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 4):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and \
                    board[row + 3][col] == player and board[row + 4][col] == player:
                return True

    # Check diagonal lines (top-left to bottom-right)
    for row in range(BOARD_ROWS - 4):
        for col in range(BOARD_COLS - 4):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and \
                    board[row + 3][col + 3] == player and board[row + 4][col + 4] == player:
                return True

    # Check diagonal lines (bottom-left to top-right)
    for row in range(4, BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and \
                    board[row - 3][col + 3] == player and board[row - 4][col + 4] == player:
                return True

    return False


def print_winner(player):
    # Print the winner on the screen
    player_color = "Black" if player == 2 else "White"
    font = pygame.font.Font(None, 48)
    text = font.render(f"Player {player_color} wins!", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)


def restart():
    # Restart the game by resetting the board and other variables
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


##------------------------------------------minmax---------------------------------------------#
def evaluate_board():
    # Check if any player has already won
    if check_win(1):
        return -1  # Human wins
    elif check_win(2):
        return 1  # Computer wins

    # Define the weights for each position on the board
    weights = [
        [4, 3, 4, 3, 4, 3, 4, 3],
        [3, 5, 3, 5, 3, 5, 3, 5],
        [4, 3, 4, 3, 4, 3, 4, 3],
        [3, 5, 3, 5, 3, 5, 3, 5],
        [4, 3, 4, 3, 4, 3, 4, 3],
        [3, 5, 3, 5, 3, 5, 3, 5],
        [4, 3, 4, 3, 4, 3, 4, 3],
        [3, 5, 3, 5, 3, 5, 3, 5]
    ]

    score = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] == 2:
                # Increase score for the maximizing player based on weights
                score += weights[row][col]
            elif board[row][col] == 1:
                # Decrease score for the minimizing player based on weights
                score -= weights[row][col]

    # Count the number of potential winning moves for each player
    computer_moves = count_moves(board, 2)
    human_moves = count_moves(board, 1)

    # Adjust the score based on the number of potential moves for each player
    score += computer_moves
    score -= human_moves

    return score


def count_moves(board, player):
    # Evaluate the current board state based on the number of potential winning moves for each player
    human_moves = 0
    computer_moves = 0

    # Check horizontal lines
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            count = 0
            empty_cell = None
            for i in range(5):
                if board[row][col + i] == player:
                    count += 1
                elif board[row][col + i] == 0:
                    if i == 2 and board[row][col + i + 1] == player and board[row][col + i + 2] == player:
                        empty_cell = (row, col + i)
                        break
                    elif i == 3 and board[row][col + i + 1] == player:
                        empty_cell = (row, col + i)
                        break
                    if i == 1 and board[row][col + i + 1] == player and board[row][col + i + 2] == player:
                        empty_cell = (row, col + i)
                        break
                    else:
                        empty_cell = None
                else:
                    count = 0
                    empty_cell = None
                    break
            if count == 4 and empty_cell:
                if is_legal_move(empty_cell[0], empty_cell[1]):
                    human_moves += 1
            elif count == 0:
                computer_moves += 1

    # Check vertical lines
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 4):
            count = 0
            empty_cell = None
            for i in range(5):
                if board[row + i][col] == player:
                    count += 1
                elif board[row + i][col] == 0:
                    if i == 2 and board[row + i + 1][col] == player and board[row + i + 2][col] == player:
                        empty_cell = (row + i, col)
                        break
                    elif i == 3 and board[row + i + 1][col] == player:
                        empty_cell = (row + i, col)
                        break
                    if i == 1 and board[row + i + 1][col] == player and board[row + i + 2][col] == player:
                        empty_cell = (row + i, col)
                        break
                    else:
                        empty_cell = None
                else:
                    count = 0
                    empty_cell = None
                    break
            if count == 4 and empty_cell:
                if is_legal_move(empty_cell[0], empty_cell[1]):
                    human_moves += 1
            elif count == 0:
                computer_moves += 1

    # Check diagonal lines (top-left to bottom-right)
    for row in range(BOARD_ROWS - 4):
        for col in range(BOARD_COLS - 4):
            count = 0
            empty_cell = None
            for i in range(5):
                if board[row + i][col + i] == player:
                    count += 1
                elif board[row + i][col + i] == 0:
                    if i == 2 and board[row + i + 1][col + i + 1] == player and board[row + i + 2][
                        col + i + 2] == player:
                        empty_cell = (row + i, col + i)
                        break
                    elif i == 3 and board[row + i + 1][col + i + 1] == player:
                        empty_cell = (row + i, col + i)
                        break
                    if i == 1 and board[row + i - 1][col + i - 1] == player and board[row + i + 1][
                        col + i + 1] == player:
                        empty_cell = (row + i, col + i)
                        break
                    else:
                        empty_cell = None
                else:
                    count = 0
                    empty_cell = None
                    break
            if count == 4 and empty_cell:
                if is_legal_move(empty_cell[0], empty_cell[1]):
                    human_moves += 1
            elif count == 0:
                computer_moves += 1

    # Check diagonal lines (bottom-left to top-right)
    for row in range(4, BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            count = 0
            empty_cell = None
            for i in range(5):
                if board[row - i][col + i] == player:
                    count += 1
                elif board[row - i][col + i] == 0:
                    if i == 2 and board[row - i - 1][col + i + 1] == player and board[row - i - 2][
                        col + i + 2] == player:
                        empty_cell = (row - i, col + i)
                        break
                    elif i == 3 and board[row - i - 1][col + i + 1] == player:
                        empty_cell = (row - i, col + i)
                        break
                    if i == 1 and board[row - i + 1][col + i - 1] == player and board[row - i - 1][
                        col + i + 1] == player:
                        empty_cell = (row - i, col + i)
                        break
                    else:
                        empty_cell = None
                else:
                    count = 0
                    empty_cell = None
                    break
            if count == 4 and empty_cell:
                if is_legal_move(empty_cell[0], empty_cell[1]):
                    human_moves += 1
            elif count == 0:
                computer_moves += 1

    # Advanced Diagonal Patterns
    for row in range(BOARD_ROWS - 5):
        for col in range(BOARD_COLS - 5):
            pattern = [board[row + i][col + i] for i in range(6)]
            if pattern.count(player) == 3 and pattern.count(0) >= 2:
                if is_legal_move(row + 3, col + 3):  # Place piece in the empty cell
                    human_moves += 1

    # Blocked Winning Moves
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if np.array_equal(board[row][col:col + 4], [player, 0, player, 2]):
                if is_legal_move(row, col + 1):  # Place piece in the empty cell
                    human_moves += 1

    # Calculate the heuristic value based on the difference between the number of moves
    heuristic_value = computer_moves - human_moves

    return heuristic_value


# Minimax algorithm with alpha-beta pruning
def minimax(depth, maximizing_player, alpha, beta):
    # Check if the maximum depth has been reached or the board is full
    if depth == 0 or is_board_full():
        return evaluate_board()

    if maximizing_player:
        # It is the maximizing player's turn (computer)
        max_eval = float('-inf')

        # Iterate over each cell on the board
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col) and is_legal_move(row, col):
                    # Make a move for the computer (player 2)
                    board[row][col] = 2
                    # Recursively call minimax for the next depth with the opposite player (minimizing)
                    eval = minimax(depth - 1, False, alpha, beta)
                    # Undo the move
                    board[row][col] = 0
                    # Update the maximum evaluation value
                    max_eval = max(max_eval, eval)
                    # Update the alpha value (best value for the maximizing player)
                    alpha = max(alpha, eval)
                    # Perform beta cut-off if beta is less than or equal to alpha
                    if beta <= alpha:
                        break  # Beta cut-off
        return max_eval
    else:
        # It is the minimizing player's turn (human player)
        min_eval = float('inf')

        # Iterate over each cell on the board
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col) and is_legal_move(row, col):
                    # Make a move for the human player (player 1)
                    board[row][col] = 1
                    # Recursively call minimax for the next depth with the opposite player (maximizing)
                    eval = minimax(depth - 1, True, alpha, beta)
                    # Undo the move
                    board[row][col] = 0
                    # Update the minimum evaluation value
                    min_eval = min(min_eval, eval)
                    # Update the beta value (best value for the minimizing player)
                    beta = min(beta, eval)
                    # Perform alpha cut-off if beta is less than or equal to alpha
                    if beta <= alpha:
                        break  # Alpha cut-off
        return min_eval


# Get the best move for the computer player using the Minimax algorithm
def get_computer_move():
    # Start the timer to measure execution time
    start_time = time.time()

    # Initialize variables to store the best evaluation and move
    best_eval = float('-inf')
    best_move = None

    # Iterate over each cell on the board
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row, col) and is_legal_move(row, col):
                # Make a move for the computer (player 2)
                board[row][col] = 2

                # Use the minimax algorithm to evaluate the current board position
                eval = minimax(3, False, float('-inf'), float('inf'))

                # Mark the square on the board
                mark_square(row, col, 2)

                # Undo the move
                board[row][col] = 0

                # Update the best evaluation and move if a better move is found
                if eval > best_eval:
                    best_eval = eval
                    best_move = (row, col)

    # End the timer and calculate the execution time
    end_time = time.time()
    execution_time = end_time - start_time

    # Print the duration of the computer's move
    print(f"Computer move took {end_time - start_time:.2f} seconds.")

    # Return the best move
    return best_move


def is_winning_move(board, player):
    winning_length = 4

    # Check rows for a winning move
    for row in board:
        for i in range(len(row) - winning_length + 1):
            sequence = row[i:i + winning_length]
            if np.count_nonzero(sequence == player) == winning_length - 1 and np.count_nonzero(sequence == 0) == 1:
                return True

    # Check columns for a winning move
    for col in range(len(board[0])):
        column = [row[col] for row in board]
        for i in range(len(column) - winning_length + 1):
            sequence = column[i:i + winning_length]
            if np.count_nonzero(sequence == player) == winning_length - 1 and np.count_nonzero(sequence == 0) == 1:
                return True

    # Check diagonal lines (top-left to bottom-right)
    for row in range(len(board) - winning_length + 1):
        for col in range(len(board[0]) - winning_length + 1):
            sequence = [board[row + i][col + i] for i in range(winning_length)]
            sequence = np.array(sequence)
            if np.count_nonzero(sequence == player) == winning_length - 1 and np.count_nonzero(sequence == 0) == 1:
                return True

    # Check diagonal lines (bottom-left to top-right)
    for row in range(winning_length - 1, len(board)):
        for col in range(len(board[0]) - winning_length + 1):
            sequence = [board[row - i][col + i] for i in range(winning_length)]
            sequence = np.array(sequence)
            if np.count_nonzero(sequence == player) == winning_length - 1 and np.count_nonzero(sequence == 0) == 1:
                return True

    return False


def make_move(board, player):
    # Check if the computer can win in the next move
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                board[row][col] = player
                if is_winning_move(board, player):
                    return (row, col)
                board[row][col] = 0

    # Check if the human can win in the next move
    opponent = 1 if player == 2 else 2
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                board[row][col] = opponent
                if is_winning_move(board, opponent):
                    return (row, col)
                board[row][col] = 0

    # No winning move found, use the get_computer_move() function to make a move
    return get_computer_move()


# ----------------------------------------------------------------------------------------------#

# Draw the initial chessboard lines
draw_lines()
player = 2  # Start with the black player
game_over = False
running = True

# A loop that runs the code until the player exits the game
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # Terminate the program

        for object in objects:
            object.process()

        if player == 1:
            print("the white turn")
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if available_square(clicked_row, clicked_col) and is_legal_move(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    draw_figures()
                    pygame.display.update()
                    pygame.time.wait(500)  # Wait for a short duration (in milliseconds) to show the updated boar

                    if check_win(1):
                        game_over = True
                        print("white win")
                        print_winner(1)
                    elif is_board_full():
                        game_over = True
                    player = 2  # Switch to the black player
        if player == 2:
            print("the black turn")
            start_time = time.time()
            computer_move = make_move(board, 2)
            end_time = time.time()
            execution_time = end_time - start_time

            if computer_move is not None:
                row, col = computer_move
                board[row][col] = 2
                print("row: col:", row, col)
                mark_square(row, col, player)

                draw_figures()

                if check_win(2):
                    game_over = True
                    print("black win")
                    print_winner(2)
                elif is_board_full():
                    game_over = True
                player = 1  # Switch to the white player

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            restart()
            player = 2  # Start with the black player
            game_over = False

    button.process()
    pygame.display.flip()
    fpsClock.tick(fps)
    pygame.display.update()

import subprocess

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
    # Check if a square on the board is available (not marked by any player)
    return board[row][col] == 0


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


# Draw the initial chessboard lines
draw_lines()

player = 2  # Start with the black player
game_over = False
running=True
# a loop that run the code untill the palyer exite the game
while running:
    # it always checks for an event that exits the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # terminate the program
        
                    

        for object in objects:
            object.process()
        # when player clicks the mouse and calculates the row and column that the player clicked
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            # if the square the player clicked is available, it draws a square on it and checks who wins
            if available_square(clicked_row, clicked_col):
                if is_legal_move(clicked_row, clicked_col):
                    # Draw a white figure for player 1
                    mark_square(clicked_row, clicked_col, player)

                else:
                    # Delete the illegal value by setting it to 0
                    board[clicked_row][clicked_col] = 0
                    player = player % 2 + 1
                if board[clicked_row][clicked_col] == 2:
                    if is_legal_move(clicked_row, clicked_col):
                        # Draw a black figure for player 2
                        mark_square(clicked_row, clicked_col, player)

                    else:
                        # Delete the illegal value by setting it to 0
                        board[clicked_row][clicked_col] = 0
                        player = player % 2 + 1
                if check_win(player):
                    game_over = True
                    print_winner(player)
                # to switch between players in the game
                player = player % 2 + 1

                draw_figures()
            # to check if the key clicked is 'r', then it restarts the game and starts with the black player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 2  # Start with the black player
                game_over = False
    button.process()
    pygame.display.flip()
    fpsClock.tick(fps)
    # to constantly show the changes that happen while running the game
    pygame.display.update()

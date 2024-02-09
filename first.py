import pygame
import subprocess

pygame.init()
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Magnetic Cave')

# Set initial positions for the cave and magnet
cave_x = 10
cave_y = 70
magnet_x = screen_width - 10 - 100  # Place magnet on the right side
magnet_y = 70

# Set image sizes
cave_width = 100
cave_height = 100
magnet_width = 100
magnet_height = 100

# Set animation properties
cave_speed = 0  # Set the speed to 0 to make the cave image fixed
magnet_speed = 0  # Set the speed to 0 to make the magnet image fixed

# Define button properties
button_width = 680
button_height = 55
button_color = (238, 203, 173)  # Brown color
button_text_color = (139, 125, 123)
button_font = pygame.font.Font(None, 25)

# Create buttons
button1_rect = pygame.Rect(screen_width // 2 - button_width // 2, 200, button_width, button_height)
button1_text = button_font.render("Manual entry for both ■'s moves and □'s moves", True, button_text_color)
button1_text_rect = button1_text.get_rect(center=button1_rect.center)

button2_rect = pygame.Rect(screen_width // 2 - button_width // 2, 300, button_width, button_height)
button2_text = button_font.render("Manual entry for ■'s moves & automatic moves for □", True, button_text_color)
button2_text_rect = button2_text.get_rect(center=button2_rect.center)

button3_rect = pygame.Rect(screen_width // 2 - button_width // 2, 400, button_width, button_height)
button3_text = button_font.render("Manual entry for □'s moves & automatic moves for ■", True, button_text_color)
button3_text_rect = button3_text.get_rect(center=button3_rect.center)

def open_app():
    subprocess.Popen(["python", "app.py"])

def open_app1():
    subprocess.Popen(["python", "computer.py"])

def open_app2():
    subprocess.Popen(["python", "humanfist.py"])

# Text label animation variables
label_font = pygame.font.Font(None, 60)
label_text = label_font.render("Magnetic Cave", True, button_color)  # Set text color to button color
label_x = screen_width // 2 - label_text.get_width() // 2
label_y = 50
label_speed = 2

# Load the images for the cave and magnet squares
cave_image = pygame.image.load("MA.png")
cave_image = pygame.transform.scale(cave_image, (cave_width, cave_height))
magnet_image = pygame.image.load("MA.png")
magnet_image = pygame.transform.scale(magnet_image, (magnet_width, magnet_height))
background_image = pygame.image.load("cc.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale the image to screen size

run = True
clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if button1_rect.collidepoint(mouse_pos):
                    print("Button 1 clicked")
                    open_app()
                elif button2_rect.collidepoint(mouse_pos):
                    print("Button 2 clicked")
                    open_app1()
                elif button3_rect.collidepoint(mouse_pos):
                    print("Button 3 clicked")
                    open_app2()

    # Update positions
    label_x += label_speed

    # Check if the label reaches the screen edges
    if label_x <= cave_x + cave_width or label_x + label_text.get_width() >= magnet_x:
        label_speed *= -1  # Reverse the direction

    screen.fill((255, 239, 219))  # Fill the screen with nude color

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Draw cave and magnet images
    screen.blit(cave_image, (cave_x, cave_y))
    screen.blit(magnet_image, (magnet_x, magnet_y))

    # Draw buttons
    pygame.draw.rect(screen, button_color, button1_rect)
    screen.blit(button1_text, button1_text_rect)

    pygame.draw.rect(screen, button_color, button2_rect)
    screen.blit(button2_text, button2_text_rect)

    pygame.draw.rect(screen, button_color, button3_rect)
    screen.blit(button3_text, button3_text_rect)

    # Draw text label for "Magnetic Cave"
    screen.blit(label_text, (label_x, label_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

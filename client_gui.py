import pygame
import socket
import threading
import queue
from grid import Layout  # your existing grid class
import json
from server import get_layout_from_file


def draw_letter(letter,screen,rectangle, bg_color, font = None):
    # draw a certain letter on top of a defined rectangle
    pygame.draw.rect(screen, bg_color, rectangle)
    # a font that is 2 pixels smaller than the cell
    font = pygame.font.SysFont(font, CELL_SIZE - 2)
    #a black letter of the given font
    text = font.render(letter, True, (0, 0, 0))
    text_rect = text.get_rect(center=rectangle.center)
    screen.blit(text, text_rect)

def draw_player(dir, screen, rectangle, bg_color, font = None):
    text_char = '>'
    if dir == "U":
        text_char = '^'
    elif dir == "R":
        text_char = '>'
    elif dir == "L":
        text_char = '<'
    elif dir == "D":
        text_char = 'V'
    # draw a certain letter on top of a defined rectangle
    pygame.draw.rect(screen, bg_color, rectangle)
    # a font that is 2 pixels smaller than the cell
    font = pygame.font.SysFont(font, CELL_SIZE - 2)
    #a black letter of the given font
    text = font.render(text_char, True, (0, 0, 0))
    text_rect = text.get_rect(center=rectangle.center)
    screen.blit(text, text_rect)

# === CONFIGURATION ===
CELL_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 10
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# === NETWORK CONFIG ===
host = 'localhost'
port = 53333
key_queue = queue.Queue()

# === Setup Layout for local rendering ===
local_grid = Layout(layout=get_layout_from_file("grid.txt"))

# === Networking Thread ===
def network_thread(client_socket):
    while True:
        message = key_queue.get()
        if message == "quit":
            break

        try:
            client_socket.sendall(message.encode())
            response = client_socket.recv(4096).decode()
            grid_data = json.loads(response)
            local_grid.grid = grid_data  # Update local grid with server data
            #print("Server response:", response)
        except:
            break

    client_socket.close()

# === Pygame Front-End ===
def start_client_gui():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Grid Game")
    clock = pygame.time.Clock()

    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Start networking thread
    threading.Thread(target=network_thread, args=(client_socket,), daemon=True).start()

    running = True
    move_delay = 100  # milliseconds between moves
    last_move_time = pygame.time.get_ticks()
    interact_cd = 0
    while running:
        screen.fill((255, 255, 255))  # White background

        # === Draw Grid ===
        for row in range(local_grid.height):
            for col in range(local_grid.width):
                value = local_grid.get_cell(row, col)
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                cell_object = value[0]
                # Draw filled cells
                if cell_object == "P":
                    dir = value[1]
                    draw_player(dir,screen,rect,(0, 100, 255))
                elif cell_object.isalpha() and cell_object.isupper():
                    draw_letter(cell_object,screen,rect, (200,200,200))
                else:
                    pygame.draw.rect(screen, (200, 200, 200), rect)  # Empty

                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Border

        pygame.display.flip()


        # === Handle Events ===
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    key_queue.put("quit")
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        key_queue.put("quit")
                        running = False

        # === Continuous movement check ===
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        if now - last_move_time > move_delay:
            if keys[pygame.K_UP]:
                key_queue.put("up")
                last_move_time = now
            elif keys[pygame.K_DOWN]:
                key_queue.put("down")
                last_move_time = now
            elif keys[pygame.K_LEFT]:
                key_queue.put("left")
                last_move_time = now
            elif keys[pygame.K_RIGHT]:
                key_queue.put("right")
                last_move_time = now
            elif keys[pygame.K_SPACE]:
                if interact_cd == 0:
                    key_queue.put("interact")
                    interact_cd += 8
            elif keys[pygame.K_LSHIFT]:
                move_delay = 20  # Speed up movement
            else:
                move_delay = 100

        clock.tick(60)
        if interact_cd>0:
            interact_cd -= 1
    pygame.quit()

if __name__ == "__main__":
    start_client_gui()

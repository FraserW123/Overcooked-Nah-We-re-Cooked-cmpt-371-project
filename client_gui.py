import pygame
import socket
import threading
import queue
from grid import Layout
import json
from server import get_layout_from_file


def draw_interactable(letter,items,screen,rectangle, bg_color, font = None):
    # draw a certain letter on top of a defined rectangle
    pygame.draw.rect(screen, bg_color, rectangle)
    # a font that is 2 pixels smaller than the cell
    inter_font = pygame.font.SysFont(font, CELL_SIZE - 2)
    #a black letter of the given font
    text = inter_font.render(letter, True, (0, 0, 0))
    text_rect = text.get_rect(center=rectangle.center)
    screen.blit(text, text_rect)
    if items:
        item_font = pygame.font.SysFont(font, CELL_SIZE -6)
        item_text = item_font.render(items, True, (178, 34, 34))
        item_rect = item_text.get_rect()
        item_rect.bottomright = rectangle.bottomright
        item_rect.x -= 2  # slight padding
        item_rect.y -= 2

        screen.blit(item_text, item_rect)


def draw_player(dir, item, screen, rectangle, bg_color, font = None):
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
    dir_font = pygame.font.SysFont(font, CELL_SIZE - 2)
    #a black letter of the given font
    text = dir_font.render(text_char, True, (0, 0, 0))
    text_rect = text.get_rect(center=rectangle.center)
    screen.blit(text, text_rect)
    if item:
        item_font = pygame.font.SysFont(font, CELL_SIZE -6)
        item_text = item_font.render(item, True, (178, 34, 34))
        item_rect = item_text.get_rect()
        item_rect.bottomright = rectangle.bottomright
        item_rect.x -= 2  # slight padding
        item_rect.y -= 2

        screen.blit(item_text, item_rect)

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

                    if len(value)>2:
                        item = value[2]
                    else:
                        item = None
                    draw_player(dir,item,screen,rect,(0, 100, 255))
                elif cell_object.isalpha() and cell_object.isupper():
                    if len(value)>1:
                        items = value[1:]
                    else: items = None
                    draw_interactable(cell_object, items, screen,rect, (200,200,200))
                else:
                    pygame.draw.rect(screen, (200, 200, 200), rect)  # Empty

                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Border

        pygame.display.flip()


        # === Handle Events ===
        for event in pygame.event.get():
            pass


        # === Continuous movement check ===
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        if now - last_move_time > move_delay:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                key_queue.put("up")
                last_move_time = now
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                key_queue.put("down")
                last_move_time = now
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                key_queue.put("left")
                last_move_time = now
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                key_queue.put("right")
                last_move_time = now
            elif keys[pygame.K_SPACE]:
                if interact_cd == 0:
                    key_queue.put("interact")
                    interact_cd += 8
            elif keys[pygame.K_LSHIFT]:
                move_delay = 20  # Speed up movement
            elif keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                key_queue.put("quit")
                running = False
            else:
                move_delay = 100

        clock.tick(60)
        if interact_cd>0:
            interact_cd -= 1
    pygame.quit()

if __name__ == "__main__":
    start_client_gui()

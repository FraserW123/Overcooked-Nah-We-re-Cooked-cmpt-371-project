import pygame
from player import Player
import socket

# Grid settings
GRID_WIDTH = 25
GRID_HEIGHT = 25
CELL_SIZE = 30

# Window dimensions based on grid
width = GRID_WIDTH * CELL_SIZE
height = GRID_HEIGHT * CELL_SIZE

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Overcooked? Nah, we're cooked!")

def draw_grid(win):
    """Draw the grid lines"""
    for x in range(0, width, CELL_SIZE):
        pygame.draw.line(win, (200, 200, 200), (x, 0), (x, height))
    for y in range(0, height, CELL_SIZE):
        pygame.draw.line(win, (200, 200, 200), (0, y), (width, y))

def redraw_window(win, player):
    win.fill((255, 255, 255))
    draw_grid(win)
    player.draw(win)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 53333))
        print("Connected to server at localhost:53333")
        # player_id = client_socket.recv(1024).decode()
        # client_socket.sendall("get_pos".encode())
        # player_position = client_socket.recv(1024).decode()
        # x, y = map(int, player_position.split(','))
        # player_position = (x, y)
        player_position = (0, 0)
        player_id = client_socket.recv(1024).decode()
        # print(f"Player ID: {player_id}, Position: {player_position}")

    except Exception as e:
        print(f"Error connecting to server: {e}")
        return
    

    p = Player(player_position[0], player_position[1], player_id, 30, 30)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move(client_socket)
        redraw_window(win, p)
        clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    main()




































# import socket

# from pynput import keyboard
# from player import Player
# import time
# from grid import Layout
# import queue

# key_queue = queue.Queue()   
# host = 'localhost'
# def start_client(host='localhost', port=53333):
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         client_socket.connect((host, port))
#         print(f"Connected to server at {host}:{port}")

#         listener = keyboard.Listener(on_press=on_press)
#         listener.start()

#         while True:

#             message = key_queue.get()

#             if message == "quit":
#                 print("Exiting client.")
#                 break

#             client_socket.sendall(message.encode())
#             response = client_socket.recv(1024)
#             print(f"Server response: {response.decode()}")
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         client_socket.close()
#         print("Connection closed")

# def on_press(key):
#     try:
#         if key.char == 'q':
#             key_queue.put("quit")
#         elif key.char == 'p':
#             print("You pressed p")
#             key_queue.put("p")
#     except AttributeError:
#         if key == keyboard.Key.up:
#             key_queue.put("up")
#         elif key == keyboard.Key.down:
#             key_queue.put("down")
#         elif key == keyboard.Key.left:
#             key_queue.put("left")
#         elif key == keyboard.Key.right:
#             key_queue.put("right")

# def main():
#     start_client(host)

# if __name__ == "__main__":
#     main()
        
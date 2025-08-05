import socket
from grid import Layout
from player import Player
from interactable import initialize_interactable_grid
import threading
import json
import random
import signal
from tasklist import TaskList

host = 'localhost'
port = 53333
server_running = True
CLIENT_LIMIT = 4
GRID_HEIGHT = 10
GRID_WIDTH = 10
NUM_TASKS = 5
lock = threading.Lock()

def get_layout_from_file(file_name):
    with open(file_name, 'r') as f:
        grid_string = f.read()
    grid_list = grid_string.split("\n")
    grid_matrix = []
    width = -1
    for row in grid_list:
        row_list = row.split(" ")
        if width == -1:
            width = len(row_list)
        if width != -1 and width!= len(row_list):
            print("row has wrong number of items")
        row_list = list(filter(None, row_list))
        grid_matrix.append(row_list)
    return grid_matrix


def choose_random_color():
    R = random.randint(0, 255)
    G = random.randint(0, 255)
    B = random.randint(0, 255)

    # Ensure the values are not too close to each other
    while abs(R - G) < 50 or abs(G - B) < 50 or abs(B - R) < 50:
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
    return (R, G, B)

def start_server(game_grid, interactable_grid, task_list, host='localhost', port=53333):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")
    player_id = 0
    task_list.get_tasklist(NUM_TASKS)
    
    try:
        while server_running:
            client_socket, addr = server_socket.accept()
            
            color = choose_random_color()
            player = Player(player_id, color, max_height=10, max_width=10)
            
            thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, player_id, player, game_grid, interactable_grid, task_list, server_socket),
                daemon=True
            )
            thread.start()
            player_id += 1
    except KeyboardInterrupt:
        print("\n[!] Shutting down server...")
    finally:
        server_socket.close()
        print("[+] Server socket closed.")

def handle_client(client_socket, addr, player, game_grid, interactable_grid, task_list, server_socket=None):
    try:
        prev_position = player.get_position()
        prev_inventory = player.item
        game_grid.update_cell(prev_position[1], prev_position[0], "PR")
        game_grid.display()
        
        while True:
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                break
            print(f"Received: {data}")

            position = (prev_position[0], prev_position[1])  # Default position
            if data == "up":
                #player.move("up")
                position = (prev_position[0], prev_position[1] - 1)
                player.direction = 'U'
            elif data == "down":
                #player.move("down")
                position = (prev_position[0], prev_position[1] + 1)
                player.direction = 'D'
            elif data == "left":
                #player.move("left")
                position = (prev_position[0] - 1, prev_position[1])
                player.direction = 'L'
            elif data == "right":
                #player.move("right")
                position = (prev_position[0] + 1, prev_position[1])
                player.direction = 'R'
            elif data == "interact":
                #the player wants to interact with the items
                looking_x,looking_y = player.get_looking_position()
                looking_interactable = interactable_grid[looking_y][looking_x]
                if looking_interactable:
                    player.interact(looking_interactable)
                    item_str = "".join(looking_interactable.items)
                    cell_string = game_grid.get_grid()[looking_y][looking_x][0]+item_str
                    game_grid.update_cell(looking_y,looking_x,cell_string)
            elif data == "operate":
                #operate to cook an item
                pass
            elif data == "heartbeat":
                pass
            elif data == "quit":
                print("Client requested to quit.")
                break
            

            # position = player.get_position()
            lock.acquire()
            player_str = create_player_string(player)

            if 0 <= position[0] < game_grid.width and 0 <= position[1] < game_grid.height and game_grid.get_cell(position[1], position[0]) == '.':
                player.set_position((position[0], position[1]))
                game_grid.update_cell(prev_position[1], prev_position[0],'.')
                game_grid.update_cell(position[1], position[0], player_str)
                prev_position = position
                game_grid.display()
            else:
                game_grid.update_cell(prev_position[1],prev_position[0],player_str)


                print(f"Player position: {position}")
            lock.release()

            response_data = {
                "grid": game_grid.get_grid(),
                "player_inventory": player.item,
                "tasklist": task_list.create_string(),
                "tasklist_completed": task_list.check_completed()
            }
            client_socket.sendall(json.dumps(response_data).encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        position = player.get_position()
        game_grid.update_cell(position[1], position[0],'.')
        client_socket.close()
        print("Connection closed")

def create_player_string(player):
    player_str = "P;" + player.direction+";"
    if player.item:
        item = player.item + ";"
        player_str += item
    else:
        player_str += "None;"
    player_str += str(player.get_color())
    id = ";"+str(player.get_id())
    player_str += id
    return player_str

def main():
    grid_matrix = get_layout_from_file("grid.txt")
    game_grid = Layout(layout = grid_matrix)
    task_list = TaskList()
    interactable_grid = initialize_interactable_grid(grid_matrix, task_list)
    start_server(game_grid, interactable_grid, task_list, host, port)
       
    

if __name__ == "__main__":
    main()
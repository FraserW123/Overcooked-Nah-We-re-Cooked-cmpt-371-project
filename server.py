import socket
from grid import Layout
from player import Player
from interactable import initialize_interactable_grid
import threading
import json

host = 'localhost'
server_running = True
GRID_HEIGHT = 10
GRID_WIDTH = 10

def get_layout_from_file(file_name):
    with open(file_name, 'r') as f:
        grid_string = f.read()
    grid_list = grid_string.split("\n")
    grid_matrix = []
    for row in grid_list:
        row_list = row.split(" ")
        row_list = list(filter(None, row_list))
        grid_matrix.append(row_list)
    return grid_matrix




def start_server(game_grid, interactable_grid, host='localhost', port=53333):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    #server_socket.settimeout(1.0)  # Set timeout to 1 second
    print(f"Server started on {host}:{port}")


    try:
        while server_running:
            client_socket, addr = server_socket.accept()
            player = Player(addr, max_height=10, max_width=10)
            thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, addr, player, game_grid, interactable_grid, server_socket),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server...")
    finally:
        server_socket.close()
        print("[+] Server socket closed.")



    #handle_client(client_socket, addr, player, game_grid)

def handle_client(client_socket, addr, player, game_grid, interactable_grid, server_socket=None):
    try:
        prev_position = player.get_position()
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
                    print(player.item)
                    print(looking_interactable.items)
                    player.interact(looking_interactable)
                    print("\n")
                    print(player.item)
                    print(looking_interactable.items)
            elif data == "operate":
                #operate to cook an item
                pass
            # elif data == "p":
            #     client_socket.sendall(b"Shutting down server.\n")
            #     client_socket.close()
            #     server_socket.close()  # Close server socket to unblock accept()
                
            elif data == "quit":
                print("Client requested to quit.")
                break
            

            # position = player.get_position()
            player_str = "P" + player.direction
            if player.item:
                player_str += player.item
            if 0 <= position[0] < game_grid.width and 0 <= position[1] < game_grid.height and game_grid.get_cell(position[1], position[0]) == '.':
                player.set_position((position[0], position[1]))
                game_grid.update_cell(prev_position[1], prev_position[0],'.')
                game_grid.update_cell(position[1], position[0], player_str)
                prev_position = position
                game_grid.display()
            else:
                game_grid.update_cell(prev_position[1],prev_position[0],player_str)


                print(f"Player position: {position}")
            

            

            response = "Message received"
            grid_state = json.dumps(game_grid.get_grid())
            client_socket.sendall(grid_state.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed")

def main():
    grid_matrix = get_layout_from_file("grid.txt")
    game_grid = Layout(layout = grid_matrix)
    interactable_grid = initialize_interactable_grid(grid_matrix)
    start_server(game_grid, interactable_grid, host)
       
    

if __name__ == "__main__":
    main()
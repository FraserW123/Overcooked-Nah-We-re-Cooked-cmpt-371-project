import socket
from grid import Layout
from player import Player
import threading

def start_server(game_grid, host='192.168.1.81', port=53333):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    #server_socket.settimeout(1.0)  # Set timeout to 1 second
    print(f"Server started on {host}:{port}")


    try:
        while True:
            client_socket, addr = server_socket.accept()
            player = Player(addr, max_height=10, max_width=10)
            thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, addr, player, game_grid), 
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server...")
    finally:
        server_socket.close()
        print("[+] Server socket closed.")



    #handle_client(client_socket, addr, player, game_grid)

def handle_client(client_socket, addr, player, game_grid):
    try:
        prev_position = player.get_position()
        game_grid.update_cell(prev_position[1], prev_position[0], 'P')
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
            elif data == "down":
                #player.move("down")
                position = (prev_position[0], prev_position[1] + 1)
            elif data == "left":
                #player.move("left")
                position = (prev_position[0] - 1, prev_position[1])
            elif data == "right":
                #player.move("right")
                position = (prev_position[0] + 1, prev_position[1])
            elif data == "quit":
                print("Client requested to quit.")
                break

            # position = player.get_position()
            
            if 0 <= position[0] < game_grid.width and 0 <= position[1] < game_grid.height and game_grid.get_cell(position[1], position[0]) == '.':
                player.set_position((position[0], position[1]))
                game_grid.update_cell(prev_position[1], prev_position[0],'.')
                game_grid.update_cell(position[1], position[0], 'P' )
                prev_position = position
                game_grid.display()
                print(f"Player position: {position}")
            

            

            response = "Message received"
            client_socket.sendall(response.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed")

def main():
    game_grid = Layout(10, 10)
    
    start_server(game_grid)
       
    

if __name__ == "__main__":
    main()
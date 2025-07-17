import socket
from grid import Layout
from player import Player

def start_server(player, game_grid, host='localhost', port=53333):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")


    client_socket, addr = server_socket.accept()
    print("Client connected")
    print(f"Connection from {addr}")
    print(addr[1])



    handle_client(client_socket, player, game_grid)

def handle_client(client_socket, player, game_grid):
    try:
        prev_position = player.get_position()
        game_grid.update_cell(prev_position[1], prev_position[0], 'P')
        game_grid.display()
        
        while True:
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                break
            print(f"Received: {data}")

            if data == "up":
                player.move("up")
            elif data == "down":
                player.move("down")
            elif data == "left":
                player.move("left")
            elif data == "right":
                player.move("right")
            elif data == "quit":
                print("Client requested to quit.")
                break

            position = player.get_position()
            
            if position != prev_position and 0 <= position[0] < game_grid.width and 0 <= position[1] < game_grid.height:
                game_grid.update_cell(prev_position[1], prev_position[0],'.')
                game_grid.update_cell(position[1], position[0], 'P')
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
    #game_grid.display()
    player = Player(max_height=10, max_width=10)
    start_server(player, game_grid)
       
    

if __name__ == "__main__":
    main()
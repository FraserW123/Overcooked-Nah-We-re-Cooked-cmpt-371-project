import socket
from grid import Layout
from player import Player
import threading
import sys

host = 'localhost'
port = 53333
server_running = True

# def start_server(game_grid, host=host, port=port):
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((host, port))
#     server_socket.listen(5)
#     #server_socket.settimeout(1.0)  # Set timeout to 1 second
#     print(f"Server started on {host}:{port}")


#     try:
#         while server_running:
#             client_socket, addr = server_socket.accept()
#             player = Player(addr, max_height=10, max_width=10)
#             thread = threading.Thread(
#                 target=handle_client, 
#                 args=(client_socket, addr, player, game_grid, server_socket), 
#                 daemon=True
#             )
#             thread.start()
#     except KeyboardInterrupt:
#         print("\n[!] Shutting down server...")
#     finally:
#         server_socket.close()
#         print("[+] Server socket closed.")



#     #handle_client(client_socket, addr, player, game_grid)

# def handle_client(client_socket, addr, player, game_grid, server_socket=None):
#     try:
#         prev_position = player.get_position()
#         game_grid.update_cell(prev_position[1], prev_position[0], 'P')
#         game_grid.display()
        
#         while True:
#             data = client_socket.recv(1024).decode('utf-8')

#             if not data:
#                 break
#             print(f"Received: {data}")

#             position = (prev_position[0], prev_position[1])  # Default position

#             if data == "up":
#                 #player.move("up")
#                 position = (prev_position[0], prev_position[1] - 1)
#             elif data == "down":
#                 #player.move("down")
#                 position = (prev_position[0], prev_position[1] + 1)
#             elif data == "left":
#                 #player.move("left")
#                 position = (prev_position[0] - 1, prev_position[1])
#             elif data == "right":
#                 #player.move("right")
#                 position = (prev_position[0] + 1, prev_position[1])
#             # elif data == "p":
#             #     client_socket.sendall(b"Shutting down server.\n")
#             #     client_socket.close()
#             #     server_socket.close()  # Close server socket to unblock accept()
                
#             elif data == "quit":
#                 print("Client requested to quit.")
#                 break
            

#             # position = player.get_position()
            
#             if 0 <= position[0] < game_grid.width and 0 <= position[1] < game_grid.height and game_grid.get_cell(position[1], position[0]) == '.':
#                 player.set_position((position[0], position[1]))
#                 game_grid.update_cell(prev_position[1], prev_position[0],'.')
#                 game_grid.update_cell(position[1], position[0], 'P' )
#                 prev_position = position
#                 game_grid.display()
#                 print(f"Player position: {position}")
            

            

#             response = "Message received"
#             client_socket.sendall(response.encode())
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         client_socket.close()
#         print("Connection closed")

def handle_client(client_socket, addr, client_id):

    client_socket.sendall(str(client_id).encode())
    
    while True:
        try:
            
            data = client_socket.recv(1024)
            print(f"Received from {addr}: {data.decode()}")
            if not data:
                break
            # if data.decode() == "get_pos":
            #     position = clients[str(client_id)]
            #     position = position.strip('()')
            #     client_socket.sendall(position.encode())
            if data.decode() == "up":
            #     print(f"Client {client_id} moved up")
            #     clients[str(client_id)] = (clients[str(client_id)][0], clients[str(client_id)][1] - 30)
            #     new_pos = clients[str(client_id)].strip('()')
                client_socket.sendall("up".encode())
            if data.decode() == "down":
            #     print(f"Client {client_id} moved down")
            #     clients[str(client_id)] = (clients[str(client_id)][0], clients[str(client_id)][1] + 30)
            #     new_pos = clients[str(client_id)].strip('()')
                client_socket.sendall("down".encode())
            if data.decode() == "left":
            #     print(f"Client {client_id} moved left")
            #     clients[str(client_id)] = (clients[str(client_id)][0] - 30, clients[str(client_id)][1])
            #     new_pos = clients[str(client_id)].strip('()')
                client_socket.sendall("left".encode())
            if data.decode() == "right":
            #     print(f"Client {client_id} moved right")
            #     clients[str(client_id)] = (clients[str(client_id)][0] + 30, clients[str(client_id)][1])
            #     new_pos = clients[str(client_id)].strip('()')
                client_socket.sendall("right".encode())

        except socket.error as e:
            print(f"Socket error: {e}")
            break


def main():
    
    pos = [(0,0)]
    client_id = 0

    # start_server(game_grid, host)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))

    except socket.error as e:
        print(f"Socket error: {e}")
        # sys.exit(1)
       
    server_socket.listen(5)
    # server_socket.settimeout(1.0)  # Set timeout to 1 second
    print(f"Server started on {host}:{port}")

    while True:
        try:
            connection, address = server_socket.accept()
            print(f"Connection from {address} has been established.")

            threading.Thread(target=handle_client, args=(connection, address, client_id)).start()
            client_id += 1

        except KeyboardInterrupt:
            print("\n[!] Shutting down server...")

        finally:
            server_socket.close()
            print("[+] Server socket closed.")

if __name__ == "__main__":
    main()
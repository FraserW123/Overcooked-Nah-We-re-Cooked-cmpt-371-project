import socket

from pynput import keyboard
from player import Player
import time
from grid import Layout
import queue

key_queue = queue.Queue()   

def start_client(host='localhost', port=53333):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while True:

            message = key_queue.get()

            if message == "quit":
                print("Exiting client.")
                break
            
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode()}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed")

def on_press(key):
    try:
        if key.char == 'q':
            key_queue.put("quit")
        elif key.char == 'p':
            print("You pressed p")
            key_queue.put("p")
    except AttributeError:
        if key == keyboard.Key.up:
            key_queue.put("up")
        elif key == keyboard.Key.down:
            key_queue.put("down")
        elif key == keyboard.Key.left:
            key_queue.put("left")
        elif key == keyboard.Key.right:
            key_queue.put("right")

def main():
    start_client()

if __name__ == "__main__":
    main()
        
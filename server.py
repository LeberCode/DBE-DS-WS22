import socket
import threading

HOST = ''
PORT = 8080
BUFSIZ = 1024
ADDR = (HOST, PORT)

clients = {}
addresses = {}

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print(f"{client_address}: has connected.")
        client.send(bytes("Greetings! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        threading.Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = f"Welcome {name}! If you ever want to quit, type '{quit}' to exit."
    client.send(bytes(welcome, "utf8"))
    msg = f"{name} has joined the chat!"
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes(f"{name} has left the chat.", "utf8"))
            break


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = threading.Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
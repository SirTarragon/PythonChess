#This code is running on the server I set up, not designed to be run locally
"""
import socket
from objects.chess.chess import Chess
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")
turnNum = 1
players = [False, False]
game = Chess()

def threaded_client(conn, num):
    global turnNum, players, game_board
    conn.send(str.encode(str(num)))
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if game.get_turn() and num == 2:
                continue
            if num == 1 and not game.get_turn():
                continue
            if not data:
                #do more game ending shit here
                conn.send(str.encode("Goodbye"))
            else:
                print("Recieved: " + reply)
                if reply != game.board_to_string():
                    #udpate game_board
                    game.string_to_board(reply)
                print("Sending: " + reply)

            conn.sendall(str.encode(game.board_to_string()))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    if not players[0]:
        players[0] = True
        start_new_thread(threaded_client, (conn, 1))
    elif not players[1]:
        players[1] = True
        start_new_thread(threaded_client, (conn, 2))
    else:
        print("Game is full, rejecting connection")
        conn.close()

"""
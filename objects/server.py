#Code in production on the server
import socket
try:
    import chess as Chess
except ModuleNotFoundError:
    print("Chess not found in same directory as head file")
    try:
        from . import chess as Chess
    except ModuleNotFoundError:
        print("Chess not found in same directory")
        from objects import chess as Chess
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
game = Chess.Chess()


def threaded_client(conn, num):
    global turnNum, players, game
    conn.send(str.encode(str(num)))
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            print("Receiving from clt " +str(num)+": " + reply)
            if game.get_turn() and num == 1:
                if data and reply and reply != game.board_to_string():
                    game.string_to_board(reply)
            if num == 2 and not game.get_turn():
                if data and reply and reply != game.board_to_string():
                    game.string_to_board(reply)

            print("Sending to clt " + str(num) + ": " + reply)

            conn.sendall(str.encode(game.board_to_string()))
        except:
            break
    players[num-1] = False
    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    if not players[0]:
        players[0] = True
        print("Starting thread 1")
        start_new_thread(threaded_client, (conn, 1))
    elif not players[1]:
        players[1] = True
        print("Starting thread 2")
        start_new_thread(threaded_client, (conn, 2))
    else:
        print("Game is full, rejecting connection")
        conn.close()

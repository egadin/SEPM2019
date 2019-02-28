import socketio
from aiohttp import web


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
gamelist = []
roomlist = []
class gamelobby:
    def __init__(self,id, player1, player2, winner,room):
        self.id = id
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        self.room = room

class room:
    def __init__(self,p1, p2):
        self.player1 = p1
        self.player2 = p2


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ')

@sio.on('nextPiece')
def nextpiece_event(sid, data):
    room=filter(lambda room: room.player1 == sid or room.player2 == sid, roomlist)
    
    sio.emit('nextPiece', data=data, room=str(room.player1), skip_sid=sid)

@sio.on('board')
def board_event(sid, data):
    room=filter(lambda room: room.player1 == sid or room.player2 == sid, roomlist)
    sio.emit('board', data=data, room=str(room.player1), skip_sid=sid)

@sio.on('create tournament')

@sio.on('join tournament')

@sio.on('start tournament')


@sio.on('create game')
def creategame_event(sid, data):
    gamelist.append(gamelobby(sid,sid,None,None,None))
    sio.emit('create game', data=gamelist)

@sio.on('join game')
def joingame_event(sid, data):
    for game in range(len(gamelist)):
        if (game.id == data):
            game.player2 = sid
    sio.emit('join game', data=gamelist)

@sio.on('start game')
def startgame_event(sid):
    currentgame=filter(lambda game: game.player1 == sid or game.player2 == sid, gamelist)
    gamelist.remove(currentgame)
    currentgame.room=room(currentgame.player1, currentgame.player2)
    roomlist.append(currentgame.room)
    sio.enter_room(currentgame.player1, str(currentgame.player1))
    sio.enter_room(currentgame.player2, str(currentgame.player1))
    sio.emit('init game', data=currentgame, room=str(player1))
    sio.emit('start game', room=str(player1), skip_sid=currentgame.player2)

if __name__ == '__main__':
    web.run_app(app)

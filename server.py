import socketio
from aiohttp import web


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
gamelist = []
roomlist = []
class gamelobby:
    def __init__(self,id, player1id, player2id, player1, player2, winner,room):
        self.id = id
        self.player1id = player1id
        self.player2id = player2id
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        self.room = room

class room:
    def __init__(self,p1, p2):
        self.player1id = p1
        self.player2id = p2


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ')

@sio.on('nextPiece')
def nextpiece_event(sid, data):
    room=filter(lambda room: room.player1id == sid or room.player2id == sid, roomlist)

    sio.emit('nextPiece', data=data, room=str(room.player1id), skip_sid=sid)

@sio.on('board')
def board_event(sid, data):
    room=filter(lambda room: room.player1id == sid or room.player2id == sid, roomlist)
    sio.emit('board', data=data, room=str(room.player1id), skip_sid=sid)

@sio.on('create tournament')

@sio.on('join tournament')

@sio.on('start tournament')


@sio.on('create game')
def creategame_event(sid, data):
    if (data.player2!=None):
        id2 = sid
        p2name = data.player2
    gamelist.append(gamelobby(sid,sid,id2,data.player1,p2name,None,None))
    sio.emit('create game', data=gamelist)


@sio.on('join game')
def joingame_event(sid, data):
    for game in range(len(gamelist)):
        if (game.id == data):
            game.player2id = sid
            game.player2 = data.name
    sio.emit('join game', data=gamelist)


@sio.on('start game')
def startgame_event(sid):
    currentgame=filter(lambda game: game.player1id == sid or game.player2id == sid, gamelist)
    gamelist.remove(currentgame)
    currentgame.room=room(currentgame.player1id, currentgame.player2id)
    roomlist.append(currentgame.room)
    sio.enter_room(currentgame.player1id, str(currentgame.player1id))
    sio.enter_room(currentgame.player2id, str(currentgame.player1id))
    sio.emit('init game', data=currentgame, room=str(currentgame.player1id))
    sio.emit('start game', room=str(currentgame.player1id), skip_sid=currentgame.player2id)


if __name__ == '__main__':
    web.run_app(app)

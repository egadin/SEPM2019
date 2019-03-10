import socketio
from aiohttp import web


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
gamelist = []
roomlist = []
class gamelobby:
    def __init__(self,id, player1id, player2id, player1, player2, AI1, AI2, winner):
        self.id = id
        self.player1id = player1id
        self.player2id = player2id
        self.player1 = player1
        self.player2 = player2
        self.AI1 = AI1
        self.AI2 = AI2
        self.winner = winner
        # self.room = room
#fixa bort rooms från transmissions
    """
    Translates a gamelobby object into a dictionary, that is returned.
    """
    def toDictionary(self):
        return {
            'id'        : self.id,
            'player1id' : self.player1id,
            'player2id' : self.player2id,
            'player1'   : self.player1,
            'player2'   : self.player2,
            'AI1'       : self.AI1,
            'AI2'       : self.AI2,
            'winner'    : self.winner
            }

    """
    Translates a dictionary data structure to a gamelobby object, that is returned.
    Note that this is a static method, so it is called with its class and not instance.
    """
    @staticmethod
    def fromDictionary(data):
        return gamelobby(data['id'], data['player1id'], data['player2id'],
                        data['player1'], data['player2'], data['AI1'], data['AI2'],
                        data['winner'])

    def getPlayer1Name(self):
        if (self.player1 == None):
            return "None"
        else:
            return self.player1

    def getPlayer2Name(self):
        if (self.player2 == None):
            return "None"
        else:
            return self.player2

    # Intended to provide more than the name, as a string
    def getPlayer1info(self):
        return self.getPlayer1Name()

    def getPlayer2info(self):
        return self.getPlayer2Name()

"""
This class represents a waiting game -- initially created with only player 1
"""
class Room:
    def __init__(self, p1, p2):
        self.player1id = p1
        self.player2id = p2


@sio.on('connect')
def connect(sid, environ):
    # Borde spara en lista av alla klienter?
    print("New client connection on socked ID ", sid)

@sio.on('disconnect')
def disconnect(sid):
    # I så fall, ta bort klienten?
    print('disconnect ')

@sio.on('nextPiece')
async def nextpiece_event(sid, data):
    room=filter(lambda room: room.player1id == sid or room.player2id == sid, roomlist)

    await sio.emit('nextPiece', {'data':data}, room=str(room.player1id), skip_sid=sid)

@sio.on('board')
async def board_event(sid, data):
    room=filter(lambda room: room.player1id == sid or room.player2id == sid, roomlist)
    await sio.emit('board', {'data': data}, room=str(room.player1id), skip_sid=sid)

@sio.on('create tournament')

@sio.on('join tournament')

@sio.on('start tournament')

@sio.on('gamelobby request')
async def requestevent(sid):
    await updatelobby()

@sio.on('create gamelobby') #I didn't accept the todict since data doesn't contain all the neccessary variables.
async def creategame_event(sid, data):
    print("creating game lobby")
    global gamelist
    gamelist.append(gamelobby.fromDictionary(data))
    #gamelist.append(gamelobby(sid, sid, data['player2id'], data['player1'], data['player2'], data['AI1'], data['AI2'] , data['winner'], data['room']))
    print("Current game lobbies are:")
    print(gamelist)
    await updatelobby()

async def updatelobby():
    global gamelist
    sendlist = []
    global gamelist
    for lobby in gamelist:
        sendlist.append(lobby.toDictionary())
        print(repr(sendlist))
        #sendlist.append({'id': lobby.id, 'player1id': lobby.player1id, 'player2id': lobby.player2id, 'player1': lobby.player1, 'player2': lobby.player2, 'AI1': lobby.AI1, 'AI2': lobby.AI2, 'winner': lobby.winner, 'room': lobby.room})
    await sio.emit('lobby update', sendlist)


@sio.on('join gamelobby')
async def joingame_event(sid, data):
    print("Player "+data['player2']+" joined lobby server")
    global gamelist
    for game in gamelist:
        print(game.id)
        print(data['gameid'])
        if (game.id == data['gameid']):
            game.player2id = sid
            game.player2 = data['player2']
            await updatelobby()
            break


@sio.on('start gamelobby')
async def startgame_event(sid):
    # Find the game in gamelist, where player1 or 2 have id = sid
    global gamelist
    print("sid"+sid)
    flist=filter(lambda game: game.player1id == sid or game.player2id == sid, gamelist)
    currentgame=next(flist)
    print("current game"+repr(currentgame))
    print(repr(gamelist))
    gamelist.remove(currentgame)
    newroom=Room(currentgame.player1id, currentgame.player2id)
    roomlist.append(newroom)
    sio.enter_room(currentgame.player1id, str(currentgame.player1id))
    sio.enter_room(currentgame.player2id, str(currentgame.player1id))
    await sio.emit('init game', {'data':gamelobby.toDictionary(currentgame)}, room=str(currentgame.player1id))
    await sio.emit('start game', room=str(currentgame.player1id), skip_sid=currentgame.player2id)
"""
fix data outputs to dict
"""

if __name__ == '__main__':
    web.run_app(app)

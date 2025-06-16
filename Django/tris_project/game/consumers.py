import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Stato globale condiviso (solo per test in singolo processo)
game_state = {
    "players": {},       # channel_name -> simbolo ("X" o "O")
    "board": [""] * 9,   # 9 celle vuote
    "turn": "X",         # turno corrente
}

class TrisConsumer(AsyncWebsocketConsumer):
    room_name = "game_room"

    async def connect(self):
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        if len(game_state["players"]) < 2:
            symbol = "X" if "X" not in game_state["players"].values() else "O"
            game_state["players"][self.channel_name] = symbol
            await self.send(json.dumps({"type": "init", "symbol": symbol}))
            await self.channel_layer.group_send(self.room_name, {"type": "game_update"})
        else:
            await self.send(json.dumps({"type": "full"}))
            await self.close()

    async def disconnect(self, close_code):
        game_state["players"].pop(self.channel_name, None)
        game_state["board"] = [""] * 9
        game_state["turn"] = "X"
        await self.channel_layer.group_send(self.room_name, {"type": "reset_game"})
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "move":
            index = data["index"]
            symbol = game_state["players"].get(self.channel_name)
            if game_state["board"][index] == "" and game_state["turn"] == symbol:
                game_state["board"][index] = symbol
                game_state["turn"] = "O" if game_state["turn"] == "X" else "X"
                winner = self.check_winner()
                await self.channel_layer.group_send(self.room_name, {
                    "type": "game_update",
                    "winner": winner
                })

    async def game_update(self, event):
        await self.send(json.dumps({
            "type": "update",
            "board": game_state["board"],
            "turn": game_state["turn"],
            "winner": event.get("winner")
        }))

    async def reset_game(self, event):
        game_state["board"] = [""] * 9
        game_state["turn"] = "X"
        await self.send(json.dumps({
            "type": "reset"
        }))

    def check_winner(self):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6],
        ]
        for a,b,c in wins:
            if game_state["board"][a] and game_state["board"][a] == game_state["board"][b] == game_state["board"][c]:
                return game_state["board"][a]
        if all(cell != "" for cell in game_state["board"]):
            return "draw"
        return None

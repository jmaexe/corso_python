import json
import redis.asyncio as aioredis
from channels.generic.websocket import AsyncWebsocketConsumer

# REDIS_GAME_STATE_KEY = "tris_game_state"

class TrisConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]['room_name']
        # Connetti al Redis
        self.redis = await aioredis.from_url("redis://127.0.0.1")
        # Unisci il client al gruppo
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        # Carica lo stato da Redis, o inizializza
        raw_state = await self.redis.get(f"{self.room_name}_state")
        if raw_state:
            game_state = json.loads(raw_state)
        else:
            game_state = {
                "players": {},
                "board": [""] * 9,
                "turn": "X",
            }

        # Assegna simbolo al giocatore se c'è posto
        if len(game_state["players"]) < 2:
            symbol = "X" if "X" not in game_state["players"].values() else "O"
            game_state["players"][self.channel_name] = symbol
            # Salva su Redis
            await self.redis.set(f"{self.room_name}_state", json.dumps(game_state))
            await self.send(json.dumps({"type": "init", "symbol": symbol}))
            await self.channel_layer.group_send(self.room_name, {"type": "game_update"})
        else:
            await self.send(json.dumps({"type": "full"}))
            await self.close()

    async def disconnect(self, close_code):
        # Carica stato da Redis
        raw_state = await self.redis.get(f"{self.room_name}_state")
        if raw_state:
            game_state = json.loads(raw_state)

            game_state["players"].pop(self.channel_name, None)
            # Se nessun player, resetta tutto
            if len(game_state["players"]) == 0:
                game_state["board"] = [""] * 9
                game_state["turn"] = "X"
            # Salva su Redis
            await self.redis.set(f"{self.room_name}_state", json.dumps(game_state))
            await self.channel_layer.group_send(self.room_name, {"type": "reset_game"})

        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.redis.close()

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "move":
            index = data["index"]

            raw_state = await self.redis.get(f"{self.room_name}_state")
            if not raw_state:
                return  # no game state? ignora

            game_state = json.loads(raw_state)
            symbol = game_state["players"].get(self.channel_name)

            if symbol is None:
                return  # giocatore non registrato

            if game_state["board"][index] == "" and game_state["turn"] == symbol:
                game_state["board"][index] = symbol
                game_state["turn"] = "O" if game_state["turn"] == "X" else "X"

                winner = self.check_winner(game_state["board"])

                # Salva stato aggiornato
                await self.redis.set(f"{self.room_name}_state", json.dumps(game_state))

                await self.channel_layer.group_send(self.room_name, {
                    "type": "game_update",
                    "winner": winner
                })

    async def game_update(self, event):
        raw_state = await self.redis.get(f"{self.room_name}_state")
        if raw_state:
            game_state = json.loads(raw_state)
        else:
            game_state = {
                "board": [""] * 9,
                "turn": "X",
            }
        await self.send(json.dumps({
            "type": "update",
            "board": game_state["board"],
            "turn": game_state["turn"],
            "winner": event.get("winner")
        }))

    async def reset_game(self, event):
        # Quando ricevi reset, invia messaggio al client
        await self.send(json.dumps({"type": "reset"}))

    def check_winner(self, board):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6],
        ]
        for a,b,c in wins:
            if board[a] and board[a] == board[b] == board[c]:
                return board[a]
        if all(cell != "" for cell in board):
            return "draw"
        return None

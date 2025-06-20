import json
import re
import uuid
import redis.asyncio as aioredis
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

from game.utils import check_winner, find_one_room_with_one_player, find_rooms_with_one_player, generate_room_name

logger = logging.getLogger("game")

class TrisConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"].get("room_name", None)
        self.redis = await aioredis.from_url("redis://127.0.0.1")
        self.redis.set("player_name", "bo")
        logger.info(f"Connessione richiesta per stanza: {self.room_name}")
        if not self.room_name:
            logger.info("Nessuna stanza specificata, cerco una stanza con un solo giocatore...")
            self.room_name = await find_one_room_with_one_player(self.redis)
            if not self.room_name:
                self.room_name = generate_room_name()
                logger.info(f"Nessuna stanza disponibile, generata nuova stanza: {self.room_name}")
            else:
                logger.info(f"Trovata stanza con un solo giocatore: {self.room_name}")
        else:
            logger.info(f"Connessione richiesta per stanza: {self.room_name}")

        self.redis_key = f"game:{self.room_name}:state"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        logger.info(f"Client {self.channel_name} connesso alla stanza {self.room_name}")

        raw_state = await self.redis.get(self.redis_key)
        if raw_state:
            game_state = json.loads(raw_state)
        else:
            game_state = {
                "players": {},
                "player_names": {},  
                "board": [""] * 9,
                "turn": "X",
            }

        if len(game_state["players"]) < 2:
            symbol = "X" if "X" not in game_state["players"].values() else "O"
            game_state["players"][self.channel_name] = symbol
            await self.redis.set(self.redis_key, json.dumps(game_state))
            await self.send(json.dumps({"type": "init", "symbol": symbol,"room_name": self.room_name}))
            await self.channel_layer.group_send(self.room_name, {"type": "game_update"})
            logger.info(f"Client {self.channel_name} assegnato simbolo '{symbol}' nella stanza {self.room_name}")
        else:
            await self.send(json.dumps({"type": "full"}))
            logger.warning(f"Stanza {self.room_name} piena. Connessione rifiutata per {self.channel_name}")
            await self.close()

    async def disconnect(self, close_code):
        logger.info(f"Disconnessione client {self.channel_name} dalla stanza {self.room_name} (code {close_code})")

        raw_state = await self.redis.get(self.redis_key)
        if raw_state:
            game_state = json.loads(raw_state)
            game_state["players"].pop(self.channel_name, None)

            if len(game_state["players"]) == 0:
                await self.redis.delete(self.redis_key)
                logger.info(f"Stanza {self.room_name} svuotata. Reset della partita.")
            else : 
                await self.redis.set(self.redis_key, json.dumps(game_state))
            await self.redis.set(self.redis_key, json.dumps(game_state))
            await self.channel_layer.group_send(self.room_name, {"type": "reset_game"})

        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.redis.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "init" :
            player_name = data.get("player_name", "Anonymous")
            logger.info(f"Ricevuto nome giocatore: {player_name} per client {self.channel_name}")

            raw_state = await self.redis.get(self.redis_key)
            if raw_state:
                game_state = json.loads(raw_state)
            else:
                game_state = {
                    "players": {},
                    "player_names": {},  # aggiungiamo questa mappa per associare channel_name -> player_name
                    "board": [""] * 9,
                    "turn": "X",
                }

            # Salva il nome del giocatore
            game_state["player_names"][self.channel_name] = player_name
            await self.redis.set(self.redis_key, json.dumps(game_state))

            # Puoi mandare conferma al client
            await self.send(json.dumps({"type": "init_confirm", "player_name": player_name}))
            return 
        if data["type"] == "move":
            index = data["index"]
            logger.debug(f"Ricevuta mossa da {self.channel_name} sulla cella {index}")

            raw_state = await self.redis.get(self.redis_key)
            if not raw_state:
                logger.warning("Game state non trovato su Redis. Mossa ignorata.")
                return

            game_state = json.loads(raw_state)
            symbol = game_state["players"].get(self.channel_name)

            if symbol is None:
                logger.warning(f"Client {self.channel_name} non registrato nella stanza.")
                return

            if game_state["board"][index] == "" and game_state["turn"] == symbol:
                game_state["board"][index] = symbol
                game_state["turn"] = "O" if symbol == "X" else "X"

                winner = check_winner(game_state["board"])
                if winner:
                    logger.info(f"Vittoria di '{winner}' nella stanza {self.room_name}")

                await self.redis.set(self.redis_key, json.dumps(game_state))
                await self.channel_layer.group_send(self.room_name, {
                    "type": "game_update",
                    "winner": winner
                })
            else:
                logger.debug(f"Mossa non valida: cella occupata o non è il turno di {symbol}")

    async def game_update(self, event):
        raw_state = await self.redis.get(self.redis_key)
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
        logger.info(f"Reset partita per stanza {self.room_name}")
        await self.send(json.dumps({"type": "reset"}))

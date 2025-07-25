import json
import logging
import redis.asyncio as aioredis
from channels.generic.websocket import AsyncWebsocketConsumer
from game.utils import check_winner, find_one_room_with_one_player, generate_room_name

logger = logging.getLogger("game")
TTL = 600  # Tempo di vita delle stanze in secondi (10 minuti)

class TrisConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"].get("room_name", None)
        self.redis = await aioredis.from_url("redis://127.0.0.1")
        logger.info(f"Connessione richiesta per stanza: {self.room_name}")

        if not self.room_name:
            self.room_name = await find_one_room_with_one_player(self.redis)
            if not self.room_name:
                self.room_name = generate_room_name()
                logger.info(f"Nessuna stanza disponibile, generata nuova stanza: {self.room_name}")
            else:
                logger.info(f"Trovata stanza con un solo giocatore: {self.room_name}")

        self.redis_key = f"game:{self.room_name}:state"
        logger.info(f"Client {self.channel_name} connesso alla stanza {self.room_name}")

        # Accetta la connessione WebSocket
        await self.accept()

        #  Ricarica stato aggiornato da Redis dopo accept
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

        #  Se ci sono già 2 giocatori, rifiuta la connessione
        if len(game_state["players"]) >= 2:
            await self.send(json.dumps({"type": "full"}))
            logger.warning(f"Stanza {self.room_name} piena. Connessione rifiutata per {self.channel_name}")
            await self.close()
            return

        #  Aggiungi giocatore
        symbol = "X" if "X" not in game_state["players"].values() else "O"
        game_state["players"][self.channel_name] = symbol

        # Salva stato e aggiungi al gruppo
        await self.redis.set(self.redis_key, json.dumps(game_state), ex=TTL)
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.send(json.dumps({
            "type": "init",
            "symbol": symbol,
            "room_name": self.room_name
        }))

        # Invia update a tutti i client nella stanza
        await self.channel_layer.group_send(self.room_name, {"type": "game_update"})

        logger.info(f"Client {self.channel_name} assegnato simbolo '{symbol}' nella stanza {self.room_name}")

        #  Se entrambi i giocatori sono connessi
        if len(game_state["players"]) == 2:
            logger.info(f"Entrambi i giocatori connessi nella stanza {self.room_name}, gioco pronto.")
            await self.channel_layer.group_send(self.room_name, {"type": "game_ready"})
 
    async def disconnect(self, close_code):
        logger.info(f"Disconnessione client {self.channel_name} dalla stanza {self.room_name} (code {close_code})")

        raw_state = await self.redis.get(self.redis_key)
        if not raw_state:
            return

        game_state = json.loads(raw_state)

        #  Se il client non era tra i giocatori registrati, non fare nulla
        if self.channel_name not in game_state["players"]:
            logger.info(f"{self.channel_name} non era registrato come giocatore, nessuna azione necessaria.")
            await self.redis.close()
            return

        # ✅ Rimuovi solo se è un player reale
        game_state["players"].pop(self.channel_name, None)
        game_state["player_names"].pop(self.channel_name, None)

        if len(game_state["players"]) == 0:
            await self.redis.delete(self.redis_key)
            logger.info(f"Stanza {self.room_name} svuotata. Reset della partita.")
        else:
            await self.redis.set(self.redis_key, json.dumps(game_state), ex=TTL)

        await self.channel_layer.group_send(self.room_name, {"type": "reset_game"})
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.redis.close()
 

  
    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "init":
            player_name = data.get("player_name", "Anonymous")
            logger.info(f"Ricevuto nome giocatore: {player_name} per client {self.channel_name}")

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
            logger.info("aggiungendo player ...")
            game_state["player_names"][self.channel_name] = player_name
            await self.redis.set(self.redis_key, json.dumps(game_state), ex=TTL)
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

                await self.redis.set(self.redis_key, json.dumps(game_state), ex=TTL)
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

    # partita pronta (entrambi i giocatori connessi)
    async def game_ready(self, event):
        await self.send(json.dumps({"type": "ready"}))

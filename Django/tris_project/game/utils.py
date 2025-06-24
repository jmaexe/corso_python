# utils.py

import json
import random
import string
from typing import Tuple, Union
from typing import List, Optional

from django.http import HttpRequest, JsonResponse
import logging 

logger = logging.getLogger("game")

wins = [
        [0,1,2], [3,4,5], [6,7,8],  # righe
        [0,3,6], [1,4,7], [2,5,8],  # colonne
        [0,4,8], [2,4,6]            # diagonali
    ]
def check_winner(board: List[str]) -> Optional[str]:
    """
    Controlla se c'è un vincitore o pareggio.
    Ritorna:
        - "X" o "O" se uno dei due ha vinto
        - "draw" se la board è piena senza vincitori
        - None se il gioco non è concluso
    """
    
    for combo in wins:
        a, b, c = combo
        if board[a] == board[b] == board[c] != "":
            return board[a]  # vincitore X o O
    
    if all(cell != "" for cell in board):
        return "draw"
    
    return None

def is_board_full(board: List[str]) -> bool:
    """Ritorna True se la board è piena, False altrimenti."""
    return all(cell != "" for cell in board)

def get_best_move(board: List[str], bot_symbol: str) -> Optional[int]:
    """
    Calcola la miglior mossa per il bot usando l'algoritmo minimax.
    Ritorna l'indice della cella dove giocare, o None se non possibile.
    """
    opponent = "O" if bot_symbol == "X" else "X"

    def is_winner(b: List[str], symbol: str) -> bool:
        wins = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6],
        ]
        return any(all(b[i] == symbol for i in combo) for combo in wins)

    def minimax(b: List[str], depth: int, is_maximizing: bool) -> int:
        if is_winner(b, bot_symbol):
            return 10 - depth
        if is_winner(b, opponent):
            return depth - 10
        if is_board_full(b):
            return 0  # pareggio

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if b[i] == "":
                    b[i] = bot_symbol
                    score = minimax(b, depth + 1, False)
                    b[i] = ""
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if b[i] == "":
                    b[i] = opponent
                    score = minimax(b, depth + 1, True)
                    b[i] = ""
                    best_score = min(best_score, score)
            return best_score


    best_score = -float("inf")
    best_move = None
    for i in range(9):
        if board[i] == "":
            board[i] = bot_symbol
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i

    print(board)
    return best_move

def get_random_move(board: List[str], bot_symbol : str) -> Optional[int]:
    """
    Restituisce una mossa casuale valida per il bot.
    Ritorna l'indice della cella dove giocare, o None se non possibile.
    """
    valid_moves = [i for i in range(9) if board[i] == ""]
    if not valid_moves:
        return None
    return random.choice(valid_moves)

def available_moves(board: List[str]) -> List[int]:
    """
    Restituisce una lista di indici delle celle disponibili.
    """
    return [i for i in range(9) if board[i] == ""]


def get_medium_move(board: List[str], player_symbol: str) -> Optional[int]:
    bot_symbol = "O" if player_symbol == "X" else "X"
    logger.info(f"mosse consentite {available_moves(board)}")
     # Vincere se può
    for move in available_moves(board):
        copy_board = board[:]
        copy_board[move] = bot_symbol 
        if any(all(copy_board[i] == bot_symbol for i in combo) for combo in wins):
            logger.info(f"mossa vincente trovata {move}")
            return move

    #  Bloccare il giocatore se sta per vincere
    for move in available_moves(board):
        copy_board = board[:]
        copy_board[move] = player_symbol
        if any(all(copy_board[i] == player_symbol for i in combo) for combo in wins):
            logger.info(f"mossa bloccante trovata {move}")
            return move


    #  Prendere il centro se disponibile
    if board[4] == "":
        logger.info("bot prende il centro")
        return 4

    #  Prendere angolo libero
    corners = [i for i in [0,2,6,8] if board[i] == ""]
    if corners:
        logger.info(f"bot prende un angolo libero casuale {corners}")
        return random.choice(corners)

    #  Mossa casuale tra le restanti
    return random.choice(available_moves(board)) 


def get_move(board: List[str], player_symbol: str, difficulty : str ) -> Optional[int]:
    if difficulty == "easy":
        valid_moves = available_moves(board)
        return random.choice(valid_moves)
    elif difficulty == "medium":
      return get_medium_move(board, player_symbol)
    elif difficulty == "hard":
        return get_best_move(board, player_symbol)

async def get_rooms(redis):
    """
    Recupera tutte le stanze attive da Redis.
    Ritorna una lista di nomi delle stanze.
    """
    cursor = 0
    keys = []

    while True:
        cursor, partial_keys = await redis.scan(cursor, match="game:*:state",count=50)
        keys.extend(partial_keys)
        if cursor == 0:
            break

    rooms = [key.decode().split(":")[1] for key in keys]
    return rooms


def generate_room_name(length=6):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))


async def find_rooms_with_one_player(redis):
    """
    Trova le stanze con un solo giocatore.
    Ritorna una lista di nomi delle stanze.
    """
    
    rooms = await get_rooms(redis)
    single_player_rooms = []

    for room in rooms:
        raw_state = await redis.get(f"game:{room}:state")
        if raw_state:
            game_state = json.loads(raw_state)
            if len(game_state.get("players", {})) == 1:
                single_player_rooms.append(room)

    return single_player_rooms

async def find_one_room_with_one_player(redis):
    """
    Trova una stanza con un solo giocatore.
    Ritorna il nome della stanza o None se non trovata.
    """
    single_player_rooms = await find_rooms_with_one_player(redis)
    return single_player_rooms[0] if single_player_rooms else None



def is_valid_data(request: HttpRequest) -> Union[Tuple[list, str, str], JsonResponse]:
    logger.info("Verifica dati della richiesta...")
    try:
        data = json.loads(request.body)

        board = data.get("board")
        bot_symbol = data.get("bot_symbol")
        difficulty = data.get("difficulty")

        if difficulty not in ("easy", "medium", "hard"):
            return JsonResponse({"error": "Difficolta' non valida"}, status=400)

        if  bot_symbol not in ("X", "O"):
            return JsonResponse({"error": "simbolo del bot non valido"}, status=400)

        if len(board) != 9 or any(cell not in ("X", "O", "") for cell in board) or board.count("X") < board.count("O") or board.count("X") - board.count("O") > 1 :
            return JsonResponse({"error": "Board non valida"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON non valido"}, status=400)

    return board, bot_symbol, difficulty

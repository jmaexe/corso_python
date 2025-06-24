import copy
import json
import redis.asyncio as aioredis
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from game.utils import check_winner, get_move, is_valid_data
import logging

logger = logging.getLogger("game")

@csrf_exempt
def play_bot(request):
    # Permette solo richieste POST
    logger.info(f"Richiesta ricevuta: {request.method} {request.path}")
    if request.method != "POST":
        return HttpResponseBadRequest("Solo POST permesso")
        
    # Verifica i dati della richiesta
    logger.info(f"Contenuto della richiesta: {request.body}")

    result = is_valid_data(request)
    if isinstance(result, JsonResponse):
        return result  # errore

    board, bot_symbol, difficulty = result  # dati validi


    # Verifica se c'è già un vincitore
    winner = check_winner(board)
    if winner:
        return JsonResponse({"winner": winner})

    # Calcola la prossima mossa del bot (usando la funzione `get_move`)
    move = get_move(copy.deepcopy(board), bot_symbol, difficulty)

    if move is not None:
        board[move] = bot_symbol  # Applica la mossa del bot

    # Dopo la mossa, controlla di nuovo se c'è un vincitore
    winner = check_winner(board)

    # Risponde con:
    # - la board aggiornata
    # - l'indice della mossa fatta dal bot
    # - l'eventuale vincitore (X, O o None)
    return JsonResponse({
        "board": board,
        "index": move,
        "winner": winner,
    })


async def rooms(request):
    if request.method != "GET":
        return HttpResponseBadRequest("Solo GET permesso")
    
    redis = await aioredis.from_url("redis://127.0.0.1")
    cursor = 0
    keys = []

    while True:
        cursor, partial_keys = await  redis.scan(match="game:*:state", count=50)
        keys.extend(partial_keys)
        if cursor == 0:
            break
    
    rooms = []
    for key in keys:
        raw_state = await redis.get(key)
        if not raw_state: 
            continue
        game_state = json.loads(raw_state)
        logger.info(f"Game state for {key}: {game_state["player_names"]}")
        if game_state.get("players"):
            room_name = key.decode() if isinstance(key, bytes) else key
            room_name = room_name.split(":")[1]
            player_names = list(game_state["player_names"].values()) 
            rooms.append({"room_name": room_name, "players": player_names}) 

    await redis.close()

    return JsonResponse({"rooms": rooms})
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .utils import get_best_move, check_winner



@csrf_exempt
def play_bot(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Solo POST permesso")

    try:
        data = json.loads(request.body)
        board = data.get("board")
        bot_symbol = data.get("bot_symbol")
        if not board or bot_symbol not in ("X", "O"):
            return JsonResponse({"error": "Dati non validi"}, status=400)

        # Controlla che la board sia valida
        if len(board) != 9 or any(cell not in ("X", "O", "") for cell in board):
            return JsonResponse({"error": "Board non valida"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON non valido"}, status=400)

    # Controlla se c'è già un vincitore
    winner = check_winner(board)
    if winner:
        return JsonResponse({"winner": winner})

  # Verifica se è il turno del bot
    x_count = board.count("X")
    o_count = board.count("O")

    if bot_symbol == "X" and x_count > o_count:
        return JsonResponse({"error": "Non è il turno del bot"}, status=400)
    elif bot_symbol == "O" and o_count >= x_count:
        return JsonResponse({"error": "Non è il turno del bot"}, status=400)
    # Calcola la mossa migliore del bot
    best_move = get_best_move(board[:], bot_symbol)
    print(best_move)
    print("dopo best move : " , board)
    if best_move is not None:
        board[best_move] = bot_symbol

    # Dopo la mossa del bot, ricontrolla il vincitore
    winner = check_winner(board)
    print("dopo check winner : " , board)
    print("winner : " , winner)
    print("best move : " , best_move)

    return JsonResponse({
        "board": board,
        "index": best_move,
        "winner": winner,
    })

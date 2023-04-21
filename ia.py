import random

def ia(board, signe, difficulty="easy"):
    print(f"IA difficulty level: {difficulty}")
    if difficulty == "easy":
        play_easy(board)
    elif difficulty == "medium":
        play_medium(board, signe)
    elif difficulty == "hard":
        play_hard(board, signe)
    else:
        print("Invalid difficulty level")
        return False

def play_easy(board):
    # Jouer sur une case aléatoire
    while True:
        i = random.randint(0, 8)
        if board[i] == 0:
            return i

def play_medium(board, signe):
    # Vérifier si l'IA peut gagner en jouant sur une case libre
    for i in range(9):
        if board[i] == 0:
            board[i] = 2 if signe == "X" else 1
            if check_win(board, 2 if signe == "X" else 1):
                board[i] = 0
                return i
            board[i] = 0

    # Vérifier si l'adversaire peut gagner en jouant sur une case libre
    for i in range(9):
        if board[i] == 0:
            board[i] = 1 if signe == "X" else 2
            if check_win(board, 1 if signe == "X" else 2):
                board[i] = 0
                return i
            board[i] = 0

    # Jouer sur une case aléatoire
    while True:
        i = random.randint(0, 8)
        if board[i] == 0:
            return i

def play_hard(board, signe):
    # Vérifier si l'IA peut gagner en jouant sur une case libre
    for i in range(9):
        if board[i] == 0:
            board[i] = 2 if signe == "X" else 1
            if check_win(board, 2 if signe == "X" else 1):
                board[i] = 0
                return i
            board[i] = 0

    # Vérifier si l'adversaire peut gagner en jouant sur une case libre
    for i in range(9):
        if board[i] == 0:
            board[i] = 1 if signe == "X" else 2
            if check_win(board, 1 if signe == "X" else 2):
                board[i] = 0
                return i
            board[i] = 0

    # Jouer au centre si possible
    if board[4] == 0:
        return 4

    # Jouer dans un coin s'il est vide et l'adversaire n'occupe pas le centre
    corners = [0, 2, 6, 8]
    random.shuffle(corners)
    for i in corners:
        if board[i] == 0 and not board[4] == (1 if signe == "X" else 2):
            return i

    # Jouer dans une case adjacente à un signe déjà posé
    sides = [1, 3, 5, 7]
    random.shuffle(sides)
    for i in sides:
        if board[i] == 0:
            return i

    # Jouer sur une case aléatoire
    while True:
        i = random.randint(0, 8)
        if board[i] == 0:
            return i

    # Aucune case disponible pour jouer
    return False

def check_win(board, player):
    # Vérifier les lignes
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == player:
            return True
    # Vérifier les colonnes
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] == player:
            return True
    # Vérifier les diagonales
    if board[0] == board[4] == board[8] == player:
        return True
    if board[2] == board[4] == board[6] == player:
        return True
    # Aucun alignement de trois signes trouvés
    return False
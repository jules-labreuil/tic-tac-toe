# Importer les modules nécessaires
import ia
import tkinter as tk  # Module pour créer des interfaces graphiques
from tkinter import simpledialog  # Boîte de dialogue pour poser une question simple
from tkinter import messagebox  # Boîte de dialogue pour afficher des messages d'erreur ou des informations
import io
from PIL import ImageTk, Image
import urllib.request

# Créer la fenêtre principale
root = tk.Tk()
root.title("Konoha_Tic_Tac_Toe")

# Télécharger l'image à partir d'une URL
url = "https://zupimages.net/up/23/16/hxx6.png"
with urllib.request.urlopen(url) as url_file:
    img_data = url_file.read()

# Ouvrir l'image et la convertir pour Tkinter
img = Image.open(io.BytesIO(img_data))
tk_img = ImageTk.PhotoImage(img)

# Utiliser l'image dans votre fenêtre Tkinter
root.iconphoto(True, tk_img)

# Créer les boutons pour les cases du plateau de jeu
BUTTON_WIDTH = 8  # Largeur des boutons
BUTTON_HEIGHT = 4  # Hauteur des boutons
buttons = []  # Liste pour stocker les boutons
for i in range(9):  # Boucle pour créer 9 boutons
    # Créer le bouton avec un texte vide et la fonction on_click() comme callback
    button = tk.Button(root, text="", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                       command=lambda i=i: on_click(i))
    # Positionner le bouton dans la grille (3x3) en fonction de son index
    button.grid(row=i//3, column=i%3)
    # Ajouter le bouton à la liste
    buttons.append(button)

# Créer une étiquette pour afficher le message de fin de partie
label = tk.Label(root, text="")
label.grid(row=3, column=0, columnspan=3)

# Définir la fonction pour mettre à jour la couleur des boutons en fonction de la difficulté choisie
def update_button_color():
    global buttons, selected_difficulty
    if difficulty == "easy":
        color = "#A9F5A9"  # Vert clair pour la difficulté facile
    elif difficulty == "medium":
        color = "#CED8F6"  # Bleu clair pour la difficulté moyenne
    elif difficulty == "hard":
        color = "#F78181"  # Rouge clair pour la difficulté difficile
    for button in buttons:  # Parcourir la liste des boutons
        button.config(bg=color)  # Mettre à jour la couleur du bouton

# Définir la fonction pour choisir la difficulté
def choose_difficulty():
    global difficulty, selected_difficulty
    valid_difficulties = ["easy", "medium", "hard"]
    while True:
        difficulty = simpledialog.askstring("Difficulté", "Choisissez la difficulté (easy/medium/hard)")
        if difficulty in valid_difficulties:
            break
        elif difficulty is None:  # Vérifier si l'utilisateur a cliqué sur Annuler
            root.destroy()  # Fermer la fenêtre principale
            return
        else:
            messagebox.showerror("Difficulté invalide", "La difficulté choisie est invalide. Veuillez choisir une difficulté valide (easy, medium ou hard).")
    selected_difficulty = difficulty
    update_button_color()  # Ajout de cet appel pour mettre à jour la couleur des boutons

# Fonction pour réinitialiser les variables de jeu
def reset_game():
    global player, board, game_over
    player = 1
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    game_over = False
    label.config(text="")
    for i in range(9):
        buttons[i].config(text="")

# Appeler la fonction pour choisir la difficulté
choose_difficulty()

# Initialiser les variables de jeu
player = 1  # Le joueur 1 commence
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # Plateau de jeu vide
game_over = False

# Fonction pour vérifier si un joueur a gagné
def check_win(player):
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

# Fonction pour afficher un message de fin de partie
def show_message(message):
    global label
    label.config(text=message)

# Fonction pour gérer le clic sur une case
def on_click(i):
    global player, game_over
    
    # Vérifier si la partie est terminée ou si la case est déjà prise
    if game_over or board[i] != 0:
        return
    
    # Mettre à jour le plateau de jeu et le bouton cliqué
    board[i] = player
    buttons[i].config(text="X" if player == 1 else "O")
    
    # Vérifier si le joueur a gagné ou s'il y a un match nul
    if check_win(player):
        show_message("Joueur " + str(player) + " a gagné !")
        game_over = True
    elif all(board):
        show_message("Match nul !")
        game_over = True
    else:
        # Changer de joueur
        player = 2 if player == 1 else 1
        
        # Laisser l'IA jouer si c'est son tour
        if player == 2:
            # Déterminer le coup à jouer en fonction de la difficulté choisie
            if difficulty == "easy":
                i = ia.play_easy(board)
            elif difficulty == "medium":
                i = ia.play_medium(board, "O" if player == 1 else "X")
            elif difficulty == "hard":
                i = ia.play_hard(board, "O" if player == 1 else "X")
            
            # Vérifier si l'IA a rencontré une erreur ou si le coup est déjà pris
            if i is False:
                show_message("L'IA a rencontré une erreur.")
                messagebox.showerror("Erreur", "L'IA a rencontré une erreur.")
                game_over = True
            elif board[i] != 0:
                # Si le coup est déjà pris, changer de joueur et laisser l'humain jouer
                player = 2 if player == 1 else 1
                messagebox.showerror("Coup invalide", "Le coup sélectionné est invalide. Veuillez sélectionner une autre case.")
            else:
                # Sinon, laisser l'IA jouer son coup
                on_click(i)
    
    # Si la partie est terminée, proposer de lancer une nouvelle partie ou de quitter
    if game_over:
        answer = messagebox.askyesno("Nouvelle partie ?", "Voulez-vous lancer une nouvelle partie ?")
        if answer:
            # Réinitialiser le plateau de jeu et lancer une nouvelle partie
            reset_game()
            choose_difficulty()
            if player == 2:
                on_click(None)
        else:
            # Quitter le jeu
            root.destroy()

# Boucle principale du jeu
root.mainloop()
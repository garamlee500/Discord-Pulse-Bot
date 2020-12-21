all_game_strings = {
    "rockrock":'Draw',
    "rockpaper":'Loss',
    'rockscissors':'Victory',
    'paperrock':'Victory',
    'paperpaper':'Draw',
    'paperscissors':'Loss',
    'scissorsrock':'Loss',
    'scissorspaper':'Victory',
    'scissorsscissors':'Draw'
    }




def play(player_choice): # player_choice should be either rock paper or scissors
    player_choice = player_choice.strip().lower()
    possible_choices = ["rock","paper","scissors"]
    # check if player's choice is a real option
    if not player_choice in possible_choices:
        return("Invalid choice. Please either choose rock, paper or scissors")

    from random import randint
    computer_choice = possible_choices[randint(0,2)]
    
    game_string= player_choice + computer_choice
    
    
    result = all_game_strings[game_string]
    
    return (result + '\n' + 'You played ' + player_choice + ' and the computer chose '+ computer_choice + '.')
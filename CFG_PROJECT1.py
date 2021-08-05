import random

import requests

def random_pokemon():
    pokemon_number = random.randint(1, 151)
    url = "https://pokeapi.co/api/v2/pokemon/{}/".format(pokemon_number)
    response = requests.get(url)
    pokemon = response.json()

    return {
        "name": pokemon["name"],
        "id": pokemon["id"],
        "height": pokemon["height"],
        "weight": pokemon["weight"],
        "moves": pokemon["moves"],
    }

def run():
    my_pokemon = random_pokemon()
    print('You were given {}'.format(my_pokemon['name']))
    moves = len(my_pokemon['moves'])
    print(moves)
    stat_choice = input('Which stat do you want to use? (id, height, weight, moves) ')
    opponent_pokemon = random_pokemon()
    print('The opponent chose {}'.format(opponent_pokemon['name']))
    opponent_moves = len(opponent_pokemon['moves'])
    print(opponent_moves)

    if stat_choice.lower() == 'moves':
        my_stat = moves
        opponent_stat = opponent_moves
    else:
        my_stat = my_pokemon[stat_choice]
        opponent_stat = opponent_pokemon[stat_choice]

    if my_stat > opponent_stat:
        print('You Win!')
    elif my_stat < opponent_stat:
        print('You Lose!')
    else:
        print('Draw!')

run()

# testing!
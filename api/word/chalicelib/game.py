

import boto3

from api.word.chalicelib.constants import ACTIVE_GAMES, LEXICON
from chalicelib.data import address_to_partition


def get_new_word(ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')
    lexicon = ddb.Table(LEXICON)
    lexicon.query(
        
    )

def guess_result(guess, word):
    guess = guess.lower()
    word = word.lower()
    word_chars = set(word)

    result = []
    for i, char in enumerate(guess):
        if char == word[i]:
            result.append(1)
        elif char in word_chars:
            result.append(2)
        else:
            result.append(0)
    return result


def get_new_game(address, ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')
    word = get_new_word(ddb)
    item = {
        'address_partition': address_to_partition(address),
        'address': address,
        'solution': word,
        'guesses': [],
        'results': []
    }
    active_games = ddb.Table(ACTIVE_GAMES)
    active_games.put_item(
        Item=item
    )
    return item
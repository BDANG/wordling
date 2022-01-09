

import boto3

from api.word.chalicelib.constants import ACTIVE_GAMES, LEXICON, MIN_LEN, MAX_LEN
from chalicelib.data import address_to_partition
import random
import hashlib
import uuid


def get_new_word(ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')
    lexicon = ddb.Table(LEXICON)

    for _ in range(10):
        length = random.randint(MIN_LEN, MAX_LEN)
        random_hash = hashlib.sha256(str(uuid.uuid4()).encode('utf-8')).hexdigest()
        result = lexicon.query(
            ProjectionExpression="word",
            KeyConditionExpression='length = :length AND hash < :hash',
            ExpressionAttributeValues={
                ':length': {'N': length},
                ':hash': {'S': random_hash}
            }
        )

        if result:
            break
    word = random.choice(result['Items'])
    print(word)
    

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
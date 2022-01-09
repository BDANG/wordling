import hashlib
import boto3
from chalicelib.constants import ACTIVE_GAMES, ADDRESS_PARITIONS, LEXICON


def address_to_partition(addr_str):
    return int(addr_str, 16) % ADDRESS_PARITIONS


def get_active_game(address, ddb=None):
    if not ddb:
        ddb = boto3.resource('dyanmodb')
    active_games = ddb.Table(ACTIVE_GAMES)

    response = active_games.get_item(
        Key={'address_partition': address_to_partition(address), 'address': address}
    )

    return response['Item']


def add_word(word, ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')
    word = word.lower()
    word_hash = hashlib.sha256(word.encode('utf-8')).hexdigest()
    item = {
        'length': len(word),
        'hash': word_hash,
        'word': word
    }

    lexicon = ddb.Table(LEXICON)
    lexicon.put_item(Item=item)

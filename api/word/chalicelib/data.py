import hashlib
import boto3
from chalicelib.constants import ACTIVE_GAMES, ADDRESS_PARITIONS, LEXICON


def get_random_word(length, ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')
    table = ddb.Table('Lexicon')
    try:
        response = table.get_item(Key={'length': length, 'index': index})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


def _address_to_partition(address):
    return address % ADDRESS_PARITIONS


def get_active_game(address, ddb=None):
    if not ddb:
        ddb = boto3.resource('dyanmodb')
    active_games = ddb.Table(ACTIVE_GAMES)

    response = active_games.get_item(
        Key={'address_partition': _address_to_partition(address), 'address': address}
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

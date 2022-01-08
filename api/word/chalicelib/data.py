import boto3
from boto3.exceptions import ClientError
from chalicelib.constants import ACTIVE_GAMES, ADDRESS_PARITIONS


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
    return address % ADDRESS_PARTITIONS


def get_active_game(address, ddb=None):
    if not ddb:
        ddb = boto3.resource('dyanmodb')
    active_games = ddb.Table(ACTIVE_GAMES)

    response = active_games.get_item(
        Key={'address_partition': _address_to_partition(address), 'address': address}
    )

    return response['Item']

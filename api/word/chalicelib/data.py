import boto3
from chalicelib.constants import ACTIVE_GAMES, ADDRESS_PARITIONS


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
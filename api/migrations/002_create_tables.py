import boto3
from chalicelib.constants import ACTIVE_GAMES, UNCLAIMED, HISTORICAL


def create_table(table_name, ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')
    return ddb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'address_partition',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'address',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'address_partition',
                'AttributeType': 's'
            },
            {
                'AttributeName': 'address',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )


if __name__ == '__main__':
    ddb = boto3.resource('dynamodb')
    active_games = create_table(ACTIVE_GAMES, ddb=ddb)
    print(f'Active Games status: {active_games.table_status}')
    unclaimed = create_table(UNCLAIMED, ddb=ddb)
    print(f'Unclaimed Games status: {unclaimed.table_status}')
    historical = create_table(HISTORICAL, ddb=ddb)
    print(f'Historical Games status: {historical.table_status}')

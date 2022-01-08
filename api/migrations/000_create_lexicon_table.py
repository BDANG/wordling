import boto3
from chalicelib.constants import LEXICON


def create_lexicon(ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')
    return ddb.create_table(
        TableName=LEXICON,
        KeySchema=[
            {
                'AttributeName': 'length',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'hash',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'length',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'hash',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )


if __name__ == '__main__':
    lexicon_table = create_lexicon()
    print(f'Lexicon status: {lexicon_table.table_status}')
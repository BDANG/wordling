import boto3


def create_lexicon(ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')
    return ddb.create_table(
        TableName="Lexicon",
        KeySchema=[
            {
                'AttributeName': 'length',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'index',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'length',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'index',
                'AttributeType': 'N'
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
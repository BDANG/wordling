import boto3
from boto3.exceptions import ClientError


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

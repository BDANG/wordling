import boto3


def load_lexicon(ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')
    
    lexicon_table = ddb.Table('Lexicon')
    lexicon_table.put_item(
        Item={
            'length': 3,
            'word': 'foo',
            'index': 1
        }
    )
    lexicon_table.put_item(
        Item={
            'length': 3,
            'word': 'woo',
            'index': 2
        }
    )
    lexicon_table.put_item(
        Item={
            'length': 4,
            'word': 'woow',
            'index': 1
        }
    )


if __name__ == '__main__':
    load_lexicon()
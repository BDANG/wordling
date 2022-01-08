import boto3
from chalicelib.data import add_word


def load_lexicon(ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')
    
    add_word('free', ddb=ddb)
    add_word('yolo', ddb=ddb)
    add_word('yolo', ddb=ddb)


if __name__ == '__main__':
    load_lexicon()
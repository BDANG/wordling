from chalice import Chalice
import boto3
from boto3.dynamodb.conditions import Key
import hashlib
from chalicelib.constants import LEXICON, ACTIVE_GAMES


app = Chalice(app_name='word')


@app.route('/')
def index():
    return {'wordling': 'by daoistdang'}


@app.route('/game/guess', methods=['POST'])
def guess_route():
    """
    Submit a guess, returns 404 if the guess is not a word
    Otherwise returns list of ints to indicate the results of the guess
      0: not found
      1: found but not correct
      2: correct
    """
    ddb = boto3.resource('dynamodb')
    game = get_active_game(address, ddb=ddb)

    word = game['solution']
    result = guess_result(guess, word)


@app.route('/game', methods=['POST'])
def get_game_route():
    """
    Retrieve a new game (or an existing game)
    """
    body = app.current_request.json_body
    address = body['address']

    ddb = boto3.resource('dynamodb')
    lexicon = ddb.Table(LEXICON)
    
    game = get_active_game(address, ddb=ddb)
    # if not found fetch a new word

    # get random length
    r = random.randint(5, 8)

    # TODO: include sort key
    response = lexicon.query(
        KeyConditionExpression=Key('length').eq(r)
    )

    word = random.choice(response['Items'])
    return word


@app.route('/word', methods=['POST'])
def add_word_route():
    """
    Adds a word to the lexicon
    """
    body = app.current_request.json_body
    word = body['word'].lower()
    length = len(word)
    word_hash = hashlib.sha256(bytes(word)).hexdigest()

    ddb = boto3.resource('dynamodb')
    lexicon = ddb.Table(LEXICON)
    lexicon.put_item(
        Item={
            'length': length,
            'hash': word_hash,
            'word': word
        }
    )
    return {
        'message': f'Added {word}'
        'success': True
    }


@app.route('/word/{word}', methods=['GET'])
def word_check_route(word):
    """
    Check if a word exists
    """
    word = word.lower()
    ddb = boto3.resource('dynamodb')
    lexicon = ddb.Table(LEXICON)
    try:
        response = lexicon.get_item(Key={'length': length, 'word': word})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

from chalice import Chalice

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


@app.route('/game', methods=['GET'])
def get_game_route():
    """
    Retrieve a new game (or an existing game)
    """


@app.route('/word', methods=['POST'])
def add_word_route():
    """
    Adds a word to the lexicon
    """


@app.route('/word/{word}', methods=['GET'])
def word_check_route():
    """
    Check if a word exists
    """
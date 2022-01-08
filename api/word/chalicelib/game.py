

def guess_result(guess, word):
    guess = guess.lower()
    word = word.lower()
    word_chars = set(word)

    result = []
    for i, char in enumerate(guess):
        if char == word[i]:
            result.append(1)
        elif char in word_chars:
            result.append(2)
        else:
            result.append(0)
    return result

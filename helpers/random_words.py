import random
from resources.words import words as words_list

def random_words() -> list[str]:
    return [random.choice(words_list) for _ in range(15)]
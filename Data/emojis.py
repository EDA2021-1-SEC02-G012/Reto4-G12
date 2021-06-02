import random

lista_emojis = [
    '🤠', '🤡', '💯', '🤑', '🥲',
    '🌈', '🐸', '🦠', '🆘', '🍕',
    '🦋', '💟', '✨', '🧚', '🧃',
    '🐸', '⭐', '💅', '🧷', '📈',
    '🔥', '💩', '👽', '💋', '🧚',
    '🤰'
    ]


def random_emoji(lenght):
    random_num = random.sample(range(len(lista_emojis)), lenght)
    string = " "
    for i in random_num:
        string += (lista_emojis[i])
        string += ' '
    return string

one_letter_point = ['e', 'a', 'o', 't', 'i', 'n', 'r', 's', 'l', 'u']
two_letter_point = ['d', 'g']
three_letter_point = ['c', 'm', 'b', 'p']
four_letter_point = ['h', 'f', 'w', 'y', 'p']
five_letter_point = ['k']
eight_letter_point = ['j']
ten_letter_point = ['q', 'z']


def scrabble_word_count(word):
    res = 0
    for letter in word:
        if letter in one_letter_point:
            res += 1
        elif letter in two_letter_point:
            res += 2
        elif letter in three_letter_point:
            res += 3
        elif letter in four_letter_point:
            res += 4
        elif letter in five_letter_point:
            res += 5
        elif letter in eight_letter_point:
            res += 8
        elif letter in ten_letter_point:
            res += 10
    return res




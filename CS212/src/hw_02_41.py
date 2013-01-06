import re

# --------------
# User Instructions
#
# Write a function, compile_word(word), that compiles a word
# of UPPERCASE letters as numeric digits. For example:
# compile_word('YOU') => '(1*U + 10*O +100*Y)'
# Non-uppercase words should remain unchaged.

def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""

    w = '('
    if word.isupper():
        for i in range(len(word)):
            w += str(10**i) + '*' + word[len(word)-(i+1)] + '+'
        return w[:len(w)-1] + ')'
    else:
        return word


def compile_word_better(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""

    if word.isupper():
        terms = [('%s*%s' % (10**i, d))
                for (i,d) in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    else:
        return word


if __name__ == "__main__":
    print compile_word_better('YOU');
    print compile_word_better('you');



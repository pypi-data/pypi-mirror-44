from sys import argv

from ttrw import get_random_words

if len(argv) > 1:
    print(get_random_words(lang=argv[1]))
else:
    print(get_random_words())

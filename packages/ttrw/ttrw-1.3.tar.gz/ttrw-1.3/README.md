# TTRW

It's a simple python package that returns a string with a few random words similar to name generator for twitch.tv clips.
Words are chosen from built in dictionary and capitalized.
The first one is an adverb, the second is an adjective and the third is a noun.

You can also choose to get single word (adjective/adverb/noun).

There are english and polish dictionaries available (Polish words without national/accented characters).

```
>>> ttrw.get_random_words()  
VerySadFish
```

```
$ python -m ttrw
SlightlyHandsomePotato
```

## Installation:
Use pip:
```commandline
pip install ttrw
```

## Usage:
Sample usage:
```python
import ttrw

print("Available languages:")
print(ttrw.languages)

print(ttrw.get_random_words())
print(ttrw.get_random_words("en"))
print(ttrw.get_random_words(lang="pl"))

print(ttrw.random_noun())
print(ttrw.random_adjective(lang="pl"))
```

You can also just execute the module in terminal:
```
python -m ttrw
python -m ttrw en
python -m ttrw pl
```

## References:

English dictionary is based on WordNet®.  
Polish Dictionary is based on ArkadiaWiki and https://sjp.pl/.  

Licenses for each dictionary are in their respective folders.

## License:
Code is under MIT license. See "LICENSE" file.
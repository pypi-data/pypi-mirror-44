# TTRW

It's a simple python package that returns a string with a few random words similiar to name generator for twitch.tv clips.
Words are chosen from built in dictionary and capitalized.
The first one is an adverb, the second is an adjective and the third is a noun.

Currently there are english and polish dictionaries available (Polish words without national characters).

```
>>> ttrw.get_random_words()  
VerySadFish
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
```

## References:

English dictionary is based on WordNet®.  
Polish Dictionary is based on ArkadiaWiki and https://sjp.pl/.  

Licenses for each dictionary are in their respective folders.

## License:
Code is under MIT license. See "LICENSE" file.
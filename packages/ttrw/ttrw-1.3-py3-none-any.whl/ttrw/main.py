from random import choice

from ttrw.dictionaries import words, languages


def get_random_words(lang: str = "en") -> str:
    """Function returns a string with random set of three words form selected language (default is english).
    Words are chosen from built in dictionary and capitalized.
    The first one is an adverb, the second is an adjective and the third is a noun.

    Raises ValueError if chosen language is not supported.
    """

    adv = random_adverb(lang).capitalize()
    adj = random_adjective(lang).capitalize()
    nou = random_noun(lang).capitalize()

    if lang == "pl" and nou[-1] == "a":
        return_string = adv + adj[:-1] + "a" + nou
    else:
        return_string = adv + adj + nou

    return return_string


def random_adverb(lang: str = "en") -> str:
    """Function returns random adverb in a given language.

    Raises ValueError if chosen language is not supported."""
    if lang in languages:
        return str.rstrip(choice(words.get(lang).get("adverbs")))
    else:
        raise ValueError(f"Value: '{lang}' is not a supported language.")


def random_adjective(lang: str = "en") -> str:
    """Function returns random adjective in a given language.

    Raises ValueError if chosen language is not supported."""
    if lang in languages:
        return str.rstrip(choice(words.get(lang).get("adjectives")))
    else:
        raise ValueError(f"Value: '{lang}' is not a supported language.")


def random_noun(lang: str = "en") -> str:
    """Function returns random noun in a given language.

    Raises ValueError if chosen language is not supported."""
    if lang in languages:
        return str.rstrip(choice(words.get(lang).get("nouns")))
    else:
        raise ValueError(f"Value: '{lang}' is not a supported language.")


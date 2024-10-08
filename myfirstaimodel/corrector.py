import csv
import random

PHRASES = {}
WORD_TREES = {}

"""
The WORD_TREES is a binary tree, when containing three lowercase phrases:

"what is meaning of life"
"who makes best beers"
"who is president of united states"

The three phrases would be represented as:

{
    "what": {
        "is": {
            "meaning": {
                "of": {
                    "life": {}
                }
            }
        }
    },
    "who": {
        "makes": {
            "best": {
                "beers": {}
            }
        },
        "is": {
            "president": {
                "of": {
                    "united": {
                        "states": {}
                    }
                }
            }
        }
    }
}
"""

def recurse_word(phrase, tree):
    """
    Return the first word in the phrase and add following words to the tree.
    """

    word, _, after = phrase.partition(" ")

    if word not in tree:
        tree[word] = {}

    if after:
        recurse_word(after, tree[word])


def initialize():
    """
    Initialize the corrector by loading the phrases and building the word trees.
    """

    # Load the phrases
    with open('/app/ai_out.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            line = row[0]
            phrase = line.strip()
            lower = phrase.lower()
            PHRASES[lower] = phrase

            # Also add partial phrases
            prefix = ''
            lower_prefix = ''
            for partial, lower_partial in zip(phrase.split(), lower.split()):
                prefix += partial
                lower_prefix += lower_partial
                PHRASES[lower_prefix] = prefix

                prefix += ' '
                lower_prefix += ' '

            recurse_word(lower, WORD_TREES)

    print('Loaded phrases:', len(PHRASES))


def levenshtein_distance(s1, s2):
    """
    Return the Levenshtein distance between two strings.
    """

    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]

        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]


def ensure_valid(text):
    """
    Takes in text and if it is already valid, returns it.
    Otherwise, fills in random words from tree to make it valid.
    """

    if len(text) > 0 and text[-1] in ['.', '?', '!']:
        return text
    
    words = text.lower().split()
    current_tree = WORD_TREES
    parts = []

    while True:
        if words and words[0] in current_tree:
            word = words.pop(0)
        else:
            word = random.choice(list(current_tree.keys()))

        parts.append(word)

        current_tree = current_tree[word]

        if not current_tree:
            return PHRASES[" ".join(parts)]


def matcher(prefix, word, next, tree):
    """
    Return the closest match to the word in the tree.

    prefix is the currently built phrase from previous parts of tree
    word is the current word to match either by direct match or by calculating minimal Lev distance
    next is the next parts of phrase to match
    tree is the current tree to traverse
    """

    print('Matcher:', prefix, word, next, list(tree.keys()))

    if not tree or not word:
        return prefix
    
    next_word, _, next_next = next.partition(" ")

    if word in tree:
        prefix.append(word)
        return matcher(prefix, next_word, next_next, tree[word])

    distances = {}
    for key in tree:
        distances[key] = levenshtein_distance(word, key)
    
    closest = min(distances, key=distances.get)
    prefix.append(closest)

    return matcher(prefix, next_word, next_next, tree[closest])


def corrector(text):
    """
    Take in a question string and return a corrected version of it.
    """

    if text.strip() == "":
        return ""

    # Split to words
    words = text.split()

    # Check for exact match
    if text.strip().lower() in PHRASES.keys():
        return PHRASES[text.lower().strip()]
    
    # Check for word by word match
    tree = WORD_TREES
    prefix = []
    current, _, next = text.lower().partition(" ")
    corrected = matcher(prefix, current, next, tree)

    return PHRASES[" ".join(corrected).lower()]


# Ensure the corrector DB is initialized when module code loads
if not PHRASES:
    initialize()
    #print('Phrases:', PHRASES)

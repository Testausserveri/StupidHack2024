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
    with open('/app/helpers/phrases.txt') as f:
        for line in f:
            phrase = line.strip()
            lower = phrase.lower()
            PHRASES[lower] = phrase
            recurse_word(lower, WORD_TREES)


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


def matcher(prefix, word, next, tree):
    """
    Return the closest match to the word in the tree.

    prefix is the currently built phrase from previous parts of tree
    word is the current word to match either by direct match or by calculating minimal Lev distance
    next is the next parts of phrase to match
    tree is the current tree to traverse
    """

    if not tree or not next:
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

    # Split to words
    words = text.split()

    # Check for exact match
    if text.strip().lower() in PHRASES.keys():
        return PHRASES[text]
    
    # Check for word by word match
    tree = WORD_TREES
    prefix = []
    next = text.lower()
    corrected = matcher(prefix, words[0], next, tree)

    return " ".join(corrected)



initialize()
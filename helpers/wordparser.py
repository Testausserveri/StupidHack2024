import json
import requests
import csv


def recurse_word(phrase, answer, tree):
    word, _, after = phrase.partition(" ")
    if after:
        if word not in tree:
            tree[word] = {}
        recurse_word(after, answer, tree[word])
    else:
        tree[word] = answer


def write_if(file, current_indentation, tree):
    for word, answer in tree.items():
        file.write(" "*4*current_indentation + f"if input[{current_indentation-1}] == {repr(word)}:\n")
        if isinstance(answer, dict):
            write_if(file, current_indentation+1, answer)
        else:
            file.write(" "*4*(current_indentation+1) + f"return {answer}\n")



def output():
    with open("ai_out.csv", "r") as f:
        reader = csv.reader(f)
        phrases = [(row[0], row[1]) for row in reader]

    tree = {}
    for phrase in phrases:
        recurse_word(phrase[0], phrase[1], tree)

    with open("myfirstaimodel/backend.py", "w") as f:
        f.write("def aimodel(input):\n")
        write_if(f, 1, tree)

        f.write("    return \"Invalid input\"\n")

if __name__=="__main__":
    output()

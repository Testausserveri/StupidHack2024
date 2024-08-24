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


def generate(prompt):
    req = requests.post('http://localhost:11434/api/generate',
                 json={"model":"dolphin-mixtral","prompt":prompt})

    ans = ""
    for line in req.iter_lines():
        print(line)
        line_obj = json.loads(line)
        if line_obj['done'] == "true":
            break
        ans += str(line_obj['response'])

    print(ans)
    return ans


def main():
    with open("phrases.txt", "r") as f:
        prompts = [x.strip() for x in f.readlines()]

    print(len(prompts))
    with open("ai_out.csv", "w") as w:
        for prompt in prompts:
            print(f"generating: {prompt}")
            answer = generate(prompt)
            csv_writer = csv.writer(w)
            csv_writer.writerow([prompt, answer])


def write_if(file, current_indentation, tree):
    for word, answer in tree.items():
        file.write(" "*4*current_indentation + f"if input[{current_indentation}] == '{word}':\n")
        if isinstance(answer, dict):
            write_if(file, current_indentation+1, answer)
        else:
            file.write(" "*4*(current_indentation+1) + f"return '{answer}'\n")



def output():
    with open("ai_out.csv", "r") as f:
        reader = csv.reader(f)
        phrases = [(row[0], row[1]) for row in reader]

    tree = {}
    for phrase in phrases:
        recurse_word(phrase[0], phrase[1], tree)

    with open("myfirstaimodel/backend.py", "w") as f:
        f.write("def aimodel(input):\n")
<<<<<<< HEAD
        for phrase in phrases:
            for i,word in enumerate(phrase[0].split()):
                f.write(" "*4*(i+1) + f"if input[{i}] == '{word}':\n")
            f.write(" "*4*(len(phrase[0].split())+1) + f"return '''{phrase[1]}'''\n")
=======
        write_if(f, 1, tree)


        # for phrase in phrases:
        #     for i,word in enumerate(phrase[0].split()):
        #         f.write(" "*4*(i+1) + f"if input[{i}] == '{word}':\n")
        #     f.write(" "*4*(len(phrase[0].split())+1) + f"return '{phrase[1]}'\n")
>>>>>>> 7c51e05 (Small changes to JS logic and wordparser)


if __name__=="__main__":
    output()

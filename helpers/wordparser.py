import json
import requests
import csv


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


def output():
    with open("ai_out.csv", "r") as f:
        reader = csv.reader(f)
        phrases = [(row[0], row[1]) for row in reader]

    with open("myfirstaimodel/backend.py", "w") as f:
        f.write("def aimodel(input):\n")
        for phrase in phrases:
            for i,word in enumerate(phrase[0].split()):
                f.write(" "*4*(i+1) + f"if input[{i}] == '{word}':\n")
            f.write(" "*4*(len(phrase[0].split())+1) + f"return '''{phrase[1]}'''\n")


if __name__=="__main__":
    output()

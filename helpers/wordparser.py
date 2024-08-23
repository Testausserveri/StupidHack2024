import csv
import json
import requests

def generate(prompt):
    req = requests.post('http://localhost:11434/api/generate',
                 json={"model":"dolphin-mixtral","prompt":prompt})

    ans = ""
    for line in req.iter_lines():
        print(line)
        line_obj = json.loads(str(line))
        if line_obj['done'] == "true":
            break
        ans.join(line_obj['response'])

    print(ans)
    return ans

def main():
    words = []
    with open("words.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            for word in row:
                if word != "" and word != "INTERROGATIVE" and word != "NOUN" and word != "VERB" and word != "ADJECTIVE":
                    print(word)
                    words.append(word)

        i = 0
        print(len(words))
        for first_word in words:
            for second_word in words:
                for third_word in words:
                    prompt = f"{first_word} {second_word} {third_word}"
                    print(f"generating: {prompt}")
                    generate(prompt)
                    i += 1
                    if i > 50:
                        break

if __name__=="__main__":
    main()



import json
import requests


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
    answers = []
    for prompt in prompts:
        print(f"generating: {prompt}")
        answers += generate(prompt)

    return answers


if __name__=="__main__":
    main()

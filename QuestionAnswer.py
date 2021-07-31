import json
from random import randint


def load_json():
    with open('./sample.json') as f:
        data = json.load(f)
        return data


def generator(data):
    question_num = len(data)
    no = randint(0, question_num - 1)

    # Indexing
    q = list(data.keys())[no]
    answer = data[q][0]['answer']
    option1 = data[q][0]['options'][0]['option1']
    option2 = data[q][0]['options'][0]['option2']
    option3 = data[q][0]['options'][0]['option3']
    option4 = data[q][0]['options'][0]['option4']

    print('Question: ', q)
    print('Option 1: ', option1)
    print('Option 2: ', option2)
    print('Option 3: ', option3)
    print('Option 4: ', option4)
    print('Correct Answer: ', answer)


if __name__ == "__main__":
    generator(load_json())

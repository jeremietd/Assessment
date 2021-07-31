import json
import inquirer

data = {}


def create(question, answer1, answer2, answer3, answer4, correct_answer):
    data[question] = []
    data[question].append({
        'options':
            [{'option1': str(answer1),
              'option2': str(answer2),
              'option3': str(answer3),
              'option4': str(answer4)}],
        'answer': str(correct_answer)
    })

    return data

def qa():
    questions = [
        inquirer.Text('question', message="Enter Question"),
        inquirer.Text('answer1', message="Enter 1st option"),
        inquirer.Text('answer2', message="Enter 2nd option"),
        inquirer.Text('answer3', message="Enter 3rd option"),
        inquirer.Text('answer4', message="Enter 4th option")
    ]

    return inquirer.prompt(questions)

def confirm(ans1, ans2, ans3, ans4):
    questions = [
        inquirer.List('correct_answer',
                      message="Which one is the correct answer?",
                      choices=[ans1, ans2, ans3, ans4],
                      ),
        inquirer.List('status',
                      message="Do you want to add more?",
                      choices=[True, False],
                      )
    ]

    return inquirer.prompt(questions)


if __name__ == "__main__":
    status = 'True'
    while status == "True":
        qas = qa()
        confirmation = confirm(str(qas['answer1']), str(qas['answer2']), str(qas['answer3']), str(qas['answer4']))
        correct_answer = str(confirmation['correct_answer'])
        status = str(confirmation['status'])

        data = create(qas['question'], qas['answer1'], qas['answer2'], qas['answer3'], qas['answer4'], correct_answer)

    print(data)
    with open("sample.json", "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)



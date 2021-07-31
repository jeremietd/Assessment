import random
import tkinter as tk
from tkinter import ttk
import time
import pandas as pd
import easygui
from tkmacosx import Button as button
from essential_generators import DocumentGenerator, MarkovTextGenerator
import json
from math import nan

passage = DocumentGenerator(text_generator=MarkovTextGenerator())


def question():
    global difficulty  # accessible outside of the function
    global nummax
    age = int(userdata.age)
    if age < 10:
        nummax = 10
        difficulty = 2
    elif 10 <= age < 20:
        nummax = 25
        difficulty = 3
    elif 20 <= age < 40:
        nummax = 50
        difficulty = 8
    elif age >= 40:
        nummax = 30
        difficulty = 3

    a = random.randint(0, int(nummax))  # generate random number from 0 to nummax
    b = random.randint(0, int(nummax))
    c = random.randint(0, int(nummax))
    showpg(Game)  # calls up the main game page

    symbol = random.randint(1, difficulty)  # generate a random operator from the dictionary
    global answer
    if symbol == 1:
        equation = str(a) + " + " + str(b)
        answer = a + b

    elif symbol == 2:
        equation = str(a) + " - " + str(b)
        answer = a - b

    elif symbol == 3:
        equation = str(a) + " x " + str(b)
        answer = a * b

    elif symbol == 4:
        equation = str(a) + " - " + str(b) + " x " + str(c)
        answer = a - b * c

    elif symbol == 5:
        equation = str(a) + " + " + str(b) + " x " + str(c)
        answer = a + b * c

    elif symbol == 6:
        equation = str(a) + " x " + str(b) + " - " + str(c)
        answer = a * b - c

    elif symbol == 7:
        equation = str(a) + " x " + str(b) + " + " + str(c)
        answer = a * b + c

    elif symbol == 8:
        equation = str(a) + " x " + str(b) + " x " + str(c)
        answer = a * b * c  # generate the correct answer

    print(equation)  # print the question in python
    quest['text'] = equation  # GUI output of question
    print('Answer:', answer)

    # answer options
    option1, option2, option3, option4 = random.sample(range(answer - 2, answer + 2), 4)  # generate the option of choices
    opt = [option1, option2, option3, option4]
    # ensure answer in options
    if answer not in opt:
        loc = random.randint(0, 4)
        opt[loc] = answer

    print('Options 1:', opt[0])  # prints the choices in python
    options1["text"] = opt[0]  # GUI output of choices
    print('Options 2:', opt[1])
    options2["text"] = opt[1]
    print('Options 3:', opt[2])
    options3["text"] = opt[2]
    print('Options 4:', opt[3])
    options4["text"] = opt[3]


def startgame():
    startgame.score = 0  # score counter
    startgame.played = 0  # Rounds played counter
    startgame.starttime = time.time()  # records the starting time of the game
    question()  # begins the game


def checkscore(chosen):
    if chosen == answer:  # checks if the chosen answer matches the correct answer
        startgame.score = startgame.score + 1  # number of correct questions
    startgame.played = startgame.played + 1  # number of rounds played
    percent = (startgame.score / startgame.played) * 100  # counts the percentage of correct answer

    if startgame.played == 10:  # stops the game if the rounds played is equal to 10
        endtime = time.time()  # records the time at the end of the game
        nettime = timeformatter(endtime - startgame.starttime)  # elapsed time

        res['text'] = "Module: Mathematics\nScore: {}/10 ({}%)\nTime: {}".format(startgame.score, percent, nettime)
        userres['text'] = "Name: {}\nAge: {}".format(userdata.name, userdata.age)

        showpg(results)  # calls the results page
        mathmsg['text'] = 'Done'
        math_button['state'] = 'disabled'
        math_button['background'] = 'white'
        userdata.mathstatus = True
    else:  # if it is not 10 rounds yet,
        match['text'] = 'Round:\n {}/10'.format(startgame.played + 1)  # changes message of the current round
        question()  # generate another set of question and choices


def completemodule():
    global qa_score
    finish_testtime = time.time()
    net_testtime = timeformatter(finish_testtime - userdata.testtime)
    startgame.leaderboard = startgame.leaderboard.append({'Name': userdata.name,
                                                          'Age': userdata.age,
                                                          'Time': net_testtime,
                                                          'Score': startgame.score,
                                                          'WPM': submittype.finalwpm,
                                                          'Accuracy': submittype.finalaccuracy,
                                                          'QA Score': qa_score}, ignore_index=True)
    startgame.leaderboard.sort_values(by=['Score', 'WPM', 'Accuracy', 'QA Score'], ascending=False)  # sorting the leaderboard
    startgame.leaderboard.to_pickle("./scores.pickle")

    # removes the entries and messages on the start screens
    name_set.delete(0, "end")
    age_set.delete(0, "end")
    errmsg['text'] = ''
    type_button.config(state="normal", text="Typing", bg="#9AC3FD", fg='white', justify='center',
                       activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='')
    math_button.config(state="normal", text="Mathematics", bg="#9AC3FD", fg='white', justify='center',
                       activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='')
    qa_button.config(state="normal", text="Mathematics", bg="#9AC3FD", fg='white', justify='center',
                     activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='')
    mathmsg['text'] = ''
    typemsg['text'] = ''
    qamsg['text'] = ''
    userdata.mathstatus = False
    userdata.typestatus = False
    userdata.questionstatus = False

    showpg(Start)


def timeformatter(elapsedtime):  # output format of the function is in seconds
    hours, rem = divmod(elapsedtime, 3600)  # divide to get the hours
    minutes, seconds = divmod(rem, 60)  # remaining will be divided again to get the minutes and seconds
    return "{:0>2}m : {:05.2f}s".format(int(minutes), seconds)  # format used in the output


def load_score():  # function to get load the leaderboard
    try:
        startgame.leaderboard = pd.read_pickle("./scores.pickle")  # read existing leaderboard file
    except FileNotFoundError:
        errmsg.config(text="No Leaderboards Found!")
        return None

    table["columns"] = list(startgame.leaderboard.columns)  # take the column names from dataframe to widget
    table["show"] = "headings"
    for column in table["columns"]:  # reiterate to place the column into widget
        table.heading(column, text=column)
        if column == "Time":
            table.column(column, width=120, stretch=False, anchor='center')  # custom adjust for time column
        elif column == "Name":
            table.column(column, width=70, stretch=False, anchor='center')  # custom adjust for name column
        elif column == "Age":
            table.column(column, width=32, stretch=False, anchor='center')
        elif column == "Score":
            table.column(column, width=40, stretch=False, anchor='center')
        else:
            table.column(column, width=70, stretch=False, anchor='center')  # format for the other columns

    record_rows = startgame.leaderboard.to_numpy().tolist()  # convert the rows in the dataframe to list
    for row in record_rows:  # insert the rows individually to the widget
        table.insert('', 'end', values=row)

    errmsg['text'] = ''  # clears the error message on the previous screen
    showpg(leaderboard)  # shows the leaderboard page


def resetscores():  # function to reset the leaderboard
    if startgame.leaderboard.empty:  # if leaderboard is already empty an error message will be shown instead
        emptymsg['text'] = "Leaderboard is already empty!"
    else:
        startgame.leaderboard = startgame.leaderboard[0:0]  # delete rows of the dataframe
        startgame.leaderboard.to_pickle("./scores.pickle")  # save cleared dataframe into file (overwrite)
        deleteview()  # clear the widget


def deleteview():
    table.delete(*table.get_children())  # clear the content of the
    emptymsg['text'] = ''  # clear the previous error message


def showpg(frame):  # function to call a page/screen
    frame.tkraise()


def savetocsv():  # function to convert the leaderboard file into csv
    if startgame.leaderboard.empty:  # if empty, error message is shown instead
        emptymsg['text'] = "Leaderboard is empty!"
    else:
        try:  # saving the csv, opens a system GUI to select the directory for the csv
            startgame.leaderboard.to_csv(easygui.diropenbox() + '/Leaderboard.csv', header=True)
        except:
            emptymsg['text'] = "Saving to csv cancelled"


def userdata(name, age):
    if len(name) == 0:  # ensure a name/user identifier is filled
        errmsg.config(text="Enter a name!")  # error message
        return
    if len(age) == 0:  # ensure age is filled
        errmsg.config(text="Enter an age!")  # error message
        return
    if not age.isnumeric():  # ensure age is a number
        errmsg.config(text="Invalid age: Value must be a number!")  # error message
        return
    if len(age) >= 3:  # ensure age is inserted properly
        errmsg.config(text="Enter appropriate age!")  # error message
        return
    else:  # if proper entry is fulfilled
        userdata.name = name  # stores the name
        userdata.age = age  # stores the age
        try:
            startgame.leaderboard = pd.read_pickle("./scores.pickle")  # load a created leaderboard file
        except:
            startgame.leaderboard = pd.DataFrame(
                columns=['Name', 'Age', 'Time', 'Score', 'WPM', 'Accuracy', 'QA Score'])  # create one

        try:
            load_question()
            userdata.questionstatus = False
        except:
            qamsg['text'] = 'Not Available'
            qa_button['state'] = 'disabled'
            qa_button['background'] = 'white'
            userdata.questionstatus = True

        userdata.mathstatus = False
        userdata.typestatus = False
        statuscheck()
        showpg(MOD)
        userdata.testtime = time.time()


def typetest():
    typetest.text = passage.sentence()
    text['text'] = typetest.text
    print(typetest.text)
    showpg(TYPE)
    typetest.starttime = time.time()


def starttype():
    starttype.netaccuracy = 0
    starttype.netwpm = 0
    starttype.counter = 0
    typetest()


def submittype(input_text):
    # time
    typetest.endtime = time.time()
    totaltime = typetest.endtime - typetest.starttime

    # accuracy
    count = 0
    for i, c in enumerate(typetest.text):
        try:
            if input_text[i] == c:
                count += 1
        except:
            pass
    accuracy = (count / len(typetest.text)) * 100
    starttype.netaccuracy += accuracy

    # WPM
    wpm = (len(input_text) * 60) / (5 * totaltime)
    print(wpm)
    starttype.netwpm += wpm

    starttype.counter += 1
    typeinput.delete(0, "end")
    typetest()

    if starttype.counter == 3:
        submittype.finalaccuracy = round((starttype.netaccuracy / 3), 2)
        submittype.finalwpm = round(starttype.netwpm / 3, 2)

        res['text'] = "Module: Typing\nAccuracy: {}\nWords Per Minute: {}".format(submittype.finalaccuracy, submittype.finalwpm)
        userres['text'] = "Name: {}\nAge: {}".format(userdata.name, userdata.age)

        typemsg['text'] = 'Done'
        type_button['state'] = 'disabled'
        type_button['background'] = 'white'
        userdata.typestatus = True

        showpg(results)  # calls the results page


def statuscheck():
    if userdata.mathstatus and userdata.typestatus and userdata.questionstatus:
        complete_button.config(state="normal", bg="#9AC3FD", fg='white', justify='center',
                               activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='')
    else:
        complete_button['state'] = 'disabled'
        complete_button['background'] = 'white'

    showpg(MOD)


def load_question():
    with open('./sample.json') as f:
        load_question.data = json.load(f)
        return load_question.data


qa_score = nan


def start_qa():
    global qa_score
    qa_score = 0
    start_qa.played = 0
    start_qa.questioned = []
    generator(load_question.data)
    showpg(QA)
    start_qa.starttime = time.time()


def unique_random(exclude, upper):
    randInt = random.randint(0, upper)
    return unique_random(exclude, upper) if randInt in exclude else randInt


def generator(data):
    generator.question_num = len(data)
    no = unique_random(start_qa.questioned, generator.question_num - 1)
    start_qa.questioned.append(no)

    q = list(data.keys())[no]
    generator.correct_answer = data[q][0]['answer']
    option1 = data[q][0]['options'][0]['option1']
    option2 = data[q][0]['options'][0]['option2']
    option3 = data[q][0]['options'][0]['option3']
    option4 = data[q][0]['options'][0]['option4']

    print('Question: ', q)
    qa_quest['text'] = q

    print('Option 1: ', option1)
    qa_options1["text"] = option1

    print('Option 2: ', option2)
    qa_options2["text"] = option2

    print('Option 3: ', option3)
    qa_options3["text"] = option3

    print('Option 4: ', option4)
    qa_options4["text"] = option4

    print('Correct Answer: ', generator.correct_answer)

    showpg(QA)


def qa_checker(input):
    global qa_score
    if input == generator.correct_answer:
        qa_score += 1

    start_qa.played += 1
    qa_checker.percent = (qa_score / start_qa.played) * 100

    if start_qa.played == generator.question_num:  # stops the game if the rounds played is equal to 10
        finaltime = timeformatter(time.time() - start_qa.starttime)  # elapsed time

        res['text'] = "Module: Questions\nScore: {}/{} ({}%)\nTime: {}".format(qa_score, generator.question_num, qa_checker.percent, finaltime)
        userres['text'] = "Name: {}\nAge: {}".format(userdata.name, userdata.age)

        showpg(results)  # calls the results page
        qamsg['text'] = 'Done'
        qa_button['state'] = 'disabled'
        qa_button['background'] = 'white'
        userdata.questionstatus = True
    else:  # if it is not 10 rounds yet,
        rounds['text'] = 'Round:\n {}/{}'.format(start_qa.played + 1, generator.question_num)  # changes message of the current round
        generator(load_question.data)  # generate another set of question and choices


# =================== GUI ===================

HEIGHT = 300
WIDTH = 500

app = tk.Tk()
app.title("Assessment Program")
app.geometry("500x300")  # width x height

# Pages/Screens used in the app
Start = tk.Frame(app, width=WIDTH, height=HEIGHT, bg="white")
MOD = tk.Frame(app, width=WIDTH, height=HEIGHT, bg="white")
Game = tk.Frame(app, width=WIDTH, height=HEIGHT, bg="white")
TYPE = tk.Frame(app, width=WIDTH, height=HEIGHT, bg="white")
results = tk.Frame(app, width=WIDTH, height=HEIGHT, bg="white")
leaderboard = tk.Frame(app, width=WIDTH, height=HEIGHT, bg="white")
QA = tk.Frame(app, width=WIDTH, height=HEIGHT, bg="white")

for frame in (Start, MOD, Game, TYPE, QA, results, leaderboard):  # placing the screen on top of each other
    frame.place(relwidth=1, relheight=1)

showpg(Start)  # Initial Home screen

# =================== Start Screen ===================
Start_title = tk.Label(Start, text="Assessment", font=("Helvetica Neue Thin", 45), bg='white', fg="#6EA9FB")
Start_title.place(relx=0.5, rely=0.15, anchor='center')

namemsg = tk.Label(Start, text="Name: ", font=("Helvetica Neue Thin", 15), fg="black", bg="white")
namemsg.place(relx=0.25, rely=0.425, anchor='center')

nameinput_frame = tk.Frame(Start, bg="#9AC3FD", bd=1.5)
nameinput_frame.place(relx=0.4, rely=0.425, relwidth=0.2, relheight=0.1, anchor='center')

name_set = tk.Entry(nameinput_frame, justify='center', relief='flat', highlightthickness=1)
name_set.place(relwidth=1, relheight=1)

agemsg = tk.Label(Start, text="Age: ", font=("Helvetica Neue Thin", 15), fg="black", bg="white")
agemsg.place(relx=0.26, rely=0.575, anchor='center')

ageinput_frame = tk.Frame(Start, bg="#9AC3FD", bd=1.5)
ageinput_frame.place(relx=0.4, rely=0.575, relwidth=0.2, relheight=0.1, anchor='center')

age_set = tk.Entry(ageinput_frame, justify='center', relief='flat', highlightthickness=1)
age_set.place(relwidth=1, relheight=1)

Start_button = button(Start, text="Start", bg="#9AC3FD", fg='white', justify='center',
                      activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                      command=lambda: userdata(name_set.get(), age_set.get()))
Start_button.place(relx=0.65, rely=0.5, relwidth=0.2, relheight=0.1, anchor='center')

lb_button = button(Start, text="Records", bg="#9AC3FD", fg='white', justify='center',
                   activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                   command=lambda: load_score())
lb_button.place(relx=0.5, rely=0.93, relwidth=0.2, relheight=0.1, anchor='center')

errmsg = tk.Label(Start, text='', fg="red", bg="white")
errmsg.place(relx=0.5, rely=0.75, relwidth=1, relheight=0.1, anchor='center')

# ================== Modules Screen ====================
Dif_title = tk.Label(MOD, text="Modules", font=("Helvetica Neue Thin", 45), bg='white', fg="#6EA9FB")
Dif_title.place(relx=0.5, rely=0.15, anchor='center')

math_button = button(MOD, text="Mathematics", bg="#9AC3FD", fg='white', justify='center',
                     activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                     command=lambda: startgame())
math_button.place(relx=0.28, rely=0.45, relwidth=0.2, relheight=0.1, anchor='center')

mathmsg = tk.Label(MOD, text="", font=("Helvetica Neue Thin", 12), fg="black",
                   bg="white")
mathmsg.place(relx=0.28, rely=0.55, anchor='center')

type_button = button(MOD, text="Typing", bg="#9AC3FD", fg='white', justify='center',
                     activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                     command=lambda: starttype())
type_button.place(relx=0.5, rely=0.45, relwidth=0.2, relheight=0.1, anchor='center')

typemsg = tk.Label(MOD, text="", font=("Helvetica Neue Thin", 12), fg="black",
                   bg="white")
typemsg.place(relx=0.5, rely=0.55, anchor='center')

qa_button = button(MOD, text="Questions", bg="#9AC3FD", fg='white', justify='center',
                   activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                   command=lambda: start_qa())
qa_button.place(relx=0.72, rely=0.45, relwidth=0.2, relheight=0.1, anchor='center')

qamsg = tk.Label(MOD, text="", font=("Helvetica Neue Thin", 12), fg="black",
                 bg="white")
qamsg.place(relx=0.72, rely=0.55, anchor='center')

complete_button = button(MOD, text="Completed", bg="#9AC3FD", fg='white', justify='center',
                         activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                         command=lambda: completemodule())
complete_button.place(relx=0.5, rely=0.85, relwidth=0.2, relheight=0.1, anchor='center')

# ================== QUIZ Screen ====================
Start_title = tk.Label(Game, text="Question:", font=("Helvetica Neue Thin", 45), bg='white', fg="#6EA9FB")
Start_title.place(relx=0.5, rely=0.15, anchor='center')

match = tk.Label(Game, text="Round:\n 1/10", font=('Times New Roman', 12), anchor='s', bg="white")
match.place(rely=0.05, relx=0.96, anchor="center")

q_frame = tk.Frame(Game, bg="#9AC3FD", bd=1)
q_frame.place(relx=0.5, rely=0.25, relwidth=0.7, relheight=0.25, anchor='n')

quest = tk.Label(q_frame, font=('Helvetica', 20), anchor='center', bg="white")
quest.place(relwidth=1, relheight=1)

options1 = button(Game, bg="#9AC3FD", fg='white', justify='center',
                  activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                  command=lambda: checkscore(options1['text']))
options1.place(relx=0.35, rely=0.53, relwidth=0.3, relheight=0.15, anchor='n')

options2 = button(Game, bg="white", fg='#9AC3FD', justify='center',
                  activebackground='#9AC3FD', activeforeground="white", borderless=1, takefocus='',
                  command=lambda: checkscore(options2['text']))
options2.place(relx=0.35, rely=0.69, relwidth=0.3, relheight=0.15, anchor='n')

options3 = button(Game, bg="white", fg='#9AC3FD', justify='center',
                  activebackground='#9AC3FD', activeforeground="white", borderless=1, takefocus='',
                  command=lambda: checkscore(options3['text']))
options3.place(relx=0.65, rely=0.53, relwidth=0.3, relheight=0.15, anchor='n')

options4 = button(Game, bg="#9AC3FD", fg='white', justify='center',
                  activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                  command=lambda: checkscore(options4['text']))
options4.place(relx=0.65, rely=0.69, relwidth=0.3, relheight=0.15, anchor='n')

# ================== Typing Screen ====================
type_title = tk.Label(TYPE, text="Type this:", font=("Helvetica Neue Thin", 30), bg='white', fg="#6EA9FB")
type_title.place(relx=0.5, rely=0.15, anchor='center')

text_frame = tk.Frame(TYPE, bg="#9AC3FD", bd=1)
text_frame.place(relx=0.5, rely=0.25, relwidth=0.7, relheight=0.25, anchor='n')

text = tk.Label(text_frame, font=('Helvetica', 15), anchor='c', bg="white", wraplength=250)
text.place(relwidth=1, relheight=1)

input_frame = tk.Frame(TYPE, bg="#9AC3FD", bd=1)
input_frame.place(relx=0.5, rely=0.6, relwidth=0.9, relheight=0.15, anchor='c')

typeinput = tk.Entry(input_frame, justify='center', relief='flat', highlightthickness=1)
typeinput.place(relwidth=1, relheight=1)

sub_button = button(TYPE, text="Submit", bg="white", fg='#9AC3FD', justify='center',
                    activebackground='#9AC3FD', activeforeground="white", borderless=1, takefocus='',
                    command=lambda: submittype(typeinput.get()))
sub_button.place(relx=0.5, rely=0.75, relwidth=0.2, relheight=0.1, anchor='center')

# ================== Results Screen ====================
result_title = tk.Label(results, text="Results", font=("Helvetica Neue Thin", 45), bg='white', fg="#6EA9FB")
result_title.place(relx=0.5, rely=0.15, anchor='center')

userres = tk.Label(results, font=('Helvetica Neue Thin', 15), fg="black", bg="white")
userres.place(relx=0.5, rely=0.4, relwidth=0.3, relheight=0.3, anchor='center')

res = tk.Label(results, font=('Helvetica Neue Thin', 15), fg="#6EA9FB", bg="white")
res.place(relx=0.5, rely=0.65, relwidth=0.5, relheight=0.2, anchor='center')

confirmmod_button = button(results, text="Confirm Module", bg="white", fg='#9AC3FD', justify='center',
                           activebackground='#9AC3FD', activeforeground="white", borderless=1, takefocus='',
                           command=lambda: statuscheck())
confirmmod_button.place(relx=0.5, rely=0.825, relwidth=0.3, relheight=0.1, anchor='center')

# ================== Leaderboard Screen ====================
leaderboard_title = tk.Label(leaderboard, text="Records", font=("Helvetica Neue Thin", 30), bg='white',
                             fg="#6EA9FB")
leaderboard_title.place(relx=0.5, rely=0.1, anchor='center')

table = tk.ttk.Treeview(leaderboard)
table.place(relheight=0.6, relwidth=0.95, relx=0.5, rely=0.52, anchor='center')

reset_button = button(leaderboard, text="Reset", bg="white", fg='#9AC3FD', justify='center',
                      activebackground='#9AC3FD', activeforeground="white", borderless=1, takefocus='',
                      command=lambda: resetscores())
reset_button.place(relx=0.09, rely=0.9, relwidth=0.1, relheight=0.1, anchor='center')

emptymsg = tk.Label(leaderboard, text='', fg="red", bg="white")
emptymsg.place(relx=0.36, rely=0.9, relwidth=0.38, relheight=0.1, anchor='center')

savecsv = button(leaderboard, text="Save as CSV", bg="#9AC3FD", fg='white', justify='center',
                 activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                 command=lambda: savetocsv())
savecsv.place(relx=0.66, rely=0.9, relwidth=0.2, relheight=0.1, anchor='center')

returnhome_button = button(leaderboard, text="Return Home", bg="white", fg='#9AC3FD', justify='center',
                           activebackground='#9AC3FD', activeforeground="white", borderless=1, takefocus='',
                           command=lambda: [showpg(Start), deleteview()])
returnhome_button.place(relx=0.87, rely=0.9, relwidth=0.2, relheight=0.1, anchor='center')

# ================== QA Screen ====================
qa_Start_title = tk.Label(QA, text="Question: ", font=("Helvetica Neue Thin", 45), bg='white', fg="#6EA9FB")
qa_Start_title.place(relx=0.5, rely=0.15, anchor='center')

rounds = tk.Label(QA, text="Round:\n 1/10", font=('Times New Roman', 12), anchor='s', bg="white")
rounds.place(rely=0.05, relx=0.96, anchor="center")

qa_frame = tk.Frame(QA, bg="#9AC3FD", bd=1)
qa_frame.place(relx=0.5, rely=0.25, relwidth=0.7, relheight=0.25, anchor='n')

qa_quest = tk.Label(qa_frame, font=('Helvetica', 20), anchor='center', bg="white")
qa_quest.place(relwidth=1, relheight=1)

qa_options1 = button(QA, bg="#9AC3FD", fg='white', justify='center',
                     activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                     command=lambda: qa_checker(qa_options1['text']))
qa_options1.place(relx=0.35, rely=0.53, relwidth=0.3, relheight=0.15, anchor='n')

qa_options2 = button(QA, bg="white", fg='#9AC3FD', justify='center',
                     activebackground='#9AC3FD', activeforeground="white", borderless=1, takefocus='',
                     command=lambda: qa_checker(qa_options2['text']))
qa_options2.place(relx=0.35, rely=0.69, relwidth=0.3, relheight=0.15, anchor='n')

qa_options3 = button(QA, bg="white", fg='#9AC3FD', justify='center',
                     activebackground='#9AC3FD', activeforeground="white", borderless=1, takefocus='',
                     command=lambda: qa_checker(qa_options3['text']))
qa_options3.place(relx=0.65, rely=0.53, relwidth=0.3, relheight=0.15, anchor='n')

qa_options4 = button(QA, bg="#9AC3FD", fg='white', justify='center',
                     activebackground='white', activeforeground="#9AC3FD", borderless=1, takefocus='',
                     command=lambda: qa_checker(qa_options4['text']))
qa_options4.place(relx=0.65, rely=0.69, relwidth=0.3, relheight=0.15, anchor='n')

# ================== CLOSING GUI ====================
app.mainloop()
# ================== END GUI ====================

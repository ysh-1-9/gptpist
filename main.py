import pandas as pd
import re
import json


class Prompt:
    def __init__(self, window=5):
        self.summary = ""
        self.specifics = ""
        self.window = window
        self.clientMessages = ["" for _ in range(self.window)]
        self.therapistMessages = ["" for _ in range(self.window)]  # last therapist message is empty

    def to_string(self):
        s = ""
        s += "Summary: " + self.summary + "\n\n"
        s += "Specific Information: " + self.specifics + "\n\n###\n\n"
        for i in range(self.window):
            s += "Client: " + self.clientMessages[i] + '\n'
            s += "Therapist: " + self.therapistMessages[i] + '\n'

        return s[:-1]


# final dataset will be list of jsons, each json with one prompt, one completion
# isko csv mein daalke cli data-prep tool ko de denge


def get_summary(s):
    # takes in the last
    return f"<summary tbi {len(s)}>"
    pass


def get_specifics(s):
    return f"<specifics tbi {len(s)}>"
    pass



def ops(line):
    line = line[line.find(' ') + 1:]
    # strip all the shit within brackets
    line = re.sub("[\(\[].*?[\)\]]", "", line)
    line = line.replace('\n', '')
    return line





def convert_to_csv(file, window=5):
    f = open(file)

    therapist = []
    client = []

    w = open(file.split('.')[0] + '_proc.jsonl', 'w')

    tchar = file_data[file][0]
    cchar = file_data[file][1]

    for line in f:
        if line[0] == tchar:
            therapist.append(ops(line))
        elif line[0] == cchar:
            client.append(ops(line))
        else:
            print('EOF\n')

    therapist = therapist[1:]

    l = min(len(therapist), len(client))

    # therapist[i] is what goes into the completion
    # client[index] i,i-1,i-2 .. i-(window-1) goes into clientMessages
    # therapist[index] _,i-1,... i-(window-1) goes into therapistMessages
    # client[index] i,i-1,...0 goes into summary
    conv = []
    prompt = Prompt(window)
    for i in range(l):
        conv.append("Client: " + client[i])

        prompt.summary = get_summary(conv)
        prompt.specifics = get_specifics(conv)
        prompt.clientMessages = prompt.clientMessages[1:] + [client[i]]
        prompt.therapistMessages = prompt.therapistMessages[1:-1] + [therapist[i - 1] if i > 0 else ""] + [""]

        completion = ' ' + therapist[i] + "<end>"

        j = {"prompt": prompt.to_string(), "completion": completion}
        print(f'[{i}]: Made JSON: {json.dumps(j)}')
        w.write(json.dumps(j) + '\n')

        conv.append("Therapist: " + therapist[i])


file_data = {'gloria.txt': ['T','C'], 'sylvia.txt': ['C','S']}
for file,data in file_data.items():
    convert_to_csv(file)

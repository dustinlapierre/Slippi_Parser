import os
import ast

#reads training set files and compiles them into single list
def compile_data():
    print("Compiling data set...")
    data = []
    path = 'training_set/data'
    for filename in os.listdir(path):
        file = open(('training_set/data/' + filename), "r")
        mylist = ast.literal_eval(file.read())
        data.append(mylist)
        file.close()
    return data

#reads training label files and compiles them into single list
def compile_labels():
    print("Compiling labels...")
    labels = []
    path = 'training_set/labels'
    for filename in os.listdir(path):
        file = open(('training_set/labels/' + filename), "r")
        mylist = ast.literal_eval(file.read())
        labels.append(mylist)
        file.close()
    return labels

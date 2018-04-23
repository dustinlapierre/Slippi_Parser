from random import randint, randrange

#pick between two things
def choose(option1, option2):
    choice = randint(0, 1)
    if(choice == 0):
        return option1
    return option2

#select randomly from a list
def choose_list(choice_list):
    random_index = randrange(0, len(choice_list))
    return choice_list[random_index]

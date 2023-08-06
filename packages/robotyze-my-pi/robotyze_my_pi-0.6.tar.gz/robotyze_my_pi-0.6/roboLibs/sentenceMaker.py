import random

s_nouns = ["A dragon", "Maddie", "Craig", "My Dad", "My mom", "The king",
           "Some guy", "A cat with rabies", "A sloth", "Your homie",
           "This cool guy my gardener met yesterday", "Superman"]
p_nouns = ["These dudes", "Both of my moms", "All the kings of the world",
           "Some guys", "All of a cattery's cats",
           "The multitude of sloths living under your bed", "Your homies",
           "Like, these, like, all these people", "Supermen"]
s_verbs = ["eats", "kicks", "gives", "drinks bubble tea", "treats",
           "meets with", "creates", "hacks", "configures", "spies on",
           "smells", "meows on", "flees from", "tries to automate", "explodes"]
p_verbs = ["eat", "kick", "play fortnite", "treat", "meet with", "create",
           "hack", "dabs", "spy on", "looks at", "meow on", "flee from",
           "try to automate", "explode"]
infinitives = ["has sugar rush", "to make a pie.", "for no apparent reason.",
               "because the sky is green.", "for a disease.",
               "to be able to make toast explode.",
               "to know more about archeology."]


def sen_maker(s_nouns=s_nouns, s_verbs=s_verbs, p_nouns=p_nouns, p_verbs=p_verbs, infinitives=infinitives, num_sen=None):
    if not num_sen:
        num_sen = int(input("How many sentences would you like your Madlibs to be?"))

    stringParagraph = ""
    singular = [s_nouns, s_verbs]
    plural = [p_nouns, p_verbs]

    for i in range(num_sen):
        singularOrPlural1 = random.choice([singular, plural])
        singularOrPlural2 = random.choice([singular, plural])
        stringParagraph += random.choice(singularOrPlural1[0]) + " " + random.choice(singularOrPlural1[1]) + " " + random.choice(singularOrPlural2[0]).lower() + " " + random.choice(infinitives) + " "
    return stringParagraph

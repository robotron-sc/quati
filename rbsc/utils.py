def only(list, *index):
    ls = list[:]
    for i in index:
        ls.pop(i)
    return not any(ls)

def compare(list1, list2):
    if len(list1) != len(list2):
        raise Exception('Lists must have equal size')
        return
    
    for i in range(len(list1)):
        a, b = list1[i], list2[i]
        if type(a) == type(any):
            continue
        if type(a) != tuple:
            if a != b:
                return False
        elif b not in a :
            return False 
    return True 

import os, os.path
def empty_folder(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))

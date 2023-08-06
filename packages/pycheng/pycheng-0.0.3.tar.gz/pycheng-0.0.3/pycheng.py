"""
pycheng 
"""


def print_list(val, indent=False, level=0):
    for item in val:
        if isinstance(item, list):
            print_list(item, level+1)
        else:
            if indent:
                for i in range(level):
                    print('\t', end='')
            print(item)


"""
verison
"""


def version():
    print('my first python module !!!')

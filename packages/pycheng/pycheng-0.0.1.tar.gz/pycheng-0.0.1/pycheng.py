"""
pycheng 
"""
def print_list(val):
    for item in val:
        if isinstance(item, list):
            print_list(item)
        else:
            print(item)


"""
verison
"""
def version():
    print('my first python module !!!')

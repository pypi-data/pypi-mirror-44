def print_list(the_list):
    for i in the_list:
        if isinstance(i,list):
            print_list(i)
        else:
            print(i)

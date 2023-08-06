from scientistsgenerator import ScientistsGenerator as sg

def main_test():
    print("**********************************************")
    print("Random name: {}".format(sg.generate_name()))
    print("Random scientist: {}".format(sg.generate_scientist()))
    print("Random mathematician: {}".format(sg.generate_mathematician()))
    print("Random philosopher: {}".format(sg.generate_philosopher()))
    print("**********************************************")
    

if __name__ == "__main__":
    main_test()

import sys, json
from src.Manager import Manager
from src.Utils import validate_testcase

import time

if __name__ == '__main__':
    Manager().mainloop()

    # # check if testcase file is provided
    # if len(sys.argv) < 2:
    #     print("Usage: python main.py <testcase_file> [--algorithm=<genetic or knuth>] [--vectorized]")
    #     exit(1)
    
    # start_time = time.time()
    # testcase_file = sys.argv[1]
    # validate_testcase(testcase_file)
    # with open(testcase_file, 'r') as json_file:
    #     testcase = json.load(json_file)
    #     Manager = Manager(algorithm_name="genetic_algorithm", parameters=testcase["parameters"])
    #     Manager.mainloop()
    #     # Manager.process(testcase["minterms"], testcase["dontcares"])

    # end_time = time.time()
    # print(f"Excution_time: {end_time - start_time:.1f}sec")
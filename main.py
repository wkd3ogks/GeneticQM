import sys, json

from src.QuineMcCluskey import QuineMcClusky
from src.GeneticAlgorithm import GeneticAlgorithm

from src.Utils import validate_testcase

from src.Application import Application

if __name__ == '__main__':
    # check if testcase file is provided
    if len(sys.argv) < 2:
        print("Usage: python main.py [--gui] <testcase_file> [--vectorized] [--visualization] [--algorithm=<genetic or knuth>] [--crossover=<strategy>] [--selection=<strategy>]")
        exit(1)

    if sys.argv[1] == "--gui":
        app = Application()
        app.mainloop()
        exit(0)

    testcase_file = sys.argv[1]
    validate_testcase(testcase_file)
    with open(testcase_file, 'r') as json_file:
        testcase = json.load(json_file)
        # 파라미터 값은 그리드 서치가 진행된다.
        qm = QuineMcClusky(testcase["minterms"], testcase["dontcares"])
        # 문자열로 크로스 오버 선택하도록 변경하자.
        parameters = testcase["parameters"]
        genetic_algorithm = GeneticAlgorithm(parameters)
        qm.process(genetic_algorithm)
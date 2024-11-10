import json

from Builders import GeneticAlgorithmBuilder
from QuineMcCluskey import QuineMcClusky

from Crossover import UniformCrossover

if __name__ == '__main__':
    with open('./testcases/testcase2.json', 'r') as json_file:
        testcase = json.load(json_file)
        # 파라미터 값은 그리드 서치가 진행된다.
        # 결과물을 폴더로 해서 각 그리드 서치에 따라서 저장하자. 최고 결과물도 뭔지 알려줘야 한다.
        qm = QuineMcClusky(testcase["minterms"], testcase["dontcares"])
        # 문자열로 크로스 오버 선택하도록 변경하자.
        gene_builder = (GeneticAlgorithmBuilder().set_crossover_strategy(UniformCrossover())
        .set_population_size(600)
        .set_epoch(750)
        .set_weight(2)
        .set_mutation_rate(0.15))
        qm.process(gene_builder)
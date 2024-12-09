# Quine McCluskey with Genetic Algorithm

## Description
이 프로젝트는 **퀸 맥클러스키(Quine-McCluskey) 알고리즘**의 마지막 과정인 **Pi 테이블**에서 최적의 조합을 찾는 문제에 관심을 두고 있습니다. 해당 문제를 해결하기 위해 **유전 알고리즘**을 사용했습니다.

## Language
- Python

## Library
- matplotlib
- tkinter

## Project Structure

  
    ├── testcases                # testcases
    ├── strategy                 
    │   ├── Selection.py         # Selection Implementation
    │   ├── Crossover.py         # Crossover Implementation
    ├── GeneticQM.py             # Main for running the Genetic, Quine-McCluskey algorithm
    ├── GeneticAlgorithm.py      # Genetic Algorithm Implementation   
    └── QuineMcCluskey.py        # Quine McCluskey Implementation

## Genetic Algorithm
1. 초기화: 초기화 과정으로 랜덤하게 유전자를 생성합니다.([__init_population method](https://github.com/wkd3ogks/GeneticQM/blob/207686d6991fe6d09662d18ec1220c0319eb3b88/GeneticAlgorithm.py#L64))
2.  평가: 생성한 유전자에 대해 적합도 함수를 통해 평가합니다.([__evaluate_fitness method](https://github.com/wkd3ogks/GeneticQM/blob/207686d6991fe6d09662d18ec1220c0319eb3b88/GeneticAlgorithm.py#L110))
3.  선택: 평가된 적합도를 바탕으로 부모 개체를 선택합니다.([__selection method](https://github.com/wkd3ogks/GeneticQM/blob/207686d6991fe6d09662d18ec1220c0319eb3b88/GeneticAlgorithm.py#L87))
     - 선택의 자세한 구현은 RouletteWheel 방식을 사용했습니다.([RouletteWheel class](https://github.com/wkd3ogks/GeneticQM/blob/d8a04129fc0955593c4fdcff38081d99573cfc61/strategy/Selection.py#L23))
     -  적합도는 항상 양의 정수라는 점을 활용해 이분 탐색(lower bound)을 통해 효율적으로 부모를 선택하고자 했습니다.
4. 교차: 부모 개체를 바탕으로 교차를 통해 다음 세대 유전자를 생성합니다.([__crossover method](https://github.com/wkd3ogks/GeneticQM/blob/d8a04129fc0955593c4fdcff38081d99573cfc61/GeneticAlgorithm.py#L84))
     -  single_point와 uniform으로 총 2가지의 방법이 구현되어 있습니다.([single_point class](https://github.com/wkd3ogks/GeneticQM/blob/d8a04129fc0955593c4fdcff38081d99573cfc61/strategy/Crossover.py#L24), [uniform class](https://github.com/wkd3ogks/GeneticQM/blob/d8a04129fc0955593c4fdcff38081d99573cfc61/strategy/Crossover.py#L36))
5. 변이: 교차로 생성된 유전자에 대해 변의를 만듭니다.([__mutation method](https://github.com/wkd3ogks/GeneticQM/blob/d8a04129fc0955593c4fdcff38081d99573cfc61/GeneticAlgorithm.py#L77))
6. 지정한 에포크에 도달할 때까지 2-5번을 반복합니다.

- crossover, selection의 경우 다양한 방법이 있어 각각 CrossoverStrategy, SelectionStrategy를 상속해 유연하게 사용 가능하고자 했습니다.
## Fitness Function

- **최소한의 주항**을 사용하여 **최대한 많은 민텀을 커버**하는 데 높은 점수를 부여합니다.

### 적합도 함수 정의
적합도 = 가중치 × 커버한 민텀의 개수 + 필수 주항의 총 개수 − 사용한 필수 주항의 수

- 가중치: 필수 주항을 사용하는 것과 비교하여 얼마나 민텀을 채우는 것을 중요하게 여기는지를 나타냅니다.
- 커버한 민텀의 개수: 유전자가 커버한 민텀의 수를 나타내며, 이는 적합도를 높이는 주요 요소입니다.
- 필수 주항의 총 개수: 적합도가 음수가 나오지 않도록 하는 역할을 합니다.
- 사용한 필수 주항의 수: 실제로 사용된 필수 주항의 수를 나타내며, 적합도를 낮추는 요소로 작용합니다.

## Testcase
![testcase1](https://github.com/user-attachments/assets/85ac4b28-b348-4894-b6ad-5c254256e305)

- minterms : 민텀의 리스트
- dontcares : 돈캐어항의 리스트
- parameters : 유전 알고리즘의 파라미터
  - population_size: 유전자 집합의 크기
  - parent_population_size: 부모 유전자 집합의 크기
  - epoch: 반복 횟수
  - weight: 적합도 함수의 가중치
  - mutation_rate: 변이 확율
  - bit_mutation_rate: 변이가 일어난 경우, 각 비트가 변경될 확률
- strategy : 유전 알고리즘 전략
  - crossover : 교차 전략 선택(single_point or uniform)
- visualization : 시각화 데이터
  - group : 그룹의 개수(다양성 그래프에서 epoch를 그룹화하여 단순화한 결과를 나타냄)

## Result

### 세대별 최대, 최소, 평균 적합도 그래프
<img width="502" alt="image" src="https://github.com/user-attachments/assets/24ebcd3a-9202-44a9-803e-6a6592ddd866">

- 이 그래프는 각 세대에서 최대, 최소, 평균 적합도의 변화를 나타냅니다. 적합도가 상승한다는 것은 유전 알고리즘이 세대가 거듭될수록 적합도가 높은 해(solution)에 점점 더 가까워지고 있다는 것을 의미합니다.

### 정규화된 적합도 그래프
<img width="521" alt="image" src="https://github.com/user-attachments/assets/3d34ad35-ad34-41b1-a6a8-2537ba489cf6">

- 이 그래프는 세대별 개체들의 적합도를 min-max 정규화를 통해 0~1 범위로 시각화한 것입니다. 적합도 함수의 증가 폭이 세대 수에 비해 상대적으로 크지 않아, 변화 추이를 보다 명확히 관찰하기 위해 정규화 과정을 거쳤습니다. 이를 통해 세대별 적합도의 변화 추이를 보다 직관적으로 파악할 수 있습니다. 

### 유전적 다양성 그래프
<img width="499" alt="image" src="https://github.com/user-attachments/assets/059d9f14-e95d-4148-ae23-287baec0749a">

- 적합도가 높은 개체 위주로 선택되기 때문에 세대가 거듭될수록 유전적 다양성은 점점 줄어듭니다. 이는 유전 알고리즘의 자연스러운 현상으로, 적합도가 높은 개체들이 다음 세대로 선택되면서 유전자 풀의 다양성이 감소하게 됩니다. 그러나 지나치게 다양성이 줄어들면 탐색 능력이 저하될 수 있어, 변이(mutation) 비율을 적절히 조정하여 이를 완화할 수 있습니다.

### 그룹으로 묶은 유전적 다양성 그래프
<img width="501" alt="image" src="https://github.com/user-attachments/assets/79538c18-d0b4-432e-8b62-8c2d6774108a">

- 이 그래프는 세대를 일정 간격으로 그룹화하여 유전적 다양성의 변화를 시각화한 것입니다. 세대를 개별적으로 시각화하는 대신 그룹으로 묶어 전반적인 다양성 변화 경향을 한눈에 파악하고자 했습니다.

### 세대별 최대 적합도 유전자의 커버한 민텀 히트맵

<img width="215" alt="image" src="https://github.com/user-attachments/assets/2f3082de-b648-4f46-8209-c9335d6d4879">

### 세대별 최대 적합도 유전자의 사용한 필수 주항 히트맵

<img width="157" alt="image" src="https://github.com/user-attachments/assets/bdbeb837-5689-481b-88ea-804eb540b1ba">

- 세대별 최대 적합도 유전자의 커버한 민텀 히트맵과 세대별 최대 적합도 유전자의 사용한 필수 주항 히트맵은 생각보다 유용한 정보를 제공하지 못했습니다. 해당 정보는 적합도 향상을 확인하는 데 직접적으로 기여하지 않았고 민텀과 주항이 많아짐에 따라 해석도 쉽지 않았습니다.

### 결과(result.txt)
<img width="316" alt="image" src="https://github.com/user-attachments/assets/08cea92c-4332-4766-ad79-eb7ab7ed46dd">

## How to Run/Use

![Run](https://github.com/user-attachments/assets/d7a07073-27bd-4924-9e72-10b6776e733d)


```
python3 GeneticQM.py
```

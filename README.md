# Quine McCluskey with Genetic Algorithm

## Description
이 프로젝트는 **퀸 맥클러스키(Quine-McCluskey) 알고리즘**의 마지막 과정인 **Pi 테이블**에서 최적의 조합을 찾는 문제에 관심을 두고 있습니다.

해당 문제를 해결하기 위해 **유전 알고리즘**을 사용했습니다.

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

### 정규화된 적합도 그래프
<img width="521" alt="image" src="https://github.com/user-attachments/assets/3d34ad35-ad34-41b1-a6a8-2537ba489cf6">

### 유전적 다양성 그래프
<img width="499" alt="image" src="https://github.com/user-attachments/assets/059d9f14-e95d-4148-ae23-287baec0749a">

### 그룹으로 묶은 유전적 다양성 그래프
<img width="501" alt="image" src="https://github.com/user-attachments/assets/79538c18-d0b4-432e-8b62-8c2d6774108a">

### 세대별 최대 적합도 유전자의 커버한 민텀 히트맵

<img width="215" alt="image" src="https://github.com/user-attachments/assets/2f3082de-b648-4f46-8209-c9335d6d4879">

### 세대별 최대 적합도 유전자의 사용한 필수 주항 히트맵

<img width="157" alt="image" src="https://github.com/user-attachments/assets/bdbeb837-5689-481b-88ea-804eb540b1ba">


### 결과(result.txt)
<img width="316" alt="image" src="https://github.com/user-attachments/assets/08cea92c-4332-4766-ad79-eb7ab7ed46dd">

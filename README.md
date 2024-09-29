# Quine McCluskey with Genetic Algorithm

<div align="center">

![Figure_1](https://github.com/user-attachments/assets/f34b0d8f-1c0c-4465-beb8-5b8c054efaaf)


</div>

## Description
이 프로젝트는 **퀸 맥클러스키(Quine-McCluskey) 알고리즘**을 최적화하기 위해 **유전 알고리즘(Genetic Algorithm)** 을 적용한 논리식 최소화 도구입니다. 퀸 맥클러스키는 논리식의 진리표를 기반으로 하여 모든 소항을 분석하고, 가능한 한 적은 소항으로 논리식을 축약하는 데 사용됩니다. 그러나 복잡한 논리식에서는 계산 시간이 증가하는 문제를 해결하기 위해, 유전 알고리즘을 도입하여 효율성을 높였습니다.

## Tech Stack
- Python

## Example

<div align="center">
  
![Figure_1](https://github.com/user-attachments/assets/addab4c2-1ac0-4132-a158-165b694d0239)
![Cover Minterms](https://github.com/user-attachments/assets/ea483178-cca7-40c5-a470-b128eb457c32)
![Best Gene Hitmap(Used Prime Implicants)](https://github.com/user-attachments/assets/d323619d-a52b-4a7d-bbb4-192dce86267b)
<img width="1228" alt="스크린샷 2024-09-29 오후 6 51 06" src="https://github.com/user-attachments/assets/6e9e8099-e6bf-46a7-918b-5e3e4fb91fb1">

</div>

## Fitness Function

이 적합도 함수는 최소한의 주항을 사용하여 최대한 많은 민텀을 커버하는 데 높은 점수를 부여합니다.

### 적합도 함수 정의
적합도 = 가중치 × 커버한 민텀의 개수 + 필수 주항의 총 개수 − 사용한 필수 주항의 수

- 가중치: 필수 주항을 사용하는 것과 비교하여 얼마나 민텀을 채우는 것을 중요하게 여기는지를 나타냅니다.
- 커버한 민텀의 개수: 유전자가 커버한 민텀의 수를 나타내며, 이는 적합도를 높이는 주요 요소입니다.
- 필수 주항의 총 개수: 적합도가 음수가 나오지 않도록 하는 역할을 합니다.
- 사용한 필수 주항의 수: 실제로 사용된 필수 주항의 수를 나타내며, 적합도를 낮추는 요소로 작용합니다.

## Features
- 입력 비트 제한 없음: 파이썬의 특성을 활용하여 숫자 비트에 제한을 두지 않았습니다.
- 효율적인 룰렛 휠 방식: 부분합과 이분 탐색을 통해 효율적으로 선택 과정을 진행합니다.
- 매개변수 수정 용이: 빌더 패턴을 사용하여 사용자가 쉽게 매개변수를 수정할 수 있도록 설계했습니다.
- 유연한 교차 알고리즘: 전략 패턴을 활용하여 교차 알고리즘을 간편하게 변경할 수 있습니다.

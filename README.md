# Untacticon

### 언택티콘 (2020.10 ~ 2020.12)

**2020학년도 제 2회 SM AI 경진 대회 최우수상**

----------

**주제** : 비대면 강의 중 학습자 상태 파악 AI 모듈

**기획 배경** : 비대면 강의의 불편한 점 해소

**팀원**

- [limjustin(임재영)](https://github.com/limjustin)
- [yoonho0922(안윤호)](https://github.com/yoonho0922)
- [goodaehong(구대홍)](https://github.com/goodaehong)
- [DADA201910841(최다경)](https://github.com/DADA201910841)

----------

**1. 프로젝트 설명**

비대면 강의의 불편한 점들을 해소하기 위해 만든 AI 모듈인 언택티콘은 'Untact'와 'Emoticon'의 합성어입니다. 언택티콘은 인공지능으로 사용자의 모습을 인식하여 사용자의 반응 및 상태를 이모티콘으로 표시해줍니다. 학습자의 반응을 즉각적으로 파악하기 때문에, 학습자의 수업 몰입도 및 집중력이 증가되며 즉각적인 피드백을 통해 강의 질을 향상할 수 있습니다. 또한 반응의 종류를 이모티콘으로 표시해주기 때문에, 화상 캠을 켜지 않고도 원활한 상호작용이 가능하며 교육자는 학습자들의 반응을 쉽고 간단하게 파악할 수 있습니다.

----------

**2. 기능**

- **학습자의 반응을 즉각적으로 파악**

  - ```긍정``` / ```부정```   : 학습자의 고개 끄덕임 / 젓는 여부
  
  - ```의문``` : 학습자의 학습 내용 이해 여부
  
  - ```졸음``` : 학습자의 졸음 여부 
  
- **반응의 종류를 이모티콘으로 표시**

- **질문 버튼을 통해 질문 의사 표시**

----------

**3. 기술 다이어그램**

![image](https://user-images.githubusercontent.com/55044278/100983892-4806d400-358d-11eb-8e0c-2008391b8b5b.png)

----------

**4. 사용 기술**

- **Python 3.7**

- **Opencv**

- **Dlib**

- **PyQt5**

----------

**5. 실행 화면**

- **긍정 표현**

  - 학습자가 현재 고개를 끄덕이고 있는 상태

    <p><img src="https://github.com/yoonho0922/Untacticon/blob/master/readme_util/yes_motion.gif?raw=true" width="30%" height="30%"></p>

- **부정 표현**

  - 학습자가 현재 고개를 젓고 있는 상태

    <p><img src="https://github.com/yoonho0922/Untacticon/blob/master/readme_util/no_motion.gif?raw=true" width="30%" height="30%"></p>

 - **의문 상태**

     - 학습자가 현재 학습 내용에 의문이 있는 상태

       <p><img src="https://github.com/yoonho0922/Untacticon/blob/master/readme_util/doubt_motion.gif?raw=true" width="30%" height="30%"></p>

- **졸음 상태**

  - 학습자가 현재 졸고 있는 상태

    <p><img src="https://user-images.githubusercontent.com/55044278/101001720-d76ab200-35a2-11eb-871d-feadc2fd5c74.gif" width="30%" height="30%"></p>

- **자리 비움 상태**

  - 학습자가 현재 자리를 비 모듈이 사람을 인식하지 못하는 상태

    <p><img src="https://github.com/yoonho0922/Untacticon/blob/master/readme_util/left_motion.gif?raw=true" width="30%" height="30%"></p>

- **질문 버튼**

  - 학습자가 현재 질문이 있는 상태

    <p><img src="https://github.com/yoonho0922/Untacticon/blob/master/readme_util/question_motion.gif?raw=true" width="30%" height="30%"></p>

----------

**6. 기대 효과**

![image](https://user-images.githubusercontent.com/55044278/100985320-2f97b900-358f-11eb-8be6-ad5955710d16.png)

----------

**7. 설명 동영상 링크**

[![image](https://user-images.githubusercontent.com/55044278/101017572-9c21b080-35ad-11eb-894a-93fe443ab318.png)](https://youtu.be/Ry_QrVTIT5k)

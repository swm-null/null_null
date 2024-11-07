import asyncio
import json
import struct
import textwrap
import pytest
from httpx import ASGITransport, AsyncClient
from ai.memo import structure
from main import app
from routers._models.memo.tags import Res_post_memo_tags


tag_basebody={
  "user_id": "ecc2fbea-b0c7-4889-a613-d8f4a6cff108",
  "raw_memos": [
    {
      "content": "",
      "image_urls": [],
      "voice_urls": [],
      "timestamp": "2024-11-07T04:32:29.216Z"
    }
  ]
}

structure_basebody={
  "user_id": "ecc2fbea-b0c7-4889-a613-d8f4a6cff108",
  "memos": [
    {
      "content": "",
      "image_urls": [],
      "voice_urls": [],
      "timestamp": "2024-11-07T16:25:30.643Z",
      "tags": []
    }
  ]
}

contents=[
"""
https://m.10000recipe.com/recipe/6900101
""",
"""
탕평채

재료 및 분량 (4인분)
청포묵 1모(500g), 소고기(우둔살) 90g, 미나리 90g, 숙주 150g, 홍고추 1개(15g), 계란 1개 김 1장, 소금·식용유 약간씩
고기 양념장
간장 1큰술, 설탕 2작은술, 다진 파 1작은술, 다진 마늘 ½작은술, 참기름 ½작은술, 깨소금 ½작은술, 후춧가루 약간
탕평채 양념(초간장)
간장 1큰술, 설탕 1작은술, 식초 1큰술, 물 1큰술

준비하기
청포묵은 굳은 면을 썰어내어 6×0.5×0.5cm 크기로 채 썬다. 끓는 물에 소금을 넣고 데친 후 물기를 뺀다.
소고기는 결 방향대로 가늘게 채 썰어 고기 양념장 재료를 모두 넣고 10분 동안 재운다.
미나리는 잎을 떼어 다듬은 뒤 끓는 물에 소금을 약간 넣고 데친다. 찬물에 헹궈 물기를 꼭 짜고 4cm 길이로 썬다.
숙주는 머리와 꼬리를 다듬어서 끓는 물에 소금을 약간 넣고 데친 다음 찬물에 헹군 후 물기를 제거한다.
홍고추는 반을 갈라 씨를 빼고 곱게 채 썬다.
계란은 노른자와 흰자로 나누어 소금을 약간 넣고 각각 잘 풀어놓는다.
김은 구워서 비닐봉지에 넣고 잘게 부순다.
간장에 나머지 재료를 섞어서 탕평채 양념(초간장)을 만든다.
조리하기
팬에 기름을 약간 두르고 양념한 고기를 중간 불에서 볶아 식힌다.
계란 노른자와 흰자는 각각 황백 지단을 얇게 부친 뒤 4cm 길이로 가늘게 채 썬다.
계란 지단은 고명용으로 조금만 남기고 모든 재료를 큰 그릇에 넣어 한데 합한 다음 탕평채 양념을 넣고 가볍게 고루 섞는다.
탕평채를 접시에 가지런히 담고 남겨둔 계란 지단을 고명으로 얹는다.
조언
묵은 녹말(전분)에 물을 붓고 되직하게 풀을 쑤어서 굳힌 것이다. 초간장에 새콤하게 무 쳐 먹기도 하지만 소금과 참기름만으로 무 쳐도 맛있다.
""",
"""
[ 전복솥밥 ] 1~2인분 기준

[ 재료 ]

전복 솥밥 재료 
밥 2공기(400g)
전복 2마리(10미)
대파 흰부분 약 1대(50g)
참기름 2큰술(14g)
식용유 2큰술(14g)

양념장 재료
양파 1/5개(50g)
대파 1/5대(20g)
청양고추 2개(20g)
진간장 5큰술(50g)
간마늘 약 1/2큰술(8g)
황설탕 1/2큰술(6g)
통깨 약 1큰술(6g)

[ 만드는 법 ]
1. 전복을 준비 한 후 흐르는 물에 솔로 전복을 깨끗이 씻어준다.
2. 냄비를 준비한 후 전복이 잠길만큼 물을 받아서 불에 올린 후 강불로 켠다.
3. 냄비에 담긴 물이 끓는 사이 양념장을 준비한다.
4. 양념장은 양파 사방 약 0.5cm로 잘게 다지고 대파와 청양고추는 길게 반 갈라서 두께 0.3cm로 송송 썰어서 준비한다.
5. 통깨는 절구에 빻아서 깨소금을 만들어 준비한다.
절구가 없을시에는 통깨를 봉투에 담아 소스병들을 이용하여 으깨서 깨소금을 만들어 사용한다. 
6. 양념장 만들 그릇을 준비한 후 썰어 놓은 양파, 대파, 청양고추와 진간장, 간마늘, 황설탕, 깨소금을 넣고 잘 섞어 양념장을 만든다.
7. 냄비에 담긴 물이 팔팔 끓으면 씻어 놓은 전복을 넣고 1분~1분 30초간 데쳐준다.
8. 데친 전복은 찬물에 담가서 식힌다.
9. 데친 전복은 껍질과 살 사이에 숟가락을 넣고 껍질과 살을 분리한다.
10. 전복살에 붙어 있는 내장은 가위를 이용하여 잘라 놓고 이빨은 손으로 눌러서 제거하거나 가위를 이용하여 제거해준다.
11. 손질한 전복살은 찬물에 살짝 씻어 준 후 전복살 안쪽을 위로 올려 놓고 길게 칼집을 두줄 넣어 준 후 두께 0.4cm로 사선으로 썰어준다.   
구매한 전복양이 많을 시에는 데쳐서 손질한 전복을 봉지에 2마리씩 나눠 담아 공기를 빼서 묶어 포장한 후 냉동 보관해 놓고 먹으면 된다.
남은 전복 내장은 전복죽을 만들어서 먹거나 전복 솥밥에 2개 정도 추가로 넣어 줘도 된다.
12. 전복 내장은 듬성듬성 잘라서 준비한다.
13. 전복 솥밥용 대파는 길게 반 갈라서 두께 0.4cm로 썰어서 준비한다.
14. 후라이팬을 준비한 후 불을 켜고 식용유, 참기름 1큰술을 넣고 준비해 놓은 대파, 전복살, 전복 내장을 넣고 대파가 숨이 죽을때까지 볶아준다. 
15. 양은 냄비에 밥을 펴준 후 참기름 1큰술을 둘러 넣고 볶아 놓은 전복을 펴올려 담아준다.
밥을 담을때 눌러 담지 않는다.
16. 양은 냄비 뚜껑을 덮어 준 후 약불에 올려 약 5~6분 정도 밥이 눌도록 익혀준다.
약불로 해야 밥이 가지고 있는 수분이 나와서 쪄진다.
냄비 뚜껑을 열지 않은 상태로 냄새로도 타지 않는지 확인한다.
17. 완성 된 전복 솥밥은 양념장과 함께 비벼 먹는다.
버터를 추가로 넣어서 비벼 먹어도 맛있다. 
전복 숙회는 기호에 따라서 전복솥밥 양념장, 간마늘소금장, 초장을 찍어먹으면 맛있다.
""",
"""
[ 초계라면 ]

[ 재료 ]
진라면 순한맛 1개
정수물 1컵(180ml)
조미닭가슴살 1/2개(50g)
양조식초 3큰술(24g)
황설탕 1과1/3큰술(16g)
오이 약간(15g)
연겨자 1큰술(6g)
청양고추 약1/3개(3g)
얼음 적당량
통깨 약간

[ 만드는 법 ]
1. 깊은 그릇에 라면 분말스프, 양조식초, 황설탕, 연겨자를 넣어 덩어리가 풀어지고 설탕이 녹을 때 까지 섞은 후 정수물 1컵을 섞어 육수를 만든다.
설탕은 취향에 맞게 1큰술~1과1/2큰술 사이로 조절한다.
2. 닭가슴살 반개를 결대로 찢어 준비한다.
닭가슴살 1개를 다 사용해도 좋다.
3. 오이는 두께0.3cm로 채 썰고, 청양고추는 두께 0.3cm로 어슷썰어 준비한다.
오이와 청양고추의 양은 기호에 맞게 준비한다.
4. 냄비에 물 500ml를 넣고 바글바글 끓으면 면, 후레이크, 닭가슴살을 넣고 약 4분 삶는다.
꼬들하게 면을 삶을 경우 찬물에 식혔을때 면이 딱딱해질 수 있으니 주의한다.
5. 삶은 면은 찬물에 충분히 헹군 후 체에 밭쳐 물기를 제거한다.
6. 완성 그릇에 삶은 면, 닭가슴살을 담고 얼음을 넣는다. 
7. 고명으로 오이채, 청양고추를 올리고 육수를 붓는다.
8. 통깨를 뿌려 완성한다.

https://www.youtube.com/watch?v=EhTxL1sWnMI
""",
"""
[감자탕 재료]
[육수]
돼지 목뼈 or 등뼈 5kg
통후추 1테이블스푼 https://link.coupang.com/a/bTCnv2
월계수잎 4~5장 https://link.coupang.com/a/bTCnv2
생강 손가락 크기 2개

[양념장]
(모두 밥숟가락)
된장 10  https://link.coupang.com/a/bTCnOK
고추장 3 https://link.coupang.com/a/bTCnSs
고추가루 7
간장 3
다진마늘 5
다시다 2 https://link.coupang.com/a/bTCnVV

[오리지널 감자탕]
육수 1.5리터 (뼈 끓인 국물 2:1로 희석)
뼈고기 2~3조각
양념장 3숟가락 (크게 퍼서)
감자 3개
우거지 (얼갈이 배추 300g 분량) https://link.coupang.com/a/bTCn3d
대파 1대
청양고추 1개 
깻잎 or 깻순 30g https://link.coupang.com/a/bTCn6w
들깨가루 3숟가락 https://link.coupang.com/a/bTCn9z
(전골요리니 먹어보면서 취향에 맞게 추가하세요
끓이면 끓일 수록 맛있어집니다)

[제주도 접짝뼈국]
육수 1.5리터 (뼈 끓인 국물 2:1로 희석)
무 1/3개
메밀가루 100g https://link.coupang.com/a/bTComC (메밀 100% 아니어도 됨)
대파 1개 송송 썰어서
소금
후추
참깨 (토핑)

[콩비지 감자탕]
육수 1.5리터 (뼈 끓인 국물 2:1로 희석)
양념장 3숟가락 (적당히)
마늘 1숟가락 (크게 퍼서)
깻잎 or 깻순 80g https://link.coupang.com/a/bTCn6w
대파 3대
청양고추 3개
콩비지 (불리기 전 백태 콩 200g 분량) https://link.coupang.com/a/bTCoCD
들깨가루 3숟가락  https://link.coupang.com/a/bTCn9z
(전골요리니 먹어보면서 취향에 맞게 추가하세요
끓이면 끓일 수록 맛있어집니다)
(이상 제휴 링크로 구매 시 수수료를 받아 채널 운영에 도움이 됩니다.) 
""",
"""
후쿠오카

현지유심
속옷 3셋
나갈때 입을 티셔츠 3벌
잘 때 입을 옷 1셋
세면도구 (칫솔 치약 비누 샴푸 면도기)
아이패드 + 매직키보드
충전기(미국향) + C타입 케이블 2개 + 워치 충전기

보조배터리
여권
지갑 + 엔화
삼각대
""",
"""
수강권 사용내역

XksW2atnNQlXYoZZ 정예원
euSLCwEsPOTXoFtt 정보운
yqQwxAGHhmcTYXog 김소현

--미사용
gH6pH1DNG25oMUuR
MXArhETTTaNeWD0n
Uwa1auru26IQvScM
a6OvSmFVRFalenQf
pGajhmYYt3a6DLFJ
pslVMG4SIvc3frOI
ChLa3Jx3ZY6AHhQn
""",
"""
https://forum.ragezone.com/threads/ragnarok-m-korea-mobile-game-source-o.1212464/page-33#post-9300253
""",
"""
https://forum.ragezone.com/threads/destiny-child-client-source-code-server-source-code-development-documentation.1229955/
""",
"""
https://forum.ragezone.com/threads/full-source-code-destiny6-mobile-game-ios-android-vm-server-android-unity-project-source-code-server-and-some-tools.1234464/
""",
"""
[0단계 : 중앙대학교 310관 지하] : https://open.kakao.com/o/gY84doif
이곳은 중앙대학교 310관 지하의 어떤 강의실입니다.
빠르게 문제를 풀어 탈출해야해요!
GDSC CAU의 공식 기수를 X,
GDSC YSU의 공식 기수를 Y라고 할 때,
다음 C++ 코드의 GNU GCC 환경에서의 출력 결과는?
#include <bits/stdc++.h>
using namespace std;
int main(){
int N = X + (int)Y;
cout << "GDSC" << pow(N, 4);
}
답 -> GDSC81

""",
"""
안녕하세요!
다음주 화요일 첫 모임에 앞서, 활동 진행에 대한 이야기를 해보려고 합니다.
올려주신 각자의 BOJ 아이디를 확인하였습니다!

이미 BOJ를 해오셔서 레이팅이 있는 3분은, Solved.ac의 레벨별 문제를 통해, 지난번에 공지드린것과 같이 자신의 티어보다 하위 5단계까지의 범위 내에서 자유롭게 5문제 선정해서 풀어와보시면 됩니다!
https://solved.ac/problems/level

Unrated로 새로 시작하시는 3분의 경우는, Solved.ac에서 제공하는 새싹문제들부터 풀어보시면 좋을 것 같아요.
https://solved.ac/problems/sprout

각자 풀이한 5개씩의 문제들 중, 가장 까다로웠다고 생각하는 문제 1개에 대해서 간단한 코드소개와 왜 그런 아이디어를 이용하게 되었는지를 돌아가며 소개해볼 예정이니 참고해주세요!
""",
"""
제목: 액트 TODO

https://drive.google.com/file/d/1J6yVzvLUpAFbBOx3RWYsVXLIS9uPkoOb/view?usp=share_link

- 타이틀 이미지 적용 -> 해결
- 상황별 BGM
- 자막 작업
- #1 뉴스 스타일 자막
- #8 접종 장면 자르기

- 타이틀
- #6 확진 문자 확인
- #7 증거자료 고뇌 장면 시작할때
- #8 주사기 등장 ~ 접종
- #10 전화끊고 나감 ~ 엔딩
""",
"""
## AI 인생네컷

생각보다 얼굴이 진짜처럼 그려지지 않아서 아쉬움

인물의 포즈, 배치를 최적으로 조정하기 어려움

## 보이스피싱 실시간 음성분석 앱/서비스

Android API에서 실시간으로 음성통화를 받아올 수 없음

외부장비 필요

## 패션쇼핑몰 옷 사이즈 시뮬레이션 서비스

체형이 너무 다양함. 값을 일일히 입력해줘야함.

키 몸무게만으로는 정확한 체형 시뮬레이션 불가

## 면접 도우미 AI

일단 이게 이미 있는거 같긴한데, 기존건 어떤지 모름.
아이디어는 다음과 같음.

1. 사용자 입력: 본인이 만든 예상 질문지 or 자기소개서 or 포트폴리오
2. 서비스: 사용자의 입력 기반으로 본인의 질문을 만듬
3. 사용자 입력: 이제 카메라가 켜지면 ai 면접관과 대화를 시작함
4. 서비스: 사용자의 답변에 따라서 추가질문을 할지 다음 질문을 할지 결정함. 대화는 gpt기반의 tts라고 생각하면 됨.
5. 면접이 끝나면, ai는 피드백 종이를 제공함. 거기에는 답변에 대한 분석 뿐만 아니라 얼굴의 표정이라던지, 음성의 높낮이 같은 분석또한 제공해주는거임 ㅇㅇ.

쓰다보니 알게된건데 이미 해주는 서비스들이 있긴하네. 몬스터 ai

## 음식 혈당 등 이미지 기반 영양분 분석 ai

https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71392

### 말동무 AI

남들한테 말하기 힘든 고민 등에 대한 이야기를 나눌 수 있는 앱

이미 관련 앱이 있긴 하지만 차별화되는 서비스를 추가하면 좋을 것 같음

텍스트가 아닌 tts 형태로 대화
""",
"""
3/29 교수님면담
## 인트로

인사

## 팀원소개

유용민 - 팀장 / HW / App

오재환 - 팀원 / AI / 클라우드

임윤지 - 팀원 / Back-End / DB

## 주제소개

실시간 음성통화 분석을 통한 보이스피싱 탐지 및 알림 애플리케이션

## 배경

보이스피싱 비율 늘어남

인지가 쉽지 않은 노인분들 늘어남

## 관련서비스

(23. 11.) 경찰청 음성모델 - 통화녹음 데이터를 이용해 음성모델 분석 및 용의자 탐지

(23. 11.) 이통3사 - 음성통화 실시간 분석 서비스? 아직 뒷소식 없음

## 차별점

하드웨어장비 하나만 폰에 붙이고 앱을 깔면 일반적인 사용자의 서비스 활용이 가능하다는 접근성

별다른 사용자의 조치 없이도, 통화만 하면 자동적으로 분석 및 탐지가 진행됨

## 공학적 가치..?

## 구현내용

AI - 음성 관련 데이터 탐색 및 전처리

BE - 필요 API 구성 및 기반작업 준비 중

HW - ESP32 개발보드 준비 / 라이브러리 탐색

프로젝트 전체적인 플로우 상세화 중 

## 멘토링 & 진행상황

주제에 대해 상기하고, 관련 서비스나 뉴스기사 함께 탐색

## 앞으로계획

빠른시일 내 상세 플로우 확정하고, 하드웨어 및 각자 소프트웨어 파트 개발 진행
""",
"""
4/12 멘토링
## 역할분담

---

유용민 : 팀장 / 앱 개발 / 하드웨어 개발

오재환 : AI / 모델관리 / 모델 호스팅 (ML Ops?)

임윤지 : BE / DB관리

## 그동안 무엇을 했는가

---

하드웨어

- ESP32 기반 환경 설정
- 각종 센서류 / 통신방식 탐색
    - HSP / HFP / A2DP 프로토콜 관련 라이브러리 조사
- Flow
    - 앱 : 통화시작 시 BE와 소켓열기
    - 하드웨어 : 통화시작하면 HFP연결 후 자체마이크로 수음
        - 수음된 사운드 자체스피커로 재생
    - 동시에 5초간격으로 녹음된 음성데이터 앱으로 블루투스 전송
    - 앱 : 블루투스로 수신한 음성데이터 소켓을 통해 업로드
    
    → 따로 저장 안하고 분석만 할거면 사용자 인증도 필요없지않을까?
    
    → 통화녹음데이터 처리에 따른 개인정보 이슈는 일단 기술적 구현 이후에 생각 
    

백엔드 @윤지 임 

- 실시간 녹음데이터 수집 방식
    - 소켓 열어두고 지속 업로드?
    - 5초간격?

AI / ML @큐비트 

- 재환이 노션이름 왜 큐비트임 검색해도 안나와서 헤맸네 ㅎㅎ
- 관련 모델 + 기반데이터 탐색 (그놈목소리)
- 정확도 높일 방안 강구 (LLM…어쩌구…)

- 두가지 학습된 모델을 사용
    - koBERT기반 분류 모델 ⇒ base 모델
        - training process: KorCCVi_v2.1.csv + 바로 이 목소리
        - inference process: 텍스트 → koBERT로 벡터 변환 → 이진 분류
    - LLM기반 분류 모델 ⇒
        - 업데이트 되는 [피해사례](https://fss.or.kr/fss/bbs/B0000059/list.do?menuNo=200359&bbsId=&viewType=&cl1Cd=&pageIndex=1&sdate=&edate=&searchCnd=1&searchWrd=)에서 데이터를 크롤링 진행 ⇒ b라고 지칭
        - 실시간 전화 내용 요약 후 벡터 변환 ⇒ a라고 지칭
        - a와 b들의 유사도 비교를 통해 사례 몇개 추출하여 llm에게 전달하여 분류 요청
        
        - 흠….그냥 본인 데이터셋에서 가져와야 하나…?
- 가장 큰 문제점 2가지
    - 보이스피싱 데이터가 현저하게 적다는 점
        1. KorCCVi_v2.1에서 피싱 시도 데이터는 600개에 불과함. 2200개가 일반데이터임
    - 보이스피싱이 아닌 일반 전화에 대한 대처가 어렵다는 점
    
    - 그냥 프롬프트를 이렇게 줘야 하나?
        - 뭔가 돈, 개인정보를 달라고 하는 시도를 하는게 있나요?
        + 통화내용
        true, false로 대답해주셈.
""",
"""
# 실험 자료

- 4-15 실험
    - 모델명: gemini-1.0-pro
    - 사용한 프롬프트: 다음 나오는 문장에서 정보를 탈취하거나 금전을 요구하고 있는지 '반드시' True/False로만 대답해줘. + 데이터셋 내용
    - 평균 데이터 길이: 4000자(공백 포함)
    - 개당 평균 쿼리 시간: 3~4초
    - 날린 쿼리 갯수: 2928
        - 유효한 쿼리: 2870
            1. 2144 :  False인데 False로 나온거
            2. 21 : False인데 True로 나온거  ⇒ 금전 탈취 시도가 있었는지 체크해야함.
            3. 294 : True인데 False로 나온거 ⇒ 시도만 있고, 액션은 없었는지 체크해야함
            4. 390 : True인데 True로 나온거 ⇒ 이건 뭐 잘한게 맞음
            ⇒ 2,3번에 대한게 중요함. 잘한건지는 내일 중으로 모두 검토 예정
        - 응답이 안온 쿼리: 58 ⇒ 원인 파악 하긴 해야함.
    
    아이디어:
    
    1. 데이터셋을 하나더 라벨링 해하겠다. 금전적인거를 요구한거, 아니면 그냥 시도만 한거 이 두개로. 그래야 llm 모델에 대한  검증이 더 잘 이루어질거라고 봄.
""",
"""
유용민 01081821022

업무진행상황: 개통완료
통신사/유형: KT  번호이동
모델명: SM-A155
색상: 라이트블루
요금제: LTE 베이직
약정: 선택약정24개월  현금완납
회선유지기간: 2025년 04월10일
요금제유지기간: 2025년 02월09일
""",
"""
https://novemberde.github.io/post/2024/11/07/http-https-hxxp-hxxps/
""",
"""
갈미조개샤브샤브,밀면,꼼장어,물회,돼지국밥,회,포장마차

계획은 대충 짜는게 미덕

1일차
점심에 붓산 도착해서 시장돌면서 길거리음식 ㄱㄱ
자갈치쪽 시장 반나절동안 싹 돌기~
국제시장 깡통시장 BIFF거리 책방골목 (한 다섯시?)
- 깡돼후 먹어보기

대충 해 져가면
태종대ㄱㄱ
두시간쯤 있으려나?

슬슬 해지고 배고파지면
저녁은 뭐 먹을까? (8시)
- 냉채족발?
차이나타운에서 먹든가 구경하면 좋을 것 같은데? (9시)

이제 그럼 집 주변 포장마차 가도 되고?

2일차
-----
아침? 어캄? 뭐먹음?
    - 국밥?

붓산패스 시작(9시)
블루라인파크 해변열차 - 부산패스 (편도 30분 * 2 + 1시간) -> 11시

샌텀시티쪽 이동해서 점심이건 그 전에 점심이건 (~12.5시)
    - 밀면 ㄱ
뮤지엄원(7시까지) - 부산패스 8000원 (14)

영화체험박물관 + 트릭아이뮤지엄(6시까지) - 부산패스 (18)?
저녁먹고 (19)
    - 꼼장어?

용두산공원 좀 돌다가 (20)
부산타워 (22시 운영종료) - 부산패스
-----
그다음 내려와서 집 주변에서 놀까요?
가려면 해운대 야시장 가도 되고. 해운대 구경도 좋고.

3일차
아침 먹고
    - 국밥?

집주변 해리단길
영화의거리 (13시)?

해운대쪽에서 점심먹고 
    - 물회 ㄱ

f1963 (16)

감천 문화마을?
소망계단/닥밭골벽화마을?
흰여울 문화마을?

대충 돌다가 저녁먹고 올라가야지 이제
    - 만호갈미샤브샤브

""",
"""
안녕하십니까 지원자 조태식 입니다.

개발과 함께 보낸 제 3년을 요약하자면, 꾸준하고 그리디했다고 요약할 수 있을 것 같습니다.
그동안 개발을 손에서 놓은 적이 없었다는 점에서 꾸준하고, 그때그때 할 수 있는 최선의 선택으로 인생의 근사해를 찾아가고 있다는 점에서 그리디하다고 말할 수 있겠습니다.

제가 사용 가능한 기술들에 대한 적어두었는데요, 이해하고 사용할 수 있다는 건 언어와 라이브러리의 내부 로직을 대부분 이해하고 있으며, 이를 활용해 효율적인 코드를 짤 수 있다는 의미이며, 아래로 갈 수록 효율적이라고는 단언할 수 없지만, 필요한 코드는 작성할 수 있다는 의미입니다.

저는 프로그래밍을 시작하고 얼마 되지 않아 삼성전자 하계 대학생 알고리즘 특강에 참여하게 되었으며,
이 곳에서 복잡한 명세사항을 코드로 정확하고 빠르게, 또 효율적으로 표현하는 것에 대해 훈련할 수 있었습니다.
하루 6시간 이상 시간을 투자한 결과 우수수료생이라는 좋은 결과를 받을 수 있었습니다.

제가 본격적으로 cs를 공부하게 된건 42서울이라는 학교에서였습니다.
이 곳은 교재나 강의, 선생 없이 단지 문제 상황만이 주어지고, 이 문제를 해결하기 위해 내가 모르는 것은 무엇인지, 그 지식을 내 것으로 만들기 위한 방법은 무엇인지, 동료와 함께 어떻게 부족한 지식을 채울 수 있는지를 배울 수 있는 곳입니다.
요약하자면 배우는 방법을 배우는 곳이라고 할 수 있겠습니다.
이 곳에서 cs와 관련된 여러 프로젝트를 진행하였고, 이는 그 중 일부입니다.

공부하다보니 제 열정이 재단의 눈에 들었는지 좋은 기회로 인터뷰를 진행하기도 하였고,
내부 대회에서 1등을 차지하여 서울캠퍼스 대표로 해외에 다녀오기도 하였습니다.
그 과정에서 처음 만난 동료와 해커톤에서 우승하는 등의 성과를 얻기도 하였습니다.

저는 꾸준히 알고리즘을 공부해왔습니다.
프로그래밍 실력은 결국 주어진 문제를 빠르게 효율적으로 해결할 수 있는 능력이라고 생각하기 때문입니다.
이 과정에서 저는 공동체에 기여하기 위해 이러한 능력을 향상시킬 수 있는 기회를 제공하기도 하였습니다.

지난 겨울, 저는 스마트 스피커를 호출하는 등의 행동이 없어도, 내 의도에 맞춰 작동할 수 있는 플랫폼을 구현하였습니다.
추후 iot시장에서 표준이 될 matter를 이용한, 통합된 플랫폼을 의도하였으며,
ultralaytics의 yolo모델을 이용해 사람의 행동을 인식했습니다.
저는 팀장을 맡았으며, 기획, 디자인, 프론트엔드 등 여러 부분에 관여했습니다.

이 프로젝트는 제가 자기소개서에서 언급한, 소마에서 해보고 싶은 프로젝트입니다.
소규모 그룹에게 적합한 회계 솔루션을 만드는 것에 집중하였으며, 몇 가지 문제를 제외하면 거의 구상이 끝났습니다.
글만으로 이해가 어려울 것이라 생각되어 예시 디자인과 아키텍처를 첨부하였으니 확인해주십시오.

이 외에도 교내 경시대회나 외부 대회에서 제가 쌓아온 것들을 이용해 수상한 내역이 있습니다.
발표를 들어주셔서 감사합니다.
""",
"""
문제아이디어

https://www.acmicpc.net/problem/2560
여기서 pq 두개를 사용한 스위핑풀이로 풀 수 있는 문제
""",
"""

1. 자기소개 (2분)
    1-1. 프로필
    1-2. 어떻게 연수를 가게 되었는가

2. 여러 우여곡절 (2분)
    2-1. 출발일정을 착각한 일
    2-2. 혼자 네덜란드 입국심사에서 걸린 일

3. 네덜란드에서 (8분)
    3-1. 코담 캠퍼스
        3-1-1. 밥집
        3-1-2. 네덜란드어와 공용어
    3-2. 간담회
        3-2-1. 내용들?
        3-2-2. 간담회 마이크
    3-3. 인터뷰
        3-3-1. 어려웠던 점과 좋았던 점
        3-3-2. 42서울과 코담 학생의 차이

4. 프랑스에서 (8분)
    4-1. station f (1분)
        station f for 42
    4-2. 자기소개 발표했던 일 (1분)
    4-3. make something 42 (6분)
        4-2-0. 주어진 시간과 한계, 조건
        4-2-1. 어떤 프로젝트를 했는가 (3분)
        4-2-2. tig (1분)

5. 마무리 (2분)
    5-1. 영어의 중요성
        근데 프랑스는 영어 안 통함
        그지같은 수능영어 말고 듣기 말하기가 잘 돼야함..
    5-2. ?

""",
"""
Nice to meet you. 
My name is Taesik Jo, and my Intra ID is TJO. 
I'm here to briefly introduce myself and explain why I'm here.
First, I'll describe my ID to help you remember it and then explain about how I came here.

First of all, you might be wondering why there's a picture of an ostrich on this slide instead of a different image.

My Intra ID, TJO, is pronounced as '티조' in Korea. When written in Hangul, the korean language, it looks like this. 
This might seem quite unnatural to pronounce for Korean speakers, so some people around me started reading my ID differently. 
In Korean, '타' is a more comfortable and natural pronunciation than '티' in my ID. They simply added a line to the '티' to TAJO. By coincidence, even before my time at 42, my friends used to call me 'ostrich,' in korean 타조, 
and I have carried that nickname here as well. 
So, after this presentation, I'd appreciate it if you remember me as 'TaJo' or 'ostrich.'

Now, let me explain how I got here. I have a hobby of problem-solving, which involves efficiently solving problems using computers. 
To make it more understandable, let's consider a problem. 
Suppose we need to find the minimum 
 path from point A to point F. 
We could explore all the paths one by one, but it would be highly inefficient, especially for large problems. 
Instead, we analyze the problem's restrictions to find the best solution effectively and efficiently.
In this case, since the edges have different weights, the fastest method, BFS, is not applicable. 
However, since there are no negative weights on the edges, 
we can use a reasonably fast algorithm like Dijkstra.

This process involves abstracting a specific problem, and finding the optimal solution available in that restriction.
This process is what we call problem-solving.

The image on the left is a screenshot of a problem from Leetcode. I'm sure that you have heard of coding interview practicing  platforms like Leetcode. 
Korea also has similar platforms, and I have achieved a rank of 382 out of approximately 500,000 users on Baekjoon Online Judge, a platform Korean programmers prefer. 
Also, I have experience with getting the awards from programming competitions and have organized competitions with over a few hundred participants multiple times.

42 Seoul organized coding interviews to help students prepare for real-life experiences.
They provided various prizes to encourage student participation, and the most significant prize was the opportunity for this program. They offered this opportunity to top scorers, and from the first exam, I received a perfect score. I continued to take the exams and consistently received high scores.

Through this opportunity, I had several interviews about my life, 
and eventually, I came to Paris to meet all of you. 
Before finish,
I want to express my gratitude to 42Seoul for providing this excellent opportunity. 
To the Ecole, 
Enchanté de faire votre connaissance.
""",
"""
OHOBRKPWNFBQDOCUGRAR 10만
JQKCMNJWOJOJODHQWCQX 5만
AFPOOMQGBXSRBRBDOIVR 3만
MQOMRKEOIOBAQCCWGHPF 1만
CMTQSNQGQCMJBHDVWQHI 5천
FGHVDKFOJKKPOPMFWABO 1천
""",
"""
박현호01099032034
창원시 진해구 장천동 대동다숲아파트 102-703
""",
"""
문제 아이디어: https://www.acmicpc.net/problem/2374
이거 최대값 어떻게 구함?
""",
"""
대회·공모전 > IT•소프트웨어•게임 - 콘테스트코리아 - https://www.contestkorea.com/sub/view.php?displayrow=12&int_gbn=1&Txt_sGn=1&Txt_key=all&Txt_word=&Txt_code1=&Txt_aarea=&Txt_area=&Txt_sortkey=a.int_sort&Txt_sortword=desc&Txt_host=&Txt_actcode=&page=1&Txt_bcode=030510001&str_no=202303220069
""",
"""
안녕하세요. 안산학생입니다.

오늘 자소서 첨삭을 7분 정도 봐드렸습니다. 공통점이 있어서 말씀드립니다.

자소서는 주저리주저리 시간과 장소, 상황을 설명하는 소설을 쓰는 곳이 아닙니다. 간결하게 내가 했던 일들을 요약하고 자랑하는 공간입니다.

잘못된 예
'나는 너네 회사가 좋아. 너네 이것도 하구 저것도 하구.. 그래서 나도 거기가서 같이 하구 싶어...'

올바른 예
'나는 너네 회사가 좋아. x기술이 업계 최고 잖아. 나도 ??프로젝트를 수행하면서 x, y기술을 익혔어. 그래서 x기술을 ~~해서 더 발전시킬 수 있어. 서로 윈윈할 수 있을거야.'

어떠한 말을 적을 때 근거가 있어야합니다. '난 이거 알아'가 아닌 '난 이거 ~프로젝트 해봐서 알아, 이거 이렇게 하면돼'가 되야합니다. 그리고 결국엔 '그래서 난 그 회사에서 ~도움을 줄 수 있어, 왜냐면 난 ??경험이 있으니까'로 되야합니다.

대부분의 분들이 경험들만 무지성으로 나열한다거나, 혹은 소설처럼 '대학생때 우연찮게 공모전 기회가 있어 지원했는데, 시간이 너무 없어서. 이렇게 했습니다.' 불필요한 말로 가득합니다.

자소서 작성할 때 이 말(문장)이 있어도 되는지, 없어도 되는지. 확인해보세요. 빼서 읽히면 없어도 되는 문장입니다.

그리고 면접관 입장이 되서 읽어보세요. '내가 널 왜뽑아야되지? 그래서 하고싶은말이 뭔대? 왜 오고 싶은거지? 와서 뭘 할 수 있는데? 기술을 안다고? 근거는? 왜?' 라는 질문에 대한 답변이 자소서에 다 있어야 합니다.

소설을 쓰지마세요. 거짓말도 하지마세요. 내 인생을, 내 경험을 요약하고 근거를 제시하며 어필하세요. 그게 자소서입니다.

곧 하반기 채용시즌이 끝나고 상반기가 돌아올텐데, 미리 자소서 작성하셔서 대비하시기 바랍니다.

파이팅입니다!
""",
"""
누적합과 쿼리 -> psum의 모든 값을 map에 저장해두고 특정 누적합을 입력받으면 쿼리당 O(n)정도로 해당 구간의 개수를 구할 수 있음 -> 더 빠른 방법이 있나??
""",
"""
6. 한글
    1. 훈민정음의 의미
        훈민정음 = 책의 이름 and 체계 이름
        혜례본 - 한문으로 해설과 용례를 적은 책
        언해본 - 혜례본 중 서문과 예의부분만을 번역한 책
    2.1 훈민정음 창제 배경
        우리나라 말이 중국과 달라 한자와는 서로 통하지 않아서
    2.2 훈민정음 창제 목적
        어리석은 백성이 말하고자 하는 바가 있어도 마침내 제 뜻을 말하지 못하는 사람이 많다.
    2.3 한글 창제 시기
        세종 25년(1443년) 음력 12월 창제, 1446년 9월 반포
    2.4 한글 창제의 원리
        1) 초성 제자 원리
            기본자 - 상형의 원리(발음기관)
            나머지 - 가획의 원리
            예외 - 이체자 (ㅇ ㄹ 반치음시옷)
        2) 중성 제자 원리
            기본자 - 천 지 인 삼재를 추상화
            나머지 - 초출자, 재출자
        3) 종성 제자 원리
            종성부용초성
    3. 한글의 우수성
        1) 창제 원리 측면
            독창성: 기본자를 발음기관과 관련시키거나, 천지인의 생김새를 본떠 독창적으로 창제함
            조직성: 기본자를 만들고 파생시켜 그 밖의 글자를 만든 가획의 원리와, 
                같은 계열의 소리는 글자의 모양이 비슷하여 배우기 쉽고 쓰기 쉬움
            개방성: 초성과 중성 기본자를 바탕으로 가획, 병서, 연서등의 방법으로 무수히 많은 글자를 만들 수 있음
            경제성: 유한한 수의 자음과 모음으로 수많은 음절을 만들 수 있음
                소수 민족에게 글자를 보급하거나, 문맹인을 교육하는 등 발음기호로 활용할 수도 있음.
        2) 활용 편리성 측면
            모아쓰기: 해례의 부서법(브텨쓰기)에 따라, 모아쓰면 뜻을 알기 쉬워서 효율적이고,
                한자와 한글이 음절단위로 일대일 대응을 이뤄 한글로 표기할 때 편리함, 가로쓰기 세로쓰기 모두 가능
        3) 형태 측면
            다른 언어와 다르게 자음과 모음의 형태가 다름.
            최소한의 도형만을 가지고 글자를 만들고, 대칭과 가획으로 자형을 이룸.
            양성 모음자는 오른쪽과 위쪽에, 음성 모음자는 왼쪽과 아래쪽에 배치함
""",
"""
    4. 한글 자음과 모음의 이름
        1527년 최세진이 지은 한자 학습서인 '훈몽자회'에서 나옴
    4.1 우리 글자 이름의 변천
        훈민정음: 세종이 글자를 만들 때 씀, 백성을 가르치는 바른 소리
        정음: 정인지의 서문, 훈민정음을 줄인 말
        언문: '언'은 우리말, 우리글의 뜻으로, 훈민정음 이전부터 쓰이다가 훈민정음 이후 '정음'의 뜻으로 쓰임.
        언서: 한문을 '진서'라고 한 데 대한 대립어
        반절: 최세진의 '훈몽자회'에서 등장, 중국 운학의 반절법에서 유래
        암클: 부녀자들이나 쓰는 글
        상말글: 상놈들이나 쓰는 글
        한글: 1910년 주시경이 지음, 1927년 '한글'지에서부터 널리 쓰임
    5. 한글날
        1926년, 조선어연구회가 음력 9월 29일을 가갸날이라고 이름하여 기념하기 시작
        1928년에 한글날로 이름이 바뀜
        음력 9월 상순에 훈민정음을 퍼낸 것으로부터, 이를 양력으로 바꿔 10월 9일을 한글날로 정함
7. 외래어 표기법
    1. 대상과 목적
        외래어의 구분은 동화의 정도로 판단함
        발음의 변화 - file(파일)
        형태의 동화 - -하다의 결합, smart하다
        의미의 동화 - meeting, boots
        외래어 표기법의 목적은 외래어들을 통일된 방식으로 적기 위한것이지, 정확하게 발음을 나타내기 위한 것이 아님
""",
"""
    4. 한글 자음과 모음의 이름
        1527년 최세진이 지은 한자 학습서인 '훈몽자회'에서 나옴
    4.1 우리 글자 이름의 변천
        훈민정음: 세종이 글자를 만들 때 씀, 백성을 가르치는 바른 소리
        정음: 정인지의 서문, 훈민정음을 줄인 말
        언문: '언'은 우리말, 우리글의 뜻으로, 훈민정음 이전부터 쓰이다가 훈민정음 이후 '정음'의 뜻으로 쓰임.
        언서: 한문을 '진서'라고 한 데 대한 대립어
        반절: 최세진의 '훈몽자회'에서 등장, 중국 운학의 반절법에서 유래
        암클: 부녀자들이나 쓰는 글
        상말글: 상놈들이나 쓰는 글
        한글: 1910년 주시경이 지음, 1927년 '한글'지에서부터 널리 쓰임
    5. 한글날
        1926년, 조선어연구회가 음력 9월 29일을 가갸날이라고 이름하여 기념하기 시작
        1928년에 한글날로 이름이 바뀜
        음력 9월 상순에 훈민정음을 퍼낸 것으로부터, 이를 양력으로 바꿔 10월 9일을 한글날로 정함
7. 외래어 표기법
    1. 대상과 목적
        외래어의 구분은 동화의 정도로 판단함
        발음의 변화 - file(파일)
        형태의 동화 - -하다의 결합, smart하다
        의미의 동화 - meeting, boots
        외래어 표기법의 목적은 외래어들을 통일된 방식으로 적기 위한것이지, 정확하게 발음을 나타내기 위한 것이 아님
""",
"""
토스 1000-0060-5839
국민 785802 00 031347
카카오 3333 20 0437640
""",
"""
통학/통근 버스 플랫폼
시내버스나 지하철은 어디에 있는지, 얼마나 기다리면 되는지 파악이 가능한 반면, 학교나 학원 또는 통근버스가 어디에 있는지 알 수 없다는 점에서 착안함
차량을 운전하는 기사 휴대폰이나, 별도의 기기를 차량에 부착하면, gps를 이용해 지금 버스가 어디에 있는지 파악할 수 있음.
기관마다 미리 시간표나 경로를 등록해둘 수 있으며, 미리 어플을 통해 예약하면 타기로 예약된 곳에서만 정차하는 등의 용도로 활용 가능할 것으로 예상됨
""",
"""
에듀케이셔널 크라우드펀딩 플랫폼
항상 공급자가 일방적으로 강의 등을 공급한다는 데에서 착안한 플랫폼
사람들은 이 플랫폼에 등록되어있는 강사/강연자에게 특정한 내용에 대해 강연을 요청할 수 있음
만약 강사가 이 플랫폼에 없더라도 일정 요건이 충족되면 플랫폼을 통해 요청을 보낸다던가?
""",
"""
3. 그룹 의견 취합 플랫폼
    목표: 
    그룹의 의사결정권자가 그룹 내 여론을 빠르고 정확하게 파악할 수 있도록 함

    대상:
    일단 생각중인 건, 학교 총학생회나 과학생회. 꼭 대학교가 아니더라도.
    사기업에서도 이러한 니즈가 있는지는 직접 확인해봐야 할 것 같음.

    핵심 가치:
    구성원 입장에서는 나의 의견을 적극적으로 표현할 수 있는 기회를 마련해 줄 뿐만 아니라, 타인의 의견에 공감한다는 의사표현이 가능해짐. 쉬운 공론화.
    관리자 입장에서는 학생들의 의견을 시의적절하게 모을 수 있으며, 해당 의견에 대한 지표를 활용하면 사람들의 의견을 취합하기 위한 노력을 기울이지 않아도 됨(간담회 등).  

    비즈니스 모델:
    역시 직접 관리자에게 접근해서 판매해야하지 않을까
    https://ohpick.me/price/ - 조직 투표 서비스(투표 개당, 유권자 한 명에 300원정도)
    노동조합 투표, 협회 · 학회 투표, 행사 · 축제 투표, 총학생회 투표, 단과대학 · 학과 투표, 동아리 · 생활관 투표

    왜?:
    내가 필요하다고 생각했었고, 지금도 학교에서 아주 필요해보임..
""",
"""
010-2199-2487
모빙, 24/09/xx
S20+
1년동안 상품권

010-8906-3042
아이즈, 24/10/08
샤오미노트12
2개월 뒤 상품권

010-8039-2487
에이모바일?, 
샤오미노트12

010-8629-3498
skt, 24/05/10~
A15 블루

010-4792-9841
skt, 24/06/25~
A15 옐로우

010-2419-2938
skt, 24/10/08
레드미노트12프로

""",
"""
과제에 있는 내용풀어보시고 첫번째 과제의 신호등 내용은 아예 안나왔습니다.
heapsort는 ppt내용처럼 예측한 복잡도와 실제 복잡도가 있을텐데 헷갈려서 예측한 복잡도 쓰시지 않도록 주의하시구요, 시간복잡도 비교 문제는 과제 형식대로 푸시면 됩니다.
sorting network는 굉장히 간단하게 나오니까 너무 부담갖지 말고, 반례는 저같은 경우에 (a, b, c, d, e)를 넣어서 해당 그래프가 틀렸다는 것을 증명했습니다.

heapsort 과정(과제와 동일한 형식)
heapsort의 time complexity(실수 조심할것)
time complexity T/F(과제와 동일한 형식)
countingsort 수도코드 빈칸 채우기(외우세요)
sorting network 제시하고 sort되는지 여부와 증명(반례 들면 쉽게 풀림)

카운팅소트 수도코드 빈칸채우기
빅오노테이션 증명
시간복잡도 증명

""",
"""
Counting sort(A, n, k)

for i, 1 to k:
    count[i]=0

for i, 1 to n:
    count[A[i]]+=1

for i, 2 to k
    count[i]+=count[i-1]

for i, n to 1
    B[count[A[i]]]=A[i]
    count[A[i]]-=1
""",
"""
물크

**유니크**
- **진 : 장총 맥스 카드** <2600613>
  - 머리어깨
  - 물리 크리티컬 히트 +10%
  - -
  - 한 방에 보내주지!

**유니크**
- **노블 스카이 황옥 보주** <2600542>
  - 머리어깨, 벨트, 신발
  - 물리 크리티컬 히트 +5%
  - 교환가능
  - 운 라이오닐이 안토니움 525개에 판매한다.

**유니크**
- **노블스카이 홍옥 보주** <2600540>
  - 보조장비
  - 물리 공격력 / 독립 공격력 +42, 물리 크리티컬 히트 +2%
  - 교환불가
  - 운 라이오닐이 안토니움 810개에 판매한다.

**유니크**
- **네이트람의 붉은 보주** <2600334>
  - 마법석
  - 모든 속성 강화 +5, 크리티컬 히트 Lv+1, 백 어택 Lv+1
  - 교환가능
  - 백명이 정제된 넨의 결정 3300개에 판매한다.

마크 

**유니크**
- **찬란한 불꽃의 아그네스 카드** <2600675>
  - 머리어깨
  - 마법 크리티컬 히트 +10%
  - -
  - 귀여운 불꽃 요정들아, 인간들을 괴롭혀라

**유니크**
- **노블 스카이 녹옥 보주** <2600543>
  - 머리어깨, 벨트, 신발
  - 마법 크리티컬 히트 +5%
  - 교환가능
  - 운 라이오닐이 안토니움 525개에 판매한다.

**유니크**
- **노블스카이 청옥 보주** <2600541>
  - 보조장비
  - 마법 공격력 / 독립 공격력 +42, 마법 크리티컬 히트 +2%
  - 교환불가
  - 운 라이오닐이 안토니움 810개에 판매한다.

**유니크**
- **네이트람의 푸른 보주** <2600336>
  - 마법석
  - 모든 속성 강화 +5, 크리티컬 히트 Lv+1, 백 어택 Lv+1
  - 교환가능
  - 백명이 정제된 넨의 결정 3300개에 판매한다.
""",
"""
ㄴㅁ디ㅑㅑㄷㄴ리ㅣㅁㄹㄷㄴ
""",
"""
sfeilsjeifliasfeiljfl
""",
"""
ㅁ니ㅑㄷㅁ댜리ㅑ미랴ㅣㄷㄴㅁ리ㅑㄷ
""",
"""
23oal8fw3o8awfolw8
""",
"""
졸려
""",
"""
2024 ICPC Seoul Regional Onsite Contest :
Nov. 22(Fri) – Nov. 23(Sat)

Nov.22 (Friday)
13:30 – 14:30 Registration, Name-tag Holding,
. team-note, private devices(mouse, keyboard) submission.
. Those are returned on Nov.23 morning after the inspection by committee.
14:30 – 15:30 Contest Orientation
15:30 – 17:00 Practice Session

Nov.23 (Saturday)
08:00 – 9:00 Registration (All three team members are required to participate)
09:00 – 9:30 Entry to the venue (Desk Assignment)
09:30 – 10:00 Rule Announcement, Problem Sheets Distribution
10:00 – 15:00 Competition
15:00 – 15:30 Exit from the venue, Break
15:30 – 17:00 Tech. Talks
17:00 – 18:30 Closing Ceremony (Award)
18:30 Dinner (TakeOut, expected)

Contest Place : KINTEX ( https://www.kintex.com/web/en/index.do )
2nd Exhibition Hall Room 404-405

KINTEX is located 1.5 hours away from Incheon International Airport and
1.0 hour from Seoul KTX train station.

Accommodation : You can easily find an affordable business-class
hotel within walking distance of the KINTEX Hall.
""",
"""
2024 ICPC 대학생 프로그래밍 경시대회 진행 스태프 모집
일정 : 11/22(금) ~ 11/23(토)
시간 : 11/22(금) 11:00~18:00, 11/23(토) 07:30~19:30 (*양일 모두 참여)
장소 : 킨텍스 제2전시장 4층
담당업무 : 대회 준비 및 진행 (참가자 안내 및 통솔, 식사 및 기념품 전달 등)
스태프 참여혜택 : 티셔츠, 기념품, 명찰, 중식, 소정의 사례비 (20만원) 제공
참여신청: https://forms.gle/dabnyqwhnKCX1ggK6
※ 영어가능자 우대
※ 신청자가 많을 시, 조기 마감될 수 있습니다.
※ 자세한 시간 및 장소는 개별 안내 드리도록 하겠습니다.
감사합니다.
""",
"""
2024 ICPC Seoul Regional 본선 진출팀 공지
ICPC 2024 Seoul 예선 참가자분께

이번 예선에 열정적으로 참여해주신 모든 팀원, 코치님들께
다시 한번 감사드립니다. 논란이 있었던 문제 C에 대한
재채점 전의 점수판과 재채점 결과가 반영된 점수판을 올려드립니다.

http://static.icpckorea.net/2024/preliminary/scoreboard/
http://static.icpckorea.net/2024/first_round/scoreboard_10282200/

1차 채점 결과와 2차 재채점 후의 결과를 종합하여
앞서 설명드린 운영위원회가 정한 규정에 따라서
아래와 같이 총 83개팀을 선발하게 되었습니다.
원래 예정한 75개팀에서 +8개의 팀의 추가된 상황입니다.

아쉽게 이번 본선에 진출하지 못한 모든 팀원에게는
위로의 말씀을 드리며, 다음 기회에는 더 좋은 성적으로
원하시는 것을 성취하시길 소망해 봅니다.

혹 본선진출팀으로 선발되었지만 팀내 사정으로 본선 참석이
어려운 경우에는 11월 11일까지 운영위원회에 알려주시기 바랍니다.
""",
"""
SW마에스트로 제15기 프로젝트 최종점검 안내 

프로젝트 최종점검이 이제 한달 앞으로 다가왔습니다.   

프로젝트 최종점검은 총 2회(1차 /2차) 진행 되는데, 1차 최종점검은 전체 팀(67팀) 대상으로 오는 11월 21일부터 23일까지 3일간 진행되며 2차 최종점검은 11월 27일 하루동안 1차 최종점검 분과별 상위 3개 팀(총 9개 팀)을 대상으로 실시 할 예정입니다. 

* 2차 최종점검(11.27(수)) 이후 개인평가 및 팀평가를 합산하여 제15기 우수자 선정 예정
프로젝트 최종점검은 연수생 종합 평가에서 비중이 가장 큰 평가 항목으로 지금까지 열심히 한만큼 조금만 더 힘내서 탄탄하게 준비해주시기 바라며 최종점검 관련 안내사항 꼼꼼히 숙지하여 주시기 바랍니다.  

 ★ 프로젝트 최종점검 안내 요약!

프로젝트 최종점검 : 11.21(목) ~ 11.23(토), 10:00 ~ 17:00
프로젝트 최종보고서 제출 마감 : ~11.18(월) 10:00
★ 멘토 의견은 연수생들이 최종보고서 작성완료 후 해당 보고서 내용을 검토하여 작성해 주시기 바랍니다.
연수센터 출입 제한 기간 : 11.20(수) 09:00 ~ 11.23(토) 20:00 / 평가 준비 및 운영
                                 11.26(화) 09:00 ~ 11.27(수) 20:00 / 2차 최종점검 운영
- 발표 및 결과물 시연 세팅 테스트 오픈 : 11.20(수) 14:00~16:00, 해당 시간은 출입 가능하며 자유롭게 시연 및 세팅 테스트 가능  
발표 순서는 분과 내 팀 간 협의 후 변경 가능(~11.7(목), 15:00)
발표 시간 15분 전까지 대기실(남자 휴게실)에 팀 전원 도착
발표자료(PPT or PDF) 및 노트북 준비 : 팀별 개인 노트북 연결 예정으로 발표자료가 저장된 노트북 (팀별 1대) 준비
발표 시간 팀당 40분(시연 포함 발표 15분, 질의응답 25분)
최종점검 보고서 미제출 및 최종점검 무단 불참하는 경우 경고 부여 예정
최종점검 관련 문의는 @사무국_김가영 / 02-6933-0712 / gykim@fkii.org / 사무국 방문
""",
"""
제15기 수료식 및 컨퍼런스 행사 안내

[행사 안내]
 일시 : 2024년 12월 12일(목) 13:00 - 19:30
 장소 : 양재 엘타워 6층 그레이스홀
 대상 : 제15기 연수생(필수), 엑스퍼트, 수료생, 멘토 등 참여 희망자
 내용 : 수료증 수여 및 참석자 네트워킹 등
 기타 : 점심(다과), 석식(코스요리), 기념품 제공
 문의 : 웹엑스 사무국_김상아, 02-6933-0701, ksa@fkii.org

응답조사(~11/7(목) 15시까지)
- 링크 : https://forms.gle/KsCQ5B2BrvsVTuPa8
모든 연수생 필수 응답(불참시 사유서 제출 필수)

안내사항
학업, 취업 등으로 바쁘시겠지만 15기 연수생 모두가 모여 축하하고 소회를 나누는 마지막 공식 행사이오니 가능한 함께해주시기를 부탁드립니다
""",
"""
https://item.gmarket.co.kr/Item?goodscode=3075536766
""",
"""
https://www.coupang.com/vp/products/8260813923?itemId=23797342510&vendorItemId=90821317205&sourceType=cmgoms&omsPageId=s45491&omsPageUrl=s45491&isAddedCart=
""",
"""
https://smartstore.naver.com/inflow/ep/gw?url=%2Finflow%2Fep%2Fdanawa%2Fproducts%2F9475469995&service_id=pcdn
""",
"""
민지 생일 3월 24일
""",
"""
다음 주 목요일 ICPC 본선
""",
"""
배진호 010 3817 2918
""",
"""
엄마 생일 7월 27일
아빠 생일 4월 10일
태식 생일 4월 11일
혜윤 생일 1월 2일
""",
"""
도커(Docker)는 컨테이너 기반 가상화 플랫폼으로, 응용 프로그램과 그 종속성을 격리된 환경인 컨테이너로 패키징하여 실행하는 기술이다. 이를 통해 응용 프로그램을 서로 다른 환경에서도 일관되게 실행할 수 있고, 개발 환경과 운영 환경 사이의 차이로 인한 문제를 줄일 수 있다. 도커 컨테이너는 가볍고 빠르며 확장성이 좋아서 개발 및 배포 프로세스를 간소화하는 데 사용된다.

*컨테이너 : 가상화 기술을 이용하여 어플리케이션과 개발 환경을 격리된 공간에서 실행하는 단위 

도커 컴포즈(Docker Compose)는 여러 개의 도커 컨테이너를 정의하고 실행하기 위한 도구로, 하나의 설정 파일로 여러 개의 컨테이너를 관리하고, 컨테이너 간의 네트워크 및 종속성을 설정하는 데 사용된다. 주로 복잡한 응용 프로그램이 여러 컴포넌트로 구성되어 있을 때 사용한다.
""",
"""
nth_element 는 first 부터 last 전 까지의 원소들을 부분적으로 정렬합니다. 이 때, 정렬하는 방식은 다음과 같습니다.

nth 가 가리키고 있는 원소는 first 부터 last 전 까지의 모든 원소들을 정렬하였을 때 자리할 원소로 바뀝니다.

새로운 nth 가 가리키고 있는 원소 앞에 오는 원소들은 nth 가 가리키는 원소 뒤에 오는 원소들보다 작거나 같습니다.

엄밀히 말하자면 모든 i∈[first,n) 와 j∈[n,last) 인 i, j 에 대해서 !(*j < * i) (혹은 comp(*j, *i) == false) 를 만족하게 해줍니다.

(1) 의 경우 operator< 를 통해 비교합니다.

(3) 의 경우 이항 함수인 comp 를 통해 비교합니다.

(2), (4) 의 경우 각각 (1), (3) 과 동일하지만, ExecutionPolicy 에 따라 연산을 수행합니다.

인자들
first, last : 원소들을 가리키는 반복자

nth : n 번째 위치를 가리키는 반복자

policy : 어떠한 ExecutionPolicy 를 사용할 것인지

comp : 두 원소를 비교할 함수 객체로 첫 번째 인자로 전달된 원소가 두 번째 인자로 전달된 원소 보다 작다면 true 를 리턴한다.

comp 함수는 아래와 같은 형태를 취해야 한다.

bool cmp(const Type1 &a, const Type2 &b);
참고로 comp 함수는 const& 로 인자를 꼭 받을 필요는 없지만, 전달된 원소들을 수정하면 안된다.
""",
"""
집현전 신입 부원 모집
안녕하세요. 집현전입니다!
집현전은
새롬관 5층 5클러스터에 자리 잡고 있는 42 서울의 도서관을 관리하는 동아리이자
카뎃이라면 누구나 언제든지 이용하실 수 있는 도서관입니다. :책:
집현전은 동아리 부원들이 자율적으로 운영해 나가고 있으며,
현재까지 장서 관리, 책 라벨링, 사서의 날 행사, 도서관 운영 웹서비스 및 동아리 친목 도모, 서비스 개발 등을 해왔습니다.
앞으로도 이러한 활동들을 집현전과 함께 진행하실 동료를 모집합니다 :미소짓는_얼굴:
(개발팀은 머지 않은 시기에 모집할 예정이니, 조금 더 기다려주시기 바랍니다!)
---
사서가 되면 좋은 점! :심박:
러너부터 멤버까지 개성 넘치는 사람들과 친목 형성
대출 가능 권수 추가 지원 (2권 -> 4권)
---
모집 기간 | 7/15~7/21
과정 | 구글폼 작성 -> 면접 -> 개별 발표
자세한 사항은 아래 링크를 참고해 주세요.
https://forms.gle/tQWfoA5kMnnbsCC97
기타 문의 사항은 
@hyeunkim
 으로 DM 부탁드립니다 :미소짓는_얼굴: (편집됨) 
""",
"""
[발표 관련 공지]

창업아이템 발표 내용
1. 창업아이템의 개요와 배경
2. 창업아이템 적용에 따른 목표고객
3. 창업아이템 사업화 방안
4. 향후 기대효과
순서로 한글파일이나 ppt로 5페이지 정도 작성하셔서 5분이내로 발표하시면 되겟습니다.
아이디어 차원이니 너무 부담갖지 않으셔도 됩니다.
""",
"""
https://n.news.naver.com/article/052/0002110771
""",
"""
https://n.news.naver.com/article/448/0000487665
""",
"""
Do you ever feel like a plastic bag
Drifting through the wind, wanting to start again?
Do you ever feel, feel so paper thin
Like a house of cards, one blow from cavin' in?
Do you ever feel already buried deep?
Six feet under screams, but no one seems to hear a thing
Do you know that there's still a chance for you?
'Cause there's a spark in you
You just gotta ignite the light
And let it shine
Just own the night
Like the Fourth of July
'Cause baby, you're a firework
Come on, show 'em what you're worth
Make 'em go, "Oh, oh, oh"
As you shoot across the sky
Baby, you're a firework
Come on, let your colors burst
Make 'em go, "Oh, oh, oh"
You're gonna leave 'em all in awe, awe, awe
You don't have to feel like a waste of space
You're original, cannot be replaced
If you only knew what the future holds
After a hurricane comes a rainbow
Maybe a reason why all the doors are closed
So you could open one that leads you to the perfect road
Like a lightning bolt, your heart will glow
And when it's time, you'll know
You just gotta ignite the light
And let it shine
Just own the night
Like the Fourth of July
'Cause baby, you're a firework
Come on, show 'em what you're worth
Make 'em go, "Oh, oh, oh"
As you shoot across the sky
Baby, you're a firework
Come on, let your colors burst
Make 'em go, "Oh, oh, oh"
You're gonna leave 'em all in awe, awe, awe
Boom, boom, boom
Even brighter than the moon, moon, moon
It's always been inside of you, you, you
And now it's time to let it through
'Cause baby, you're a firework
Come on, show 'em what you're worth
Make 'em go, "Oh, oh, oh"
As you shoot across the sky
Baby, you're a firework
Come on, let your colors burst
Make 'em go, "Oh, oh, oh"
You're gonna leave 'em all in awe, awe, awe
Boom, boom, boom
Even brighter than the moon, moon, moon
Boom, boom, boom
Even brighter than the moon, moon, moon
""",
"""
겨울이 가고 봄이 찾아오죠 우린 시들고
그리움 속에 맘이 멍들었죠

(I’m singing my blues)
파란 눈물에 파란 슬픔에 길들여져
(I’m singing my blues)
뜬구름에 날려보낸 사랑 oh oh

같은 하늘 다른 곳 너와나 위험하니까
너에게서 떠나주는 거야
님이란 글자에 점하나 비겁하지만
내가 못나 숨는 거야
잔인한 이별은 사랑의 말로
그 어떤 말도 위로 될 수는 없다고
아마 내 인생의 마지막 멜로
막이 내려오네요 이제

태어나서 널 만나고 죽을 만큼 사랑하고
파랗게 물들어 시린 내 마음
눈을 감아도 널 느낄 수 없잖아

겨울이 가고 봄이 찾아오죠 우린 시들고
그리움 속에 맘이 멍들었죠

(I’m singing my blues)
파란 눈물에 파란 슬픔에 길들여져
(I’m singing my blues)
뜬구름에 날려보낸 사랑 oh oh

심장이 멎은 것 만 같아 전쟁이 끝나고
그 곳에 얼어 붙은 너와나
내 머릿속 새겨진 Trauma 이 눈물 마르면
촉촉히 기억하리 내 사랑
괴롭지도 외롭지도 않아 행복은 다 혼잣말
그 이상에 복잡한 건 못 참아
대수롭지 아무렇지도 않아
별수없는 방황 사람들은 왔다 간다

태어나서 널 만나고 죽을 만큼 사랑하고
파랗게 물들어 시린 내 마음
너는 떠나도 난 그대로 있잖아

겨울이 가고 봄이 찾아오죠 우린 시들고
그리움 속에 맘이 멍들었죠

오늘도 파란 저 달빛아래에 나 홀로 잠이 들겠죠
꿈속에서도 난 그대를 찾아
헤매이며 이 노래를 불러요

(I’m singing my blues)
파란 눈물에 파란 슬픔에 길들여져
(I’m singing my blues)
뜬구름에 날려보낸 사랑 oh oh

(I’m singing my blues)
파란 눈물에 파란 슬픔에 길들여져
(I’m singing my blues)
뜬구름에 날려보낸 사랑 oh oh
""",
]

@pytest.mark.asyncio(loop_scope="session")
async def test_tags():
    tasks=[asyncio.create_task(send_request_and_validate()) for _ in range(1)]
    await asyncio.gather(*tasks)
    
async def send_request_and_validate():
  global contents
  for content in contents:
    tag_body=tag_basebody
    tag_body["raw_memos"][0]["content"]=content
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        res_tags=await client.post("/memo/tags", json=tag_body)
        
    assert res_tags.status_code==200
    res_model: Res_post_memo_tags=Res_post_memo_tags.model_validate(res_tags.json())
    
    ###
    
    structure_body=structure_basebody
    structure_body["memos"][0]["content"]=content
    structure_body["memos"][0]["tags"]=[{"id": tag.id, "name": tag.name, "is_new": tag.is_new} for tag in res_model.tags[0]]
    
    print(structure_body)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        res_structures=await client.post("/memo/structures", json=structure_body)
    
    assert res_structures.status_code==200

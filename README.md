# 법률, 판례 정보를 가진 대화형 AI, Lawyerty

**사용한 생성형 AI** : gpt-3.5-turbo  
**사용한 언어** : Python  
**사용한 데이터셋** : 판례 데이터(출처: 국가법령정보 공동활용)  
  
<br/><br/>
## GPT에게 법률 및 판례 관련 정보 학습시키기  
**1) GPT 파인튜닝**  
openai를 이용하기 때문에 설치를 하고, 아래 이미지와 같이 gpt에게 학습시킬 질문과 이에 따른 답변을 적은 json데이터를 만든다.  
```
pip install openai
```
<img width="957" alt="lawdata" src="https://github.com/custom-LawGPT/lawyerty/assets/150711075/c6bcb170-c8d5-46b8-a5e0-94514f7950f3">  
첨부한 파이썬 코드를 참고하면, 위 이미지처럼 만든 데이터셋을 gpt에게 학습시킬 jsonl형식의 파일로 업로드하여, 학습을 진행할 수 있다. 이 때 openai에서 API키를 꼭 발급받은 뒤, 사용하길 바란다.  

<br/><br/>

**2) 학습한 gpt 사용하기**  
```
from openai import OpenAI
client = OpenAI(
    api_key = "Your OpenAI API Key"
)

completion = client.chat.completions.create(
  model="ft:gpt-3.5-turbo로 시작하는 모델 이름 넣기",
  messages=[
    {"role": "system", "content": "당신만의 AI 법률 상담가, Lawyerty입니다. 무엇을 도와드릴까요?"},
    {"role": "user", "content": "질문하고 싶은 내용 or 'input()'함수를 이용하여 직접 질문을 작성"}
  ]
)
print(completion.choices[0].message.content)
```
- 약 <>가지의 질문 및 답변을 학습시켰으며, 결과는 아래와 같다.  

[여기 추가해야 할 부분]

<br/><br/>  

---
**부록) 국가법령정보 공동활용 API활용**  
판례 본문 데이터를 다운받아, 자동적으로 json파일로 변환하는 것을 시도해 보려고 국가법령정보의 API를 활용하여 판례를 크롤링하는 과정이다.  
사이트에서 로그인 후, API신청 시에 자신의 서버장비의 IP주소를 꼭 추가해서 신청하면 1~2일 후엔 승인이 되어 API를 사용할 수 있게 된다. 아래는 IP주소를 확인하는 방법이다. 터미널에 입력하면 IP주소를 얻을 수 있다.
```
curl ifconfig.me
```
승인이 났다면 사이트의 API활용 가이드를 통해 자신이 얻고자 하는 데이터에 대한 API를 이용할 수 있게 될 것이다. 이번에는 판례 데이터가 필요하기 때문에 판례본문을 검색하는 API예시는 아래와 같다.  
OC={아이디} 부분의 아이디는 사이트에 로그인했을 때 사용했던 ID의 도메인 부분이다. ex) ID가 test@gmail.com 일 때, 아래 코드에 작성할 아이디는 **test**가 된다.  
```
# 판례 목록
http://www.law.go.kr/DRF/lawService.do?OC={아이디}&target=prec

# 판례 일련번호가 112233인 판례 HTML 조회
http://www.law.go.kr/DRF/lawService.do?OC={아이디}&target=prec&ID=112233&type=HTML
```
첨부한 파이썬 코드를 참고하면, 판례 본문 데이터를 다운받을 수 있을 것이다.  
아래는 데이터 구성 내용이다.  
```
data
├── 판례                  
│   ├── 참조조문(.txt파일) 
|   ├── 참조판례(.txt파일) 
│   ├── 판결요지(.txt파일) 
│   ├── 판례내용(.txt파일)       
│   └── 판시사항(.txt파일) 
```
각 폴더별로 텍스트 파일 양이 많기 때문에 하나로 통합시킨다.  
```
import os

def merge_text_files(folder_path, output_file):
    # 주어진 폴더 내의 모든 텍스트 파일 목록을 가져옴
    text_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]

    # 텍스트 파일들을 하나의 파일로 통합
    with open(output_file, 'w') as merged_file:
        for text_file in text_files:
            with open(os.path.join(folder_path, text_file), 'r') as file:
                content = file.read()
                merged_file.write(content + '\n\n')  # 파일 내용을 작성하고, 파일 사이에 공백 라인을 추가

# 사용 예시
folder_path = './path/판례/통합할 폴더명 예)판시사항'  # 통합할 폴더 경로
output_file = './path/판례/통합한 뒤 파일명 예)판시사항.txt'  # 통합될 파일 경로
merge_text_files(folder_path, output_file)
```
현재 통합된 텍스트 파일을 gpt에 학습시키기 위해 알맞는 파일 형식인 jsonl형식으로 변환하는 방법을 알아보는 중에 있습니다. (추후 업데이트 예정)  


<br/><br/>

## 참고 자료
[국가법령정보 공동활용](https://open.law.go.kr/LSO/main.do)  
[국가법령정보 API 사용법](https://flyingsquirrel.tistory.com/33)  
[GPT 3.5 파인튜닝으로 커스텀 언어모델 만들기](https://www.youtube.com/watch?v=WsMB0hOEosI)  

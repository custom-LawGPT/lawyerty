# 법률, 판례 정보를 가진 대화형 AI Law-gpt

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



<br/><br/>  

---
**부록) 국가법령정보 공동활용 API활용**  
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
http://www.law.go.kr/DRF/lawService.do?OC=test&target=prec&ID=112233&type=HTML
```

import os
import openai
import json

# 예시 데이터셋(최소 10개 필요)
dataset = {
    "train": [
        {
    "question":"폭언으로 직장 내 괴롭힘을 당하고 있는데 관련된 판례 알려줘",
    "answer": "사건번호 : 22가단241657\n\n[민사] 직장 상사의 폭언 등을 '직장 내 괴롭힘'으로 인정하여 정신적 손해배상책임을 인정한 사례\n\n같은 회사에서 근무하던 직장 상사의 폭언과 욕설 행위 등이 원고의 인격권을 침해하는 불법행위에 해당한다고 판단하여 위자료 700만 원을 인정(위 불법행위와 치료비 및 일실수입 사이의 인과관계는 부정). 다만 일부 행위(다른 직원을 불러 갈등을 이야기하거나 핀잔을 준 행위 등)에 대해서는 불리한 처우 또는 적정한 수준을 넘는 행위로 판단하지 아니함"
    },
    {
    "question":"질문",
    "answer": "답변"
    }
    ]
}

# 학습 데이터 jsonl 형태로 생성 및 저장
list_message = []
num_data = len(dataset["train"])

for i in range(num_data):
    question = dataset["train"][i]["question"]
    answer = dataset["train"][i]["answer"]
    print("질문: ",question)
    print("답변",answer)
    message = [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ]
    list_message.append(message)

with open("output1.jsonl", "w") as file:
    for messages in list_message:
        json_line = json.dumps({"messages": messages})
        file.write(json_line + '\n')
        

# jsonl파일 업로드
from openai import OpenAI
client = OpenAI(
    api_key = "{Your OpenAI API key}"
)

upload_file = client.files.create(
  file=open("./path/output1.jsonl", "rb"),
  purpose="fine-tune"
)

# 모델 학습
# upload_file을 print하면 나오는 id를 training_file에 입력
start_train = client.fine_tuning.jobs.create(
  training_file='upload_file의 ID부분 입력', 
  model="gpt-3.5-turbo-1106"
)

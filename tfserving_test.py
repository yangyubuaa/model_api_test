### 直接测试tfserving的并发性能
import time
import requests
from concurrent import futures
from transformers import BertTokenizer
from tqdm import tqdm


def test(keywordList):
    t_token = time.time()
    tokenizer = BertTokenizer.from_pretrained("albert-tiny-chinese")
    tokenized = tokenizer(keywordList, max_length=64, truncation=True, padding="max_length")
    # print(tokenized)
    t_token_end = time.time()
    print("token用时{}".format(t_token_end-t_token))
    input_ids = tokenized["input_ids"]
    token_type_ids = tokenized["token_type_ids"]
    attention_mask = tokenized["attention_mask"]
    headers = {'content-type': 'application/json'}
    # 行格式
    data = {
        # "signature_name": "call",
        "instances":
            [
                {"token_type_ids": token_type_ids[0],
                 "attention_mask": attention_mask[0],
                 "input_ids": input_ids[0]},
            ]

    }
    for i in range(1, len(input_ids)):
        data["instances"].append({"token_type_ids": token_type_ids[i],
                                  "attention_mask": attention_mask[i],
                                  "input_ids": input_ids[i]})

    url = "http://10.160.35.122:8510/v1/models/latency_test_model/versions/1:predict"
    t_post = time.time()
    r = requests.post(url, json=data, headers=headers)
    t_post_end = time.time()
    print("请求用时{}".format(t_post_end-t_post))
    # print(r.text)
    return r.text


if __name__ == '__main__':
    keywordList = list()
    for i in range(50):
        keywordList.append("今天天气怎么样")
    MAX_WORKERS = 240

    with futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
        todo = []
        t1 = time.time()
        for i in range(240):
            future = executor.submit(test, keywordList)
            todo.append(future)
        for future in tqdm(futures.as_completed(todo)):
            result = future.result()
        t2 = time.time()
        print(t2-t1)
    # test(keywordList)

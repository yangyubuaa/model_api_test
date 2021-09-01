from concurrent import futures
import path
from tqdm import tqdm
import requests


def request_once():
    params = {"requestId": "id1",
              "contentType": 1,
              "data": {
                  "contents": [
                  ]
              }
              }
    for i in range(50):
        params["data"]["contents"].append({
            "content": "关键词1",
            "indust": 100010,
            "acctId": 8696900
        })
    headers = {'content-type': 'application/json'}

    url = "http://10.160.35.122:8000/indus-cls-api/indus"
    import time
    t1 = time.time()
    r = requests.post(url, json=params, headers=headers)
    t2 = time.time()
    print(t2-t1)
    print(r.text)
    return r.text


def test():
    # 模拟240个人同时发起请求
    MAX_WORKERS = 240

    with futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
        todo = []
        # 模拟1000次请求
        for i in range(10000):
            future = executor.submit(request_once)
            todo.append(future)
        for future in tqdm(futures.as_completed(todo)):
            result = future.result()
            # print(result)


if __name__ == '__main__':
    test()

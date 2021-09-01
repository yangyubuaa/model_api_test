import requests
import json
if __name__ == '__main__':

    params = {"requestId": "id1",
              "contentType": 1,
              "data": {
                    "contents": [
                        {
                            "content": "关键词1",
                            "indust": 100010,
                            "acctId": 8696900
                        },
                        {
                            "content": "关键词2",
                            "indust": 100010,
                            "acctId": 8696900
                        }
                    ]
                }
    }
    for i in range(198):
        params["data"]["contents"].append({
                            "content": "关键词1",
                            "indust": 100010,
                            "acctId": 8696900
                        })
    headers = {'content-type': 'application/json'}

    url = "http://10.160.35.116:8000/indus-cls-api/indus"
    import time
    t1 = time.time()
    r = requests.post(url, json=params, headers=headers)
    t2 = time.time()
    print(t2-t1)
    print(r.text)

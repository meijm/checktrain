import requests
import json


def main():
        
    url = "https://aip.baidubce.com/rpc/2.0/ernievilg/v1/getImg?access_token=24.c2bd7648a8f8338752ff48c3f3e397cc.2592000.1682834210.282335-31851845"
    
    payload = json.dumps({
        "taskId": "15043694"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

if __name__ == '__main__':
    main()

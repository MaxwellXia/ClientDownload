import sys
import requests
import os
import json

# 屏蔽warning信息
requests.packages.urllib3.disable_warnings()


def download(url, file_path):
    headers = {
        "Host": "youpin.mi.com",
        "Content-Type": "application/json",
        "Referer": "http://192.168.128.29/",  # 必须带这个参数，不然会报错
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Range":"0-1024",
             }
    url = "http://localhost:18080/client"

    # 第一次请求是为了得到文件总大小
   # data = {'getlen'}
   # data=urllib.urlencode(values)
   # r1 = requests.get(url, stream=True, verify=False)
    #total_size = int(r1.headers['Content-Length'])

    #登录
    pyload = {"Head":"Login","UserID":"12345678","Password":"12345678"}
    response = requests.post(url, data=json.dumps(pyload), headers=headers).text
    res = json.loads(response)

    #获取文件列表
    pyload = {"Head":"GetFrameList","SessionID":res['SessionID'],"FirmwareKind":"LiftTable","FirmwareVersion":"V1"}
    response = requests.post(url, data=json.dumps(pyload), headers=headers).text
    res2 = json.loads(response)

    #下载文件
    pyload = {"Head":"GetFrame","SessionID":res['SessionID'],"URL":res2[2]['URL']}
    r = requests.post(url, data=json.dumps(pyload), headers=headers)
    filename = res2[2]['FrameName']

    with open(file_path + '\\' + filename, "ab") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()


    pyload = {"Head":"getleanth"}
    response = requests.post(url, data=json.dumps(pyload), headers=headers).text
    size = json.loads(response)["size"]

    # 这重要了，先看看本地文件下载了多少
    if os.path.exists(file_path):
        temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
    else:
        temp_size = 0

    #while(temp_size != total_size):
        # 显示一下下载了多少   
        print(temp_size)
        print(total_size)
        # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
        headers = {'Range': 'bytes=%d-' % temp_size}  
        # 重新请求网址，加入新的请求头的
        r = requests.get(url, stream=True, verify=False, headers=headers)

        # 下面写入文件也要注意，看到"ab"了吗？
        # "ab"表示追加形式写入文件
        with open(file_path, "ab") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()

                    ###这是下载实现进度显示####
                    done = int(50 * temp_size / total_size)
                    sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                    sys.stdout.flush()
    print()  # 避免上面\r 回车符


if __name__ == '__main__':
    link = r'http://localhost:18080/reg'
    UUID = r'2a4a3044-0b1a-4722-83ed-43ba5d6d25b0'
    path = r'./DownLoad'
    url = link #os.path.join(link, UUID)
    # 调用一下函数试试
    download(url, path)
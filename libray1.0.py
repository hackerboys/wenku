# encoding:utf-8
import requests
from bs4 import BeautifulSoup
import os
"""

功能说明：
    获取文库URL，保存为 txt , 然用第三方下载工具，下载文库。

使用说明：
    用Pycharm 打开软件，然后右键index.py文件 点击 open in terminal ,然后pycharm会跳出控制台模式。
    1. 安装 pyinstaller,lxml,requests,bs4。pycharm安装了，不代表控制台环境安装了，如果不安装会出现闪退。
    
        pip install pyinstaller
        pip install lxml
        pip install requests
        pip install bs4
    
    2.然后执行控制台输入：pyinstaller -F index.py (index.py，尽量写相对路径 比如：D:/xxx/xxx/index.py )
        相对目录案列：
            pyinstaller -F D:/xxx/xxx/index.py
"""

if os.path.isfile("DownUrl.txt"):
    while True:
        file = input("已经检测到当前目录存在Downurl.txt文件，是否删除（y/n）：")
        if file == "y" or file == "Y":
            os.remove('DownUrl.txt')
            break
        elif file == "N" or file == "n":
            pass
            break
        else:
            print("输入有误，请重新输入!")

while True:

    keystr = str(input("请输入你需要的资料的关键词【回车】："))
    print("")
    if keystr != "":
        break
    else:
        pass


while True:
    try:
        pagenumber = int(input("请输入需要多少页【回车开始爬取】："))
        break
    except:
        print("请输入数字")


url_list = []

def baiduwenku():
    """
    百度文库找资料
    :return:
    """
    headers = {
        "Cookie": "BIDUPSID=3F34CA36A5D876E62AF7D294FAB5E36D; PSTM=1604331526; BAIDUID=3F34CA36A5D876E69989DD1C07D32068:FG=1; _click_param_reader_query_ab=-1; _click_param_pc_rec_doc_2017_testid=3; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=o1S25nNUMxelZVTVNhSTJ1V05hbWF3RG5DZWF4QXVaSX5EZ3RIdGV0Zm9XUDFmRVFBQUFBJCQAAAAAAAAAAAEAAAAPJXtzeW~JtdPWtPTT1rfo8bIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOjL1V~oy9VfQl; BDUSS_BFESS=o1S25nNUMxelZVTVNhSTJ1V05hbWF3RG5DZWF4QXVaSX5EZ3RIdGV0Zm9XUDFmRVFBQUFBJCQAAAAAAAAAAAEAAAAPJXtzeW~JtdPWtPTT1rfo8bIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOjL1V~oy9VfQl; Hm_lvt_d8bfb560f8d03bbefc9bdecafc4a4bf6=1606927015,1606997933,1607426860,1607928330; delPer=0; PSINO=6; BAIDUID_BFESS=3F34CA36A5D876E69989DD1C07D32068:FG=1; murmur=undefined--Win32; Hm_lvt_f06186a102b11eb5f7bcfeeab8d86b34=1606273272,1606938085,1607426860,1607929538; isJiaoyuVip=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=1454_33224_33060_31660_32973_33098_33100_33218_33199_33148_33265; BA_HECTOR=aha5048k8h212ka53g1fte44i0q; BCLID=7125724943647939514; BDSFRCVID=xbFOJexroG3_7c3rcT9fuiKhqLWYvd6TDYLEMU5h7wgNoS_VJeC6EG0Pts1-dEu-EHtdogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJIJ_ID2JCD3enTmbt__-P4DenonaMRZ5mAqofopb4TZH4on0RjC5tFUMhLHL5KJ-KonaIQqaM5KMIjT0lo8yUJQ2tje5qR43bRTWhCy5KJvfJ_lQMcMhP-UyPvLWh37LI3lMKoaMp78jR093JO4y4Ldj4oxJpOJ5JbMonLafD_hMK06j5L-ePvH5UQXKPRt264X3b7Ef5C28h7_bf--DlTXjHofBJj2fCoyLRTc2PD5hK3p5jjxy5K_hPOA2RTeBI573KDEblvHED5HQT3m3lQbbN3i34DDQenDWb3cWhRV8UbS0-RPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JD-50eG-Dt6DqJnk8V-OO5tbfDP3kqR6ohKCShUFX5-CsKaIO2hcH0KLKMMOj5PL-K4tPMh3taxn3-Rrq5JT_QUb1MRjv2tcMDb_ObhjfQnQCbn7x_h5TtUJ4JKnTDMRh-x-_K4ryKMniBIj9-pnx2hQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuD68Me5J3DHLs-bbfHj73B4JVatcsfJjkMboHhCCShGR2LKr9WDTm_DoyXMjIfMo4-UrahRLtyU7DJJc7tavq-pPKKR7ieJRNLpJFhxFN0UIJa6Ft3mkjbpbzfn02OP5PXqJG5t4syPRr2xRnWNRWKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCFabP3Nh4Rhq4D_MfOtetJyaR3O3qQvWJ5WqR7jDpPb-TtX-n88KJQ0WKbD2U3wbJ--ShbXXMoY3jLJjpJMWtRgXacZ0l8K3l02V-bRDDcfQJQDQt7JKPRMW20j0h7mWIQvsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjj6jK4JKDGDqtj3P; ab_sr=1.0.0_MzM1ZTczOTA4OTE0NjgzZDI4MTA1OWM4NjRkNmM5ZTlkZmQ5ZGE2ZjU5YTJiZTllNTNlMDZmM2MzMGE0NTE0NzU4YTJkYzcxNWNjYTQ4OWM0OGZlZTFhYWUxMmU3ZWNiZGYwOTViMzYzM2NmODk0YWE5NDM4YzJkZmM1M2IyOGE=; bcat=81d8ebe8721b1ba954b6c650ce9b6cce8a61f4a61f638cdb7f1d51dbac549e5590aa2ec2ee738f82b31ae78fdfc66238731b83cb848a9bd4054dc69632c9a8f88ce5259a246a3b2f6b9e2f3288980146639e492dc71edcbe5035a39ddeac6af9426a6266193f3e4a9fe9f9bb8206f923eb330448e49aced59935cb234b86d558; ___wk_scode_token=q3%2BoNZaM0CHhV84kFQAHNAzaUGMjQqTsi%2FdwAUnBIbU%3D; Hm_lpvt_f06186a102b11eb5f7bcfeeab8d86b34=1607930181; Hm_lpvt_d8bfb560f8d03bbefc9bdecafc4a4bf6=1607930181; session_id=1607930181810; session_name=",
        "Host": "wenku.baidu.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    for i in range(0, pagenumber * 10, 10):
        url = "https://wenku.baidu.com/search?word={}CC&org=0&fd=0&lm=0&od=0&ie=gbk&pt=1&pn={}".format(keystr, i)
        respon = requests.get(url, headers=headers)
        html = BeautifulSoup(respon.content, 'lxml')
        p_title = html.find_all('p', class_='fl')
        for p in p_title:
            ahref = p.find_all('a')[0]['href']
            data_url = str(ahref).split('-i')[0]
            # print(data_url)
            url_list.append(data_url)

def docinwenku():
    """
    豆丁网

    :return:
    """
    headers = {

        "Cookie": 'mobilefirsttip=tip; docin_session_id=ad7cbc92-4ad2-45ca-a9e1-9025818d8d4f; refererfunction=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DCmatHecwbgN6e-McPTrY8k7V9y-Ga1Lz5KCiUSePCd3%26wd%3D%26eqid%3Df640b6d5000c8531000000065fd720e6; cookie_id=C92C90B793800001E1721FBF25001474; time_id=2020121416237; userchoose=usertags172_999_171_170_169_102_104_165_129_105_; _ga=GA1.2.1550783635.1607934188; _gid=GA1.2.471687866.1607934188; jumpIn=400; saveFinProductToCookieValue=2164571821; netfunction="/search.do"; JSESSIONID=EFB3D1E385F921DDA591C87D94E4D279-n1; remindClickId=-1; _gat=1',
        "Host": "www.docin.com",
        "Referer": "https://www.docin.com/search.do?nkey=%E6%96%B0%E9%9B%B6%E5%94%AE&searchcat=1001&fnorePage=&currentPage=2",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",

    }
    for i in range(0,pagenumber):
        url = "https://www.docin.com/search.do?nkey={}&searchcat=1001&fnorePage=&currentPage={}".format(keystr,i)
        respon = requests.get(url, headers=headers)
        html = BeautifulSoup(respon.content, 'lxml')
        dd = html.find_all('dd',class_='fc-baidu title')

        for d in dd:
            # print(d.find_all('a'))
            'https://www.docin.com/p-6969952.html'
            ahref = d.find_all('a')[0]['href']
            data_url = "https://www.docin.com"+ahref
            # print(data_url)
            url_list.append(data_url)


def mbalib():
    """
    MBA智库

    :return:
    """
    headers = {

    "Cookie": "__gads=ID=32f882cb9895e4eb-22e2e50bc3c4008c:T=1605626096:RT=1605626096:S=ALNI_MaM3WfQtA3svRaFSOSkOuveGe1cLQ; wikidb_session=nigih16f8vj7v01grlo4k69tr5; BAIDU_SSP_lcr=https://www.baidu.com/link?url=57aywD0Q6WTnl7XKbIHuEvz4Rnt7SJXZXk9q-sqR5DUG1AAe_KDPd_QC5wT2HK2R&wd=&eqid=fbfabcd000002a95000000065fd72710; Hm_lvt_9cafc024a7b2920462df19fb7150d4b9=1607935765; wikidbAccessToken=eyJ1c2VybmFtZSI6Ik1faWRfYWI2Njg1MWE2ZDllMDYyOGRiOTgwM2FmOTZhOWY3OTYiLCJ0aW1lIjoxNjA3NDI0NjUxLCJrZXkiOiIxZmYxODM2NWYxYzZjZTFjMGE2OTAwYmNjYTY5ODBhYiJ9; Hm_lpvt_9cafc024a7b2920462df19fb7150d4b9=1607939252",
    "Host": "www.mbalib.com",
    "Referer": "https://www.mbalib.com/s?q=%E9%9B%B6%E5%94%AE&pn=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"


    }
    for i in range(0, pagenumber):
        url = "https://www.mbalib.com/s?q={}&pn={}".format(keystr,i)
        respon = requests.get(url,headers=headers)
        html = BeautifulSoup(respon.content,'lxml')
        h3 = html.find_all('h3',class_='h3url')
        for h in h3:
            ahref = h.find_all('a')[0]['href']
            url_list.append(ahref)


def saveurl():
    urldata = list(set(url_list))

    for u in urldata:
        with open('DownUrl.txt', 'a+', encoding='utf-8') as f:
            f.write(f"{u}\n")
            f.close()

    print("")
    print("**********************************")
    print("")
    print(f"一共获取到 {len(urldata)} 个数据URL")
    print("")
    print("**********************************")
    print("")

def mains():

    baiduwenku()
    docinwenku()
    mbalib()
    saveurl()

if __name__ == '__main__':
    mains()
    input("下载URL已经写入downUrl文本中【回车结束】：")

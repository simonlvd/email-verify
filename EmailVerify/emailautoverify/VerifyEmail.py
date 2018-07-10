# !/Users/simon/anaconda3/bin/python
# coding = utf-8
import imaplib
import re
import email
import pandas as pd
import xlrd
from xlutils.copy import copy
import requests
from bs4 import BeautifulSoup


def read_excel():
    data = pd.read_excel(r'邮箱.xlsx')
    return data


def writ_add_to_excel(username, userpsd):
    rexcel = xlrd.open_workbook(r"需手动设置imap.xls")  # 用wlrd提供的方法读取一个excel文件
    row = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
    table.write(row, 0, username)  # xlwt对象的写方法，参数分别是行、列、值
    table.write(row, 1, userpsd)
    excel.save(r"需手动设置imap.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel


# def parseEmail(msg):
#     # sub = msg.get('subject')
#     body = []
#     for part in msg.walk():
#         # 如果ture的话内容是没用的
#         if not part.is_multipart():
#             body.append(part.get_payload(decode=True).decode('utf-8'))
#             # 解码出文本内容，直接输出来就可以了。
#     # return {"sub": sub, "body": " ".join(body)}
#     return {"body": " ".join(body)}


def get_Url(content,type):
    text = BeautifulSoup(content, 'lxml')
    urls = text.findAll('a')
    if type == 0:
        pattern = re.compile(r"https://www\.coinex\.com/my/wallet/withdraw/confirm.*")
    elif type == 1:
        # pattern = re.compile(r"https://www\.coinex\.com/my/wallet/withdraw/confirm.*")
        pass
    for u in urls:
        # print(u['href'])
        match = pattern.match(u['href'])
        if match:
            print(match.group())
            urlGet(match.group())
        # else:
        #     print('暂无需求')
        # print(u)


def urlGet(url):
    try:
        response = requests.get(url)
        print('请求成功:', response)
    except BaseException:
        print('请求失败')


def Verify_Emai(Email,Password):
    ret = ''
    needmail = ['CoinEx <noreply@news.coinex.com>']
    try:
        M = imaplib.IMAP4_SSL('imap.mail.yahoo.com')
        ret = M.login(Email, Password)
    except BaseException:
        print('login fail')
        writ_add_to_excel(Email, Password)
    retR = re.compile('^\(\'OK')
    if (retR.match(str(ret))):
        print("login succeed!")
        M.select('INBOX')
        typ, data = M.search(None, 'UnSeen')
        # type, data = M.search(None, 'RECENT')
        # typ, data = M.search(None, 'All')

        # print(data)
        newlist = data[0].split()
        if newlist is not None:
            for i in range(0, len(newlist)):
                typ1, data1 = M.fetch(newlist[i], '(RFC822)')
                msg = email.message_from_string(data1[0][1].decode('utf-8'))
                sub = msg.get('from')
                print(sub)
                if sub in needmail:
                    body = []
                    for part in msg.walk():
                        # 如果ture的话内容是没用的
                        if not part.is_multipart():
                            body.append(part.get_payload(decode=True).decode('utf-8'))
                            # 解码出文本内容，直接输出来就可以了。
                    res = {"body": " ".join(body)}
                    get_Url(content=res['body'],type=needmail.index(sub))
        M.logout()

def Test_all_mail(Email, Password):
    ret = ''
    try:
        M = imaplib.IMAP4_SSL('imap.mail.yahoo.com')
        ret = M.login(Email, Password)
    except BaseException:
        print('login fail')
        writ_add_to_excel(Email, Password)
    retR = re.compile('^\(\'OK')
    if(retR.match(str(ret))):
        print("login succeed!")
        M.select('INBOX')
        typ, data = M.search(None, 'All')
        # type, data = M.search(None, 'UnSeen')
        # type, data = M.search(None, 'RECENT')
        print(data)
        newlist = data[0].split()
        if newlist is not None:
            for i in range(0, len(newlist)):
                typ1, dat1 = M.fetch(newlist[i], '(RFC822)')
                msg = email.message_from_string(dat1[0][1].decode('utf-8'))
                # sub = msg.get('subject')
                sub = msg.get('from')
                if sub:
                    print(sub)
                    body = []
                    for part in msg.walk():
                        # 如果ture的话内容是没用的
                        if not part.is_multipart():
                            body.append(part.get_payload(decode=True).decode('utf-8'))
                        # 解码出文本内容，直接输出来就可以了。
                    res = {"body": " ".join(body)}
                    get_Url(content=res['body'],type=0)



def main():
    data = read_excel()
    for indexs in data.index:
        print(data.loc[indexs][0])
        username = data.loc[indexs][0]
        userpsd = data.loc[indexs][1]
        Test_all_mail(username, userpsd)

#
# if __name__ == '__main__':
#     main()


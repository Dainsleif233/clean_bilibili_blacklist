import time
import requests
from urllib.parse import unquote
from rev import reverse

# Cookie
cookie = ""
# 请求间隔(s)
times = 2

def encodeCookies(cookie):
    cookies = {}
    for item in cookie.split('; '):
        key, value = item.strip().split('=', 1)
        cookies[key] = unquote(value)
    return cookies

def getSession(cookies):
    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update({
        'User-Agent': 'SysHub'
    })
    return session

def login(session):
    login = session.get("https://api.bilibili.com/x/web-interface/nav")
    if login.status_code != 200:
        print(login.text)
    time.sleep(times)
    print("登录状态验证：", login.json().get('data', {}).get('isLogin'))

def getBlacklist(removeList, page):
    response = session.get(f"https://api.bilibili.com/x/relation/blacks?ps=50&pn={page}")
    if response.status_code != 200:
        print(response.text)
    time.sleep(times)
    blackList = response.json().get('data', {}).get('list', [])
    total = response.json().get('data', {}).get('total')
    for item in blackList:
        mid = item.get('mid')
        uname = item.get('uname')
        if uname == '账号已注销':
            removeList.append(mid)
            print("----------------------")
            print("用户名：账号已注销")
            print(f"UID：{mid}")
            continue
        signed_params = reverse(0, mid)
        info = session.get("https://api.bilibili.com/x/space/wbi/acc/info", params=signed_params)
        if info.status_code != 200:
            print(info.text)
        time.sleep(times)
        if info.json().get('data', {}).get('silence') == 1:
            removeList.append(mid)
            print("----------------------")
            print(f"用户名：{uname}")
            print(f"UID：{mid}")
    return removeList, total

def getRemoveList():
    page = 1
    total = 0
    removeList = []
    while page <= total // 50 + 1:
        removeList, total = getBlacklist(removeList, page)
        page += 1
    return removeList

def clean(removeList):
    print("----------------------")
    print("开始清理黑名单")
    csrf = cookies.get('bili_jct')
    for mid in removeList:
        response = session.post("https://api.bilibili.com/x/relation/modify", data={"fid": mid, "csrf": csrf, "act": 6})
        if response.status_code != 200:
            print(response.text)
        print(f"已清理UID:{mid}")
        time.sleep(times)
    print("----------------------")
    print(f"成功清理{removeList.__len__()}项黑名单")

if  __name__ == '__main__':
    cookies = encodeCookies(cookie)
    session = getSession(cookies)
    login(session)
    removeList = getRemoveList()
    clean(removeList)
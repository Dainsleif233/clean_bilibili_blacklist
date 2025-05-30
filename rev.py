# https://github.com/afterexam/bilibili_up_video_info/blob/master/rev.py
from functools import reduce
from typing import Tuple
from hashlib import md5
import urllib.parse
import time
import requests

mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]

def getMixinKey(orig: str):
    '对 imgKey 和 subKey 进行字符顺序打乱编码'
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

def encWbi(params: dict, img_key: str, sub_key: str):
    '为请求参数进行 wbi 签名'
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time                                   # 添加 wts 字段
    params = dict(sorted(params.items()))                       # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k : ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v
        in params.items()
    }
    query = urllib.parse.urlencode(params)                      # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()    # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params

def getWbiKeys() -> Tuple[str, str]:
    '获取最新的 img_key 和 sub_key'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.bilibili.com/'
    }
    resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=headers)
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return img_key, sub_key


def reverse(page,mid):
    img_key, sub_key = getWbiKeys()
    # from req import params
    signed_params = encWbi(
        params={
        "pn": page,
        "ps": 40,
        "tid": 0,
        "special_type": "",
        "order": "pubdate",
        "mid": mid ,
        "index": 0,
        "keyword": "",
        "order_avoided": "true",
        "platform": "web",
        "web_location": "333.1387",

        "dm_img_list": r'[{"x":2064,"y":521,"z":0,"timestamp":7055,"k":62,"type":0},{"x":872,"y":-1858,"z":69,"timestamp":7162,"k":103,"type":0},{"x":1727,"y":-1180,"z":98,"timestamp":8025,"k":119,"type":0},{"x":2294,"y":-593,"z":214,"timestamp":8125,"k":92,"type":0},{"x":2203,"y":-705,"z":163,"timestamp":8225,"k":109,"type":0},{"x":2047,"y":-866,"z":22,"timestamp":8326,"k":109,"type":0},{"x":2566,"y":-347,"z":541,"timestamp":8425,"k":74,"type":0},{"x":2690,"y":-226,"z":674,"timestamp":8568,"k":80,"type":0},{"x":2187,"y":-713,"z":192,"timestamp":8671,"k":112,"type":0},{"x":2691,"y":-204,"z":704,"timestamp":8772,"k":60,"type":0},{"x":2313,"y":-494,"z":384,"timestamp":8872,"k":114,"type":0},{"x":2571,"y":725,"z":1117,"timestamp":8973,"k":99,"type":0},{"x":1351,"y":-51,"z":83,"timestamp":9073,"k":118,"type":0},{"x":1501,"y":283,"z":302,"timestamp":9173,"k":65,"type":0},{"x":2118,"y":914,"z":923,"timestamp":9275,"k":122,"type":0},{"x":1522,"y":271,"z":307,"timestamp":9375,"k":65,"type":0},{"x":3033,"y":1738,"z":1766,"timestamp":9475,"k":126,"type":0},{"x":2334,"y":1392,"z":399,"timestamp":9576,"k":80,"type":0},{"x":3496,"y":2796,"z":1617,"timestamp":11401,"k":115,"type":0},{"x":2147,"y":974,"z":882,"timestamp":11502,"k":69,"type":0},{"x":3155,"y":1968,"z":1886,"timestamp":11603,"k":89,"type":0},{"x":2771,"y":1540,"z":1473,"timestamp":11703,"k":96,"type":0},{"x":1758,"y":528,"z":457,"timestamp":11810,"k":100,"type":0},{"x":2508,"y":1278,"z":1207,"timestamp":11932,"k":108,"type":0},{"x":2959,"y":1729,"z":1658,"timestamp":12033,"k":63,"type":1}]',
        "dm_img_str": "V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
        "dm_cover_img_str": "QU5HTEUgKEFNRCwgQU1EIFJhZGVvbihUTSkgR3JhcGhpY3MgKDB4MDAwMDE2MzgpIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpR29vZ2xlIEluYy4gKEFNRC",
        "dm_img_inter": "{\"ds\":[{\"t\":4,\"c\":\"YWN0aXZlIG5hdi10YWJfX2l0ZW\",\"p\":[1095,77,645],\"s\":[271,639,606]}],\"wh\":[4232,4779,64],\"of\":[218,436,218]}",

        # "w_webid": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzcG1faWQiOiIzMzMuOTk5IiwiYnV2aWQiOiJCQzYzNDBBMy00QjdFLUEwQ0UtRDE1Ny0wQTNBOTM3QTU4RTk1OTg2N2luZm9jIiwidXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMzQuMC4wLjAgU2FmYXJpLzUzNy4zNiBFZGcvMTM0LjAuMC4wIiwiYnV2aWRfZnAiOiJhMmM3MzczODgxZDg0YTk5YTJlNjZmMDIwYjhhZjFkNiIsImJpbGlfdGlja2V0IjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNkluTXdNeUlzSW5SNWNDSTZJa3BYVkNKOS5leUpsZUhBaU9qRTNOREk1TmpnNE5qWXNJbWxoZENJNk1UYzBNamN3T1RZd05pd2ljR3gwSWpvdE1YMC5lUHNITVUwTHgwV3p5OHRKei1yZGxjMERyY09wSUtvM0dGcjdMM2VoTkc4IiwiY3JlYXRlZF9hdCI6MTc0MjcwOTc5OSwidHRsIjo4NjQwMCwidXJsIjoiLzI1NDQ2MzI2OT9zcG1faWRfZnJvbT0zMzMuMTAwNy50aWFubWEuMy0yLTguY2xpY2siLCJyZXN1bHQiOjAsImlzcyI6ImdhaWEiLCJpYXQiOjE3NDI3MDk3OTl9.lFMvVjxwDbbIgICZGXAghPo3pMsz46nZioG7buHa8A8xWXWx_v5-F4agqkv1RNjciUp-VQTh8nyksiW1N1xt9bQxbpZg1Yc5Na17ZpIrC8kFiyAv2oN0PBuGL2JGvxH8p2iFOWJrTQa8P9JS1zcBimDTRhEexdr52kkNW4JF6wJ3o5lvmQTbjHVlg7aDkSDQcLvi1doJc6zwlkDXm9U0EFHNe86Mcq35Kp_SHvVlApQxid64SMGZ4U2hI7y6K69n2e7NZZO4OoB07kkciBlv0_8Ha3Zh1JqxJQ_spV44Y-IG6gum3i7dMPXBkV7lAzIf6vsRzU4nL4rBH-24Ghu5bg",
        #
        # "w_rid": "4ae9aee029d88c3a501985554d1512a5",
        # "wts": 1742709813
    },
        img_key=img_key,
        sub_key=sub_key
    )
    query = urllib.parse.urlencode(signed_params)
    # print(signed_params)
    return signed_params
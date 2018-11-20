# -*- coding: utf-8 -*-
'''
Have fun.

python 3

@author: B1u3Buf4
'''
import hashlib
import base64
import requests
import re
import sys
import os
import time
import mysettings


def checkweb():
    rurl = ''
    rproxy = {}
    maxpage = 0
    urls = ['http://jandan.net/ooxx/', 'https://i.jandan.net/ooxx/']
    for url in urls:
        r = requests.get(url, headers=mysettings.headers)
        if r.status_code == 200:
            rurl = url
            maxpage = int(re.findall('current-comment-page">\[(\d*?)\]', r.text)[0])
            break
    if rurl == '':
        if mysettings.proxy == {}:
            raise Exception('You need add a proxy in mysettings.py!')
        else:
            for url in urls:
                r = requests.get(url, headers=mysettings.headers, proxies=mysettings.proxy)
                if r.status_code == 200:
                    maxpage = int(re.findall('current-comment-page">\[(\d*?)\]', r.text)[0])
                    rurl = url
                    rproxy = ysettings.proxy
                    break
    if rurl== '':
        raise Exception('Current settings could not request data. God bless you!')
    return rurl, rproxy, maxpage
    
#def none_md5():
    #with open('None.jpg','rb') as f:
        #res = hashlib.md5(f.read()).hexdigest()
    #return res

def f4ckjiandan():
    s = requests.session()
    BaseURL, proxy, maxpage = checkweb()
    for i in range(maxpage, 0, -1):
        print(i)
        stime = time.time()
        for ii in range(3):
            try:
                r = s.get(BaseURL + 'page-' + str(i) + '#comments', headers=mysettings.headers, proxies=proxy, timeout=5)
            except Exception as e:
                print('[x]', e)   
                continue
            if r.status_code == 200:
                total = re.findall('img-hash">.*?<', r.text)
                if len(total) == 0:
                    raise Exception('Maybe you are banned in this page!')
                #cou = 0
                for j in total:
                    tmp = base64.b64decode(j[10:-1]).decode('utf-8')
                    tmp = re.sub('cn/.*?/','cn/large/', tmp)
                    tmp = 'http:' + tmp
                    rr = requests.get(tmp)
                    if rr.history != []:
                        continue
                    tmpname = tmp[tmp.rfind('/') + 1:]
                    if os.path.exists('./pics/' + tmpname):
                        #cou += 1
                        continue
                    with open('./pics/' + tmpname, 'wb') as f:
                        f.write(rr.content)
                    print('[+]', tmp)
                    with open('logs', 'a') as f:
                        f.write(tmp[tmp.rfind('/') + 1:tmp.rfind('.')] + '\n')
                    time.sleep(0.5)
                #if cou > 30:
                    #return 0
                break
        sptime = time.time() - stime
        if sptime < mysettings.betweentime:
            time.sleep(mysettings.betweentime - sptime)


if __name__ == '__main__':
    if not os.path.exists('./pics/'):
        os.mkdir('pics')
    if len(sys.argv) == 1:
        f4ckjiandan()
        print('[+] Finished!')

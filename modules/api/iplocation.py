'''
@File    :   iplocation.py
@Time    :   2020/12/14 19:55:19
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

import os
import json
import datetime
import urllib.request
import logging as log
# Maintain a JSON table, and when there is a query task, 
# first query the local JSON table whether there is a cache.
# If the local record is too long or there is no record, 
# the network API is used to query the network home.

PRIVATE_RANGE = 'PRIVATE_RANGE'

cache = {}
ipLocationCache = "data/url/ipLocationCache.json"
# updateThreshold: unit is day day day!
updateThreshold = 7

def getCitysByIPs(IPs: list)->list:
    if len(cache) == 0 and os.path.exists(ipLocationCache):
        getAll()

    citys = []
    for ip in IPs:
        if ip in cache:
            interval = datetime.datetime.today() - datetime.datetime.strptime(cache[ip]['lastUpdate'],"%Y-%m-%d")
            if interval.days >= updateThreshold:
                city = getLocationFromNet(ip)
            else:
                city = cache[ip]['city']
        else:
            city = getLocationFromNet(ip)
        log.debug("ip: city %s" % city)
        citys.append(city)
    return citys

def getLocationFromNet(ip: str)->str:
    """
    get city by api [ taobao, pconline, sohu ]
    """
    # .decode("utf-8")
    city = ipapiAPI(ip)
    if city != "ERROR":
        putValue(ip, {'city': city, 'lastUpdate': datetime.datetime.today().strftime("%Y-%m-%d")})
        return city
    return "ERROR"

def pconlineAPI(ip: str) -> str:
    return ""


def ipapiAPI(ip: str) -> str:
    r = urllib.request.urlopen("http://ip-api.com/json/{0}?lang=zh-CN".format(ip))
    content = r.read()
    content = content.decode('utf-8')
    rj = json.loads(content)
    if rj['message'] == 'private range':
        city = PRIVATE_RANGE
    else:
        city = rj['regionName'] + rj['city']
    return city



    try:
        r = urllib.request.urlopen("http://ip-api.com/json/{0}?lang=zh-CN".format(ip))
        content = r.read()
        content = content.decode('utf-8')
        rj = json.loads(content)
        if rj['message'] == 'private range':
            city = PRIVATE_RANGE
        else:
            city = rj['regionName'] + rj['city']
        return city
    except Exception as e:
        log.debug(e)
        log.debug(content)
        return "ERROR"
    
def getAll():
    """
    init
    """
    with open(ipLocationCache, "r", encoding="utf-8") as target:
        global cache
        cache = json.load(target)

def putValue(key, value):
    """
    Add or update value of config json.
    """
    global cache
    cache[key] = value
    with open(ipLocationCache, "w", encoding="utf-8") as target:
        target.write(json.dumps(cache, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    # citys = getCitysByIPs(["159.226.99.36, 114.114.114.114"])
    # print(citys)
    # print(getLocationFromNet("113.128.128.132"))
    citys = getCitysByIPs([
        "114.114.114.114",
        "112.114.114.114",
        "113.114.114.114",
        '113.128.128.132'
    ])
    print(citys)
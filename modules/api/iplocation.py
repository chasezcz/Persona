'''
@File    :   iplocation.py
@Time    :   2020/12/14 19:55:19
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

import os
import json
import time
import datetime
import urllib.request
import logging as log
from IPy import IP
from urllib.error import HTTPError
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

    citys = set()
    for ip in IPs:
        if IP(ip).iptype() != 'PUBLIC':
            city = PRIVATE_RANGE
        elif ip in cache:
            interval = datetime.datetime.today() - datetime.datetime.strptime(cache[ip]['lastUpdate'],"%Y-%m-%d")
            if interval.days >= updateThreshold:
                city = getLocationFromNet(ip)
            else:
                city = cache[ip]['city']
        else:
            city = getLocationFromNet(ip)
        log.debug("ip: city %s" % city)
        citys.add(city)
    if len(citys) > 1 and PRIVATE_RANGE in citys:
        citys.remove(PRIVATE_RANGE)
    return citys

def getLocationFromNet(ip: str)->str:
    """
    get city by api [ taobao, pconline, sohu ]
    """
    # try ip-api api, decode utf-8
    city = ipapiAPI(ip)
    if city != "ERROR":
        putValue(ip, {'city': city, 'lastUpdate': datetime.datetime.today().strftime("%Y-%m-%d")})
        return city
    # try pconline api
    city = pconlineAPI(ip)
    if city != "ERROR":
        putValue(ip, {'city': city, 'lastUpdate': datetime.datetime.today().strftime("%Y-%m-%d")})
        return city
    return "ERROR"

############################### API START

def ipapiAPI(ip: str) -> str:
    try:
        r = urllib.request.urlopen("http://ip-api.com/json/{0}?lang=zh-CN".format(ip))
        content = r.read()
        content = content.decode('utf-8')
        rj = json.loads(content)
        if rj['status'] == 'success':
            return '-'.join([
                rj['country'],
                rj['regionName'],
                rj['city']
            ])
        else:
            log.error(rj)
            return 'ERROR'
    except HTTPError as he:
        if he.code == 429:
            time.sleep(5)
            log.error(he.__str__() + ' wait 5 seconds try again')
            return ipapiAPI(ip)
        else:
            return "ERROR"
    return "ERROR"

    # try:
    #     r = urllib.request.urlopen("http://ip-api.com/json/{0}?lang=zh-CN".format(ip))
    #     content = r.read()
    #     content = content.decode('utf-8')
    #     rj = json.loads(content)
    #     if rj['message'] == 'private range':
    #         city = PRIVATE_RANGE
    #     else:
    #         city = rj['regionName'] + rj['city']
    #     return city
    # except Exception as e:
    #     log.debug(e)
    #     log.debug(content)
    #     return "ERROR"


def pconlineAPI(ip: str) -> str:
    # TODO: undo
    # r = urllib.request.urlopen("")
    return ""

############################### API END

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

def getHeaders(header_raw):
    """
    Gets the request header dictionary from the native request header
    :param header_raw: {str} headers
    :return: {dict} headers
    """
    return dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


if __name__ == "__main__":
    # citys = getCitysByIPs(["159.226.99.36, 114.114.114.114"])
    # print(citys)
    # print(getLocationFromNet("113.128.128.132"))
    # citys = getCitysByIPs([
    #     "114.114.114.114",
    #     "112.114.114.114",
    #     "113.114.114.114",
    #     '113.128.128.132'
    # ])
    # print(citys)
    # ip = IP("113.128.128.132")
    # ip = IP("127.0.0.1")
    
    # print(ip.iptype())
    # ipcnAPI('159.226.99.36')
    # print(get_headers(rawHeaders))
    # print(ipcnAPI('159.226.99.36'))
    pass
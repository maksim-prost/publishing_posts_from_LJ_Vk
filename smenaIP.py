#! ./../venv/bin/python3

import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep
import os

def get_html(url, useragent = None, proxy = None,): 
     r = requests.get(url, headers = useragent , proxies =proxy)
     return r

def get_proxy(url="https://free-proxy-list.net/"):
     soup = BeautifulSoup(get_html(url).text, "lxml")
     return(["http://"+":".join([list.find('td').text, list.find('td').find_next_sibling('td').text] )
                           for list in soup.find("table").find("tbody").find_all("tr")])
    
class requests_random_IP():
     def __init__(self):
          print('requsts__init__')
          self.useragents = open("useragents.txt").read().split("\n")
          self.proxies = get_proxy()
     def get(self,url,**kwargs):
          useragent =  {"User-Agent": choice(self.useragents)}
          proxy  =  {"http":  choice(self.proxies)}
          # print(useragent,proxy, sep='\n')
          sleep(2)
          return requests.get(url, headers = useragent , proxies =proxy,**kwargs)
     def post(self,url,**kwargs):
          useragent =  {"User-Agent": choice(self.useragents)}
          proxy  =  {"http":  "http://"+ choice(self.proxies)}
          sleep(2)
          return requests.post(url, headers = useragent , proxies =proxy,**kwargs)
     

def main():
     # os.system('hostname -I')
     print(get_proxy()[0])
     # return get_proxy()[0]
#http://proxylist.hidemyass.com/searh-1299627#listable
#https://free-proxy-list.net/
if  __name__ =="__main__": main()









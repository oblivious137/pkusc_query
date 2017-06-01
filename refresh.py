#-*- coding: utf-8 -*-
import aiohttp, asyncio, async_timeout, pymongo
from html.parser import HTMLParser
from time import sleep
from random import randint

filt = '2017年北京大学信息学体验营上机第三场'

class MyHTMLParser(HTMLParser):
    def findd(self, li, tt):
        for i in li:
            if i[0] == tt:
                return i[1]
        return None
    
    def handle_starttag(self, tag, attrs):
        if self.in_name == 1:
            if tag == 'dd':
                self.in_name = 2
        if self.getsolved and tag=='a':
            self.solved.append(self.findd(attrs,'href')[-2:-1])
        if self.getsolving and tag=='a':
            self.solving.append(self.findd(attrs,'href')[-2:-1])
        
    
    def handle_data(self, data):
        if data.find('用户名') >=0:
            self.in_name = 1
        
        if self.in_name == 2:
            self.name = data
            self.in_name = -1
        
        if data == filt:
            self.cnt1 = True
            self.canuse = True
        
        if self.cnt1 :
            if data == '已解决的问题':
                self.getsolved = True
            elif data == '尝试但未解决的问题':
                self.getsolving = True
    
    def handle_endtag(self, tag):
        if tag == 'ul':
            if self.getsolving:
                self.getsolving = False
            if self.getsolved:
                self.getsolved = False

def anay(ttt):
    parser = MyHTMLParser()
    parser.in_name = -1
    parser.cnt1 = False
    parser.canuse = False
    parser.getsolved = False
    parser.getsolving = False
    parser.solved = []
    parser.solving = []
    parser.feed(ttt)
    if parser.canuse:
        db = pymongo.MongoClient().pkuscd3.players
        mp = db.find_one({'name': parser.name})
        if mp == None:
            mp = dict()
        mp['name'] = parser.name
        s = ""
        for i in parser.solved:
            s=s+i+' '
        mp['solved']=s
        
        s = ""
        for i in parser.solving:
            s=s+i+' '
        mp['solving']=s
        mp['num'] = len(parser.solved)
        
        if '_id' in mp:
            db.save(mp)
        else:
            db.insert(mp)
    return

async def solve(num):
    url = r'http://openjudge.cn/user/'+str(num)+r'/in/group-3/'
    headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url,headers=headers) as resp:
                if resp.status == 200:
                    body = await resp.text()
                    anay(body)
    except:
        pass

#1876, 2016, 2161, 2305
while True:
    tasks = [solve(i) for i in range(772161, 772305)]#, 2016)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    sleep(100+randint(20,100))
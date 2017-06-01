#-*- coding: utf-8 -*-

import tornado.web, tornado.httpserver, tornado.ioloop
import pymongo

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data = self.application.db.find()
        tat = {}
        for tt in data:
            tat.append({'day1':trs(tt)}{'name': tt['name'],
                        'num': tt['num'],
                        'solved': tt['solved'],
                        'solving': tt['solving'],
                        })
        tat.sort(key=lambda x:x['num'], reverse=True)
        for i in range(0, len(tat)):
            tat[i]['rank']=str(i+1)
        qaq = []
        al = len(tat)
        col_num = (len(tat)+149)//150
        for r in range(0,min(150,al)):
            tmp = []
            i = r
            while i<al:
                tmp.append(tat[i])
                i+=150
            qaq.append(tmp)
        
        self.render('index.html', data=qaq, col_num=col_num)

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[(r'/', MainHandler),
            ]
        settings={'template_path': 'templates',
                  'debug': True,
            }
        self.db=pymongo.MongoClient()
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    server=tornado.httpserver.HTTPServer(Application())
    server.listen('5050')
    tornado.ioloop.IOLoop.instance().start()
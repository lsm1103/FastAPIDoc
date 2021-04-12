#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：dp
@File    ：main.py.py
@IDE     ：PyCharm
@Author  ：xm
@Date    ：2021/4/10 5:18 下午
'''
import json, os, sys
from fastapi import Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from .toSwagger2 import toSwagger2
import FastAPIDoc

class ApiDoc():
    def __init__(self):
        _lib_path = os.path.dirname(sys.modules[FastAPIDoc.__package__].__file__)
        self.static = os.path.join(_lib_path, "static/")
        # self.static = './static/'

    def buildHTMLResponse(self, data):
        # .replace('{server_group}', '/get_json/group')
        htmlUrls = {
            'swagger2JQ':f'{self.static}swagger2JQ/doc.html',
            'swagger2Vue':f'{self.static}swagger2Vue/doc.html'
        }
        with open(htmlUrls[data['type_']], 'r', encoding='utf-8') as f:
            res = f.read()
        return HTMLResponse(res)

    def buildGroup(self, data):
        # r'relyOn/openapi/json/{}.json'
        print(data)
        with open(data['jsonPath'], 'r+', encoding='utf-8') as f:
            res = json.loads(f.read())
            for t in res:
                if 'xm' in t:
                    if t['xm']:
                        t['url'] = t['url'].replace('127.0.0.1:8009', data['domin'], 1).replace('pjServer',
                                                                                                data['name'], 1)
                        t['name'] = data['name']
                        t['location'] = t['location'].replace('pjServer', data['name'], 1)
                        t['xm'] = False
                    else:
                        res.pop(res.index(t))
                        res.append(
                            {
                                "name": data['name'],
                                "url": f"http://{data['domin']}/getApidoc/{data['name']}",
                                "swaggerVersion": "2.0",
                                "location": f"/json/{data['name']}.json",
                                "xm": True
                            }
                        )
            # [{k: t[k] if k != 'url' else t[k].replace('127.0.0.1:8009', data['domin']) for k in t} for t in res]
            # f.write(json.dumps(res ) )
            f.seek(0)
            json.dump(res, f, ensure_ascii=False)
            f.truncate()

    def __call__(self, app, type_:str = 'swagger2Vue'):
        app.mount("/static", StaticFiles(directory=self.static ), name="static")
        async def apidoc(req: Request):
            # print(app.routes)
            # 生成group.json文件，考虑具体的api是生成json文件还是通过http请求，现在用http请求
            self.buildGroup(data={'jsonPath':f'{self.static}json/group.json','domin':req.headers['host'], 'name':getattr(app,'title','FastapiServer') } )
            return self.buildHTMLResponse(data={'type_': type_})

        async def getApidoc(req: Request):
            filename = req.path_params['filename']
            if filename != getattr(app,'title','FastapiServer'):   #'pjServer'
                with open(f'{self.static}json/{filename}.json', 'r', encoding='utf-8') as f:
                    res = json.loads(f.read())
            else:
                data = get_openapi(
                    title=app.title,
                    version=app.version,
                    openapi_version=app.openapi_version,
                    description=app.description,
                    routes=app.routes,
                    tags=app.openapi_tags,
                    servers=app.servers,
                )
                # print(type(data) )
                res = toSwagger2.main(data={'content': data})
            return JSONResponse(res)

        app.add_route('/apidoc', apidoc, include_in_schema=False)
        app.add_route('/getApidoc/{filename}', getApidoc, include_in_schema=False)

apiDoc = ApiDoc()
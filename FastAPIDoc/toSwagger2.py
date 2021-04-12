#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：dp 
@File    ：toSwagger2.py
@IDE     ：PyCharm 
@Author  ：xm
@Date    ：2021/4/8 5:41 下午 
'''
import json, requests

def loadjson(filePath):
    with open(filePath, 'r') as f:
        r = json.loads(f.read())
        # print(r)
        return r

class ToSwagger2():
    def __init__(self):
        self.tags:list = []
        self.tagNames:list = []
        self.paths:dict = {}
        self.definitions:dict = {}
        self.objIn = {}
        # self.objIn = loadjson('objIn.json')

    def buildPathsAndTags(self):
        for item in self.objIn['paths']:
            item_v = self.objIn['paths'][item]
            for t in item_v:
                t_v = item_v[t]
                if 'tags' in t_v:
                    for tag in t_v['tags']:
                        if tag not in self.tagNames:
                            self.tagNames.append(tag)
                            self.tags.append({
                                "name": tag,
                                "description": f"Info {tag}"
                            })
            # paths
            self.paths[item] = self.buildPaths(item_v)

    def builDefinitions(self):
        if 'components' in self.objIn:
            for t in self.objIn['components']['schemas']:
                definition = self.objIn['components']['schemas'][t]
                for key in definition['properties']:
                    definition['properties'][key]['description'] = ''
                    if '$ref' in definition['properties'][key]:
                        definition['properties'][key]['originalRef'] = definition['properties'][key]['$ref'].split('/')[-1]
                        definition['properties'][key]['$ref'] = definition['properties'][key]['$ref'].replace('components/schemas','definitions',1)
                    if 'items' in definition['properties'][key]:
                        if '$ref' in definition['properties'][key]['items']:
                            definition['properties'][key]['items']['originalRef'] = definition['properties'][key]['items']['$ref'].split('/')[-1]
                            definition['properties'][key]['items']['$ref'] = definition['properties'][key]['items']['$ref'].replace('components/schemas','definitions',1)
                        else:
                            definition['properties'][key]['items']['originalRef'] = definition['properties'][key]['items'].get('type', '')
                    if 'allOf' in definition['properties'][key]:
                        allOf = definition['properties'][key].pop('allOf')
                        if '$ref' in allOf[0]:
                            definition['properties'][key]['$ref'] = allOf[0]['$ref'].replace('components/schemas', 'definitions', 1)
                            definition['properties'][key]['originalRef'] = allOf[0]['$ref'].split('/')[-1]
                        # for allOf in definition['properties'][key]['allOf']:
                        #     if '$ref' in allOf:
                        #         allOf['$ref'] = allOf['$ref'].replace('components/schemas', 'definitions', 1)
                                # {'$ref': allOf['$ref'].replace('components/schemas', 'definitions', 1)}

                definition['description'] = ''
                self.definitions[t] = definition

    def buildPaths(self, info):
        res = {}
        for item in info:
            data = info[item]
            requestBody = data.pop('requestBody') if 'requestBody' in data else None
            data['description'] = data['summary']
            data['consumes'] = ["application/json"]
            data['produces'] = ["*/*"]
            parameters = [ {**parameter, **{'description':parameter['name']} } for parameter in data['parameters'] ] if 'parameters' in data else []
                # for parameter in parameters:
                    # parameter['description'] = parameter['name']
            if requestBody:
                parameter = {
                    "in": "body",
                    "required": True,
                }
                schema = list(requestBody['content'].values())[0]['schema']
                if '$ref' in schema:
                    parameter.update(**{
                        "name": schema['$ref'].split('/')[-1],
                        "description": schema['$ref'].split('/')[-1],
                        "schema": {
                            "originalRef": schema['$ref'].split('/')[-1],
                            "$ref": schema['$ref'].replace('components/schemas','definitions',1)
                        }
                    })
                elif 'type' in schema:
                    if schema['type'] == 'array':
                        if '$ref' in schema['items']:
                            parameter.update(**{
                                "name": f"{schema['items']['$ref'].split('/')[-1]} array",
                                "description": schema['title'],
                                "schema": {
                                    "originalRef": schema['items']['$ref'].split('/')[-1],
                                    "$ref": schema['items']['$ref'].replace('components/schemas', 'definitions', 1)
                                }
                            })
                        else:
                            # print('schema-items',schema['items'])
                            parameter.update(**{
                                "name": schema['title'],
                                "type": schema['type'],
                                "description": schema['title'],
                                "schema": schema['items']
                            })
                elif 'title' in schema:
                    parameter.update(**{
                        "name": schema['title'],
                        "description": "未设计字段的json",
                        "schema": {
                            "originalRef": "未设计字段的json",
                            "$ref": "#/definitions/nullJson"
                        }
                    })
                parameters.append(parameter )
            data['parameters'] = parameters

            for code in data['responses']:
                content = data['responses'][code].pop('content')
                # print(list(content.values())[0] )
                schemas = list(content.values())[0]
                if '$ref' in schemas['schema']:
                    schemas['schema'] = {'$ref': schemas['schema']['$ref'].replace('components/schemas', 'definitions', 1) }
                data['responses'][code].update( **schemas )
            data['security'] = [
                {
                    'BearerToken': [
                        'global'
                    ]
                },
                {
                    'BearerToken1': [
                        'global'
                    ]
                }
            ]
            data['deprecated'] = False
            data['x-order'] = 'xxx'
            res[item] = data
        return res

    def main(self, data:dict):
        if 'content' in data:
            rs = data['content']
        else:
            rs = requests.get(data['openapi_url'])
            if not rs:
                return None
            rs = rs.json()
        self.objIn = rs
        self.buildPathsAndTags()
        self.builDefinitions()
        data = {
            "swagger": "2.0",
            "openapi": "3.0.2",
            "info": {
                "description": f"<div style='font-size:14px;color:red;'>{self.objIn['info']['title'] if self.objIn['info']['version'] else 'pjServer'} RESTful APIs</div>",
                "version": self.objIn['info']['version'],
                "title": f"{self.objIn['info']['title'] if self.objIn['info']['version'] else 'pjServer'} RESTful APIs",
                "termsOfService": self.objIn['info']['termsOfService'] if 'termsOfService' in self.objIn['info'] else 'www.xm.com',
                "contact": {
                    "name": "xm",
                    "email": self.objIn['info']['email'] if 'email' in self.objIn['info'] else "18370872400@163.com"
                },
                "license": {
                    "name": "Apache License 2.0",
                    "url": "http://www.xm.com"
                }
            },
            "host": self.objIn['info']['host'] if 'host' in self.objIn['info'] else "127.0.0.1:8000",
            "basePath": self.objIn['info']['basePath'] if 'basePath' in self.objIn['info'] else "/",
            "_tags": "/* s1里面paths里的tags的集合列表，所有的描述可以默认为空，人为加上 */",
            "tags": self.tags,
            "paths": self.paths,
            # "_securityDefinitions": "/* 安全的定义，在headers里面默认的安全入参 */",
            "securityDefinitions": {
                "BearerToken": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header"
                },
                "BearerToken1": {
                    "type": "apiKey",
                    "name": "Authorization-x",
                    "in": "header"
                },
                "Token": {
                    "type": "apiKey",
                    "name": "token",
                    "in": "header"
                }
            },
            # "_definitions": "/* 出入参模型的定义，相当于s1的components */",
            "definitions":self.definitions,
            # "_swaggerBootstrapUi": "/* 不是swagger2.0标准，自定义的字段 */",
            "swaggerBootstrapUi": {
                "tagSortLists": [],
                "pathSortLists": [],
                "markdownFiles": [],
                "errorMsg": []
            }
        }
        # r = json.dumps(data)
        # print(r)
        return data

toSwagger2 = ToSwagger2()

if "__main__" == __name__:
    # print(os.getcwd())
    toSwagger2.main({ 'openapi_url':'http://127.0.0.1:669/openapi.json' } )
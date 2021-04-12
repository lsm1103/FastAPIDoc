#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：openapi
@File    ：setup.py
@IDE     ：PyCharm
@Author  ：xm
@Date    ：2021/4/10 6:46 下午
'''
import setuptools, os
from distutils.core import setup, Extension
basepath = os.path.dirname(__file__)
#这是一个要安装的文件列表和位置
#(相对于setup.py所在的“root”目录)
#你可以说得更具体一些。
# files = ["things/*"]

setup(name = "FastAPIDoc",
    version='0.1.1',
    # ext_modules=[Extension('ApiDoc', ['ApiDoc.c'],
    # libraries=['fastapi', 'json'] ) ],
    description='FastAPI Better documentation',
    author='XiaoMin',
    author_email='18370872400@163.com',
    url='https://github.com/lsm1103',
    install_requires = ['fastapi>=0.61','aiofiles','uvicorn'],

    # packages=['distutils', 'distutils.command'],
    # 命名你的包所在的文件夹:
    # (如果你有其他的包(dirs)或模块(py文件)，那么
    # 把它们放到包目录中——它们会被找到
    # 递归)。
    packages = ['FastAPIDoc','FastAPIDoc.test'],
    # 'package'必须包含文件(参见上面的列表)
    # 我称这个套餐为“套餐”，这样就很聪明地混淆了整个问题……
    # 这个字典将包名=映射到=>目录
    # 它说，包*需要*这些文件。
    # package_data = {'package' : files },
    setup_requires=['wheel'],
    #资源文件引入
    data_files = [
        (f'{basepath}/FastAPIDoc/static/json', [
            'FastAPIDoc/static/json/server1.json',
            # 'FastAPIDoc/static/json/server2.json',
            # 'FastAPIDoc/static/json/server3.json',
            'FastAPIDoc/static/json/group.json'
        ]),
        (f'{basepath}/FastAPIDoc/static/swagger2Vue', [
            'FastAPIDoc/static/swagger2Vue/doc.html',
            'FastAPIDoc/static/swagger2Vue/favicon.ico',
            'FastAPIDoc/static/swagger2Vue/robots.txt'
        ]),
        (f'{basepath}/FastAPIDoc/static/swagger2Vue/webjars/css', ['FastAPIDoc/static/swagger2Vue/webjars/css/app.3167b4c3.css']),
        (f'{basepath}/FastAPIDoc/static/swagger2Vue/webjars/fonts', [
            'FastAPIDoc/static/swagger2Vue/webjars/fonts/fontawesome-webfont.f7c2b4b7.eot',
            'FastAPIDoc/static/swagger2Vue/webjars/fonts/fontawesome-webfont.d9ee23d5.woff',
            'FastAPIDoc/static/swagger2Vue/webjars/fonts/fontawesome-webfont.706450d7.ttf',
            'FastAPIDoc/static/swagger2Vue/webjars/fonts/iconfont.4ca3d0c0.ttf',
            'FastAPIDoc/static/swagger2Vue/webjars/fonts/fontawesome-webfont.97493d3f.woff2',
            'FastAPIDoc/static/swagger2Vue/webjars/fonts/iconfont.e2d2b98e.eot',
        ]),
        (f'{basepath}/FastAPIDoc/static/swagger2Vue/webjars/img', [
            'FastAPIDoc/static/swagger2Vue/webjars/img/logo.d03f7d43.png',
            'FastAPIDoc/static/swagger2Vue/webjars/img/fontawesome-webfont.139e74e2.svg',
            'FastAPIDoc/static/swagger2Vue/webjars/img/iconfont.1d48c203.svg',
            'FastAPIDoc/static/swagger2Vue/webjars/img/loading@3x.65eacf61.gif',
            'FastAPIDoc/static/swagger2Vue/webjars/img/loading.c929501e.gif',
            'FastAPIDoc/static/swagger2Vue/webjars/img/loading@2x.695405a9.gif',
            'FastAPIDoc/static/swagger2Vue/webjars/img/editormd-logo.84b6c2a9.svg',
        ]),
        (f'{basepath}/FastAPIDoc/static/swagger2Vue/webjars/js', [
            'FastAPIDoc/static/swagger2Vue/webjars/js/app.9f299301.js',
            'FastAPIDoc/static/swagger2Vue/webjars/js/chunk-vendors.07e8b475.js',
        ])
    ],

    #'runner'在根目录中。
    # scripts = ["runner"],
    long_description = """FastAPIDoc, Integrated swaggerui 2.0, automatically generate documents, MD, word, HTML, PDF, can also be debugged like swaggerui, easy to use, ready for production"""

    #下一部分是奶酪店，看一下页面的下面
    #classifiers = []
)
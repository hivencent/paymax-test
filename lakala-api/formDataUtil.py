#!\urs\bin\env python
# encoding:utf-8    #设置编码方式

# from http2 import http
import urllib

#发送form-data请求函数

def ReadFileAsContent(filename):
    # print filename
    try:
        with open(filename, 'rb') as f:
            filecontent = f.read()
    except Exception, e:
        # print 'The Error Message in ReadFileAsContent(): ' + e.message
        return ''
    return filecontent


def get_content_type(filename):
    import mimetypes
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def isfiledata(p_str):
    import re

    r_c = re.compile("^f'(.*)'$")
    rert = r_c.search(str(p_str))
    # rert = re.search("^f'(.*)'$", p_str)
    if rert:
        return rert.group(1)
    else:
        return None


def encode_multipart_formdata(fields):
    '''''
        该函数用于拼接multipart/form-data类型的http请求中body部分的内容
        返回拼接好的body内容及Content-Type的头定义
    '''
    import random
    import os
    BOUNDARY = '----------%s' % ''.join(random.sample('0123456789abcdef', 15))
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        filepath = isfiledata(value)
        if filepath:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, os.path.basename(filepath)))
            L.append('Content-Type: %s' % get_content_type(filepath))
            L.append('')
            L.append(ReadFileAsContent(filepath))
        else:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    # print "content_type>>",content_type
    # print "body>>",body

    return content_type, body



#例子：

def example():
    '''
    #将数据zip转成多元tuple,作为请求数据
    form_data = util.dict2zip(jsonDict)
    print "form_data>>",form_util
    #发送请求
    # form_data = [('charset', '02'),()]
    #将数据转成form-data类型
    content_type, body = form_util.encode_multipart_formdata(form_data)
    # print content_type, body
    print "content_type>>", content_type
    print "body>>", body
    '''

    # form_data = [('gShopID','489'),("addItems", r"f'D:\case3guomei.xml'"), ('validateString', '92c99a2a36f47c6aa2f0019caa0591d2')]
    form_data = [('charset','02')]
    content_type, body = encode_multipart_formdata(form_data)
    # print content_type, body
    print "content_type>>",content_type
    print "body>>",body


    url = "http://172.30.21.35:8080/hipos/cashier"
    headers = {
            'Content-Type':'application/x-www-form-urlencoded',
            'cache-control': "no-cache",
        }

    import requests

    print headers
    response = requests.request("POST", url, data=body, headers=headers)

    print (response.status_code)
    print(response.text)
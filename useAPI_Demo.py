#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
本示例代码仅作参考。如果您是业务调用，建议对body体也做加密。
注意：本示例用到的鉴权方式不适用于一部分产品（语音识别、人脸识别等）。请查阅您使用产品的API文档，如果鉴权方式基于Access Key（包括Access Key ID（AK）和Secret Access Key（SK）），
且最终认证字符串为bce-auth-v{version}/{accessKeyId}/{timestamp}/{expirationPeriodInSeconds}/{signedHeaders}/{signature}，则适用本示例。
此外，部分产品在AK/SK加密之外，还会要求额外的认证，例如百度信息流推广API需要您将百度推广账号的信息填到body体里。请注意查阅文档。

'''



import hashlib
import hmac
import urllib
import time

# 1.AK/SK、host、method、URL绝对路径、querystring
AK = "input your AK"
SK = "input your SK"
host = "bcc.bj.baidubce.com"
method = "PUT"
query = "modifyAttribute"
URI = "/v2/instance/i-YufwpQAe"

# 2.x-bce-date
x_bce_date = time.gmtime()
x_bce_date = time.strftime('%Y-%m-%dT%H:%M:%SZ',x_bce_date)
# 3.header和signedHeaders
header = {
        "Host":host,
        "content-type":"application/json;charset=utf-8",
        "x-bce-date":x_bce_date
        }
signedHeaders = "content-type;host;x-bce-date"
# 4.认证字符串前缀
authStringPrefix = "bce-auth-v1" + "/" +AK + "/" +x_bce_date + "/" +"1800"
# 5.生成CanonicalRequest
#5.1生成CanonicalURI
CanonicalURI = urllib.parse.quote(URI)        # windows下为urllib.parse.quote，Linux下为urllib.quote
#5.2生成CanonicalQueryString
CanonicalQueryString = query           # 如果您调用的接口的query比较复杂的话，需要做额外处理
#5.3生成CanonicalHeaders
result = []
for key,value in header.items():
    tempStr = str(urllib.parse.quote(key.lower(),safe="")) + ":" + str(urllib.parse.quote(value,safe=""))
    result.append(tempStr)
result.sort()
CanonicalHeaders = "\n".join(result)
#5.4拼接得到CanonicalRequest
CanonicalRequest = method + "\n" + CanonicalURI + "\n" + CanonicalQueryString +"\n" + CanonicalHeaders
# 6.生成signingKey
signingKey = hmac.new(SK.encode('utf-8'),authStringPrefix.encode('utf-8'),hashlib.sha256)
# 7.生成Signature
Signature = hmac.new((signingKey.hexdigest()).encode('utf-8'),CanonicalRequest.encode('utf-8'),hashlib.sha256)
# 8.生成Authorization并放到header里
header['Authorization'] = authStringPrefix + "/" +signedHeaders + "/" +Signature.hexdigest()
# 9.发送API请求并接受响应
import requests
import json



body={
      "name" : "QQQQQQ"      
      }

url = "http://"+host + URI 

r = requests.put(url,headers = header,data=json.dumps(body))

print(r.text)













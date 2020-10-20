import urllib.request
import urllib.parse
import json
import base64
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=O6SiWlKo1qFBGQsoBSxAelAd&client_secret=HzXpHlWcfSXbfeGUYPnfa8PrG7ONznz1'
request = urllib.request.Request(host)
request.add_header('Content-Type','application/json;charset=UTF-8')
response = urllib.request.urlopen(request)
content = response.read()
if(content):
    pprint(content)

content_decoded = json.loads(content.decode('utf-8'))
access_token = content_decoded['access_token']
#显示原始图片
img_stars = mpimg.imread('timg.jpg')
plt.figure(figsize=(10,8),dpi=100)
plt.imshow(img_stars)
plt.axis('off')
plt.show()

#人脸检测与属性分析
request_url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect'

f = open(r'timg.jpg','rb')
img = base64.b64encode(f.read())

params = {'max_face_num':10,
          'image':img,
          'image_type':'BASE64',
          'face_field':'age,gender'}

params = bytes(urllib.parse.urlencode(params).encode())

request_url = request_url + '?access_token=' + access_token
request = urllib.request.Request(url=request_url,data=params)
request.add_header('Content-Type','application/json')
response = urllib.request.urlopen(request)
content = response.read()
content_decoded = json.loads(content.decode('utf-8'))
image_result = content_decoded
pprint(image_result)

#显示识别效果
if (image_result['error_code'] == 0):
    print('检测到的人脸数量：',image_result['result']['face_num'])
    for face in image_result['result']['face_list']:
        loc = face['location']
        pt1 = (int(loc['left']),int(loc['top']))
        pt2 = (int(loc['left'] + loc['width']),int(loc['top'] + loc['height']))

        cv2.rectangle(img_stars,pt1,pt2,color=(255,0,0),thickness=2)
        gender = face['gender']['type']
        age = face['age']
        cv2.putText(img_stars,'{}:{}'.format(gender,age),(pt1[0],pt1[1] - 20),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.5,color=(255,0,0))

    plt.figure(figsize=(10,8),dpi=100)
    plt.imshow(img_stars)
    plt.axis('off')
    plt.show()
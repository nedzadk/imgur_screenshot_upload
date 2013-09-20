#!/usr/bin/python
import pyscreenshot as ImageGrab
import requests
import json
import base64
import os
import sys
import ConfigParser
import datetime


config = ConfigParser.RawConfigParser()
app_path = os.path.dirname(sys.argv[0])
config.read(app_path + '/ss.ini')
img_path = config.get('config', 'img_save_path')
img_name = config.get('config', 'img_name')
client_id = config.get('config', 'imgur_client_id')

timestamp = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
full_path = img_path + img_name + str(timestamp) + '.png'

im = ImageGrab.grab_to_file(full_path)
url = 'https://api.imgur.com/3/upload.json'
f = open(full_path, 'rb')
binary_data = f.read()
image64 = base64.b64encode(binary_data)
headers = {'Authorization': 'Client-ID ' + client_id}
payload = {'key': client_id,
           'image': image64,
           'type': 'base64',
           'title': 'Python ScreenShoter'}
result = requests.post(url, headers=headers, data=payload)
jarr = json.loads(result.text)
link = jarr['data']['link']
print link
clip = 'echo ' + link.strip() + '| xclip -selection c'
os.system(clip)

import requests

url = "http://4473-2001-b011-4010-3626-3400-8dce-48cc-7ab1.ngrok.io/jpg"

payload={}
files=[
  ('files',('Apex Legends 2022-04-02 11-01-55_18.jpg',open('D://apex_data//images//Apex Legends 2022-04-02 11-01-55_18.jpg','rb'),'image/jpeg'))
]

headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)

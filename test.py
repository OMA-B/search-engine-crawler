import requests
url='http://127.0.0.1:5000'
headers ={'Content-Type':'application/json'}
# data = {'username':'jbiidjhs','password':'fgddfgd','email':'ijbh@adsjdbi.corn'}
# r = requests.post(url+'/signup',headers=headers,json=data)
# print(r.text)
# data = {'username':'Fosead','password':'ksajdnsi8','email':'ajahbsk@askjil.corn'}
# r = requests.post(url+'/signup',headers=headers,json=data)
# print(r.text)
# data = {'username':'jhbjhbi','password':'dnkscjsjdj','email':'kajska@askjil.corn'}
# r = requests.post(url+'/signup',headers=headers,json=data)
# print(r.text)

# test='user1@gmail.yam'
# del data['username']
# r=requests.post(url+'/login',json=data,headers=headers)
# print(r.text)

# r=requests.get(url+'/users')
# print(r.text)
# # r=requests.post(url+'/delete',json={'email':test},headers=headers)
# print(r.text)

data = {'search_engine_name':'google','search_phrase':'Yam and beans','page_depth_num':10,'max_search_num':10}
r = requests.post(url+'/scrape',headers=headers,json=data)
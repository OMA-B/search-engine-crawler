import requests
url='http://127.0.0.1:5000'
data = {'username':'Fathead','password':'Pajhabsi8','email':'ansk@askjil.corn'}
headers ={'Content-Type':'application/json'}
r = requests.post(url+'/signup',headers=headers,json=data)
print(r.text)


del data['username']
r=requests.post(url+'/login',json=data,headers=headers)
print(r.text)
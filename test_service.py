import requests
import sys
orig_stdout = sys.stdout

f = open('test_service.log', 'w')
sys.stdout = f


recs_url = "http://127.0.0.1:8000"
print('Проверка для холодного пользователя - выдаем  из топ-100 популярных треков')

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
params  = {"user_id": 1, "k": 10}

resp = requests.post(recs_url + "/recommendations", headers=headers, params=params) 


if resp.status_code == 200:
    result = resp.json()
else:
    result = None
    print(f"status code: {resp.status_code}")
    
print(result, '\n')


print('Тестируем пользователя, для которого  есть офлайн рекомендации')
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
params = {"user_id": 4, "k": 10 }

resp = requests.post(recs_url + "/recommendations", headers=headers, params=params)
if resp.status_code == 200:
    result = resp.json()
else:
    result = None
    print(f"status code: {resp.status_code}")
    
print(result, '\n') 


print('Тестируем пользователя, для которого  есть и офлайн, и онлайн рекомендации.')
print('Сначала сделаем для него историю ')

events_store_url = "http://127.0.0.1:8020"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
params  = {"user_id": 4, "item_id": 658327}

resp = requests.post(events_store_url + "/put", headers=headers, params=params) 

if resp.status_code == 200:
    result = resp.json()
else:
    result = None
    print(f"status code: {resp.status_code}")
    
print(result, '\n'
)

print('Выводим рекомендации')

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
params = {"user_id": 4, "k": 10 }

resp = requests.post(recs_url + "/recommendations", headers=headers, params=params)
if resp.status_code == 200:
    result = resp.json()
else:
    result = None
    print(f"status code: {resp.status_code}")
    
print(result) 


sys.stdout = orig_stdout
f.close()
import requests
import sys
import logging
import datetime

logger = logging.getLogger(__name__)

def main(): 
    logging.basicConfig(filename='recommendations_testing.log', level=logging.INFO)
    logger.info('-'*80)
    logger.info(f'STARTED at {datetime.datetime.now()}')

    recs_url = "http://127.0.0.1:8000"
    logger.info('TEST_1 - Проверка для холодного пользователя - выдаем  из топ-100 популярных треков')

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    params  = {"user_id": 1, "k": 10}

    logger.info(headers)
    logger.info(params)

    resp = requests.post(recs_url + "/recommendations", headers=headers, params=params) 


    if resp.status_code == 200:
        result = resp.json()
        logger.info(result)
        logger.info('TEST PASSED')
    else:
        result = None
        logger.error(f"status code: {resp.status_code}")
        

    logger.info('TEST_2 - Тестируем пользователя, для которого  есть офлайн рекомендации')
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    params = {"user_id": 4, "k": 10 }
    logger.info(headers)
    logger.info(params)

    resp = requests.post(recs_url + "/recommendations", headers=headers, params=params)
    if resp.status_code == 200:
        result = resp.json()
        logger.info(result)
        logger.info('TEST PASSED')
    else:
        result = None
        logger.error(f"status code: {resp.status_code}")
    

    logger.info('TEST_3 - Тестируем пользователя, для которого  есть и офлайн, и онлайн рекомендации.')
    logger.info('TEST_3_1 - Сначала сделаем для него историю ')

    events_store_url = "http://127.0.0.1:8020"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    params  = {"user_id": 4, "item_id": 658327}

    logger.info(headers)
    logger.info(params)

    resp = requests.post(events_store_url + "/put", headers=headers, params=params) 

    if resp.status_code == 200:
        result = resp.json()
        logger.info(result)
        logger.info('TEST PASSED')
    else:
        result = None
        logger.error(f"status code: {resp.status_code}")

    logger.info('TEST_3_2 - Выводим рекомендации')

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    params = {"user_id": 4, "k": 10 }

    resp = requests.post(recs_url + "/recommendations", headers=headers, params=params)
    if resp.status_code == 200:
        result = resp.json()
        logger.info(result)
        logger.info('TEST PASSED')
    else:
        result = None
        logger.error(f"status code: {resp.status_code}") 
    
    logger.info(f'FINISHED at {datetime.datetime.now()}')

if __name__ == '__main__':
    main()
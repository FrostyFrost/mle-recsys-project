# Подготовка виртуальной машины

## Склонируйте репозиторий

Склонируйте репозиторий проекта:

```
git clone https://github.com/yandex-praktikum/mle-project-sprint-4-v001.git
```

## Активируйте виртуальное окружение

Используйте то же самое виртуальное окружение, что и созданное для работы с уроками. Если его не существует, то его следует создать.

Создать новое виртуальное окружение можно командой:

```
python3 -m venv env_recsys_start
```

После его инициализации следующей командой

```
. env_recsys_start/bin/activate
```

установите в него необходимые Python-пакеты следующей командой

```
pip install -r requirements.txt
```

### Скачайте файлы с данными

Для начала работы понадобится три файла с данными:
- [tracks.parquet](https://storage.yandexcloud.net/mle-data/ym/tracks.parquet)
- [catalog_names.parquet](https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet)
- [interactions.parquet](https://storage.yandexcloud.net/mle-data/ym/interactions.parquet)
 
Скачайте их в директорию локального репозитория. Для удобства вы можете воспользоваться командой wget:

```
wget https://storage.yandexcloud.net/mle-data/ym/tracks.parquet

wget https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet

wget https://storage.yandexcloud.net/mle-data/ym/interactions.parquet
```

## Запустите Jupyter Lab

Запустите Jupyter Lab в командной строке

```
jupyter lab --ip=0.0.0.0 --no-browser
```

# Расчёт рекомендаций

Код для выполнения первой части проекта находится в файле `recommendations.ipynb`. Изначально, это шаблон. Используйте его для выполнения первой части проекта.

# Сервис рекомендаций

Код сервиса рекомендаций находится в файле `recommendations_service.py`.


Для запуска необходимо в разных терминалах запустить:

* Сервис событий 
`uvicorn events_service:app --port 8020`

* Сервис схожих треков 
`uvicorn features_service:app --port 8010`

* Сервис рекомендаций
`uvicorn recommendations_service:app --port 8000`

В сервисе рекомендаций реализована выдача онлайн и офлайн рекомендаций. 

1) Если для пользователя нет офлайн рекомендаций и его истории (холодный клиент) ему выдаются топ-100 треков
2) Если для пользователя есть офлайн рекомендации, но нет истории, то выдаются офлайн рекоемндации
3) Если для пользователя есть и офлайн рекомендации, и его история прослушивания, то для истории находятся ближайшие похожие треки (онлайн рекомендации) и происходит блендинг офлайн и онлайн рекомендаций по очереди - один трек из онлайн, один из офлайн,...


# Инструкции для тестирования сервиса

Код для тестирования сервиса находится в файле `test_service.py`.

1) Запустить все сервисы (см. "Сервис рекомендаций").
2) Выполнить код в `test_service.py`: 
`python test_service.py`
3) Результат работы сохраняется в файл `test_service.log`


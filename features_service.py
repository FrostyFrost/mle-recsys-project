import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI

PATH_TO_SIMILAR_ITEMS = './recsys/recomendations/similar_items.parquet'

logger = logging.getLogger("uvicorn.error")

class SimilarItems:

    def __init__(self):

        self._similar_items = None

    def load(self, path, **kwargs):
        """
        Загружаем данные из файла
        """

        logger.info(f"Loading data, type: {type}")
        self._similar_items = pd.read_parquet(path,**kwargs)
        self._similar_items = self._similar_items[kwargs['columns']]
        self._similar_items = self._similar_items.set_index('track_id_enc')
        logger.info(f"Loaded")
        logger.info(self._similar_items )

    def get(self, item_id: int, k: int = 10):
        """
        Возвращает список похожих объектов
        """
        # COMMENT:  > Здесь тоже можно избежать использование исключения
        # COMMENT: А я бы оставил, поскольку рекомендации могут отсутствовать по разным причинам (нет пользователя, нет рекомендаций, потерялся\сломался файл с рекомендациями,...) 
        # COMMENT: Но  добавил помимо обработки KeyError еще и else

        try:
            i2i = self._similar_items.loc[item_id].head(k)
            i2i = {"item_id_2": i2i["sim_item_id_enc"][1:].tolist(), "score": i2i['score'].tolist()}
        except KeyError:
            logger.error("No recommendations found")
            i2i = {"item_id_2": [], "score": []}
        else:
            logger.error("problem with similar recomendations")

        return i2i

sim_items_store = SimilarItems()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # код ниже (до yield) выполнится только один раз при запуске сервиса
    sim_items_store.load(
        PATH_TO_SIMILAR_ITEMS,
        columns=["track_id_enc", "sim_item_id_enc", "score"],
    )
    logger.info("Ready!")
    # код ниже выполнится только один раз при остановке сервиса
    yield

# создаём приложение FastAPI
app = FastAPI(title="features", lifespan=lifespan)

@app.post("/similar_items")
async def recommendations(item_id: int, k: int = 10):
    """
    Возвращает список похожих объектов длиной k для item_id
    """

    i2i = sim_items_store.get(item_id, k)

    return i2i
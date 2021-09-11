from typing import Optional
from fastapi import FastAPI
import pickle
import pandas as pd
from pydantic import BaseModel


app = FastAPI()

pickle_in = open("sig.pkl","rb")
sig = pickle.load(pickle_in)
df = pd.read_csv('product.csv');
indicies = pd.Series(df.index, index=df['productShortName']).drop_duplicates()

class Item(BaseModel):
    name: str
#     price: float
#     is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}

@app.post('/recommend')
def get_recomendation(product_name:str):
    idx = indicies[product_name]
    sig_scores = list(enumerate(sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores
    prod_indexes = [i[0] for i in sig_scores]
    return {'recomedations' : df['productShortName'].iloc[prod_indexes]}


@app.post("/getrecommend/")
async def create_item(item: Item):
    product_name = item.name
    idx = indicies[product_name]
    sig_scores = list(enumerate(sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores
    prod_indexes = [i[0] for i in sig_scores]
    return {'recomedations': df['productShortName'].iloc[prod_indexes].tolist()}

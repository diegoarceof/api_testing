import numpy as np

from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

from search import query

class Metric(str, Enum):
    euclidean = "euclidean" # L2 distance  
    inner_product = "IP" # dot product

class QueryParams(BaseModel):
    embeddings: list[list[float]]
    n_neighbors: int = 5
    metric: Metric = Metric.inner_product

app = FastAPI()

@app.get("/")
def root():
    return {"message": "COMC nearest neighbor search"}

@app.post("/nearest_neighbor")
async def nearest_neighbor(params: QueryParams):
    embeddings = np.array(params.embeddings)
    n_neighbors = params.n_neighbors
    metric = params.metric.value

    distances, nearest_embeddings = query(embeddings, n_neighbors, metric)
    return {
        'distances': distances.tolist(),
        'nearest_embeddings': nearest_embeddings.tolist()
        }
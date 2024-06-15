from typing import Optional
from fastapi import FastAPI, HTTPException
from models import BDD
from schemas.init_info import InitInfo

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/add")
def add(a: float, b: float):
    """
    This endpoint takes two query parameters 'a' and 'b' and returns their sum.
    """
    return {"result": a + b}

@app.post("/init_bdd")
async def init_bdd(init_info: InitInfo):
    try:
        bdd = BDD()
        bdd.init(init_info.info_init, init_type=init_info.init_type)
        return {"message": "BDD initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Pour exécuter le serveur : uvicorn main:app --reload

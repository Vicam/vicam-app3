from typing import Optional
from fastapi import FastAPI, HTTPException
from models import BDD
from schemas.init_info import InitBddBody, JoueurResponse

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
async def init_bdd(init_info: InitBddBody):
    try:
        global bdd_instance
        bdd_instance.init(init_info.info_init, init_type=init_info.init_type)
        return {"message": "BDD initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/players")
async def get_players():
    try:
        global bdd_instance
        return {"players": list(bdd_instance.dict_joueur.keys())}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/player/{player_name}", response_model=JoueurResponse)
async def get_player(player_name: str):
    try:
        global bdd_instance
        player = bdd_instance.dict_joueur.get(player_name)
        if player:
            return player.to_joueur_response()
        else:
            raise HTTPException(status_code=404, detail="Player not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()



@app.get("/")
async def read_root():

    return {"Hello": "MOTO !!!!!"}




@app.get("/posts")
def root():
    return("king kohli crisps")         


@app.post("/postcreate")
def root(payload:dict = Body(...)):
    print(payload)
    return("BABAR AZAM")

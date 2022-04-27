from urllib import response
from fastapi import FastAPI
import recomendacion
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=ORJSONResponse)
async def root(title:str):
        res = recomendacion.obtener_recomendacion(title)
        return res





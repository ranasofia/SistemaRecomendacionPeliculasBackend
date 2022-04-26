from fastapi import FastAPI
import recomendacion
app = FastAPI()


@app.get("/")
async def root(title:str):
        res = recomendacion.obtener_recomendacion(title)
        return "Las peliculas recomendadas son: {}".format(res)





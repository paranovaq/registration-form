from fastapi import FastAPI
from api.controllers.routes import router


app = FastAPI()

app.include_router(router)
